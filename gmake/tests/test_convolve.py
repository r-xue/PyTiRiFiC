import numpy as np
import multiprocessing
import pyfftw
from gmake.model import makekernel
import time
from astropy.convolution import convolve_fft
from astropy.io import fits 
import scipy
import scipy.signal
import mkl_fft._numpy_fft
import mkl_fft._scipy_fft
import cluda

pyfftw.config.NUM_THREADS=8 
pyfftw.interfaces.cache.enable()
pyfftw.interfaces.cache.set_keepalive_time(5)

def fftw_fftn(input_data): 
    
    #pyfftw.forget_wisdom()
    #fftn_obj = pyfftw.builders.fftn(input_data, planner_effort='FFTW_ESTIMATE')
    fftn_obj = pyfftw.builders.fftn(input_data)
    
    return fftn_obj()

def fftw_ifftn(input_data): 
    
    #pyfftw.forget_wisdom()
    #ifftn_obj = pyfftw.builders.ifftn(input_data, planner_effort='FFTW_ESTIMATE')
    ifftn_obj = pyfftw.builders.ifftn(input_data)
    
    return ifftn_obj()




#pyfftw.config.NUM_THREADS=1

def gpyfft_fftn(input_data):
    
    context = cl.create_some_context()
    queue = cl.CommandQueue(context)
    data_host = input_data
    data_gpu = cla.to_device(queue, data_host)
    transform =  gpyfft_fft.FFT(context, queue, data_gpu)
    event, = transform.enqueue(forward=True)
    event.wait()
    result_host = data_gpu.get()

    return result_host

def gpyfft_ifftn(input_data):
    
    context = cl.create_some_context()
    queue = cl.CommandQueue(context)
    data_host = input_data
    data_gpu = cla.to_device(queue, data_host)
    transform =  gpyfft_fft.FFT(context, queue, data_gpu)
    event, = transform.enqueue(forward=False)
    event.wait()
    result_host = data_gpu.get()

    return result_host


def reikna_get_complex_trf(arr):
    complex_dtype = dtypes.complex_for(arr.dtype)
    return Transformation(
        [Parameter('output', Annotation(Type(complex_dtype, arr.shape), 'o')),
        Parameter('input', Annotation(arr, 'i'))],
        """
        ${output.store_same}(
            COMPLEX_CTR(${output.ctype})(
                ${input.load_same},
                0));
        """)

def reikna_fftn_vx(input_data):
    
    #api=any_api()
    #api=cluda.cuda_api()
    api=cluda.ocl_api()
    thr = api.Thread.create()
    trf = reikna_get_complex_trf(input_data)
    fft = cluda_fft.FFT(trf.output) 
    fft.parameter.input.connect(trf, trf.output, new_input=trf.input)
    fftc=fft.compile(thr)
    data_dev = thr.to_device(input_data)
    res_dev = thr.array(arr.shape, numpy.complex64)
    fftc(data_dev,data_dev,inverse=False)

    return data_dev.get()

    
def reikna_fftn(input_data):
    
    #api=any_api()
    #api=cluda.cuda_api()
    api=cluda.ocl_api()
    thr = api.Thread.create()
    #data=input_data.astype(np.complex64)
    data=input_data
    fft=cluda_fft.FFT(data)
    fftc = fft.compile(thr)
    data_dev = thr.to_device(data)
    #res_dev = thr.empty_like(data_dev)
    #fftc(data_dev,res_dev,inverse=False)
    fftc(data_dev,data_dev,inverse=False)

    return data_dev.get()

def reikna_ifftn(input_data):
    
    #api=any_api()
    #api=cluda.cuda_api()
    api=cluda.ocl_api()
    thr = api.Thread.create()
    #data=input_data.astype(np.complex64)
    data=input_data
    fft=cluda_fft.FFT(data)
    fftc = fft.compile(thr)
    data_dev = thr.to_device(data)
    #res_dev = thr.empty_like(data_dev)
    #fftc(data_dev,res_dev,inverse=False)
    fftc(data_dev,data_dev,inverse=True)

    return data_dev.get()

def test_convolve_performance(imsize=128,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=2):
    """
    test different options to improve convol effciency) 
    
    References:
        https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        https://stackoverflow.com/questions/6365623/improving-fft-performance-in-python
        https://github.com/IntelPython/mkl_fft
        https://github.com/mperrin/webbpsf/issues/10
        https://poppy-optics.readthedocs.io/en/stable/fft_optimization.html
        https://blog.mide.com/matlab-vs-python-speed-for-vibration-analysis-free-download
        https://mathema.tician.de/the-state-of-opencl-for-scientific-computing-in-2018/
    
    Summary Note:
        + pyfftw is preferred over pyfftw3
        + opencl/reikna doesn't show clear advantages over CPU-based solutions for small arrays
            - too much overhead
        + MKL_FFT is the fastest option in general.
        + pyfft was replaced by reikna
        + turn on pyfftw.Threads doesn't help that much...
        + mkl out-performance others
        + pyfftw-build slightly better than pyfftw-interface
        + reikna
        + Loop vs. 3DFFT: 3DFFT slightly worse in single-thread test
        + the gain from pyfft will be more visible for larger images with threading-on!
             

    pyfftw.config.NUM_THREADS = multiprocessing.cpu_count()
    pyfftw.config.NUM_THREADS = 1
    test_convolve_performance(imsize=128,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=2)
    test_convolve_performance(imsize=128,knsize=128,nloop=128,fftpad=False,complex_dtype=np.complex64,nd=2)
    test_convolve_performance(imsize=128,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=3)
    test_convolve_performance(imsize=1024,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=2)

    LOG:
    
In [32]: test_convolve_performance(imsize=1024,knsize=256,nloop=128,fftpad=False,complex_dtype=np.complex64,nd=2)         


---fft_pad=False/numpy : 31.03843 seconds ---
---fft_pad=False/scipy : 33.68730 seconds ---
---fft_pad=False/pyfftw-interfaces : 21.66385 seconds ---
---fft_pad=False/mkl : 17.91704 seconds ---
---fft_pad=False/pyfftw-build : 18.74507 seconds ---    
    
    pyfftw.config.NUM_THREADS = multiprocessing.cpu_count()
    
    test_convolve_performance(imsize=128,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=2)
    
    ---fft_pad=False/numpy : 0.02182  seconds ---
    ---fft_pad=False/scipy : 0.01356  seconds ---
    ---fft_pad=False/pyfftw-interfaces : 0.01193  seconds ---
    ---fft_pad=False/mkl : 0.00376  seconds ---
    ---fft_pad=False/pyfftw-build : 0.02095  seconds ---
    ---fft_pad=False/reikna : 0.15106  seconds ---
    
    test_convolve_performance(imsize=128,knsize=128,nloop=128,fftpad=False,complex_dtype=np.complex64,nd=2)
    
    ---fft_pad=False/numpy : 1.80886  seconds ---
    ---fft_pad=False/scipy : 1.22826  seconds ---
    ---fft_pad=False/pyfftw-interfaces : 1.15559  seconds ---
    ---fft_pad=False/mkl : 0.39774  seconds ---
    ---fft_pad=False/pyfftw-build : 1.05104  seconds ---
    ---fft_pad=False/reikna : 15.32986 seconds ---
    
    test_convolve_performance(imsize=128,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=3)
    
    ---fft_pad=False/numpy : 7.26300  seconds ---
    ---fft_pad=False/scipy : 4.91297  seconds ---
    ---fft_pad=False/pyfftw-interfaces : 1.04028  seconds ---
    ---fft_pad=False/mkl : 0.55822  seconds ---
    ---fft_pad=False/pyfftw-build : 0.87248  seconds ---
    ---fft_pad=False/reikna : 2.00951  seconds ---
    
    test_convolve_performance(imsize=1024,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=2)
    
    ---fft_pad=False/numpy : 0.48901  seconds ---
    ---fft_pad=False/scipy : 0.28967  seconds ---
    ---fft_pad=False/pyfftw-interfaces : 0.11724  seconds ---
    ---fft_pad=False/mkl : 0.06158  seconds ---
    ---fft_pad=False/pyfftw-build : 0.10101  seconds ---
    ---fft_pad=False/reikna : 0.66387  seconds ---
    
    pyfftw.config.NUM_THREADS = 1
    
    test_convolve_performance(imsize=128,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=2)
    
    ---fft_pad=False/numpy : 0.02202  seconds ---
    ---fft_pad=False/scipy : 0.01423  seconds ---
    ---fft_pad=False/pyfftw-interfaces : 0.01028  seconds ---
    ---fft_pad=False/mkl : 0.00253  seconds ---
    ---fft_pad=False/pyfftw-build : 0.01136  seconds ---
    ---fft_pad=False/reikna : 0.16480  seconds ---
    
    test_convolve_performance(imsize=128,knsize=128,nloop=128,fftpad=False,complex_dtype=np.complex64,nd=2)
    
    ---fft_pad=False/numpy : 1.69174  seconds ---
    ---fft_pad=False/scipy : 1.17897  seconds ---
    ---fft_pad=False/pyfftw-interfaces : 1.20160  seconds ---
    ---fft_pad=False/mkl : 0.37091  seconds ---
    ---fft_pad=False/pyfftw-build : 1.16632  seconds ---
    ---fft_pad=False/reikna : 15.13192 seconds ---
    
    test_convolve_performance(imsize=128,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=3)
    
    ---fft_pad=False/numpy : 7.22203  seconds ---
    ---fft_pad=False/scipy : 4.92535  seconds ---
    ---fft_pad=False/pyfftw-interfaces : 2.38302  seconds ---
    ---fft_pad=False/mkl : 0.51912  seconds ---
    ---fft_pad=False/pyfftw-build : 2.10617  seconds ---
    ---fft_pad=False/reikna : 1.95317  seconds ---
    
    test_convolve_performance(imsize=1024,knsize=128,nloop=1,fftpad=False,complex_dtype=np.complex64,nd=2)
    
    ---fft_pad=False/numpy : 0.47751  seconds ---
    ---fft_pad=False/scipy : 0.28559  seconds ---
    ---fft_pad=False/pyfftw-interfaces : 0.17660  seconds ---
    ---fft_pad=False/mkl : 0.05815  seconds ---
    ---fft_pad=False/pyfftw-build : 0.14532  seconds ---
    ---fft_pad=False/reikna : 0.65862  seconds ---
    

    
    """
    print("\n")
    
    if  nd==2:
        im=makekernel(imsize,imsize,[6.0,6.0],pa=0)
        kn=makekernel(knsize,knsize,[15.0,5.0],pa=10)
    if  nd==3:
        im=np.ones((imsize,imsize,imsize))
        kn=np.ones((1,knsize,knsize))

    start_time = time.time()
    for i in range(nloop):
        #sm=convolve_fft(im,kn)
        # explicit default: (use fftn/ifftn rather than fft/ifft for image)
        #sm=convolve_fft(im,kn)
        # explicit default: (use fftn/ifftn rather than fft/ifft for image)
        # numpy.fft works best at 2^n
        sm=convolve_fft(im,kn,fft_pad=fftpad,complex_dtype=complex_dtype,
                        fftn=np.fft.fftn, ifftn=np.fft.ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad='+str(fftpad)+'/numpy',time.time()-start_time))
    fits.writeto('test_convolve_numpy.fits',sm,overwrite=True)    
    
    start_time = time.time()
    for i in range(nloop):
        sm=convolve_fft(im,kn,fft_pad=fftpad,complex_dtype=complex_dtype,
                        fftn=scipy.fftpack.fftn, ifftn=scipy.fftpack.ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad='+str(fftpad)+'/scipy',time.time()-start_time))
    fits.writeto('test_convolve_scipy.fits',sm,overwrite=True)    

    
    start_time = time.time()
    for i in range(nloop):
        sm=convolve_fft(im,kn,fft_pad=fftpad,complex_dtype=complex_dtype,
                        fftn=pyfftw.interfaces.numpy_fft.fftn, ifftn=pyfftw.interfaces.numpy_fft.ifftn)
        #               fftn=pyfftw.interfaces.scipy_fftpack.fftn, ifftn=pyfftw.interfaces.scipy_fftpack.ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad='+str(fftpad)+'/pyfftw-interfaces',time.time()-start_time))
    fits.writeto('test_convolve_fftw_interface.fits',sm,overwrite=True) 
    
    start_time = time.time()
    for i in range(nloop):
        print(im.flags,kn.flags)
        print(im.dtype,kn.dtype)
        sm=convolve_fft(im,kn,#fft_pad=fftpad,#complex_dtype=complex_dtype,
                        fftn=mkl_fft._numpy_fft.fftn, ifftn=mkl_fft._numpy_fft.ifftn)        
        #scipy.fftpack=mkl_fft._scipy_fft
        #sm=scipy.signal.fftconvolve(im,kn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad='+str(fftpad)+'/mkl',time.time()-start_time))
    fits.writeto('test_convolve_mkl.fits',sm,overwrite=True) 

    
    start_time = time.time()
    for i in range(nloop):
        sm=convolve_fft(im,kn,fft_pad=fftpad,complex_dtype=complex_dtype,
                        fftn=fftw_fftn, ifftn=fftw_ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad='+str(fftpad)+'/pyfftw-build',time.time()-start_time))
    fits.writeto('test_convolve_fftw_build.fits',sm,overwrite=True) 
             
    
    """         
    start_time = time.time()
    # my GPU only supported complex64 
    for i in range(nloop):
        sm=convolve_fft(im,kn,fft_pad=fftpad,complex_dtype=complex_dtype,
                        fftn=reikna_fftn, ifftn=reikna_ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad='+str(fftpad)+'/reikna',time.time()-start_time))
    fits.writeto('test_convolve_reikna.fits',sm,overwrite=True)
    """             
    
    
    """
    #
    #    gpyfft not working properly
    # 
    
    start_time = time.time()
    for i in range(1):
        sm=convolve_fft(im,kn,fft_pad=False,complex_dtype=np.complex64,
                        fftn=gpyfft_fftn, ifftn=gpyfft_ifftn)
    print("---{0:^17} : {1:<8.5f} seconds ---".format('fft_pad=False/gpyfft',time.time()-start_time))
    fits.writeto('test_convolve_gpyfft.fits',sm,overwrite=True) 
    """
def test_mkl():
    """
    mkl is rather buggy
    """
    im=np.ones(100)
    print(np.sum(np.fft.fftn(im.astype(np.float32))))  
    print(np.sum(mkl_fft.fftn(im.astype(np.complex64))))   
    im=np.ones((100,100))
    #print(im.astype(np.float32).dtype)
    print(np.sum(np.fft.fftn(im)))

    print(np.sum( mkl_fft.fftn(im,overwrite_x=False) ) )
    print(im)
    r=mkl_fft.fftn(im,overwrite_x=False)
    print(np.sum( r ) )
    print(np.sum( mkl_fft.fftn(im) ) )
    return 
    
if  __name__=="__main__":  
    
    #pyfftw.config.NUM_THREADS = multiprocessing.cpu_count()
    #test_convolve_performance(imsize=128,knsize=128,nloop=2,fftpad=False,complex_dtype=np.complex64,nd=2)
    test=test_mkl()