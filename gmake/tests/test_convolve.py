import numpy as np
import multiprocessing
import os


try:
    import mkl_fft
    import mkl_fft._numpy_fft
    import mkl_fft._scipy_fft
    import mkl
    tmp=mkl_fft.fftn(np.ones(1))
except:
    pass
import galario

import pyfftw


from gmake.model import makekernel

#import numpy as np
#from .stats import pdf2rv
#from .stats import cdf2rv
#from .stats import custom_rvs
#from .stats import custom_pdf
import astropy.units as u
#import fast_histogram as fh
import pprint
#from .utils import eval_func
#from .utils import one_beam
#from .utils import sample_grid

import time
from astropy.coordinates.matrix_utilities import rotation_matrix,matrix_product,matrix_transpose
from astropy.coordinates.representation import SphericalRepresentation, CylindricalRepresentation, CartesianRepresentation
from astropy.coordinates.representation import SphericalDifferential, CylindricalDifferential, CartesianDifferential
from io import StringIO
#from asteval import Interpreter
#aeval = Interpreter(err_writer=StringIO())
#aeval = Interpreter()
#aeval.symtable['u']=u
#from numpy.random import Generator,SFC64,PCG64
from astropy._erfa import ufunc as erfa_ufunc
from astropy import constants as const

#from galario.double import get_image_size
#from galario.double import sampleImage
import galario
import numpy as np

from astropy.modeling.models import Gaussian2D
from astropy.convolution import discretize_model
#from .meta import create_header
from astropy.stats import sigma_clipped_stats
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.wcs import WCS
from scipy.interpolate import interpn

#import logging
#logger = logging.getLogger(__name__)





import time
from astropy.convolution import convolve_fft
from astropy.io import fits 
import scipy
import scipy.signal



#import cluda

#pyfftw.config.NUM_THREADS=8 
#pyfftw.interfaces.cache.enable()
#pyfftw.interfaces.cache.set_keepalive_time(5)

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
    
    New summary:
hyperion:Downloads Rui$ python /Users/Rui/Resilio/Workspace/projects/GMaKE/gmake/tests/test_convolve.py
------------------------------
core: 8 64


---fft_pad=False/numpy : 0.01573  seconds ---
---fft_pad=False/scipy : 0.01781  seconds ---
---fft_pad=False/pyfftw-interfaces : 0.01211  seconds ---
---fft_pad=False/mkl : 0.00821  seconds ---
---fft_pad=False/pyfftw-build : 0.02241  seconds ---
core: 1 64


---fft_pad=False/numpy : 0.01578  seconds ---
---fft_pad=False/scipy : 0.01995  seconds ---
---fft_pad=False/pyfftw-interfaces : 0.00980  seconds ---
---fft_pad=False/mkl : 0.01070  seconds ---
---fft_pad=False/pyfftw-build : 0.01948  seconds ---
------------------------------
core: 8 128


---fft_pad=False/numpy : 0.07980  seconds ---
---fft_pad=False/scipy : 0.06774  seconds ---
---fft_pad=False/pyfftw-interfaces : 0.03930  seconds ---
---fft_pad=False/mkl : 0.02288  seconds ---
---fft_pad=False/pyfftw-build : 0.06307  seconds ---
core: 1 128


---fft_pad=False/numpy : 0.07151  seconds ---
---fft_pad=False/scipy : 0.06872  seconds ---
---fft_pad=False/pyfftw-interfaces : 0.06733  seconds ---
---fft_pad=False/mkl : 0.02647  seconds ---
---fft_pad=False/pyfftw-build : 0.06610  seconds ---
------------------------------
core: 8 256


---fft_pad=False/numpy : 0.36860  seconds ---
---fft_pad=False/scipy : 0.30269  seconds ---
---fft_pad=False/pyfftw-interfaces : 0.16756  seconds ---
---fft_pad=False/mkl : 0.12859  seconds ---
---fft_pad=False/pyfftw-build : 0.22736  seconds ---
core: 1 256


---fft_pad=False/numpy : 0.35906  seconds ---
---fft_pad=False/scipy : 0.30761  seconds ---
---fft_pad=False/pyfftw-interfaces : 0.31902  seconds ---
---fft_pad=False/mkl : 0.13502  seconds ---
---fft_pad=False/pyfftw-build : 0.35638  seconds ---
------------------------------
core: 8 512


---fft_pad=False/numpy : 1.37095  seconds ---
---fft_pad=False/scipy : 1.69786  seconds ---
---fft_pad=False/pyfftw-interfaces : 0.76424  seconds ---
---fft_pad=False/mkl : 0.46024  seconds ---
---fft_pad=False/pyfftw-build : 0.83339  seconds ---
core: 1 512


---fft_pad=False/numpy : 1.32977  seconds ---
---fft_pad=False/scipy : 1.57104  seconds ---
---fft_pad=False/pyfftw-interfaces : 1.25384  seconds ---
---fft_pad=False/mkl : 0.56665  seconds ---
---fft_pad=False/pyfftw-build : 1.42633  seconds ---
------------------------------
core: 8 1024


---fft_pad=False/numpy : 7.31928  seconds ---
---fft_pad=False/scipy : 7.08326  seconds ---
---fft_pad=False/pyfftw-interfaces : 3.51487  seconds ---
---fft_pad=False/mkl : 1.79977  seconds ---
---fft_pad=False/pyfftw-build : 4.45799  seconds ---
core: 1 1024


---fft_pad=False/numpy : 7.92551  seconds ---
---fft_pad=False/scipy : 8.17085  seconds ---
---fft_pad=False/pyfftw-interfaces : 7.29244  seconds ---
---fft_pad=False/mkl : 2.15090  seconds ---
---fft_pad=False/pyfftw-build : 7.44018  seconds --



    
    
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
        sm=convolve_fft(im,kn,fft_pad=fftpad,complex_dtype=complex_dtype,
                        fftn=mkl_fft.fftn, ifftn=mkl_fft.ifftn)        
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

    print("--")
    im=np.ones((100,1000))
    fftn=np.fft.fftn(im)
    print(np.min(fftn),np.max(fftn),np.median(fftn),np.sum(fftn))
    im=np.ones((100,1000))
    fftn=mkl_fft._numpy_fft.fftn(im)    
    print(np.min(fftn),np.max(fftn),np.median(fftn),np.sum(fftn))

    return 
    
if  __name__=="__main__":  
    # python /Users/Rui/Resilio/Workspace/projects/GMaKE/gmake/tests/test_convolve.py
    # https://software.intel.com/en-us/mkl-linux-developer-guide-mkl-domain-num-threads
    # http://www.diracprogram.org/doc/release-17/installation/mkl.html
    for imsize in [64,128,256,512,1024]:
        print("-"*30)
        for num in [8,1]:
            #os.environ["OMP_NUM_THREADS"]=str(num)
            #os.environ["MKL_NUM_THREADS"]=str(num)
            #os.environ['MKL_DOMAIN_NUM_THREADS']="MKL_DOMAIN_FFT="+str(num)
            mkl.domain_set_num_threads(num, domain='all')
            mkl.set_num_threads(num)
            mkl.set_dynamic(True)
            pyfftw.config.NUM_THREADS=num
            
            # for single-core comparison / mkl
            #pyfftw.config.NUM_THREADS = multiprocessing.cpu_count()
            print('core:',num,imsize)
            test_convolve_performance(imsize=imsize,knsize=imsize,nloop=10,fftpad=False,complex_dtype=np.complex64,nd=2)
            
            
    #test=test_mkl()