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
gmake.clouds_fill(mod_dct)
#%lprun -f gmake.model.potential_fromobj gmake.clouds_fill(mod_dct)

from gmake.plts import plt_rc
import astropy.units as u
import numpy as np

from gmake.model import potential_fromobj

import astropy.units as u
import galpy.potential as potential



def test_makepots():
    """
    """
    pots=potential_fromobj(mod_dct['diskdyn'])

if  __name__=="__main__":  
    test_makepots()

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