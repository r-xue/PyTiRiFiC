"""
functions:
     ranslating object keywords to numerical model
     translate source model coordinate to WCS
"""
import numpy as np
import astropy.units as u
from ..arts.discretize import clouds_perchan
from astropy import constants as const
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from astropy.cosmology import Planck13 as cosmos

def fluxscale_from_contflux(contflux,w):
    """
    obatin the fluxscaling vector from the object keyword contflux:
        contflux is a tuple of one-element or three element
    """
    wspec=w.sub(['spectral'])
    sz=wspec.pixel_to_world(np.arange(w._naxis[2])).to(u.Hz,equivalencies=u.spectral())

    try:
        fluxscale=contflux[0]*((sz/contflux[1])**contflux[2]).decompose()
    except:
        fluxscale=contflux*sz/sz
    
    return fluxscale

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
    
    if  'lineflux' in obj:
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
    
    if  'contflux' in obj:
        if  'Hz' in w.wcs.cunit[2].name:
            wz=obj['contflux'][1].to(u.Hz)
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
    kps=cosmos.kpc_proper_per_arcmin(obj['z']).to(u.kpc/u.arcsec)
    dp=cell*kps
    
    pp=w._naxis
    if  px is None: px=np.arange(pp[0])
    if  py is None: py=np.arange(pp[1])
    if  pz is None: pz=np.arange(pp[2])

    sx=(px-fpx)*dp+mxo
    sy=(py-fpy)*dp+myo
    sz=(pz-fpz)*dz+mzo
    
    return sx,sy,sz

def clouds_split(obj,w):
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

    #   fluxscale   in Jy per cloud
    #   xrange      in kpc
    #   yrange      in kpc
    #   x           in kpc
    #   y           in kpc
    #   wt          arbitary
        
    # obtain the coordinate transform vector
    
    sx,sy,sz=pix2sky(obj,w)

    #   for line component, we group clouds by their channel locations
    
    if  'lineflux' in obj:
        
        # eqavelent flux density contribution per cloud within one channel
        
        dv=sz[1]-sz[0] 
        fluxscale=obj['lineflux']/obj['clouds_loc'].size/np.abs(dv)
        fluxscale=fluxscale.to_value('Jy')
        
        x,y,wt=\
            clouds_perchan(obj['clouds_loc'],obj['clouds_wt'],sz,return_v=False)        
        
    #   fpr continuum componnet, we derive the frequency-dependent-scaling and 
    #   attached the channel-indepdent clouds location. 
    
    if  'contflux' in obj:
        
        # flux density contribution per cloud within each channel
        
        fluxscale=fluxscale_from_contflux(obj['contflux'],w)
        fluxscale=fluxscale.to_value('Jy')/obj['clouds_loc'].size
        x=obj['clouds_loc'].x.value
        y=obj['clouds_loc'].y.value
        wt=obj['clouds_wt']
        

    dx=sx[1]-sx[0]
    xrange=[sx[0].value-dx.value/2,sx[-1].value+dx.value/2]
    dy=sy[1]-sy[0]
    yrange=[sy[0].value-dy.value/2,sy[-1].value+dy.value/2]

    return fluxscale,xrange,yrange,x,y,wt