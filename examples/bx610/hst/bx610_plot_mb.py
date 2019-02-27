import glob
from spectral_cube import SpectralCube
from radio_beam import beam, Beam
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib as mpl
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table
from astropy.table import Column
import scipy.integrate

from spectral_cube import SpectralCube
from yt.mods import ColorTransferFunction, write_bitmap
import yt
import astropy.units as u
from yt.frontends.fits.misc import PlotWindowWCS
#yt.toggle_interactivity()
from astropy.coordinates import SkyCoord
import copy
#from __builtin__ import False

execfile('/Users/Rui/Dropbox/Worklib/projects/xlibpy/xlib/astro.py')

mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"


ra=356.5393232281125
dec=12.822016207663106

pa=-30
inc=30
inc=45
inc=60


flist=['stack_f814w_drc_sci_cutout.fits',
       'stack_f438w_drc_sci_cutout.fits',
       'stack_f110w_drz_sci_cutout.fits',
       'stack_f140w_drz_sci_cutout.fits',
       'stack_f160w_drz_sci_cutout.fits',
       'test_cube_submean_mom0.fits']
fname=['F814W','F438W','F110W','F140W','F160W','BB2/Line']

data,header=fits.getdata(flist[0],header=True)       
fig=plt.figure(figsize=(24,14))
ax=fig.add_subplot(3,5,1, projection=WCS(header))
cx,cy=WCS(header).celestial.wcs_world2pix(ra,dec,0)
if  inc!=0:
    data=gal_flat(data,-20.,inc,cen=(cx,cy),interp=True)

ax.imshow(data, interpolation='nearest',
           vmin=np.nanmin(data), vmax=np.nanmax(data))
dlevels=np.linspace(np.nanmin(data),np.nanmax(data),7)           
cs=ax.contour(data,levels=dlevels,colors='white', alpha=0.5)
#ax.coords.grid(color='white', ls='solid')
ax.coords[0].set_axislabel('Right Ascension (J2000)')
ax.coords[1].set_axislabel('Declination (J2000)')

ax.coords[0].set_major_formatter('hh:mm:ss.s')
ax.coords[1].set_major_formatter('dd:mm:ss')
    
xlim=ax.get_xlim()
ylim=ax.get_ylim()
xlim=(xlim[0]+25,xlim[1]-30)
ylim=(ylim[0]+27,ylim[1]-28)
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_title(fname[0]+' dp='+str(inc)+'deg'+' pa='+str(pa)+'deg')

w=WCS(header).celestial
wxlim,wylim=w.wcs_pix2world(xlim,ylim,0)

circ = mpl.patches.Circle((ra, dec), 0.5/60./60.,edgecolor='cyan', facecolor='none',
          transform=ax.get_transform('icrs'))
ax.add_patch(circ)

bshape=mpl.patches.Ellipse((ra,dec), 0.01/60/60, 2.0/60/60, angle=-pa, 
                           edgecolor='cyan', facecolor='cyan',
                           transform=ax.get_transform('icrs'))
ax.add_patch(bshape)

for i in range(1,5):

    data1,header1=fits.getdata(flist[i],header=True)
    ax1=fig.add_subplot(3,5,i+1, projection=WCS(header1))
    cx,cy=WCS(header1).celestial.wcs_world2pix(ra,dec,0)
    if  inc!=0:
        data1=gal_flat(data1,-20.,inc,cen=(cx,cy),interp=True)    
    ax1.imshow(data1, interpolation='nearest',
               vmin=np.nanmin(data1), vmax=np.nanmax(data1))
    dlevels=np.linspace(np.nanmin(data1),np.nanmax(data1),7)           
    cs=ax1.contour(data1,levels=dlevels,colors='white', alpha=0.5)    
    #ax1.coords.grid(color='white', ls='solid')
    ax1.coords[0].set_axislabel('Right Ascension (J2000)')
    ax1.coords[1].set_axislabel('Declination (J2000)')
    ax1.coords[0].set_major_formatter('hh:mm:ss.s')
    ax1.coords[1].set_major_formatter('dd:mm:ss')    
    
    w1=WCS(header1).celestial
    xlim1,ylim1=w1.wcs_world2pix(wxlim,wylim,0)
    ax1.set_xlim(xlim1)
    ax1.set_ylim(ylim1)
    ax1.set_title(fname[i]+' dp='+str(inc)+'deg'+' pa='+str(pa)+'deg')
    ax_last=ax
    dlevels_last=dlevels
    data1_last=data1
    
    circ = mpl.patches.Circle((ra, dec), 0.5/60./60.,edgecolor='cyan', facecolor='none',
              transform=ax1.get_transform('icrs'))
    ax1.add_patch(circ)
    
    bshape=mpl.patches.Ellipse((ra,dec), 0.01/60/60, 2.0/60/60, angle=-pa, 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax1.get_transform('icrs'))
    ax1.add_patch(bshape)
    
    bshape=mpl.patches.Ellipse((ra,dec), 1.0/3600.0, 1.0/3600./np.cos(np.deg2rad(inc)), angle=-pa+90., 
                           edgecolor='yellow', facecolor='none',
                           transform=ax1.get_transform('icrs'))
    ax1.add_patch(bshape)      

flist=['bb2_line_co76_mom0.fits',
       'bb2_line_ci21_mom0.fits',
       'bb3_line_h2o_mom0.fits',
       'test_cube_submean_mom0.fits']
fname=['co76','ci21','h2o']

for i in range(3):

    data1,header1=fits.getdata(flist[i],header=True)
    ax1=fig.add_subplot(3,5,i+6, projection=WCS(header1).celestial)
    
    cx,cy=WCS(header1).celestial.wcs_world2pix(ra,dec,0)
    if  inc!=0:
        data1=gal_flat(data1,-20.,inc,cen=(cx,cy),interp=True)
    ax1.imshow(data1, interpolation='nearest',
               vmin=np.nanmin(data1), vmax=np.nanmax(data1))
    dlevels1=np.linspace(np.nanmin(data1),np.nanmax(data1),7)           
    cs=ax1.contour(data1,levels=dlevels1,colors='white', alpha=0.5)
    #cs=ax_last.contour(data1_last,levels=dlevels_last,colors='yellow', alpha=0.5)    
    #ax1.coords.grid(color='white', ls='solid')


    circ = mpl.patches.Circle((ra, dec), 0.5/60./60.,edgecolor='cyan', facecolor='none',
              transform=ax1.get_transform('icrs'))
    ax1.add_patch(circ)
    
    bshape=mpl.patches.Ellipse((ra,dec), 0.01/60/60, 2.0/60/60, angle=-pa, 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax1.get_transform('icrs'))
    ax1.add_patch(bshape)    
    
    bshape=mpl.patches.Ellipse((ra,dec), 1.0/3600.0, 1.0/3600./np.cos(np.deg2rad(inc)), angle=-pa+90., 
                           edgecolor='yellow', facecolor='none',
                           transform=ax1.get_transform('icrs'))
    ax1.add_patch(bshape)    
    
    ax1.coords[0].set_axislabel('Right Ascension (J2000)')
    ax1.coords[1].set_axislabel('Declination (J2000)')
    ax1.coords[0].set_major_formatter('hh:mm:ss.s')
    ax1.coords[1].set_major_formatter('dd:mm:ss')    
    
    w1=WCS(header1).celestial
    xlim1,ylim1=w1.wcs_world2pix(wxlim,wylim,0)
    ax1.set_xlim(xlim1)
    ax1.set_ylim(ylim1)
    ax1.set_title(fname[i]+' dp='+str(inc)+'deg'+' pa='+str(pa)+'deg')
    

flist=['../bx610.bb3.mfs64x64.itern.image.fits',
       '../bx610.bb4.mfs64x64.itern.image.fits',
       '../bx610.bb1.mfs64x64.itern.image.fits',
       '../bx610.bb2.mfs64x64.itern.image.fits']
fname=['BB3','BB4','BB1','BB2']

for i in range(4):

    data1,header1=fits.getdata(flist[i],header=True)
    data1=data1[0,0,:,:]
    ax1=fig.add_subplot(3,5,i+6+5, projection=WCS(header1).celestial)
    cx,cy=WCS(header1).celestial.wcs_world2pix(ra,dec,0)
    if  inc!=0:
        data1=gal_flat(data1,-20.,inc,cen=(cx,cy),interp=True)    
    
    ax1.imshow(data1, interpolation='nearest',
               vmin=np.nanmin(data1), vmax=np.nanmax(data1))
    dlevels1=np.linspace(np.nanmin(data1),np.nanmax(data1),7)           
    cs=ax1.contour(data1,levels=dlevels1,colors='white', alpha=0.5)
    #cs=ax_last.contour(data1_last,levels=dlevels_last,colors='yellow', alpha=0.5)    
    #ax1.coords.grid(color='white', ls='solid')


    circ = mpl.patches.Circle((ra, dec), 0.5/60./60.,edgecolor='cyan', facecolor='none',
              transform=ax1.get_transform('icrs'))
    ax1.add_patch(circ)
    
    bshape=mpl.patches.Ellipse((ra,dec), 0.01/60/60, 2.0/60/60, angle=-pa, 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax1.get_transform('icrs'))
    ax1.add_patch(bshape)

    bshape=mpl.patches.Ellipse((ra,dec), 1.0/3600.0, 1.0/3600./np.cos(np.deg2rad(inc)), angle=-pa+90., 
                               edgecolor='yellow', facecolor='none',
                               transform=ax1.get_transform('icrs'))
    ax1.add_patch(bshape)    
    
    ax1.coords[0].set_axislabel('Right Ascension (J2000)')
    ax1.coords[1].set_axislabel('Declination (J2000)')
    ax1.coords[0].set_major_formatter('hh:mm:ss.s')
    ax1.coords[1].set_major_formatter('dd:mm:ss')    
    
    w1=WCS(header1).celestial
    xlim1,ylim1=w1.wcs_world2pix(wxlim,wylim,0)
    ax1.set_xlim(xlim1)
    ax1.set_ylim(ylim1)
    ax1.set_title(fname[i]+' dp='+str(inc)+'deg'+' pa='+str(pa)+'deg')
    
    

fig.subplots_adjust(left=0.08,bottom=0.08,right=0.97,top=0.97)
#fig.tight_layout()

addname=''
if  inc!=0:
    addname='_inc'+str(inc)
fig.savefig('bx610_plot_mb'+addname+'.pdf')
plt.close()

#     #"""