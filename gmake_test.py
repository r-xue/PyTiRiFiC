"""
    used to test various functions
"""

execfile('gmake_model_func.py')
execfile('gmake_model.py')
execfile('gmake_utils.py')
execfile('gmake_emcee.py')

def test_gmake_model_disk2d():
    
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
    
def test_gmnake_model_api():
    
    inp_dct=gmake_readinp('examples/bx610/bx610xy_test.inp',verbose=False)
    dat_dct=gmake_read_data(inp_dct,verbose=False,fill_mask=True,fill_error=True)

    mod_dct=gmake_inp2mod(inp_dct)
    
    start_time = time.time()
    models=gmake_model_api(mod_dct,dat_dct)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    pprint.pprint(models.keys())
    fits.writeto('test/test_gmake_model_api_imodel.fits',
                 models['imodel@examples/bx610/bx610.bb3.cube.iter0.image.fits'],
                 models['header@examples/bx610/bx610.bb3.cube.iter0.image.fits'],
                 overwrite=True)
    fits.writeto('test/test_gmake_model_api_cmodel.fits',
                 models['cmodel@examples/bx610/bx610.bb3.cube.iter0.image.fits'],
                 models['header@examples/bx610/bx610.bb3.cube.iter0.image.fits'],
                 overwrite=True)    
    
    #lnl,blobs=gmake_model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
    #                             savemodel='test/test_gmake_model_api')

    return models

if  __name__=="__main__":
    
    
    
    #test_gmake_model_disk2d()
    models=test_gmnake_model_api()

    
