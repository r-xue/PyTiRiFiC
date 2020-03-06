import sys
import glob
import os
import io
import logging
from pprint import pprint

print(sys.version)


import gmake
print(gmake.__version__)
print(gmake.__email__)
print(gmake.__demo__)

inpfile=gmake.__demo__+'/../gmake/tests/data/test_pots.inp'
print(inpfile)
#inpfile=' ../../data/test_pots.inp'

inp_dct=gmake.read_inp(inpfile)
inp_dct=gmake.inp_validate(inp_dct)
mod_dct=gmake.inp2mod(inp_dct)
#gmake.clouds_fill(mod_dct)
#%lprun -f gmake.model.potential_fromobj gmake.clouds_fill(mod_dct)

from gmake.plts import plt_rc
import astropy.units as u

from gmake.plts import plt_rc
import astropy.units as u
import numpy as np

from gmake.model import potential_fromobj

import astropy.units as u
import galpy.potential as potential


def test_plt_rc(mod_dct):

    plt_rc(mod_dct['diskdyn']['pots'],rrange=[1e-1,2e1]*u.kpc,pscorr=(60*u.km/u.s,10*u.kpc))

if  __name__=="__main__":  
    pots=potential_fromobj(mod_dct['diskdyn'])
    test_plt_rc(mod_dct)


"""
pots=potential_fromobj(mod_dct['diskdyn']) 
rho=np.linspace(0.01,10,10**5)*u.kpc
%time pots[0].vcirc(rho)
%time pots[1].vcirc(rho)
%time pots[2].vcirc(rho)
%time pots[3].vcirc(rho)
%time pots[4].vcirc(rho) 
%time pots[5].vcirc(rho) 


    ...: %time pots[0].vcirc(rho) 
    ...: %time pots[1].vcirc(rho) 
    ...: %time pots[2].vcirc(rho) 
    ...: %time pots[3].vcirc(rho) 
    ...: %time pots[4].vcirc(rho)  
    ...: %time pots[5].vcirc(rho)                                                                                                                                                                                                                                                                  
CPU times: user 2.01 ms, sys: 1.54 ms, total: 3.55 ms
Wall time: 3.02 ms
CPU times: user 33.1 ms, sys: 1.05 ms, total: 34.2 ms
Wall time: 43.9 ms
CPU times: user 27.5 s, sys: 272 ms, total: 27.7 s
Wall time: 34.7 s
CPU times: user 6.38 ms, sys: 121 µs, total: 6.5 ms
Wall time: 6.59 ms
CPU times: user 942 µs, sys: 9 µs, total: 951 µs
Wall time: 956 µs
CPU times: user 2.29 ms, sys: 4 µs, total: 2.3 ms
Wall time: 2.3 ms
Out[54]: 
<Quantity [2073.86529699, 2063.58321172, 2053.45255915, ...,   65.58203416,
             65.58170657,   65.58137899] km / s>

In [55]: pots                                                                                                                                                                                                                                                                                      
Out[55]: 
[<galpy.potential.TwoPowerSphericalPotential.NFWPotential at 0x3593e30a0>,
 <galpy.potential.RazorThinExponentialDiskPotential.RazorThinExponentialDiskPotential at 0x3593e3160>,
 <galpy.potential.DoubleExponentialDiskPotential.DoubleExponentialDiskPotential at 0x364b64be0>,
 <galpy.potential.MN3ExponentialDiskPotential.MN3ExponentialDiskPotential at 0x3594024f0>,
 <galpy.potential.IsochronePotential.IsochronePotential at 0x3594021c0>,
 <galpy.potential.PowerSphericalPotential.KeplerPotential at 0x108312820>]


#print("---")
#a=pot[0].vcirc(10*u.kpc)+
#b=pot[1].vcirc(10*u.kpc)
#vc=(a*2+b**2)**2
#print((a**2+b**2)**0.5)
#print(vcirc(pot,10*u.kpc))
#print("---")
#import hickle as hkl
#hkl.dump(pot,'test.h5',mode='w')
#"""


"""