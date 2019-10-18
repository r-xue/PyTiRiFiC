####
# ToolBox can be used
#   imager.advisechansel()
#   ms.cvelfreqs()
#   msmetadata.
#   or something in analysisUtils
###

import sys,os,glob,io,socket
import logging
from pprint import pprint

import casatasks as ctasks
import casatools as ctools

# Import wurlitzer for display real-time console logs
#   https://github.com/minrk/wurlitzer
#%reload_ext wurlitzer

# for inline plots
#%matplotlib inline
#%config InlineBackend.figure_format = "retina"


from rxutils.casa.proc import rmPointing  # help remove POINTING tables hidden under
from rxutils.casa.proc import setLogfile  # help reset the casa 6 log file
from rxutils.casa.proc import checkchflag # help check channel-wise flagging stats

print('casatools ver:',ctools.version_string())
print('casatasks ver:',ctasks.version_string())


setLogfile('tets_advisechansel.log')

im=ctools.imager()
msname='uid___A002_Xc69057_X91a.ms'
#ctasks.listobs(vis=msname,field='BX610',intent='OBSERVE_TARGET#ON_SOURCE',spw='25,27,29,31')


# im.advisechansel(getfreqrange=True) will give you
# left edge and right edge

out=im.advisechansel(msname=msname,\
                     spwselection='25',
                     getfreqrange=True,freqframe='LSRK')
print(out)
out=im.advisechansel(msname=msname,\
                     spwselection='25:0',
                     getfreqrange=True,freqframe='LSRK')
print(out)

msmd=ctools.msmetadata()
msmd.open(msname)

meanfreq = msmd.meanfreq(25)
bandwidth = msmd.bandwidths(25)
chanwidth = msmd.chanwidths(25)[0]

msmd.close()
    
ms=ctools.ms()
ms.open(msname)
fgrid=ms.cvelfreqs(spwids=[25],
            mode='channel',
            start=0,nchan=-1,width=1,outframe='TOPO')
ms.close()

import numpy as np
print(fgrid-np.roll(fgrid,1)) 