
from gmake.vis_utils import cpredict_ms
from gmake.vis_utils import gpredict_ms
from rxutils.casa.proc import setLogfile
from astropy.io import fits
from gmake.model import makepb
setLogfile('casa.log')
#cpredict_ms('test1.ms',fitsimage='../../data/mockup_basic/00.ms/im.fits',\
#            inputvis='../../data/mockup_basic/00.ms',pbcor=True)
#
# 0.0003 or 0.03 off
gpredict_ms('test2.ms',fitsimage='../../data/mockup_basic/00.ms/im.fits',\
            inputvis='../../data/mockup_basic/00.ms',pb='../../data/mockup_basic/00.ms/dm.pb.fits')

# 0.98  or 2% off
#gpredict_ms('test2.ms',fitsimage='../../data/mockup_basic/00.ms/im.fits',\
#            inputvis='../../data/mockup_basic/00.ms',antsize=25*u.m)

"""
# this is eqauivelent with the antsize=? 
header=fits.getheader('../../data/mockup_basic/00.ms/im.fits')
ms1=read_ms(vis='../../data/mockup_basic/00.ms')
pb=makepb(header,phasecenter=ms1['phasecenter@../../data/mockup_basic/00.ms'],antsize=25*u.m)
fits.writeto('pb.fits',pb,header,overwrite=True)
gpredict_ms('test2.ms',fitsimage='../../data/mockup_basic/00.ms/im.fits',\
            inputvis='../../data/mockup_basic/00.ms',pb='pb.fits')
"""

from casatools import simulator
from casatasks import importfits,imhead
from rxutils.casa.proc import setLogfile
from gmake.vis_utils import read_ms
setLogfile('casa.log')
import numpy as np
from astropy.io import fits
from gmake import makepb
import astropy.units as u


ms1=read_ms(vis='test1.ms')
print(ms1.keys())
ms2=read_ms(vis='test2.ms')
print(ms2.keys())

dt1=ms1['data@test1.ms']
dt2=ms2['data@test2.ms']


dt1=dt1[ms1['flag@test1.ms']==False].copy()
dt2=dt2[ms2['flag@test2.ms']==False].copy()

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.ticker as plticker
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.colors as colors
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"
mpl.rcParams['agg.path.chunksize'] = 10000
plt.rc('text', usetex=False)

plt.clf()
fig = plt.figure(figsize=(8,8)) 
ax = fig.add_subplot(221)
ax.scatter(dt1[::20].real,dt2[::20].real)
ymin, ymax = ax.get_ylim()
xmin, xmax = ax.get_xlim()
ax.set_ylim(ymin, ymax)
ax.set_xlim(xmin, xmax)
ax.plot([-1,1],[-1,1])



ax = fig.add_subplot(222)
ax.scatter(dt1[::20].imag,dt2[::20].imag)
ymin, ymax = ax.get_ylim()
xmin, xmax = ax.get_xlim()
ax.set_ylim(ymin, ymax)
ax.set_xlim(xmin, xmax)
ax.plot([-1,1],[-1,1])

print(np.nanmedian(dt1[::20].real/dt2[::20].real))
print(np.nanmedian(dt1[::20].imag/dt2[::20].imag))
print(np.nanmedian(np.angle(dt1[::20])/np.angle(dt2[::20])))

ax = fig.add_subplot(223)
ax.scatter(np.absolute(dt1[::20]),np.absolute(dt2[::20]))
ymin, ymax = ax.get_ylim()
xmin, xmax = ax.get_xlim()
ax.set_ylim(ymin, ymax)
ax.set_xlim(xmin, xmax)
ax.plot([-1,1],[-1,1])

ax = fig.add_subplot(224)
ax.scatter(np.angle(dt1[::20]),np.angle(dt2[::20]))
ymin, ymax = ax.get_ylim()
xmin, xmax = ax.get_xlim()
ax.set_ylim(ymin, ymax)
ax.set_xlim(xmin, xmax)
ax.plot([-1,1],[-1,1])

fig.tight_layout()
fig.savefig('test.png') 
plt.close(fig)

