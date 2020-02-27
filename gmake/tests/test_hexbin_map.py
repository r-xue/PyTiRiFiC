from gmake import sample_grid
from astropy.io import fits
import numpy as np 
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
plt.rc('text', usetex=True)


def test_hexbin_map():
    """
    """
    
    im,header=fits.getdata('../../data/mockup_spiral2_sm.fits',header=True)
    #print()
    im=np.sum(im,axis=0)
    print(im.shape)
    
    plt.clf()
    fig = plt.figure(figsize=(12,6)) 
    ax = fig.add_subplot(121)
    
    ax.imshow(im,extent=([-40,40,-40,40]),
              norm=colors.SymLogNorm(linthresh=0.03, linscale=0.03,
                                     vmin=0, vmax=im.max()))
    ax.contour(im, colors='k', origin='image', extent=([-40,40,-40,40]))
    ax.set_xlim(-40,40)
    ax.set_ylim(-40,40)
    ax.set_xlabel(r'$x_{\rm gal}$ [kpc]')
    ax.set_ylabel(r'$y_{\rm gal}$ [kpc]')
    #ax.set_xlim(-30,30)
    #ax.set_ylim(-30,30)       
    
    
    ax = fig.add_subplot(122)
    xx,yy=sample_grid(80,xrange=[-300,200],yrange=[0,500],ratio=1,angle=0*u.deg)
    print(xx.shape,yy.shape)
    #xx,yy=np.meshgrid(np.arange(256),np.arange(256))
    #pc=ax.hexbin(xx.ravel(),yy.ravel(),im.ravel(),gridsize=(24))
    #value=pc.get_array()
    #pos=pc.get_offsets()
    #print(value.shape,pos.shape)
    ax.scatter(xx,yy)
    
    fig.tight_layout()
    fig.savefig('test_hexbin_map.png') 
    plt.close(fig)     
    
    
if  __name__=="__main__":
    
    
    test_hexbin_map()