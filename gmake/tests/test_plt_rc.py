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

plt_rc(mod_dct['diskdyn']['pots'],rrange=[0,20]*u.kpc,pscorr=(60*u.km/u.s,10*u.kpc))

# est_plt_rc Rui$ python /Users/Rui/Resilio/Workspace/projects/GMaKE/gmake/tests/test_plt_rc.p