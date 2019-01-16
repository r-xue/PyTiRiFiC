from scipy.interpolate import Rbf
from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans, convolve
from astropy import units as u
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.io import fits
import numpy as np
#pyfile='/Users/Rui/Dropbox/Worklib/projects/highz/hxmm01/hxmm01_run.py'
#exec(open(pyfile).read())

#
# need ipython 3 and astropy 3
#
# exec(open('/Users/Rui/Dropbox/Worklib/projects/highz/hxmm01/py_tirific_makepsf.py').read())

def tirific_convol(datafile,psfile):
    
    mo=fitsio.read('CICO76_ppv.fits')
    sp=fitsio.read('CICO76_sp.fits')
    
    print(np.shape(sp))
    sp0=sp[0,0,:,:]
    print(np.shape(sp0))
    ind=np.where(sp0==1)
    print(ind[1])
    print(ind[0])
    py=ind[0]
    px=ind[1]
    pz=px*0.0+1.0
    
    ix=np.linspace(0,24.,25)
    iy=np.linspace(0,35.,36)
    xi,yi=np.meshgrid(ix,iy)

    rbf=Rbf(px,py,pz,function='linear')
    zi=rbf(xi,yi)
    pz[28]=3.0
    pz[36]=2.0
    rbf=Rbf(px,py,pz,function='linear')
    zi2=rbf(xi,yi)
    kernel = Gaussian2DKernel(stddev=2)
    kernel=np.expand_dims(kernel, axis=0)
    result = convolve(mo, kernel)
    
    fits.writeto('test_sp.fits',sp,overwrite=True)
    fits.writeto('test_it1.fits',zi,overwrite=True)
    fits.writeto('test_it2.fits',kernel,overwrite=True)
    fits.writeto('test_it3.fits',result,overwrite=True)
    
    print(np.shape(mo))

def tirific_makepsf(fitsfile):
    
    im,hd= fits.getdata(fitsfile,header=True)
    bmaj=hd['BMAJ']*3600.0
    bmin=hd['BMIN']*3600.0 
    bpa=hd['BPA']
    cdelt1=abs(hd['CDELT1']*3600)
    cdelt2=abs(hd['CDELT2']*3600)
    psize=cdelt1
    #print(bpa,psize,bmaj,bmin)
    kernel = Gaussian2DKernel(x_stddev=bmin/psize*gaussian_fwhm_to_sigma,
                              y_stddev=bmaj/psize*gaussian_fwhm_to_sigma,
                              theta=np.radians(bpa))
    kernel = np.expand_dims(kernel, axis=0)
    psffile=fitsfile.replace('.cm.fits','.psf.fits')
    fits.writeto(psffile,kernel,overwrite=True)


if  __name__=="__main__":
    #tirific_convol()
    tirific_makepsf('HXMM01.CI.cm.fits')
    tirific_makepsf('HXMM01.CO76.cm.fits')
    tirific_makepsf('HXMM01.water.cm.fits')
    