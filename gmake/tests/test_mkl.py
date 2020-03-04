

import numpy as np


try:
    import mkl_fft._numpy_fft as fft_use
    #tmp=fft_use.fftn(np.ones(1)) # we must do this at least once to avoidd downstream problem from galario
except:
    try:
        import pyfftw.interfaces.numpy_fft as fft_use
    except:
        import numpy.fft as fft_use
        # or import scipt.fftpack as fft_use
import mkl_random

from galario.single import threads as galario_threads

"""
fft iterface option:
    scipy.fftpack
    np.fft
    mkl_fft._numpy_fft/._scipy_fft/.
"""
# galario must imported after mkl_fft for some unknow reasons to avoid artificats
#import galario


def test_mkl_fft():

    print("fftn")
    im=np.ones((100,1000))
    fftn=np.fft.fftn(im)
    print(np.min(fftn),np.max(fftn),np.median(fftn),np.sum(fftn))
    im=np.ones((100,1000))
    fftn=fft_use.fftn(im)    
    print(np.min(fftn),np.max(fftn),np.median(fftn),np.sum(fftn))
    
    print("ifftn")
    im=np.ones((100,1000))
    fftn=np.fft.ifftn(im)
    print(np.min(fftn),np.max(fftn),np.median(fftn),np.sum(fftn))
    im=np.ones((100,1000))
    fftn=fft_use.ifftn(im)    
    print(np.min(fftn),np.max(fftn),np.median(fftn),np.sum(fftn))    
    
    return

def test_mkl_random():
    # https://software.intel.com/en-us/blogs/2016/06/15/faster-random-number-generation-in-intel-distribution-for-python
    
    import numpy as np
    from timeit import timeit, Timer
    import mkl_random as random_intel
    from operator import itemgetter
    
    def timer_brng(brng_name):
        return Timer('random_intel.uniform(0,1,size=10**5)', 
            setup='import mkl_random as random_intel; random_intel.seed(77777, brng="{}")'.format(brng_name))
    
    _brngs = ['WH', 'PHILOX4X32X10', 'MT2203', 'MCG59', 'MCG31', 'MT19937', 'MRG32K3A', 'SFMT19937', 'R250']
    tdata = sorted([(brng, timer_brng(brng).timeit(number=1000)) for brng in _brngs], key=itemgetter(1))
    
    def relative_perf(tdata):
        base = dict(tdata).get('MT19937')

        return [(name, t/base) for name, t in tdata]
    
    result=relative_perf(tdata)
    print(result)

def test_mkl_random2():
    
    from numpy.random import Generator,SFC64,PCG64 
    rng1 = Generator(SFC64(None))
    #%timeit rng1.normal(scale=2,size=(3,10,10**5))   
    import mkl_random as rng2   
    #%timeit rng2.normal(scale=2,size=(3,10,10**5))
    # see https://github.com/IntelPython/mkl_random/blob/master/mkl_random/tests/test_random.py
    
if  __name__=="__main__":  
    
    #import galario
    #pyfftw.config.NUM_THREADS = multiprocessing.cpu_count()
    #test_convolve_performance(imsize=128,knsize=128,nloop=2,fftpad=False,complex_dtype=np.complex64,nd=2)
    
    test_mkl_fft()
    #test_mkl_random()