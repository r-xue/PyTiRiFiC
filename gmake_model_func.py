from __future__ import print_function
from KinMS import KinMS
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from astropy.wcs.utils import skycoord_to_pixel
import scipy.constants as const
import time
from astropy.modeling.models import Sersic2D
from astropy.modeling.models import Sersic1D
from astropy.modeling.models import Gaussian2D
from astropy.coordinates import SkyCoord
from spectral_cube import SpectralCube


def gmake_model_disk2d(header,ra,dec,
                       r_eff=1.0,n=1.0,posang=0.,ellip=0.0,
                       intflux=1.,restfreq=235.0,alpha=3.0):
    """
    
        insert a continuum model into a 2D image or 3D cube
        
        header:    data header including WCS
        
        ra,dec:    object center ra/dec
        ellip:     1-b/a
        posang:    in the astronomical convention
        r_eff:     in arcsec
        n:         sersic index
        
        intflux:   Jy
        restfreq:  GHz
        alpha:     
        
        the header is assumed to be ra-dec-freq-stokes
    
        note:
            since the convolution is the bottom-neck, a plane-by-plane processing should
            be avoided.
    """

    #   build objects
    #   use np.meshgrid and don't worry about transposing
    
    cell=np.mean(proj_plane_pixel_scales(WCS(header).celestial))*3600.0
    px,py=skycoord_to_pixel(SkyCoord(ra,dec,unit="deg"),WCS(header),origin=0)
    vz=np.arange(header['NAXIS3'])
    wz=(WCS(header).wcs_pix2world(0,0,vz,0,0))[2]
    
    #   get 2D disk model
    
    x,y = np.meshgrid(np.arange(header['NAXIS1']), np.arange(header['NAXIS2']))
    mod = Sersic2D(amplitude=1.0,r_eff=r_eff/cell,n=n,x_0=px,y_0=py,
               ellip=ellip,theta=np.deg2rad(posang+90.0))
    model2d=mod(x,y)
    
    #   intflux at different planes / broadcasting to the data dimension
    #   return model in units of Jy/pix
    
    intflux_z=(wz/1e9/restfreq)**alpha*intflux
    model=np.broadcast_to(model2d,(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])).copy()
    for i in range(header['NAXIS3']):
        model[0,i,:,:]*=intflux_z[i]/model2d.sum()

    return model

def gmake_model_kinmspy(header,obj,
                        decomp=False,
                        verbose=False):
    """
    handle modeling parameters to kinmspy and generate the model cubes embeded into 
    a dictionary nest
    
    note:
        kinmspy can only construct a spectral cube in the ra-dec-vel space. We use kinmspy
        to construct a xyv cube with the size sufficient to cover the model object. Then 
        we insert it into the data using the WCS/dimension info. 
    """    

    #######################################################################
    #   WORLD ----      DATA        ----    MODEL
    #######################################################################
    #   ra    ----      xi_data     ----    xSize/2.+phasecen[0]/cell
    #   dec   ----      yi_data     ----    ySize/2.+phasecen[1]/cell
    #   vsys  ----      vi_data     ----    vSize/2.+voffset/dv
    #
    # collect the world coordinates of the disk center (ra,dec,freq/wave)
    # note: vsys is defined in the radio(freq)/optical(wave) convention, 
    #       within the rest frame set at obj['z']/
    #       the convention doesn't really matter, as long as vsys << c
    #######################################################################
    #   vector description of the z-axis (data in Hz or m/s; model in km/s)
    #   rfreq=obj['restfreq']/(1.0+obj['z'])            # GHz (obs-frame)
    #   fsys=(1.0-obj['vsys']/(const.c/1000.0))*rfreq   # line systematic frequency (obs-frame)
        
    if  'Hz' in header['CUNIT3']:
        wz=obj['restfreq']*1e9/(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
        dv=-const.c*header['CDELT3']/(1.0e9*obj['restfreq']/(1.0+obj['z']))/1000.
    if  'Angstrom' in header['CUNIT3']:
        wz=obj['restwave']*(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
        dv=const.c*header['CDELT3']/(obj['restwave']*(1.0+obj['z']))/1000.
    if  'm/s' in header['CUNIT3']:
        wz=obj['vsys']/1000.
        dv=header['CDELT3']/1000.        

    #   get 0-based pix-index
    
    px,py,pz,ps=WCS(header).wcs_world2pix(obj['xypos'][0],obj['xypos'][1],wz,1,0)

    xs=np.max(np.array(obj['radi']))*2.0*2.0
    ys=np.max(np.array(obj['radi']))*2.0*2.0
    vs=np.max(obj['vrot'])*1.5*2.0
    
    cell=np.mean(proj_plane_pixel_scales(WCS(header).celestial))*3600.0
    
    px_o=px-float(round(xs/cell))/2.0
    py_o=px-float(round(ys/cell))/2.0
    pz_o=pz-float(round(ys/abs(dv)))/2.0
    #   when the z-axis is decreasing in velocity, we count offset backwards
    if  dv<0: pz_o=pz_o+1.0
    
    px_o_int=round(px_o) ; px_o_frac=px_o-px_o_int
    py_o_int=round(py_o) ; py_o_frac=py_o-py_o_int
    pz_o_int=round(pz_o) ; pz_o_frac=pz_o-pz_o_int
    
    phasecen=np.array([px_o_frac,py_o_frac])*cell
    voffset=(pz_o_frac)*dv

    #   About KinMS:
    #       + cube needs to be transposed to match the fits.data dimension 
    #       + the WCS/FITSIO in KINMSPY is buggy/offseted: don't use it
    #       + turn off convolution at this point
    #       + KinMS only works in the RA/DEC/VELO domain.
    
    mod = Sersic1D(amplitude=1.0,r_eff=obj['sbser'][0],n=obj['sbser'][1])
    sbprof=mod(np.array(obj['radi']))
    #sbprof=1.*np.exp(-np.array(obj['radi'])/(obj['sbser'][0]/1.68))
    cube=KinMS(xs,ys,vs,
               cellSize=cell,dv=abs(dv),
               beamSize=1.0,cleanOut=True,
               inc=obj['inc'],gasSigma=np.array(obj['vdis']),sbProf=sbprof,
               sbRad=np.array(obj['radi']),velRad=obj['radi'],velProf=obj['vrot'],
               ra=obj['xypos'][0],dec=obj['xypos'][1],
               restFreq=obj['restfreq'],vSys=obj['vsys'],phaseCen=phasecen,vOffset=voffset,
               fixSeed=False,
               #nSamps=nsamps,fileName=outname+'_'+tag,
               posAng=obj['pa'],
               intFlux=obj['intflux'])
    
    #   KinMS provide the cube in (x,y,v) shape, but not in the Numpy fasion. transpose required
    #   flip z-axis if dv<0
    cube=cube.T
    if  dv<0: cube=np.flip(cube,axis=0)
    
    model=np.zeros((header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1']))
    model=paste_array(model,cube[np.newaxis,:,:,:],(0,int(pz_o_int),int(py_o_int),int(px_o_int)))
    
    return model


def gmake_model_simobs(data,header,beam=None,psf=None,returnkernel=False,verbose=True):
    """
        simulate the observation in the image-domain
        input is expected in units of Jy/pix
        output will in the Jy/cbeam or Jy/dbeam if kernel is peaked at unity.
        
        the adopted kernel can be returned
        
        note: we only use cellsize/bmaj/bmin/bpa info from the header.
              the header doesn't need to match the data "dimension"
    """

    
    cell=np.mean(proj_plane_pixel_scales(WCS(header).celestial))*3600.0
    
    #   get the convolution Kernel normalized to 1 at PEAK
    #   turn on normalization in convolve() will force the Jy/Pix->Jy/beam conversion
    #   priority: psf>beam>header(2D or 3D KERNEL) 
    
    dshape=data.shape
    
    if  psf is not None:
        kernel=psf.copy()
    elif beam is not None:
        if  not isinstance(beam, (list, tuple, np.ndarray)):
            gbeam = [beam,beam,0]
        else:
            gbeam = beam
        kernel=makekernel(dshape[-1],dshape[-2],
                        [gbeam[0]/cell,gbeam[1]/cell],pa=gbeam[2])
    else:
        kernel=makekernel(dshape[-1],dshape[-2],
                        [header['BMAJ']*3600./cell,header['BMIN']*3600./cell],pa=header['BPA'])

    if  verbose==True:
        print('data   dim:',data.shape)
        print('kernel dim:',kernel.shape)
        start_time = time.time()

    model=np.zeros_like(data)
    cc=0
    for i in range(dshape[-3]):
        if  np.sum(data[0,i,:,:])==0.0:
            continue
        cc=cc+1
        if  kernel.ndim==2:
            model[0,i,:,:]=convolve_fft(data[0,i,:,:],kernel,normalize_kernel=False)
        else:
            model[0,i,:,:]=convolve_fft(data[0,i,:,:],kernel[0,i,:,:],normalize_kernel=False)

    if  verbose==True:
        print("---{0:^10} : {1:<8.5f} seconds ---".format('simobs',time.time()-start_time))
        print("convolved plane counts: ",cc)
        start_time = time.time()
        test1=(data[0,:,:,:])
        test2=(kernel[np.newaxis,0,100,(52-10):(52+10),(52-10):(52+10)])
        print(test1.shape,test2.shape)
        test=convolve_fft(test1,test2)
        print("---{0:^10} : {1:<8.5f} seconds ---".format('simobs-beta',time.time()-start_time))
        

    if  returnkernel==True:
        return model,kernel
    else:
        return model
    
def makekernel(xpixels,ypixels,beam,pa=0.,cent=0):
    """

    beam=[bmaj,bmin] FWHM
    pa=east from north (ccw)deli
    
    make a "centered" Gaussian PSF kernel:
        e.g. npixel=7, centered at px=3
             npixel=8, centered at px=4
             so the single peak is always at a pixel center (not physical center)
             and the function is symmetric around that pixel
             the purpose of doing this is to avoid offset when the specified kernel size is
             even number and you build a function peaked at a pixel edge. 
             
        is x ks (peak pixel index)
        10 x 7(3) okay
        10 x 8(4) okay
        10 x 8(3.5) offset
        for convolve (non-fft), odd ks is required (the center pixel is undoubtely index=3)
                                even ks is not allowed
        for convolve_fft, you need to use cent=ks/2:
                                technically it's not the pixel index of image center
                                but the center pixel is "considers"as index=4
        the rule of thumb-up:
            cent=round((ks-1.)/2.)
        
        note:
            
            be careful about rounding:
                NumPy rounds to the nearest even value. Thus 1.5 and 2.5 round to 2.0, -0.5 and 0.5 round to 0.0,
                https://docs.scipy.org/doc/numpy/reference/generated/numpy.around.html
            
            "forget about how the np.array is stored, just use the array as it is IDL;
             when it comes down to shape/index, reverse the sequence"
            
    """
    
    if not cent: cent=[round((xpixels-1.)/2.)*1.,round((ypixels-1.)/2.)*1.]
    sigma2fwhm=np.sqrt(2.*np.log(2.))*2.
    mod=Gaussian2D(amplitude=1.,x_mean=cent[0],y_mean=cent[1],
               x_stddev=beam[1]/sigma2fwhm,y_stddev=beam[0]/sigma2fwhm,
               theta=np.deg2rad(pa))
    x,y=np.meshgrid(np.arange(xpixels),np.arange(ypixels))
    psf=mod(x,y)
    #print(psf.shape)
    #print(cent)
    return psf
    

    
if  __name__=="__main__":

    """
    examples
    """
    pass


         #   for the 2D "common-beam" case
        #   broadcasting to 4D (broadcast_to just create a "view"; .copy needed)
        
#         model2d=convolve_fft(model2d,kernel)
#         model=np.broadcast_to(model2d,(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])).copy()
#     else:
#         #   for the varying-PSF case
#         model=np.broadcast_to(model2d,(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])).copy()
     
#     model=np.zeros('')
#     if  not cleanout:
#         # end up with Jy/beam
#         #print(model.shape,psf_beam.shape)
#         model=convolve_fft(model,kernel)
#         model *= ( intflux_model*kernel.sum()/model.sum() )
#     else: 
#         # end up with Jy/pix
#         model *= ( intflux_model/model.sum() )
    #im=makekernel(29,21,[6.0,6.0],pa=0)
    #fits.writeto('makekernel_im.fits',im,overwrite=True)
    
    #psf=makekernel(15,15,[6.0,3.0],pa=20)
    #fits.writeto('makekernel_psf.fits',psf,overwrite=True)
#     psf1=makekernel(11,11,[3.0,3.0],pa=0,cent=0)
#     fits.writeto('makekernel_psf1.fits',psf1,overwrite=True)
#     psf2=makekernel(13,13,[3.0,3.0],pa=0,cent=0)
#     fits.writeto('makekernel_psf2.fits',psf2,overwrite=True)
    #cm=convolve_fft(im,psf)
    #fits.writeto('makekernel_convol.fits',cm,overwrite=True)