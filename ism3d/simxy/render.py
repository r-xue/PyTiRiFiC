import numpy as np
import scipy
import astropy.units as u
from astropy.wcs import WCS
from astropy import constants as const
from astropy.cosmology import Planck13 as cosmos
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


from ..arts.utils import fluxscale_from_contflux
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
    + for 2D objects, the render function will output a 2D plane + fluxscale for each plane.
      this is preferred for memory managament, and 3D data will only be assembed at the final rendering stage.
      it's important to do this for mutiple-object mutiple-channel data.
"""

def render_spmodel3d(obj,w,out=None):
    """
    render a sparse model 
    """
    
    return

def render_apmodel2d(obj,w,out=None,normalize=True):
    """
    obj:     object prescription
    w:       wcs 
        
    Render astropy.modeling.models into the specificied WCS system
        https://docs.astropy.org/en/stable/modeling/predef_models2D.html
    
    normalize:  True: normalize the total readout in the plane template to 1
                False: normaliz the peak readout in the plane template to 1
                
    """

    naxis=w._naxis
    # need to fix the astropy bug
    # see: https://github.com/astropy/astropy/pull/10542
    out0=np.zeros((naxis[1],naxis[0]),dtype=np.float32) 
        
    # not all model requires x/y, but we set px,py to image center by default
    try:
        px,py=w.celestial.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,0)
        #xp, yp = skycoord_to_pixel(center, wcs)
    except:
        px=naxis[0]/2.0 ; py=naxis[1]/2.0
    
    cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0*u.arcsec
    kps=cosmos.kpc_proper_per_arcmin(obj['z']).to(u.kpc/u.arcsec)
    dp=cell*kps
    
    if  not isinstance(obj['sbProf'],(tuple,list)):
        obj['sbProf']=(obj['sbProf'],)
    model_name=obj['sbProf'][0]
    model_par=obj['sbProf'][1:]

    if  model_name == 'AiryDisk2D':
        radius=(model_par[0]/dp).value
        apmodel=getattr(apmodels,model_name)(1,px,py,radius)

    if  model_name == 'Box2D':
        x_width=(model_par[0]/dp).value
        y_width=(model_par[1]/dp).value
        apmodel=getattr(apmodels,model_name)(1,px,py,x_width,y_width)

    if  model_name == 'Const2D':
        apmodel=getattr(apmodels,model_name)(1)

    if  model_name == 'Ellipse2D':
        a=(model_par[0]/dp).value
        b=(model_par[1]/dp).value
        theta=(model_par[2]+90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,model_name)(1, px,py, a, b, theta)

    if  model_name == 'Disk2D':
        R_0=(model_par[0]/dp).value
        apmodel=getattr(apmodels,model_name)(1, px,py, R_0)

    if  model_name == 'Gaussian2D':
        x_stddev=(model_par[0]/dp).value
        y_stddev=(model_par[1]/dp).value
        theta=(model_par[2]+90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,model_name)(1, px,py,x_stddev,y_stddev,theta)
    
    if  model_name == 'Planar2D':
        slope_x=(model_par[0]/dp).value
        slope_y=(model_par[1]/dp).value
        apmodel=getattr(apmodels,model_name)(slope_x,slope_y,1)
    
    if  model_name == 'Sersic2D':
        r_eff=(model_par[0]/dp).value
        n=model_par[1]
        try:
            ellip=model_par[2]
        except:
            ellip=0
        try:
            theta=(model_par[3]+90*u.deg).to_value(u.rad)
        except:
            theta=(90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,model_name)(1, r_eff,n,px,py,ellip,theta)   
    
    if  model_name == 'Ring2D':
        r_in=(model_par[0]/dp).value
        width=(model_par[1]/dp).value
        apmodel=getattr(apmodels,model_name)(1, px,py,r_in,width)

    if  model_name == 'RickerWavelet2D':
        sigma=(model_par[0]/dp).value
        apmodel=getattr(apmodels,model_name)(1, px,py,sigma)    
    
    #   try to render apmodel
    try:
        if  apmodel._bounding_box is not None:
            ((xmin,xmax),(ymin,ymax))=apmodel.bounding_box
            xmin=max(xmin,1)
            xmax=min(xmax,naxis[0]-1)
            ymin=max(ymin,1)
            ymax=min(ymax,naxis[1]-1)
            apmodel.bounding_box=((xmin,xmax),(ymin,ymax))
        apmodel.render(out=out0)
    except:
        pass
    
    #   try to add point-source model
    if  model_name == 'Point':
        out0[round(float(py)),round(float(px))]=1.0
    else:
        # only need to normalizate for non-point source
        if  normalize==True:
            if  not out0.any():
                out0/=out0.sum()
        else:
            if  model_name=='Sersic2D':
                # sersic model amp is not defined as peak value.
                # we do a peak normalization to maintain consistency
                out0/=np.max(out0)
            
    fluxscale=fluxscale_from_contflux(obj['contflux'],w)
    
    return out0,fluxscale


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