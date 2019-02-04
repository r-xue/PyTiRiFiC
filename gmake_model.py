import numpy as np
from astropy.modeling.models import Sersic2D
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.io import fits
from makebeam import makebeam
from astropy.convolution import convolve_fft

def gmake_model_disk2d(header,ra,dec,beamsize,
                       r_eff=20.0,
                       n=1.0,
                       intflux=1.,
                       ellip=0.0,       # 1-b/a
                       cleanout=False,
                       posang=0.):
    
    
    cell=np.sqrt(np.abs(header['CDELT1']*header['CDELT2']))*3600.0    
    if  not isinstance(beamsize, (list, tuple, np.ndarray)):
        beamsize = np.array([beamsize,beamsize,0])    

    w=WCS(header).celestial
    pos=w.wcs_world2pix(np.array([[ra],[dec]]).T,0)
    px=pos[:,0]
    py=pos[:,1]
    
    # use meshgrid and don't worry about transposing
    x,y = np.meshgrid(np.arange(header['NAXIS1']), np.arange(header['NAXIS2']))

    mod = Sersic2D(amplitude=1.0,r_eff=r_eff,n=4.,x_0=px,y_0=py,
               ellip=ellip,theta=np.deg2rad(posang+90.0))
    model=mod(x,y)
    
    
    psf = makebeam(header['NAXIS1'],header['NAXIS2'],[beamsize[0]/cell,beamsize[1]/cell],rot=beamsize[2])
    if  not cleanout:
        model=convolve_fft(model,psf)
    if  not cleanout:
        model *= ( intflux*psf.sum()/model.sum() )
    else: 
        model *= ( intflux/model.sum() )

    return model

if  __name__=="__main__":
    
    #pass

    #"""
    
    data,hd=fits.getdata('examples/bx610/bx610_spw25.mfs.fits',header=True,memmap=False)
    
    model=gmake_model_disk2d(hd,356.539321,12.8220179445,[0.2,0.2,0.0],
                             cleanout=False)
    
    fits.writeto('test_model_disk2d.fits',model,hd,overwrite=True)
    
    log_model=np.log(model)
    plt.figure()
    plt.imshow(np.log(model), origin='lower', interpolation='nearest',
           vmin=np.min(log_model), vmax=np.max(log_model))
    plt.xlabel('x')
    plt.ylabel('y')
    cbar = plt.colorbar()
    cbar.set_label('Log Brightness', rotation=270, labelpad=25)
    cbar.set_ticks([np.min(log_model),np.max(log_model)], update_ticks=True)
    plt.savefig('test_model_disk2d.eps')
    
    #"""



