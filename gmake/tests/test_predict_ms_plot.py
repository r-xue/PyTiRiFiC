from gmake.vis_utils import cpredict_ms
from gmake.vis_utils import gpredict_ms
from rxutils.casa.proc import setLogfile
from astropy.io import fits
from gmake.model import makepb
setLogfile('casa.log')

from casatools import simulator
from casatasks import importfits,imhead
from rxutils.casa.proc import setLogfile
from gmake.vis_utils import read_ms
setLogfile('casa.log')
import numpy as np
from astropy.io import fits
from gmake import makepb
import astropy.units as u

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


def test_predict_ms_plot(vis1,vis2):

    
    ms1=read_ms(vis=vis1)
    print(ms1.keys())
    ms2=read_ms(vis=vis2)
    print(ms2.keys())
    
    dt1=ms1['data@'+vis1]
    dt2=ms2['data@'+vis2]
    
    
    dt1=dt1[ms1['flag@'+vis1]==False].copy()
    dt2=dt2[ms2['flag@'+vis2]==False].copy()
    
    
    
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
    fig.savefig('test_predict_ms_plot_'+\
                vis1.replace(".ms",'')+
                '_vs_'+\
                vis2.replace(".ms",'')+'.png')
    plt.close(fig)
    
if  __name__=="__main__":
    
    test_predict_ms_plot('0.ms','0c.ms')

