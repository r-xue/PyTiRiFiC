from numpy.random import Generator,SFC64,PCG64 
rng1=Generator(SFC64(None))

import mkl_random
rng2=mkl_random.RandomState(None)
import astropy.units as u
import numpy as np

size=10**5
nV=10
vSigma=5*u.km/u.s

"""
%timeit rng1.random(10**5)
%timeit rng1.uniform(low=0,high=1,size=10**5)

%timeit rng1.random(10**5)*0.1
%timeit rng1.uniform(low=0,high=0.1,size=10**5)

%timeit rng2.random_sample(10**5)
%timeit rng2.rand(10**5)
%timeit rng2.uniform(low=0,high=1,size=10**5)

%timeit rng2.random_sample(10**5)*0.1
%timeit rng2.rand(10**5)*0.1
%timeit rng2.uniform(low=0,high=0.1,size=10**5)
%timeit rng2.uniform(low=-0.2,high=0.1,size=10**5)

262 µs ± 42.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
344 µs ± 13.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

249 µs ± 5.2 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
331 µs ± 2.73 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

66.4 µs ± 441 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
65.3 µs ± 339 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
66.5 µs ± 706 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

89.4 µs ± 443 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
89 µs ± 561 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
66.2 µs ± 336 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

for numpy.random
    use rng1.random(10**5)*scale
for mkl_random
    use rng2.uniform(low=0,high=0.1,size=10**5)
"""



"""

%timeit rng1.standard_normal(size=(3,10**5))*3
%timeit rng1.normal(scale=3,size=(3,10**5))

%timeit rng2.standard_normal(size=(3,10**5))*3
%timeit rng2.normal(scale=3,size=(3,10**5))


2.72 ms ± 26.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
3.03 ms ± 18.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
763 µs ± 7.93 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
719 µs ± 23.9 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
for numpy.random
    use rng1.standard_normal(10**5)*scale
for mkl_random
    use rng2.normal(scale=3,size=(3,10**5))
"""

"""
%timeit rng2.uniform(low=0,high=2*np.pi,size=size)<<u.rad
%timeit (2*np.pi)*rng1.random(size)<<u.rad
72.7 µs ± 376 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
252 µs ± 2.58 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
"""




"""
%timeit rng2.normal(scale=vSigma.value,size=(3,nV,size))<<vSigma.unit
%timeit rng2.standard_normal(size=(3,nV,size))*vSigma
%timeit rng2.standard_normal(size=(3,nV,size))<<vSigma.unit
%timeit rng1.standard_normal(size=(3,nV,size))*vSigma.value<<vSigma.unit
%timeit rng1.standard_normal(size=(3,nV,size))*vSigma
%timeit rng1.normal(scale=vSigma.value,size=(3,nV,size))<<vSigma.unit

10.3 ms ± 182 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
14.8 ms ± 1.49 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)
10.2 ms ± 445 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
28.9 ms ± 594 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
"""