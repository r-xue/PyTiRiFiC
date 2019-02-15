"""
    used to test various functions
"""

from past.builtins import execfile

execfile('gmake_model_func.py')
execfile('gmake_model.py')
execfile('gmake_utils.py')
execfile('gmake_emcee.py')

def test_makekernel():

    #   this is exactly same as the 'center' method
    
    start_time = time.time()
    im=makekernel(29,21,[6.0,3.0],pa=10,mode=None)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('default',time.time()-start_time))    
    fits.writeto('test/test_makekernel_meshgrid.fits',im,overwrite=True)
    
    #   maybe a good option for some cases
    
    start_time = time.time()
    im=makekernel(29,21,[6.0,3.0],pa=10,mode='oversample')
    print("---{0:^10} : {1:<8.5f} seconds ---".format('oversample',time.time()-start_time))
    fits.writeto('test/test_makekernel_oversample.fits',im,overwrite=True)
    
    #   not preferred if you know peak is at the center of a pixel
    
    start_time = time.time()
    im=makekernel(29,21,[6.0,3.0],pa=10,mode='linear_interp')
    print("---{0:^10} : {1:<8.5f} seconds ---".format('linearinterp',time.time()-start_time))
    fits.writeto('test/test_makekernel_linearinterp.fits',im,overwrite=True)    
    
    #   this is exactly same as the meshgrid method
    
    start_time = time.time()
    im=makekernel(29,21,[6.0,3.0],pa=10,mode='center')
    print("---{0:^10} : {1:<8.5f} seconds ---".format('center',time.time()-start_time))
    fits.writeto('test/test_makekernel_center.fits',im,overwrite=True)    
    
    #   slow..slow...
    
    start_time = time.time()
    im=makekernel(29,21,[6.0,3.0],pa=10,mode='integrate')
    print("---{0:^10} : {1:<8.5f} seconds ---".format('integrate',time.time()-start_time))
    fits.writeto('test/test_makekernel_integrate.fits',im,overwrite=True)                    
    

def test_convolve_edge():
    """
    test different options to improve convol effciency) 
    
        https://github.com/mperrin/webbpsf/issues/10
        
    """
    
    im=makekernel(135,135,[6.0,6.0],pa=0)
    #im=im*0.0+1.0
    kn=makekernel(105,105,[15.0,5.0],pa=10)
    
    start_time = time.time()
    for i in range(100):
        #sm=convolve_fft(im,kn)
        # explicit default: (use fftn/ifftn rather than fft/ifft for image)
        sm=convolve_fft(im,kn,
                        fftn=np.fft.fftn, ifftn=np.fft.ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad=True/numpy',time.time()-start_time))
    fits.writeto('test/test_convolve_fft_default.fits',sm,overwrite=True)
    
    start_time = time.time()
    for i in range(100):
        #sm=convolve_fft(im,kn)
        # explicit default: (use fftn/ifftn rather than fft/ifft for image)
        sm=convolve_fft(im,kn,fft_pad=False,
                        fftn=np.fft.fftn, ifftn=np.fft.ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad=False/numpy',time.time()-start_time))
    fits.writeto('test/test_convolve_fft_default.fits',sm,overwrite=True)    
    
    start_time = time.time()
    for i in range(100):
        sm=convolve_fft(im,kn,fft_pad=False,
                        fftn=scipy.fftpack.fftn, ifftn=scipy.fftpack.ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad=False/scipy',time.time()-start_time))
    fits.writeto('test/test_convolve_fft_scipy.fits',sm,overwrite=True)    

    
    start_time = time.time()
    for i in range(100):
        sm=convolve_fft(im,kn,fft_pad=False,
                        fftn=pyfftw.interfaces.numpy_fft.fftn, ifftn=pyfftw.interfaces.numpy_fft.ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad=False/fftw_numpy',time.time()-start_time))
    fits.writeto('test/test_convolve_fft_fftw_numpy.fits',sm,overwrite=True) 
    
    start_time = time.time()
    for i in range(100):
        sm=convolve_fft(im,kn,fft_pad=False,
                        fftn=pyfftw.interfaces.scipy_fftpack.fftn, ifftn=pyfftw.interfaces.scipy_fftpack.ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad=False/fftw_scipy',time.time()-start_time))
    fits.writeto('test/test_convolve_fft_fftw_scipy.fits',sm,overwrite=True)          
      

def test_convolve_eff():
    
    """
    convolve_fft cost: fft(im)+fft(kernel)+ifft(mutiple)
    """
    im=np.ones((100,105,105))
    kernel=np.ones((100,105,105))
    kernel_large=np.ones((100,201,201))
    kernel_small=np.ones((100,21,21))
    
    
    start_time = time.time()
    for i in range(100):
        test=convolve_fft(im[i,:,:],kernel[i,:,:])
    #   default in convolve_fft()
    #       psf_pad=True
    #       boundary='fill',fill_value=0.0
    print("---{0:^10} : {1:<8.5f} seconds ---".format('convolve_fft_2Dloop',time.time()-start_time))
    
    
    start_time = time.time()
    for i in range(100):
        test=convolve_fft(im[i,:,:],kernel[i,:,:],fft_pad=False)
    #   default in convolve_fft()
    #       psf_pad=True
    #       boundary='fill',fill_value=0.0
    print("---{0:^10} : {1:<8.5f} seconds ---".format('convolve_fft_2Dloop_nofftpad',time.time()-start_time))    
    
    #start_time = time.time()
    #for i in range(100):
    #    test=convolve_fft(im[i,:,:],kernel[i,:,:],fftn=fftn)
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('convolve_fft_2Dloop',time.time()-start_time))    
    
    start_time = time.time()
    for i in range(100):
        test=convolve_fft(im[i,:,:],kernel_large[i,:,:])
    print("---{0:^10} : {1:<8.5f} seconds ---".format('convolve_fft_2Dloop_large',time.time()-start_time))    
    
    
    
    start_time = time.time()
    for i in range(100):
        test=convolve_fft(im[i,:,:],kernel_small[i,:,:])
    print("---{0:^10} : {1:<8.5f} seconds ---".format('convolve_fft_2Dloop_small',time.time()-start_time))
    

    
    start_time = time.time()
    for i in range(100):
        test=convolve_fft(im[i,:,:],kernel_large[i,:,:],fftn=fftn)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('convolve_fft_2Dloop',time.time()-start_time))        
    
    #start_time = time.time()
    #test=convolve_fft(im,kernel[np.newaxis,0,:,:])
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('convolve_fft_3D',time.time()-start_time))
    
    #start_time = time.time()
    #test=convolve(im,kernel[np.newaxis,0,:,:])
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('convolve_3D',time.time()-start_time))    

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
    
def test_gmake_model_api():
    
    inp_dct=gmake_readinp('examples/bx610/bx610xy_dm_all.inp',verbose=False)
    dat_dct=gmake_read_data(inp_dct,verbose=False,fill_mask=True,fill_error=True)

    mod_dct=gmake_inp2mod(inp_dct)
    
    start_time = time.time()
    models=gmake_model_api(mod_dct,dat_dct,verbose=False)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('apicall',time.time() - start_time))
    
    start_time = time.time()
    gmake_model_export(models,outdir='./test')
    print("---{0:^10} : {1:<8.5f} seconds ---".format('export',time.time()-start_time))
  
    
    #lnl,blobs=gmake_model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
    #                             savemodel='test/test_gmake_model_api')

    return models

def test_gmake_model_kinmspy():
    
    inp_dct=gmake_readinp('examples/bx610/bx610xy_test.inp',verbose=False)
    dat_dct=gmake_read_data(inp_dct,verbose=False,fill_mask=True,fill_error=True)
    
    mod_dct=gmake_inp2mod(inp_dct)
    obj=mod_dct['co76']
    
    start_time = time.time()
    hd=dat_dct['header@examples/bx610/bx610.bb2.cube.iter0.image.fits']
    model=gmake_model_kinmspy(hd,obj)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    fits.writeto('test/test_model_kinmspy_model.fits',model,hd,overwrite=True)

if  __name__=="__main__":
    

    
    #test_gmake_model_disk2d()
    #models=test_gmake_model_api()
    #test_gmake_model_kinmspy()
    #test_convolve_eff()
    test_convolve_edge()
    #test_makekernel()

    
