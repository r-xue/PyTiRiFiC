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
"""
Note:    
    discretize.*render and evaluate.*chisq share similar codebase in some degree.
    However, evaluate.*chisq is written for max performance with less memory impact, 
    while evaluate.*render is configurated for saving all model metadata.

"""
import logging
logger = logging.getLogger(__name__)

from ..arts.discretize import channel_split
#from .ft import uv_sample
from ..utils.misc import render_component
from ..utils.misc import pickplane
from astropy.modeling import models as apmodels

"""
    Note: 
        performance on Quanitu/Units
        https://docs.astropy.org/en/stable/units/#performance-tips
        https://docs.astropy.org/en/stable/units/quantity.html#astropy-units-quantity-no-copy
        https://docs.astropy.org/en/stable/units/quantity.html (add functiomn argument check)
        
    .xyz / .d_xyz is not effecient as it's combined on-the-fly
    .d_xyz
    
Note:
    + astropy.convolution.discretize_model:
        offer oversampling:
      astropy.modeling.models
        offer bounding_box and tile-based efficient rendering
        https://docs.astropy.org/en/stable/modeling/models.html#efficient-evaluation-with-model-render
        - looks like bounding_box is defined in the pixel domain (so doesn't work well with coords setup)
        - also there is a bug when out.dtype is not float
        - exception when bounding_box > imsize
      We combined these two features together (see model_disk2d).

"""



def render_point(obj,w,out=None):
    """
    obj:     object prescription
    w:       wcs 
    """
    px,py=w.celestial.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,0)
    naxis=w._naxis
    if  out is None:
        out=np.zeros((naxis[2],naxis[1],naxis[0]),dtype=np.float32)      

    wspec=w.sub(['spectral'])
    sz=wspec.pixel_to_world(np.arange(w._naxis[2])).to(u.Hz,equivalencies=u.spectral())
    
    fluxscale=obj['contflux']*((sz/obj['contfreq'])**obj['alpha'])
    fluxscale.to_value('Jy')
    
    out[:,round(float(py)),round(float(px))]=fluxscale.to_value('Jy')
    
    return out

def render_poly2d(obj,w,out=None):
    """
    """
    
    return

def render_sersic2d(obj,w,out=None):
    """
    """
    px,py=w.celestial.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,0)
    naxis=w._naxis
    out0=np.zeros((naxis[1],naxis[0]),dtype=np.float32)
    
    wspec=w.sub(['spectral'])
    sz=wspec.pixel_to_world(np.arange(w._naxis[2])).to(u.Hz,equivalencies=u.spectral())
    
    cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0*u.arcsec
    kps=Planck13.kpc_proper_per_arcmin(obj['z']).to(u.kpc/u.arcsec)
    dp=cell*kps
        
    amp=10
    r_eff=(obj['sbProf'][1]/dp).value
    n=obj['sbProf'][2]
    #x_0=obj['sbProf'][3]
    #y_0=obj['sbProf'][4]
    #apmodel=getattr(apmodels,obj['sbProf'][0])(amplitude=amp,r_eff=r_eff,n=n, x_0=px,y_0=py)
    #apmodel=apmodels.Sersic2D(amplitude=amp,r_eff=r_eff,n=n, x_0=px,y_0=py)
    #print(apmodel._bounding_box)
    #"""
    apmodel=apmodels.Gaussian2D(amplitude=amp,
                                x_mean=px,y_mean=py,
                                x_stddev=20,y_stddev=20)
    if  apmodel._bounding_box is not None:
        ((xmin,xmax),(ymin,ymax))=apmodel.bounding_box
        xmin=max(xmin,1)
        xmax=min(xmax,naxis[0]-1)
        ymin=max(ymin,1)
        ymax=min(ymax,naxis[1]-1)
        apmodel.bounding_box=((xmin,xmax),(ymin,ymax))
    apmodel.render(out=out)
    
   
    
    return out
    


def xy_render(objs,w,psf=None,pb=None,normalize_kernel=False):
           
    """
    Note: psf/pb should not contain missing data
    
    map a cloudlets-based model into a gridd data model (i.a FITS image-like for exporting or XY->UV tranform)
    
    objs:       componnet list 
    obj:        target metadata (galactic center position (ra,dec), redshift, vsys, etc.)
                whatever information nesscarity to convert WCS units to physical units
    header:     data frame
    loc:        cloudlet position and velocity in the physical car on-sky frame
    weights:    cloudlet weights 
    
    convert pixel index wthin a WCS to a position in the on-sky galactic coordinates defined in the cloudlet model (ppv)
    
    
    #   get the coordinate of tl tr pix in the galactic frame
    
    #   x/y_sky is along x/y_pix
    #   here we directly map x/y_gal into x/y_pix without considering RA/DEC
        
    pb must match wcs
        if    pb is set
        the outcome is a images with a fluxscale of true_flux x pb
    
    output:
        cube:      the rendered/discretized intrinsic model with absolute flux-scaling
        scube:     convolve(cube*PB,psf)   
        
    Note:    for a frequency-indepdent continuum+PSF model (narrow-band cases), only one convolve_fft run is needed.
             for a spectral line model, the minimal number of convolve_fft runs will depend on its channel-wise extension
             avoid broadcasting in additional dimension as the memory allocation may slow down the process (even slower than loop versions)
             https://stackoverflow.com/questions/49632993/why-python-broadcasting-in-the-example-below-is-slower-than-a-simple-loop
    """
    
    if  pb is None and psf is not None:
        logger.debug("warning: pb is empty!")
        logger.debug("therefore, the primary beam response is not applied to the model image before convolve()")    
    
    convol_fft_pad=False
    convol_psf_pad=False
    convol_complex_dtype=np.complex64   
    convol_boundary='wrap'
    
    convol_count=line_count=cont_count=0
    naxis=w._naxis
    cube=np.zeros((naxis[2],naxis[1],naxis[0]),dtype=np.float32)
    if  psf is not None: scube=np.zeros((naxis[2],naxis[1],naxis[0]),dtype=np.float32)

    #   gather information per object before going into the channel loop,
    
    fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=channel_split(objs,w)
    
    #   Grid Continuum Models (continnuum cloudlets or AP models)
    #   we save fluxscale frequency depedency as vector
    
    im_cache=[]; sm_cache=[]; fluxscale_cache=[]
    iz=int(naxis[2]/2)
    
    for i,obj in enumerate(objs):
        
        if  'lineflux' in obj: continue
        
        if  obj['type'] not in ['apmodel'] and 'contflux' in obj:
            plane=fh.histogram2d(y_list[i],x_list[i],                                             
                                 range=[yrange_list[i],xrange_list[i]],
                                 bins=(naxis[1],naxis[0]),
                                 weights=wt_list[i])
        if  obj['type'] in ['apmodel'] and 'contflux' in obj:
            xx,yy=np.meshgrid(x_list[i],y_list[i])
            plane=((objs[i]['apmodel'])(xx,yy)).value        
            plane=plane/np.sum(plane)
        
        im_cache.append(plane)
        fluxscale_cache.append(fluxscale_list[i])
        
        if  psf is None: continue
        
        if  pb is not None: plane=plane*pickplane(pb,iz)
        plane=convolve_fft(plane,pickplane(psf,iz),
                           fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
                           boundary=convol_boundary,
                           complex_dtype=convol_complex_dtype,#nan_treatment='fill',fill_value=0.0,
                           fftn=fft_use.fftn, ifftn=fft_use.ifftn,
                           normalize_kernel=normalize_kernel)
        convol_count+=1
        sm_cache.append(plane)
        
    #   Render Line+Contnuum Model
    
    for iz in range(naxis[2]):
    
        #   render all line emission
        
        linein=False
        for i in range(len(objs)):
            
            if  'lineflux' not in objs[i]: continue
            if  x_list[i][iz+1].size==0: continue
            
            wt=wt_list[i][iz+1] if wt_list[i] is not None else None ; linein=True
            render_component(cube[iz,:,:],fh.histogram2d(y_list[i][iz+1],x_list[i][iz+1],                                             
                                                         range=[yrange_list[i],xrange_list[i]],
                                                         bins=(naxis[1],naxis[0]),weights=wt),
                             scale=fluxscale_list[i])
            
        #   render all continuum emission
        
        render_component(cube[iz,:,:],im_cache,
                         scale=[fluxscale_cache[j][iz] for j in range(len(im_cache))])         
         
        if  psf is None: continue
        
        if  linein==True:   # line+cont          
            plane=cube[iz,:,:] if pb is None else cube[iz,:,:]*pickplane(pb,iz)
            scube[iz,:,:]=convolve_fft(plane,pickplane(psf,iz),
                                       fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
                                       boundary=convol_boundary,
                                       complex_dtype=convol_complex_dtype,#nan_treatment='fill',fill_value=0.0,
                                       fftn=fft_use.fftn, ifftn=fft_use.ifftn,
                                       normalize_kernel=normalize_kernel)
            convol_count+=1; line_count+=1
        else:               # cont-only
            render_component(scube[iz,:,:],sm_cache,
                             scale=[fluxscale_cache[j][iz] for j in range(len(sm_cache))])
            cont_count+=1
    
    #logger.debug('convolve_fft count: '+str(convol_count))
    #logger.debug('line channel count: '+str(line_count))
    #logger.debug('cont channel count: '+str(cont_count))
    
    if  psf is None:
        return cube
    else:
        return cube,scube
    
# def xy_render(objs,w,psf=None,pb=None,normalize_kernel=False):
#            
#     """
#     Note: psf/pb should not contain missing data
#     
#     map a cloudlets-based model into a gridd data model (i.a FITS image-like for exporting or XY->UV tranform)
#     
#     objs:       componnet list 
#     obj:        target metadata (galactic center position (ra,dec), redshift, vsys, etc.)
#                 whatever information nesscarity to convert WCS units to physical units
#     header:     data frame
#     loc:        cloudlet position and velocity in the physical car on-sky frame
#     weights:    cloudlet weights 
#     
#     convert pixel index wthin a WCS to a position in the on-sky galactic coordinates defined in the cloudlet model (ppv)
#     
#     
#     #   get the coordinate of tl tr pix in the galactic frame
#     
#     #   x/y_sky is along x/y_pix
#     #   here we directly map x/y_gal into x/y_pix without considering RA/DEC
#         
#     pb must match wcs
#         if    pb is set
#         the outcome is a images with a fluxscale of true_flux x pb
#     
#     output:
#         cube:      the rendered/discretized intrinsic model with absolute flux-scaling
#         scube:     convolve(cube*PB,psf)   
#         
#     Note:    for a frequency-indepdent continuum+PSF model (narrow-band cases), only one convolve_fft run is needed.
#              for a spectral line model, the minimal number of convolve_fft runs will depend on its channel-wise extension
#              avoid broadcasting in additional dimension as the memory allocation may slow down the process (even slower than loop versions)
#              https://stackoverflow.com/questions/49632993/why-python-broadcasting-in-the-example-below-is-slower-than-a-simple-loop
#     """
#     
#     if  pb is None and psf is not None:
#         logger.debug("warning: pb is empty!")
#         logger.debug("therefore, the primary beam response is not applied to the model image before convolve()")    
#     
#     convol_fft_pad=False
#     convol_psf_pad=False
#     convol_complex_dtype=np.complex64   
#     convol_boundary='wrap'
#     
#     convol_count=line_count=cont_count=0
#     naxis=w._naxis
#     cube=np.zeros((naxis[2],naxis[1],naxis[0]),dtype=np.float32)
#     if  psf is not None: scube=np.zeros((naxis[2],naxis[1],naxis[0]),dtype=np.float32)
# 
#     #   gather information per object before going into the channel loop,
#     
#     fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=channel_split(objs,w)
#     
#     #   Grid Continuum Models (continnuum cloudlets or AP models)
#     #   we save fluxscale frequency depedency as vector
#     
#     im_cache=[]; sm_cache=[]; fluxscale_cache=[]
#     iz=int(naxis[2]/2)
#     
#     for i,obj in enumerate(objs):
#         
#         if  obj['type'] not in ['disk2d','point','apmodel']: continue
#         
#         if  obj['type'] in ['disk2d','point']:
#             plane=fh.histogram2d(y_list[i],x_list[i],                                             
#                                  range=[yrange_list[i],xrange_list[i]],
#                                  bins=(naxis[1],naxis[0]),
#                                  weights=wt_list[i])
#         if  obj['type'] in ['apmodel']:
#             xx,yy=np.meshgrid(x_list[i],y_list[i])
#             plane=((objs[i]['apmodel'])(xx,yy)).value        
#             plane=plane/np.sum(plane)
# 
#         im_cache.append(plane)
#         fluxscale_cache.append(fluxscale_list[i])
#         
#         if  psf is None: continue
#         
#         if  pb is not None: plane=plane*pickplane(pb,iz)
#         plane=convolve_fft(plane,pickplane(psf,iz),
#                            fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
#                            boundary=convol_boundary,
#                            complex_dtype=convol_complex_dtype,#nan_treatment='fill',fill_value=0.0,
#                            fftn=fft_use.fftn, ifftn=fft_use.ifftn,
#                            normalize_kernel=normalize_kernel)
#         convol_count+=1
#         sm_cache.append(plane)
#     
#     #   Render Line+Contnuum Model
#     
#     for iz in range(naxis[2]):
#     
#         #   render all line emission
#         
#         linein=False
#         for i in range(len(objs)):
#             
#             if  objs[i]['type'] not in ['disk3d']: continue
#             if  x_list[i][iz+1].size==0: continue
#             
#             wt=wt_list[i][iz+1] if wt_list[i] is not None else None ; linein=True
#             render_component(cube[iz,:,:],fh.histogram2d(y_list[i][iz+1],x_list[i][iz+1],                                             
#                                                          range=[yrange_list[i],xrange_list[i]],
#                                                          bins=(naxis[1],naxis[0]),weights=wt),
#                              scale=fluxscale_list[i])
#             
#         #   render all continuum emission
#         
#         render_component(cube[iz,:,:],im_cache,
#                          scale=[fluxscale_cache[j][iz] for j in range(len(im_cache))])         
#          
#         if  psf is None: continue
#         
#         if  linein==True:   # line+cont          
#             plane=cube[iz,:,:] if pb is None else cube[iz,:,:]*pickplane(pb,iz)
#             scube[iz,:,:]=convolve_fft(plane,pickplane(psf,iz),
#                                        fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
#                                        boundary=convol_boundary,
#                                        complex_dtype=convol_complex_dtype,#nan_treatment='fill',fill_value=0.0,
#                                        fftn=fft_use.fftn, ifftn=fft_use.ifftn,
#                                        normalize_kernel=normalize_kernel)
#             convol_count+=1; line_count+=1
#         else:               # cont-only
#             render_component(scube[iz,:,:],sm_cache,
#                              scale=[fluxscale_cache[j][iz] for j in range(len(sm_cache))])
#             cont_count+=1
#      
#     #logger.debug('convolve_fft count: '+str(convol_count))
#     #logger.debug('line channel count: '+str(line_count))
#     #logger.debug('cont channel count: '+str(cont_count))
#     
#     if  psf is None:
#         return cube
#     else:
#         return cube,scube    