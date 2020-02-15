import casatools as ctl
import casatasks as ctk

logfile=ctk.casalog.logfile()
os.system('rm -rf '+logfile+' '+'test_casa6.log')
ctk.casalog.setlogfile('logs/test_casa6.log')
ctk.casalog.showconsole(onconsole=True)

#ctl.ms.open('bx610_band6_uv_ab/p_fits/data_b6_bb1.ms')
#tb=ctl.ms.getdata('Data')
#ctk.listobs('bx610_band6_uv_ab/p_fits/data_b6_bb1.ms')


ms = ctl.ms()
ms.open('bx610_band6_uv_ab/p_fits/data_b6_bb1.ms')
data=ms.getdata('Data')
uvw=ms.getdata('uvw')
ms.close

"""
# system
import os, sys
import numpy as np

# casa
import casatasks as ct
import casatools
ia = casatools.image()

#
print("Testing casa6 with ia.maketestimage()")

# ensure directory exists
pwd = os.getcwd() + '/data'
os.system('mkdir -p %s' % pwd)

# casa
ia.maketestimage('data/test6.im',overwrite=True)
ct.imhead('data/test6.im')
s0=ia.statistics()
ia.close()

#
print(s0)
"""
