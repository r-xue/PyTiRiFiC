# coding: utf-8
import numpy as np
from astropy.convolution import convolve_fft
from astropy.convolution import convolve
from astropy.io import fits


def makebeam(xpixels,ypixels,st_dev,rot=0,cent=0):
    """
    
    st_dev:    actually this is FWHM
    
    
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
            cent=np.round((ks-1.)/2.)
        
        note:
            
            be careful about rounding:
                NumPy rounds to the nearest even value. Thus 1.5 and 2.5 round to 2.0, -0.5 and 0.5 round to 0.0,
                https://docs.scipy.org/doc/numpy/reference/generated/numpy.around.html
                             
    """
    if not cent: cent=[round((xpixels-1.)/2.)*1.,round((ypixels-1.)/2.)*1.]
    st_dev=st_dev[::-1]
    st_dev=np.array(st_dev)/2.355
    if np.tan(np.radians(rot)) == 0:
        dirfac=1
    else:
        dirfac=np.sign(np.tan(np.radians(rot)))   
    x,y=np.indices((int(xpixels),int(ypixels)),dtype='float')
    x -=cent[0]
    y -=cent[1]
    a=(np.cos(np.radians(rot))**2)/(2.0*(st_dev[0]**2)) + (np.sin(np.radians(rot))**2)/(2.0*(st_dev[1]**2))
    b=((dirfac)*(np.sin(2.0*np.radians(rot))**2)/(4.0*(st_dev[0]**2))) + ((-1*dirfac)*(np.sin(2.0*np.radians(rot))**2)/(4.0*(st_dev[1]**2)))
    c=(np.sin(np.radians(rot))**2)/(2.0*(st_dev[0]**2)) + (np.cos(np.radians(rot))**2)/(2.0*(st_dev[1]**2))
    psf=np.exp(-1.*(a*(x**2) - 2.0*b*(x*y) + c*(y**2)))
    
    print(xpixels,ypixels,cent)
          
    return psf

if  __name__=="__main__":
    """
    examples
    """
    psf=makebeam(11,11,[4.0,3.0],rot=45,cent=0)
    fits.writeto('makebeam_psf.fits',psf,overwrite=True)
    psf1=makebeam(11,11,[3.0,3.0],rot=0,cent=0)
    fits.writeto('makebeam_psf1.fits',psf1,overwrite=True)
    psf2=makebeam(13,13,[3.0,3.0],rot=0,cent=0)
    fits.writeto('makebeam_psf2.fits',psf2,overwrite=True)
    cm=convolve(psf1,psf2)
    fits.writeto('makebeam_convol.fits',cm,overwrite=True)

        