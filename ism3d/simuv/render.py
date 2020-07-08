import numpy as np
import scipy
import astropy.units as u
from astropy.wcs import WCS
from astropy import constants as const
from astropy.cosmology import Planck13
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.convolution import convolve_fft
import numexpr as ne
import pyfftw
pyfftw.interfaces.cache.enable()
pyfftw.interfaces.cache.set_keepalive_time(5)
from scipy.sparse import csr_matrix
import fast_histogram as fh
from .. import fft_use
from galario.single import sampleImage
from copy import deepcopy
#from .io import *
#from .dynamics import model_vrot
#from .utils import write_par
#from .utils import inp2mod
import operator
from scipy.interpolate import RectBivariateSpline
import scipy.fft as scipy_fft
import finufftpy  as nufft


import logging
logger = logging.getLogger(__name__)

from ..arts.discretize import channel_split
from .ft import uv_sample
from ..utils.misc import render_component

def sample_prep(w,phasecenter,tol=0.01):
    """
    do some prep for uv_sample()
    uvdata phasecenter
    w    model image wcs
    
    ref:
        https://mtazzari.github.io/galario/tech-specs.html specifically the "lower" option
    
    tol: in units of cell size
    
    """
    naxis=w._naxis    
    if  (naxis[0] % 2)!=0 or (naxis[1] % 2)!=0:
        logger.debug("the input image must have even number of pixels along x-/y-dimensions")
        return    
    
    refimcenter_ra,refimcenter_dec=w.celestial.wcs_pix2world(naxis[0]/2,naxis[1]/2,0)
    #phasecenter_sc = SkyCoord(phasecenter[0], phasecenter[1], frame='icrs')
    phasecenter_sc = phasecenter
    refimcenter_sc = SkyCoord(refimcenter_ra*u.deg,refimcenter_dec*u.deg, frame='icrs')
    dra, ddec = phasecenter_sc.spherical_offsets_to(refimcenter_sc)    
    dRA=dra.to_value(u.rad)
    dDec=ddec.to_value(u.rad)
    cell=np.mean(proj_plane_pixel_scales(w.celestial))
    cell=np.deg2rad(cell)
    if  np.abs(dRA)<cell*tol: dRA=0
    if  np.abs(dDec)<cell*tol: dDec=0
    try:
        wspec=w.sub(['spectral'])
        wv=wspec.pixel_to_world(np.arange(naxis[2])).to(u.m,equivalencies=u.spectral()).value     
    except:
        wv=None
    
    #   dRA (rad)
    #   dDec (rad)
    #   cell (rad)
    #   wv (meter)
    
    return dRA,dDec,cell,wv 

def uv_render(objs,w,uvw,phasecenter,pb=None,wideband=False):
    """
    
    Note: psf/pb should not contain missing data
    map mutiple component into one header and calculate chisq
    objs:       componnet list
    models:    a list of model to be mapped into the visibility model for the chisq calculation
    header:    pesudo fits header
    uv...:     visibility data 
    
    pb must match wcs
    """
    if  pb is None:
        logger.debug("warning: pb is empty!")
        logger.debug("therefore, the primary beam response is not applied to the model image before uv sampling")
    
    sample_count=line_count=cont_count=0
    naxis=w._naxis
    vis_shape=(uvw.shape[0],naxis[2])
    vis=np.zeros(vis_shape,dtype=np.complex128,order='F')    

    #   prep for uv_sample()
        
    dRA,dDec,cell,wv=sample_prep(w,phasecenter)

    #   gather information per object before going into the channel loop,
    
    fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=channel_split(objs,w) 
  
    #   Grid Continuum Models (continnuum cloudlets or AP models)
    #   we save fluxscale frequency depedency as vector
    
    im_cache=[]; uv_cache=[]; fluxscale_cache=[]
    iz=int(naxis[2]*0.5)
        
    for i,obj in enumerate(objs):

        if  'lineflux' in obj: continue
        
        if  obj['type'] not in ['apmodel'] and 'contflux' in obj:
            plane=fh.histogram2d(y_list[i],x_list[i],                                             
                                 range=[yrange_list[i],xrange_list[i]],
                                 bins=(naxis[1],naxis[0]),
                                 weights=wt_list[i])
        if  obj['type'] in ['apmodel']:
            xx,yy=np.meshgrid(x_list[i],y_list[i])
            plane=((objs[i]['apmodel'])(xx,yy)).value        
            plane=plane/np.sum(plane)
        
        im_cache.append(plane)
        fluxscale_cache.append(fluxscale_list[i]) 

        if  pb is not None: plane=plane*pickplane(pb,iz)
        uv0=uv_sample(plane.astype(np.float32),
                        cell,
                        (uvw[:,0]/wv[iz]),
                        (uvw[:,1]/wv[iz]),                               
                        dRA=dRA,dDec=dDec,
                        PA=0.,origin='lower')
        sample_count+=1
        uv_cache.append(uv0)

    #   Render Line+Contnuum Model
    
    for iz in range(naxis[2]):
        
        #   render all line emissions
        
        plane=None        
        for i in range(len(objs)):
             
            if  'lineflux' not in objs[i]: continue
            if  x_list[i][iz+1].size==0: continue
            
            wt=wt_list[i][iz+1] if wt_list[i] is not None else None
            plane=render_component(plane,fh.histogram2d(y_list[i][iz+1],x_list[i][iz+1],                                             
                                                         range=[yrange_list[i],xrange_list[i]],
                                                         bins=(naxis[1],naxis[0]),weights=wt),
                             scale=fluxscale_list[i])
               
        if  plane is not None or wideband==True:
            plane=render_component(plane,im_cache,
                             scale=[fluxscale_cache[j][iz] for j in range(len(im_cache))])
            
            if plane is None: continue
            if pb is not None: plane*=pickplane(pb,iz)
            
            wv_plane=wv[iz]
            vis[:,iz]=uv_sample(plane.astype(np.float32),
                                  cell,
                                  (uvw[:,0]/wv_plane),
                                  (uvw[:,1]/wv_plane),                               
                                  dRA=dRA,dDec=dDec,
                                  PA=0.,origin='lower')
            sample_count+=1; line_count+=1                    
        else:
            render_component(vis[:,iz],uv_cache,
                             scale=[fluxscale_cache[j][iz] for j in range(len(uv_cache))])  
            cont_count+=1
            
    #logger.debug('uvsample count: '+str(sample_count))
    #logger.debug('line channel count: '+str(line_count))
    #logger.debug('cont channel count: '+str(cont_count))            
            
    return vis