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
    cell=np.mean(proj_plane_pixel_scales(WCS(header).celestial))*3600.0
    
    cdelt3=header['CDELT3']     # hz or m/s
    crval3=header['CRVAL3']     # hz or m/s
    crpix3=header['CRPIX3']     # pix
    
    #   vector description of the z-axis: 
    #       vdelt3/vrval3/crpix3
    rfreq=obj['restfreq']/(1.0+obj['z'])                            #   GHz
    if  'Hz' in header['CUNIT3']:   # by freq
        vdelt3=-const.c*cdelt3/(1.0e9*rfreq)/1000.                  #   km/s
        vrval3=const.c*((1.0e9*rfreq)-crval3)/(1.0e9*rfreq)/1000.0  #   km/s
    else:                       # by velo
        vdelt3=cdelt3/1000.0
        vrval3=crval3/1000.0
    
    if  verbose==True:
        print(cell,vdelt3,vrval3,crpix3)
    
    xs=cell*header['NAXIS1']
    ys=cell*header['NAXIS2']
    vs=abs(vdelt3)*header['NAXIS3']
    cell=cell
    dv=abs(vdelt3)
    beamsize=1.0
    inc=obj['inc']
    gassigma=np.array(obj['vdis'])
    sbrad=np.array(obj['radi'])
    sbprof=1.*np.exp(-sbrad/obj['sbexp'])
    velrad=obj['radi']
    velprof=obj['vrot']
    posang=obj['pa']
    intflux=obj['intflux']
    xypos=obj['xypos']
    restfreq=obj['restfreq']
    vsys=obj['vsys']
    fsys=(1.0-vsys/(const.c/1000.0))*rfreq # line systematic frequency in the observer frame
    
    #   ra    ----      xi_data     ----    (xSize-1.)/2.+phasecen[0]/cell
    #   dec   ----      yi_data     ----    (ySize-1.)/2.+phasecen[1]/cell
    #   vsys  ----      vi_data     ----    (vSize-1.)/2.+voffset/dv
   
    #
    # collect the world coordinates of the disk center (ra,dec,freq/wave)
    # note: vsys is defined in the radio(freq)/optical(wave) convention, 
    #       within the rest frame set at obj['z']/
    #       the convention doesn't really matter, as long as vsys << c
    #
    wx=xypos[0]
    wy=xypos[1]
    ws=1    # stokes
    wo=0    # 0-based or 1-based index
    if  'Hz' in header['CUNIT3']:
        wz=obj['restfreq']*1e9/(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
        dv=-const.c*cdelt3/(1.0e9*obj['restfreq']/(1.0+obj['z']))/1000.
    if  'Angstrom' in header['CUNIT3']:
        wz=obj['restwave']*(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
        dv=const.c*cdelt3/(obj['restwave']*(1.0+obj['z']))/1000.
    if  'm/s' in header['CUNIT3']:
        wz=obj['vsys']/1000.
        dv=cdelt3/1000.        

    px,py,pz,ps=WCS(header).wcs_world2pix(wx,wy,wz,ws,wo)
    
    px_int=round(px)
    py_int=round(py)
    pz_int=round(pz)
    phasecen=np.array([px-px_int,py-py_int])*cell
    voffset=(pz-pz_int)*dv
    
    #print(phasecen,voffset)
    #print('<-->',tag,px_int,py_int,pz_int,ps)
    #print('hz:',int(xs/cell*0.5))
    phasecen=[0.,0.]
    xs=np.max(sbrad)*2.0*2.0
    ys=np.max(sbrad)*2.0*2.0
    vs=np.max(velprof)*1.5*2.0
    
    px_o=px_int-int(xs/cell*0.5)
    py_o=py_int-int(ys/cell*0.5)
    pz_o=pz_int-int(vs/abs(dv)*0.5)

    #tic=time.time()
    # cube needs to be transposed to match the fits.data dimension 
    # the WCS from kinms is buggy/offseted: don't use it
    cube=KinMS(xs,ys,vs,
               cellSize=cell,dv=abs(dv),
               beamSize=beamsize,cleanOut=False,
               inc=inc,gasSigma=gassigma,sbProf=sbprof,
               sbRad=sbrad,velRad=velrad,velProf=velprof,
               #nSamps=nsamps,
               ra=xypos[0],dec=xypos[1],
               restFreq=restfreq,vSys=vsys,phaseCen=phasecen,vOffset=voffset,
               #fileName=outname+'_'+tag,
               posAng=posang,
               intFlux=intflux)
    cube=cube.T
    if  dv<0:
        cube=np.flip(cube,axis=2)
    #print('Took {0} seconds to execute KinMSpy'.format(float(time.time()-tic)/float(1)))

    model=np.zeros((header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1']))
    model=gmake_insertmodel(model,cube,offset=[px_o,py_o,pz_o])
    #print('shape:',model.shape)
    #print('shape:',cube.shape)
    #print('-->',px_int,py_int,pz_int)
    #print('-->',[px_o,py_o,pz_o])
    
    return model


def gmake_model_simobs(data,header,beam=None,psf=None,returnkernel=False):
    """
        simulate the observation in the image-domain
        input is expected in units of Jy/pix
        output will in the Jy/cbeam or Jy/dbeam if kernel is peaked at unity.
        
        the adopted kernel can be returned
    """
    
    cell=np.mean(proj_plane_pixel_scales(WCS(header).celestial))*3600.0
    
    #   get the convolution Kernel normalized to 1 at PEAK
    #   priority: psf>beam>header(2D or 3D KERNEL) 
    
    if  psf is not None:
        kernel=psf.copy()
    elif beam is not None:
        if  not isinstance(beam, (list, tuple, np.ndarray)):
            gbeam = [beam,beam,0]
        else:
            gbeam = beam
        kernel=makekernel(header['NAXIS1'],header['NAXIS2'],
                        [gbeam[0]/cell,gbeam[1]/cell],pa=gbeam[2])
    else:
        kernel=makekernel(header['NAXIS1'],header['NAXIS2'],
                        [header['BMAJ']*3600./cell,header['BMIN']*3600./cell],pa=header['BPA'])

    model=data.copy()
    for i in range(header['NAXIS3']):
        if  kernel.ndim==2:
            model[0,i,:,:]=convolve_fft(data[0,i,:,:],kernel)
        else:
            model[0,i,:,:]=convolve_fft(data[0,i,:,:],psf[0,i,:,:])

    if  returnkernel==True:
        return model,kernel
    else:
        return model
    
def makekernel(xpixels,ypixels,beam,pa=0.,cent=0):
    """

    beam=[bmaj,bmin] FWHM
    pa=east from north (ccw)
    
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