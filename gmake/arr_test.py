import timeit
import time
#from numba import jit
import numba
import numpy as np
import numexpr as ne

ne.print_versions() 

"""


a=np.random.rand(500000,300).astype(np.complex64) 
b=np.random.rand(500000,300).astype(np.complex64)

#@jit(nopython=True,parallel=True)

#@numba.njit
def test0(a,b):
    a=b
    return c

c=a+b
    
start_time1 = time.time()
c1=np.abs(c)
print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>loop-fancy1',time.time()-start_time1))

start_time1 = time.time()
c2=ne.evaluate("(c.real**2+c.imag**2)**0.5")
print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>loop-fancy1',time.time()-start_time1))

start_time1 = time.time()
c3=ne.evaluate("abs(c)")
print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>loop-fancy1',time.time()-start_time1))

print(np.allclose(c1,c2))
print(np.allclose(c1,c3))

ne.ncores 
ne.nthreads
ne.use_vml 
"""

"""
--->>>>loop-fancy1 : 0.02579  seconds ---
--->>>>loop-fancy1 : 0.00867  seconds ---
--->>>>loop-fancy1 : 0.30167  seconds ---
--->>>>loop-fancy1 : 0.01072  seconds ---
"""


import numpy as np
import numexpr as ne
a = np.random.rand(int(1e6))
b = np.random.rand(int(1e6))

start_time1 = time.time()
for i in range(10):
    2*a + 3*b
print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>loop-fancy1',time.time()-start_time1))

start_time1 = time.time()
for i in range(10):
    ne.evaluate("2*a + 3*b",optimization='aggressive')
print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>loop-fancy1',time.time()-start_time1))


start_time1 = time.time()
for i in range(10):
    2*a+b**10
print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>loop-fancy1',time.time()-start_time1))

start_time1 = time.time()
for i in range(10):
    ne.evaluate("2*a+b**10",optimization='aggressive')
print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>loop-fancy1',time.time()-start_time1))


# source /opt/intel/intelpython3/bin/activate root

