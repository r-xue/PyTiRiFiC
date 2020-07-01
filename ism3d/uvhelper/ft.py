
import finufftpy  as nufft
import astropy.units as u
import numpy as np
from .. import fft_use, fft_fastlen
from ..utils.meta import create_header

import logging
logger = logging.getLogger(__name__)

def invert_ft(uu,vv,wv,vis,cell,imsize,wt=None,bychannel=True):
    """
    use nufft to create dirty cube from visibility
    uu: in meter (vector, nrecord
    vv: in meter (vector, nrecord)
    wv: in meter (vector, nchannel)
    psize: Quality
    wt:         apply wt when doing invert (essentialy nature weighting)
                only works when bychannle=true
    bychannel:  False ignore the wavelength changing effect on uvw
                True: uu/vv will be calculated channel by channel
                
    output (nx,ny,nz)
    """
    
    if  bychannel==False:
        uuu=-uu/np.mean(wv)*2*np.pi*(cell.to(u.rad).value)
        vvv=vv/np.mean(wv)*2*np.pi*(cell.to(u.rad).value)
        cube=np.zeros((imsize,imsize,len(wv)),dtype=np.complex128,order='F')
        nufft.nufft2d1many(uuu,vvv,vis,
                           -1,1e-15,imsize,imsize,cube,debug=1)
        cube/=uu.shape[0]         
    else:
        cube=np.zeros((imsize,imsize,len(wv)),dtype=np.complex128,order='F')
        
        #im0=np.zeros((imsize,imsize),dtype=np.complex128,order='F')
        for i in range(len(wv)):
            uuu=-uu/wv[i]*2*np.pi*(cell.to(u.rad).value)
            vvv=vv/wv[i]*2*np.pi*(cell.to(u.rad).value)
            if  wt is None:
                nufft.nufft2d1(uuu,vvv,vis[:,i],
                            -1,1e-15,imsize,imsize,cube[:,:,i],debug=0)
            else:
                nufft.nufft2d1(uuu,vvv,vis[:,i]*wt,
                            -1,1e-15,imsize,imsize,cube[:,:,i],debug=0)                
        #cube[:,:,i]=im0
        if  wt is None:
            cube/=uu.shape[0]
        else:
            cube/=np.sum(wt)
    
    return cube.real

def make_psf(uu,vv,wv,cell,imsize,wt=None,bychannel=True):
    
    vis=np.ones((uu.shape[0],len(wv)),dtype=np.complex128,order='F')
    cube=invert_ft(uu,vv,wv,vis,cell,imsize,wt=wt,bychannel=bychannel)

    return cube

def uv_to_header(uv,center,chanfreq,chanwidth,antsize=None):
    """
    create a header template for discreating cloudlet model before uv sampling
        using accroding to UV sampling and primary beam FOV
        uv.shape (nrecord,2) in units of meter
        chanfreq quantity frequency array
        center this could be phasecenter or somewhere near your target
        antsize=12*u.m
        
    f_max: determines the UV grid size, or set a image cell-size upper limit
           a valeu of >=2 would be a safe choice
           (set a upper limit of cellsize)
    f_min: set the UV cell-size upper limit, or a lower limit of image FOV.                            
           a value of >=3 would be translated into a FOV lager than >=3 of interfeormetry sensitive scale
           ***set a lower limit of imsize
    PB:    primary beam size, help set a lower limit of FOV
           however, in terms of imaging quality metric, this is not crucial
           ***set a lower limit of imsize
    The rule of thumbs are:
        * make sure f_max and f_min are good enought that all spatial frequency information is presented in
        the reference models
        * the FOV is large enough to covert the object.
        * keep the cube size within the memory limit    
    # note: if dxy is too large, uvsampling will involve extrapolation which is not stable.
    #       if nxy is too small, uvsampling should be okay as long as you believe no stucture-amp is above that scale.
    #          interplate is more or less stable.             
    """

    f_max=2.0
    f_min=2.0
    wv=np.mean(chanfreq).to(u.m,equivalencies=u.spectral())
    if  antsize is None:
        pb=0    # no restrictin from PB
    else:
        pb=(1.22*wv/antsize).value
    
    nxy, dxy = get_image_size(uv[:,0]/wv.value, uv[:,1]/wv.value,
                              pb=pb,f_max=f_max,f_min=f_min)
    
    logger.debug('nxyz:'+str(nxy)+','+str(np.size(chanfreq)))
    logger.debug('dxyz:'+(dxy<<u.rad).to(u.arcsec).to_string()+','+(np.mean(chanwidth.to(u.MHz))).to_string())
    
    header=create_header()
    header['NAXIS1']=nxy
    header['NAXIS2']=nxy
    header['NAXIS3']=np.size(chanfreq)
    
    header['CRVAL1']=center.ra.to_value(u.deg)
    header['CRVAL2']=center.dec.to_value(u.deg)
                   
    crval3=chanfreq.to_value(u.Hz)
    if  not np.isscalar(crval3):
        crval3=crval3[0]
    header['CRVAL3']=crval3
    header['CDELT1']=-np.rad2deg(dxy)
    header['CDELT2']=np.rad2deg(dxy)
    header['CDELT3']=np.mean(chanwidth.to_value(u.Hz))   
    header['CRPIX1']=np.floor(nxy/2)+1
    header['CRPIX2']=np.floor(nxy/2)+1
    
    return header

def get_image_size(u, v, pb=0, f_min=5., f_max=2.0,even=True):
    """
    Compute the recommended image size given the (u, v) locations.
    Typical call signature::
        nxy, dxy = get_image_size(u, v, PB=0, f_min=5., f_max=2.5, verbose=False)
    Parameters
    ----------
    u : array_like, float
        u coordinate of the visibility points where the FT has to be sampled.
        **units**: wavelength
    v : array_like, float
        v coordinate of the visibility points where the FT has to be sampled.
        The length of v must be equal to the length of u.
        **units**: wavelength
    PB : float, optional
        Primary beam of the antenna, e.g. 1.22*wavelength/Diameter for an idealized
        antenna with uniform illumination.
        **units**: rad
    f_min : float
        Size of the field of view covered by the (u, v) plane grid w.r.t. the field
        of view covered by the image. Recommended to be larger than 3 for better results.
        **units**: pure number
    f_max : float
        Nyquist rate: numerical factor that ensures the Nyquist criterion is satisfied when sampling
        the synthetic visibilities at the specified (u, v) locations. Must be larger than 2.
        The maximum (u, v)-distance covered is `f_max` times the maximum (u, v)-distance
        of the observed visibilities.
        **units**: pure number
    verbose : bool, optional
        If True, prints information on the criteria to be fulfilled by `nxy` and `dxy`.
    Returns
    -------
    nxy : int
        Size of the image along x and y direction.
        **units**: pixel
    dxy : float
        Returned only if not provided in input.
        Size of the image cell, assumed equal and uniform in both x and y direction.
        **units**: cm
    """
    uvdist = np.hypot(u, v) #in units of wavelength


    # X2 due to the effective sampling spatial frequency (negative->positive) from FFT is just half of uvplane size 
    
    mrs=0.6/np.min(uvdist) # maxmini sensitive scale in radian
    duv=np.min(uvdist)/0.6/f_min    # required uv cell size (smaller is better)  ;  1/duv is the xy plane size 
    maxuv = np.max(uvdist)*f_max*2  # required uv plane size (larger is better)  ;  1/maxuv is the xy cell size
    
    # if duv is not sufficient to cover PB (off-center source with fast phase changes), make it smaller
     
    if  pb>1/duv: duv=1/pb
    
    nxy=fft_fastlen(int(maxuv/duv))
    if  even==True:
        while (nxy %2 )!=0:
            nxy=fft_fastlen(nxy+1)
            
    dxy=1/duv/nxy

    return nxy, dxy