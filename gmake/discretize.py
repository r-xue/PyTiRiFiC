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
from .utils import fft_use
from galario.single import sampleImage
from galario.double import sampleImage as d_sampleImage
from copy import deepcopy
from .io import *
from .dynamics import model_vrot
from .model import model_realize    
from .model import model_setup
from .model import clouds_discretize_2d
from .utils import write_par
from .utils import inp2mod
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

def pix2sky(obj,w,px=None,py=None,pz=None):
    """
    convert pixel index (zero-based) 
    to
    the reference model coordinate system
        for line emission "cloudlet" objects:
            the sky-projected rest-frame galactic coodrinates, which is centered around the object xypos)
            z = LOS
        for continuume emission "cloudlet" objects:
            spatial-wise the sky-projected rest-frame galactic coodrinates, which is centered around the object xypos)
            spectral-wise, sky-or-rest-frame wavelength or frequency
    
    "sky-frame" could be (angular,angular,velocity) or (distance,distance,velocity)
    while typically the sky-frame is defined in angular units;
    if the sky frame is defined in length the angular seperation will be converted to physical angular size.
    the object redshift is required
        
        We assume:
            inverse-RA (and pixel-x) aligns along with x
            DEC (and pixel-y) aligns along with y 
        The functin dosn't consider pixel rotation at this moment
        
    Essentially, we transfer:
        ModelRef_origin->World->pix:
        Then map pix index back to ModelRef Vec
    
    mxo,myo,mzo:    the origin of the reference model
    
    for cloudlet3d models:    (kpc,kpc,km/s)
    for cloudlet2d models:    (kpc,kpc,Hz)
    
    """
    
    """
    wz      : galaxy zero systematic velocity or continum reference sky frquency / wavelength 
            in frequency (Hz) or wavelength (m) 
    dz/sz   : for disk3d in velocity
              for disk2d in frequency or wavelength
    
    if px/py/pz is not specified, will be 1d vector from 0 to naxiy
    the sx will tell you the sky-value for px=0/px=1/px=2...                 
    """
    
    #   Line Object
    
    if  obj['type']=='disk3d':
        if  'Hz' in w.wcs.cunit[2].name:
            wz=(obj['restfreq']/(1.0+obj['z'])*(1.-obj['vsys']/const.c)).to(u.Hz)
            dz=(-const.c*w.wcs.cdelt[2]*u.Hz/(obj['restfreq']/(1.0+obj['z']))).to(u.km/u.s)
        if  'angstrom' in w.wcs.cunit[2].name:
            wz=(obj['restwave']*(1.0+obj['z'])*(1.+obj['vsys']/const.c)).to(u.m)
            dz=(const.c*w.wcs.cdelt[2]*u.angstrom/(obj['restwave']*(1.0+obj['z']))).to(u.km/u.s)
        if  'm/s' in w.wcs.cunit[2].name:
            wz=obj['vsys']
            dv=(w.wcs.cdelt[2]*u.m/u.s).to(u.km/u.s)
        mxo=myo=mzo=0.0    
        
    #   Continuum Object
    
    if  obj['type']=='disk2d' or obj['type']=='point' or obj['type']=='apmodel':
        if  'Hz' in w.wcs.cunit[2].name:
            wz=obj['contfreq'].to(u.Hz)
            dz=w.wcs.cdelt[2]*u.Hz
        if  'angstrom' in w.wcs.cunit[2].name:
            wz=obj['contwave'].to(u.m)
            dz=w.wcs.cdelt[2]*u.angstrom
        mxo=myo=0; mzo=wz
        
    #   get 0-based pix-index of galactic center in the spectral cube
    
    if  w.naxis==4:
        fpx,fpy,fpz,fps=w.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,wz,1,0)
    if  w.naxis==3:
        fpx,fpy,fpz=w.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,wz.si,0)    
    
    cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0*u.arcsec
    kps=Planck13.kpc_proper_per_arcmin(obj['z']).to(u.kpc/u.arcsec)
    dp=cell*kps
    
    pp=w._naxis
    if  px is None: px=np.arange(pp[0])
    if  py is None: py=np.arange(pp[1])
    if  pz is None: pz=np.arange(pp[2])

    sx=(px-fpx)*dp+mxo
    sy=(py-fpy)*dp+myo
    sz=(pz-fpz)*dz+mzo
    
    return sx,sy,sz


def clouds_perchan(clouds_loc,clouds_wt,sv,return_v=False):
    """
    split clouds_loc by its LOS velocity 
    
    clouds_loc 6D cloud location
    sv:    LOS velocity sampling vector
    
    note: sv and clouds_loc.d_z are defined by flipped sign;
          so we consider sv <-> -d_z  
          
    Ref:
        The implemented method is analogous to IDL histogram's reverse_indices:
        https://stackoverflow.com/questions/26783719/efficiently-get-indices-of-histogram-bins-in-python
        https://stackoverflow.com/questions/2754905/vectorized-approach-to-binning-with-numpy-scipy-in-python
        https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)
        
    return:
        list of cloudsset: each elements contain the clouds located within each channel plane
    
    """
    
    dv=sv[1]-sv[0]
    vrange=[sv[0]-dv/2,sv[-1]+dv/2]
    nbins=sv.size
    ch=((-nbins/(vrange[1]-vrange[0]))*clouds_loc.differentials['s'].d_z+\
        (vrange[1]-nbins*vrange[0]-vrange[0])/(vrange[1]-vrange[0])).astype(int)

    ##########################################################
    # Note:  ch=1 represents cloudlets within the first data channel
    #        ch=nbins represents cloudlets within the last data channel
    #       (-0.1/0.1).astype(int):
    #        making ch=0 ambigous in terms of representation in the data frame.
    ##########################################################
    
    ch_of_firstrow=np.minimum(np.min(ch),1)
    ch_of_lastrow=np.maximum(np.max(ch),nbins)
    nrow=ch_of_lastrow-ch_of_firstrow+1
    
    N=clouds_loc.size
    
    # for x_/y_list: first/last element saving cloudlets beyond the data channel coverage
    # so len(x_list)=2+nbins  
    
    # we use csr_matrix to performance partial sorting over the entire dgitized velocity range
    # the row index (irow) of the cloudlet in the CSR storage
    irow=ch-ch_of_firstrow  
    icol=np.arange(N)

    # we can also return csr_matrix and do slicing in mapper/chi2uv/chi2im
    # but there is no signature performance benefits
    csr_x = csr_matrix((clouds_loc.x.value, (irow, icol)), shape=(nrow, N))
    csr_y = csr_matrix((clouds_loc.y.value, (irow, icol)), shape=(nrow, N))
    x_perchan=np.split(csr_x.data, csr_x.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ])
    y_perchan=np.split(csr_y.data, csr_y.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ])
    if  clouds_wt is None:
        wt_perchan=None
    else:
        csr_wt = csr_matrix((clouds_wt, (irow, icol)), shape=(nrow, N))
        wt_perchan=np.split(csr_wt.data, csr_wt.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ])
        
    if  return_v==True:
        csr_v = csr_matrix((objs[i]['clouds_loc'].differentials['s'].d_z.value, (irow, icol)), shape=(nrow, N))
        v_perchan=np.split(csr_v.data, csr_v.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ])
        return x_perchan,y_perchan,wt_perchan,v_perchan
    else:
        return x_perchan,y_perchan,wt_perchan

def channel_split(objs,w):
    """
    Divivd the cloudlet model by channel in advance
    to avoid doing it during channel looping
    


    Note:
        returned v has a flip sign from V_los
        vrange[0] first channel velocity and vrange[1] last channel velocity 
        
        The returned list should have a element number of N(objs)
    
    for ccloudlet model: fluxscale is the flux per cloud
    for continuum model: fluxscale is the flux of the object within a plane
    """

    fluxscale_list=[]   # in Jy
    xrange_list=[]      # in kpc
    yrange_list=[]      # in kpc
    x_list=[]           # in kpc
    y_list=[]           # in kpc
    wt_list=[]          # arbitary

    for i in range(len(objs)):
        
        # return coordinate transform info
        
        sx,sy,sz=pix2sky(objs[i],w)

        #   for line component, we group clouds by their channel locations
        
        if  objs[i]['type']=='disk3d':
            
            # eqavelent flux density contribution per cloud within one channel
            
            dv=sz[1]-sz[0] 
            fluxscale=objs[i]['lineflux']/objs[i]['clouds_loc'].size/np.abs(dv)
            fluxscale_list.append(fluxscale.to_value('Jy'))
            
            x_perchan,y_perchan,wt_perchan=\
                clouds_perchan(objs[i]['clouds_loc'],objs[i]['clouds_wt'],sz,return_v=False)        
            x_list.append(x_perchan)
            y_list.append(y_perchan)
            wt_list.append(wt_perchan)
            
        #   fpr continuum componnet, we derive the frequency-dependent-scaling and 
        #   attached the channel-indepdent clouds location. 
        
        if  objs[i]['type']=='disk2d' or objs[i]['type']=='point':
            
            # flux density contribution per cloud within each channel
            fluxscale=objs[i]['contflux']/objs[i]['clouds_loc'].size
            fluxscale=fluxscale*((sz/objs[i]['contfreq'])**objs[i]['alpha'])
            fluxscale_list.append(fluxscale.to_value('Jy'))
            x_list.append(objs[i]['clouds_loc'].x.value)
            y_list.append(objs[i]['clouds_loc'].y.value)
            wt_list.append(objs[i]['clouds_wt'])
            
        if  objs[i]['type']=='apmodel':
            
            # flux density contribution per cloud within each channel
            fluxscale=objs[i]['contflux']
            fluxscale=fluxscale*((sz/objs[i]['contfreq'])**objs[i]['alpha'])
            fluxscale_list.append(fluxscale.to_value('Jy'))
            x_list.append(sx)
            y_list.append(sy)
            wt_list.append(None)            

        dx=sx[1]-sx[0]
        xrange_list.append([sx[0].value-dx.value/2,sx[-1].value+dx.value/2])
        dy=sy[1]-sy[0]
        yrange_list.append([sy[0].value-dy.value/2,sy[-1].value+dy.value/2])

    return fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list


def lognsigma_lookup(objs,dname):
    """
    update some model parameters related to likelihood calculation
        In the model properties, we have some keywords related to configing the likelihood
    model and calculate log_propeorbaility:
        lognsigma: used to scale noise level (in case it's overunder estimated)
    They are actually related to data (one value per dataset)
    But it's setup per object due to the input file layout (repeated for different objects, like PSF)
    # we expected lognsigma is the same for one dname from all objs 
    """
    
    lognsigma=0
    for i in range(len(objs)):
        if  ('vis' in objs[i] or 'image' in objs[i]) and ('lognsigma' in objs[i]):
            if  'vis' in objs[i]:
                dname_list=objs[i]['vis'].split(",")
            if  'image' in objs[i]:
                dname_list=objs[i]['image'].split(",")
            for j in range(len(dname_list)):
                if  dname==dname_list[j]:
                    if  isinstance(objs[i]['lognsigma'],(list,tuple)):
                        lognsigma=objs[i]['lognsigma'][j]
                    else:
                        lognsigma=objs[i]['lognsigma']
    
    return lognsigma

def render_component(out,im,scale=1,mode='iadd'):
    """
    in-plane-add model components into spectral-cube or mutil-freq MS
    see other mode options: e.g. iadd/isub
        https://docs.python.org/3.8/library/operator.html
    
    out=None return a new obect
    out!=None return a reference point to the updated out
    
    Note:
        this may return a view of numpy if out is a slice 
        
    from gmake.discretize import render_component
    cube=np.zeros((3,3,3))
    
    cube[0,:,:]=render_component(cube[0,:,:],np.ones((3,3)),scale=5)
    x=render_component(cube[0,:,:],np.ones((3,3)),scale=5) 
    np.may_share_memory(x,cube)
    
    warning: 
        cube=render_component(cube[0,:,:],np.ones((3,3)),scale=5)
        will override your cube values.. 
        one should use instead:
        cube[0,:,:]=render_component(cube[0,:,:],np.ones((3,3)),scale=5)
    if im=[], it will do nothing...          
    
    
    if  you're not sure out is None, maybe use:
        out=render_component(out)
    if  you know out is not None, use
        render_component(out)
    
    """
    if  out is not None:
        
        if  isinstance(im,list):
            for i in range(len(im)):
                out=render_component(out,im[i],scale=scale[i],mode=mode)
        else:
            out=getattr(operator,mode)(out,im*scale)
    else:
        if  isinstance(im,list):
            for i in range(len(im)):
                out=render_component(out,im[i],scale=scale[i],mode=mode)
        else:
            out=im*scale
            
    return out

def pickplane(im,iz):
    """
    pick a channel plane from a "cube"
    """
    if  im.ndim==2:
        return im
    if  im.ndim==3:
        return im[iz,:,:]
    if  im.ndim==4:
        return im[0,iz,:,:]
    
    
def sample_prep(w,phasecenter,tol=0.01):
    """
    do some prep for galario.sampleImage()
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
    phasecenter_sc = SkyCoord(phasecenter[0], phasecenter[1], frame='icrs')
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

##########################################################################

def xy_render(objs,w,psf=None,pb=None,normalize_kernel=False):
           
    """
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
    
    if  pb is None:
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
        
        if  obj['type'] not in ['disk2d','point','apmodel']: continue
        
        if  obj['type'] in ['disk2d','point']:
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
            
            if  objs[i]['type'] not in ['disk3d']: continue
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

def uv_render(objs,w,uvw,phasecenter,pb=None,wideband=False):
    """
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

    #   prep for sampleImage()
        
    dRA,dDec,cell,wv=sample_prep(w,phasecenter)

    #   gather information per object before going into the channel loop,
    
    fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=channel_split(objs,w) 
  
    #   Grid Continuum Models (continnuum cloudlets or AP models)
    #   we save fluxscale frequency depedency as vector
    
    im_cache=[]; uv_cache=[]; fluxscale_cache=[]
    iz=int(naxis[2]*0.5)
        
    for i,obj in enumerate(objs):

        if  obj['type'] not in ['disk2d','point','apmodel']: continue
        
        if  obj['type'] in ['disk2d','point']:
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
             
            if  objs[i]['type'] not in ['disk3d']: continue
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
            
    logger.debug('uvsample count: '+str(sample_count))
    logger.debug('line channel count: '+str(line_count))
    logger.debug('cont channel count: '+str(cont_count))            
            
    return vis

def uv_sample_nearest(plane,cell,uu,vv,dRA=0.,dDec=0.,PA=0,
                      factor=10,saveuvgrid=False):
    """
    factor:    oversampling factor
    runtime scaled with oversampled plane size
    
    uv-plane oversampling (using n or s keywod) 
    xy-zero padding around image (done manually)
    """
    
    nxy_plane=plane.shape
    dRA  += nxy_plane[1]/2*cell 
    dDec -= nxy_plane[0]/2*cell
    dRA  *= 2.*np.pi
    dDec *= 2.*np.pi

    # Image FT
    
    planeft =scipy_fft.rfft2(plane,s=(nxy_plane[0]*factor,nxy_plane[1]*factor),workers=12)

    nxy = planeft.shape[0]    
    duv = 1. / (nxy*cell)

    # apply rotation
    
    cos_PA = np.cos(PA)
    sin_PA = np.sin(PA)
    urot = uu * cos_PA - vv * sin_PA
    vrot = uu * sin_PA + vv * cos_PA    
    dRArot = dRA * cos_PA - dDec * sin_PA
    dDecrot = dRA * sin_PA + dDec * cos_PA

    # uv cell indices
    
    uroti = np.abs(urot)/duv
    vroti = -vrot/duv
    uneg = urot < 0.
    vroti[uneg] = vrot[uneg]/duv
    vis=planeft[np.around(vroti).astype(np.int),np.around(uroti).astype(np.int)]
    np.conj(vis,out=vis,where=uneg)
    
    theta = urot*dRArot + vrot*dDecrot        
    vis*=np.exp(+1j*theta)
    
    if  saveuvgrid==True:
        
        fits.writeto('real.fits',planeft.real,overwrite=True)
        fits.writeto('imag.fits',planeft.imag,overwrite=True)
        fits.writeto('ap.fits',np.abs(planeft),overwrite=True)
        fits.writeto('ph.fits',np.angle(planeft),overwrite=True)         
    
    return vis   

def uv_sample_nufft(plane,cell,uu,vv,dRA=0.,dDec=0.,PA=0):
    """
    factor:    oversampling factor
    runtime scaled with oversampled plane size
    https://cims.nyu.edu/cmcl/nufft/nufft.html
    """
    
    dRA  *= 2.*np.pi
    dDec *= 2.*np.pi
    
    cos_PA = np.cos(PA)
    sin_PA = np.sin(PA)

    urot = uu * cos_PA - vv * sin_PA
    vrot = uu * sin_PA + vv * cos_PA    

    # Fast Non-uniform FFT
    
    vis=np.zeros((len(uu)),dtype=np.complex128)
    nufft.nufft2d2(vrot*(cell*2*np.pi),-urot*(cell*2*np.pi),vis,1,1e-3,plane,\
                   debug=0,spread_debug=0,spread_sort=2,fftw=1,modeord=0,\
                   chkbnds=1,upsampfac=1.25)
    return vis  
     
def uv_sample_direct(plane,cell,uu,vv,dRA=0.,dDec=0.,PA=0,dimsum='uv',drange=10):
    """
    runtime scaled with "active" pixel n (loop over active pixel)
    runtime scaled with nrecord (loop over active visibility)
    a run time is only acceptable for limited amount of point source
    """

    nxy = plane.shape[0]

    dRA *= 2.*np.pi
    dDec *= 2.*np.pi


    # apply rotation
    
    cos_PA = np.cos(PA)
    sin_PA = np.sin(PA)

    urot = uu * cos_PA - vv * sin_PA
    vrot = uu * sin_PA + vv * cos_PA

    #   remove some faint pixel
        
    planemax=np.max(plane)
    plane[np.where(plane<=planemax/drange)]=0
    
    im_csr=csr_matrix(plane)
    iy,ix=im_csr.nonzero()
    im=im_csr.data
    ny,nx=im_csr.shape
    
    vis=np.zeros((len(uu)),dtype=np.complex128)
    
    dRArot = dRA * cos_PA - dDec * sin_PA
    dDecrot = dRA * sin_PA + dDec * cos_PA
    theta = urot*dRArot + vrot*dDecrot        
    
    if  dimsum=='uv':
        for i in range(len(im)):
            vis+=im[i]*np.exp(-1j* ( -theta+2*np.pi*(urot*(nx/2-ix[i])*(-cell)+vrot*(ny/2-iy[i])*cell) ) )
    if  dimsum =='xy':
        for i in range(len(urot)):
            vis[i]=np.sum(im*np.exp(-2j*np.pi*(urot[i]*(nx/2-ix)*(-cell)+vrot[i]*(ny/2-iy)*cell)))

    return vis    

def uv_sample_interp2d(plane,cell,uu,vv,dRA=0.,dDec=0.,PA=0,origin='upper',
                mode='ap',ik=5,saveuvgrid=False):  
    
    if origin == 'upper':
        v_origin = 1.
    elif origin == 'lower':
        v_origin = -1.

    nxy = plane.shape[0]

    dRA *= 2.*np.pi
    dDec *= 2.*np.pi

    du = 1. / (nxy*cell)

    # Real to Complex transform
    fft_r2c_shifted = pyfftw.interfaces.numpy_fft.fftshift(
                        fft_use.rfft2(
                            pyfftw.interfaces.numpy_fft.fftshift(plane)), axes=0)
    
    if  saveuvgrid==True:
        
        fits.writeto('real.fits',fft_r2c_shifted.real,overwrite=True)
        fits.writeto('imag.fits',fft_r2c_shifted.imag,overwrite=True)
        fits.writeto('ap.fits',np.abs(fft_r2c_shifted),overwrite=True)
        fits.writeto('ph.fits',np.angle(fft_r2c_shifted),overwrite=True)        

    # apply rotation
    cos_PA = np.cos(PA)
    sin_PA = np.sin(PA)

    urot = uu * cos_PA - vv * sin_PA
    vrot = uu * sin_PA + vv * cos_PA

    dRArot = dRA * cos_PA - dDec * sin_PA
    dDecrot = dRA * sin_PA + dDec * cos_PA

    # interpolation indices
    uroti = np.abs(urot)/du
    vroti = nxy/2. + v_origin * vrot/du
    uneg = urot < 0.
    vroti[uneg] = nxy/2 - v_origin * vrot[uneg]/du
    

    # coordinates of FT
    u_axis = np.linspace(0., nxy // 2, nxy // 2 + 1)
    v_axis = np.linspace(0., nxy - 1, nxy)
    
    # We use RectBivariateSpline to do only linear interpolation, which is faster
    # than interp2d for our case of a regular grid.
    # RectBivariateSpline does not work for complex input, so we need to run it twice.
    f_re = RectBivariateSpline(v_axis, u_axis, fft_r2c_shifted.real, kx=ik, ky=ik, s=0)
    ReInt = f_re.ev(vroti, uroti)
    f_im = RectBivariateSpline(v_axis, u_axis, fft_r2c_shifted.imag, kx=ik, ky=ik, s=0)
    ImInt = f_im.ev(vroti, uroti)
    
    if  mode=='ap':
        f_amp = RectBivariateSpline(v_axis, u_axis, np.abs(fft_r2c_shifted), kx=ik, ky=ik, s=0)
        AmpInt = f_amp.ev(vroti, uroti)

    # correct for Real to Complex frequency mapping
    
    uneg = urot < 0.
    ImInt[uneg] *= -1.
    PhaseInt = np.angle(ReInt + 1j*ImInt)

    # apply the phase change
    #
    if  method=='ap':
        theta = urot*dRArot + vrot*dDecrot
        vis = AmpInt * (np.cos(theta+PhaseInt) + 1j*np.sin(theta+PhaseInt))
    if  method=='ri':
        theta = urot*dRArot + vrot*dDecrot
        vis = ReInt+ImInt*1j
        vis*=np.exp(+1j*theta) # shift phase
        
    return vis          

def uv_sample(plane,cell,uu,vv,dRA=0.,dDec=0.,PA=0,origin='upper',
                method='interp2d',ik=5,saveuvgrid=False):
    """
    #galario: scaled with fft-size
    
    + fourier transform of a model image
    + discretized uv sampling using MS uvw 
    
    dRA,dDec optionsare not implemented yet
    
    method:
        'direct':     brutal force direct fourier transform using summing (slow, and only okay for a couple of point sources)
                      linear+accurate but slow
        'interp2d':   this is close to the method implemented in galario (in C or py_sampleImage.py)
                      howerver, galarios linear 2D interp method is problamtics for complicated structure 
                      or multiple offcenter-source (as the amp / phase surface is not smooth)
                      see related disscussion: https://github.com/mtazzari/galario/pull/132#issuecomment-396703582
                      Although interpolae amp/phase is an working solution up to 1% for single simple source at center or offcenter
                      For more cocmplicated source, the linear interpolation is insuffcient. 
                      The issue is fixed here by introducing high-order spline interpolation, but lose linearrity in XY-UV transform
        'interp2d_ph': the algroithm used in galario (one should alway interp phase as for point sources)
                      this should give the same results as galario, just slower...
        'galario':    call galario python API interface (see the problem above)  
                      currently, it will linear-interp amp and linear-interp phase.
                      different from linear-interp real/imag  
    
    
    Some options to improve presion/accuracy
    
        interpolate in UV (be careful) REAL/IMAG or AMP/PH (preferred)
            low-order if amp/phase smooth
            high-order if amp/phase complicated.
        direct FFT (expensive)
        oversampling UV grid (expensive)
        
        disaeemble different objects (adjust input facet size) for performance and simplify UV-plane surface
        
        the power pixel location within the input image determine the ripple in phase/real/imag
    
    important note:
    
        When using any interpolation-based method, for best precision/accurancy, it's better to
            1. keep the source emission close to the input image pixel center and perform re-phasing (i.a. dRA/dDec) in UV to get the correct results
               In this way, the amp/phase is rather a smooth function, and interp2d will work best even at low-order (e.g. linear interp)
            2. it's better to interpolate amp and phase rather than interpolate real/image especially when phase (therefore real/image, this is off-center case)
            3. (offset from image center) / (half image size) is roughly the sample step in one wrap 
            4. The most critical thing:
                depress the phase change in the UV grid to make the "degridding" (i.a interpolate to discretc point) precise.
                also be careful about uv sampling beyond UV grid range.
                the phase change is determined by the source location in the fft-ready image.
                dRA,dDec could help to adjust as it phaseshift is more precise rathatan shifting object location in pixel image
    Rule:
        
        Imsize larger than twice of object size
    
    For estimating effeciency:
        if uv.size>im.size, then interpolating or nearest is likely faster
    """
    if  method=='nearest':
        
        return  uv_sample_nearest(plane,cell,uu,vv,dRA=dRA,
                                 dDec=dDec,PA=PA,factor=20,saveuvgrid=saveuvgrid)
        
    if  method=='nufft':
        
        return  uv_sample_nufft(plane,cell,uu,vv,dRA=dRA,
                                 dDec=dDec,PA=PA)        
    
    if  method=='galario':

        return  sampleImage(plane.astype(np.float32),cell,
                            uu.astype(np.float32),vv.astype(np.float32),
                            dRA=dRA,dDec=dDec,PA=PA,origin='lower',check=False)

    if  method=='direct':

        return  uv_sample_direct(plane.astype(np.float32),cell,
                                 uu.astype(np.float32),vv.astype(np.float32),
                                 dRA=dRA,dDec=dDec,PA=PA)

    if  'interp2d' in method:
        if  '-ri' in method: 
            mode='ri'
        if  '-ap' in method: 
            mode='ap'
        return  uv_sample_interp2d(plane,cell,uu,vv,dRA=dRA,dDec=dDec,PA=PA,
                                   origin=origin,
                                   mode=mode,ik=5,saveuvgrid=saveuvgrid)    
        

    
  
##########################################################################

def model_render(theta,fit_dct,inp_dct,dat_dct,
                 models=None,
                 savemodel=None,decomp=False,nsamps=1e5,
                 verbose=False,test_threading=False):
    """
    the likelihood function
    
        step:    + fill the varying parameter into inp_dct
                 + convert inp_dct to mod_dct
                 + use mod_dct to regenerate RC
    
    theta can be quanitity here
    
    returnwdev=True is a special mode reserved for lmfit
    
    retired option: returnwdev=True
    models,inp_dct0,mod_dct0=model_render(theta,fit_dct,inp_dct,meta.dat_dct_global,models=models,returnwdev=True)
    wdev=[]
    for tag in list(models.keys()):
        if  'imodel@' in tag:
            dname=tag.replace('imodel@','')
            wdev.append(models['model@'+dname].ravel().astype(np.float32))
    
    """

    
    ll=0
    chisq=0
    wdev=np.array([])

    # copy and modify model input dct
    
    inp_dct0=deepcopy(inp_dct)
    p_num=len(fit_dct['p_name']) 
    for ind in range(p_num):
        write_par(inp_dct0,fit_dct['p_name'][ind],theta[ind],verbose=False)
    
    mod_dct=inp2mod(inp_dct0)   # in physical units
    #model_vrot(mod_dct)         # in natural (default internal units)

    # attach the cloudlet (reference) model to mod_dct
    
    model_realize(mod_dct,
                nc=100000,nv=20,seeds=[None,None,None,None])

    # build model container (skipped during iteration)
    if  models is None:
        models=model_setup(inp2mod(mod_dct),dat_dct,decomp=decomp,verbose=verbose)

    # calculate chisq 
           
    for tag in list(models.keys()):
        
        if  'imodel@' in tag:
            
            dname=tag.replace('imodel@','')
            objs=[mod_dct[obj] for obj in models[tag.replace('imodel@','objs@')]]
            w=models['wcs@'+dname]
            if  models[tag.replace('imodel@','type@')]=='vis':                
                model_one=uv_render(objs,w,
                                    dat_dct['uvw@'+dname],
                                    dat_dct['phasecenter@'+dname],
                                    pb=models['pbeam@'+dname])
            if  models[tag.replace('imodel@','type@')]=='image':
                imodel,model_one=xy_render(objs,w,
                                    psf=models['psf@'+dname],normalize_kernel=False,
                                    pb=models['pbeam@'+dname])

            models['model@'+dname]=model_one

    return models,inp_dct0,mod_dct




