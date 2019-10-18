import gmake
from gmake.model_func import *
# from gmake import *      : import * doesn't import variables starting with "_"

def test_gmake_model_disk2d_old():
    
    data,hd=fits.getdata('examples/bx610/bx610.bb1.mfs.iter0.image.fits',header=True,memmap=False)
    data,hd=fits.getdata('examples/bx610/bx610.bb4.cube.iter0.image.fits',header=True,memmap=False)
    psf,phd=fits.getdata('examples/bx610/bx610.bb4.cube.iter0.psf.fits',header=True,memmap=False)
    #psf=psf[0,100,:,:]
    
    start_time = time.time()
    model=gmake_model_disk2d(hd,356.539321,12.8220179445,
                             r_eff=0.2,n=1.0,posang=20,ellip=0.5)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    start_time = time.time()
    cmodel=gmake_model_simobs(model,hd)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    start_time = time.time()
    cmodel_psf=gmake_model_simobs(model,hd,psf=psf)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    start_time = time.time()
    cmodel_beam=gmake_model_simobs(model,hd,beam=[1.0,0.2,-30.])
    print("--- %s seconds ---" % (time.time() - start_time))    
    
    fits.writeto('test/test_model_disk2d_model.fits',model,hd,overwrite=True)
    fits.writeto('test/test_model_disk2d_cmodel.fits',cmodel,hd,overwrite=True)
    fits.writeto('test/test_model_disk2d_cmodel_psf.fits',cmodel_psf,hd,overwrite=True)
    fits.writeto('test/test_model_disk2d_cmodel_beam.fits',cmodel_beam,hd,overwrite=True)
    
def test_gmake_model_disk2d():
    

    demo_dir=gmake.__demo__+'/../examples/'

    #data,hd=fits.getdata('examples/bx610/bx610_spw25.mfs.fits',header=True,memmap=False)
    data,hd=fits.getdata(demo_dir+'data/bx610/alma/band6/bx610.bb4.cube.iter0.image.fits',
                         header=True,memmap=False)
    psf,phd=fits.getdata(demo_dir+'data/bx610/alma/band6/bx610.bb4.cube.iter0.psf.fits',
                         header=True,memmap=False)
    #psf=psf[0,100,:,:]
    
    start_time = time.time()
    model=model_disk2d(hd,356.539321,12.8220179445,
                             r_eff=0.2,n=1.0,posang=20,ellip=0.5)
    print("--- %s seconds ---" % (time.time() - start_time))

    
    #fits.writeto('test/test_model_disk2d.fits',model,hd,overwrite=True)
    """
    log_model=np.log(model)
    plt.figure()
    plt.imshow(np.log(model), origin='lower', interpolation='nearest',
           vmin=np.min(log_model), vmax=np.max(log_model))
    plt.xlabel('x')
    plt.ylabel('y')
    cbar = plt.colorbar()
    cbar.set_label('Log Brightness', rotation=270, labelpad=25)
    cbar.set_ticks([np.min(log_model),np.max(log_model)], update_ticks=True)
    plt.savefig('test/test_model_disk2d.eps')
    """
