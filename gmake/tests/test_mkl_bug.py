

import numpy as np
import mkl_fft._numpy_fft
import mkl_fft._scipy_fft
im=np.ones((100,1000))
fftn=mkl_fft._numpy_fft.fftn(im)
import galario


def test_mkl():

    print("--")
    im=np.ones((100,1000))
    fftn=np.fft.fftn(im)
    print(np.min(fftn),np.max(fftn),np.median(fftn),np.sum(fftn))
    im=np.ones((100,1000))
    fftn=mkl_fft._numpy_fft.fftn(im)    
    print(np.min(fftn),np.max(fftn),np.median(fftn),np.sum(fftn))
    
    return
    
if  __name__=="__main__":  
    
    #import galario
    #pyfftw.config.NUM_THREADS = multiprocessing.cpu_count()
    #test_convolve_performance(imsize=128,knsize=128,nloop=2,fftpad=False,complex_dtype=np.complex64,nd=2)
    
    test=test_mkl()