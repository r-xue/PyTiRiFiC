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

def uv_sample_nufft(plane,cell,uu,vv,vis,dRA=0.,dDec=0.,PA=0):
    """
    factor:    oversampling factor
    runtime scaled with oversampled plane size
    https://cims.nyu.edu/cmcl/nufft/nufft.html
    """
    
    #dRA  *= 2.*np.pi
    #dDec *= 2.*np.pi
    #cos_PA = np.cos(PA)
    #sin_PA = np.sin(PA)
    #urot = uu * cos_PA - vv * sin_PA
    #vrot = uu * sin_PA + vv * cos_PA
    
    urot=uu
    vrot=vv    

    # Fast Non-uniform FFT
    nufft.nufft2d2(vrot*(cell*2*np.pi),
                   -urot*(cell*2*np.pi),
                   vis,1,1e-3,plane,\
                   debug=0,spread_debug=0,spread_sort=0,fftw=1,modeord=0,\
                   chkbnds=0,upsampfac=1.25)
    return  
     
def uv_sample_direct(plane,cell,uu,vv,dRA=0.,dDec=0.,PA=0,dimsum='uv',drange=10):
    """
    runtime scaled with "active" pixel n (loop over active pixel)
    runtime scaled with nrecord (loop over active visibility)
    a run time is only acceptable for limited amount of point source
    
    so it's not using direct sm.predict only give 70% flux and high spatial freuqnecy info is loosing
    
    sm.predict behavior:
        If the input image very small 6x6, loosing flux in sm.predict:
        It seems its using weighted average over a couple of cells arounds and run into issue for large uv cell (small image cell) case
    
    casa is likley using oversampling method:
    
    https://open-bitbucket.nrao.edu/projects/CASA/repos/casa6/browse/casa5/code/synthesis/TransformMachines/WTerm.h#114
    
    oversampling=20 or 20xPB size
    will make sure any the most rapid perips case (~pb) will be sapled by 20points.
    such the phase (from joint source of the entire image) can't change even faster than that.
    even the nearest neajobour sampling will be good enough and not introduce too much error. 
    
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
    """
    ik=1->5; high-order is more accurate
    """
    
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
                method='nufft',ik=5,saveuvgrid=False):
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
            
        vis=np.zeros((len(uu)),dtype=np.complex128)
        uv_sample_nufft(plane,cell,uu,vv,vis,dRA=dRA,dDec=dDec,PA=PA)
        return vis        
    
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


################################################################################
