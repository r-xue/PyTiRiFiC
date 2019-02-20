import glob
from spectral_cube import SpectralCube
from radio_beam import beam, Beam
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib as mpl
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

from spectral_cube import SpectralCube
from yt.mods import ColorTransferFunction, write_bitmap
import yt
import astropy.units as u
from yt.frontends.fits.misc import PlotWindowWCS
#yt.toggle_interactivity()
from astropy.coordinates import SkyCoord
#from __builtin__ import False

mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
#mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#mpl.rc('font',**{'family':'serif','serif':['Palatino']})
#mpl.rc('text',usetex=True)

import warnings
from spectral_cube.utils import SpectralCubeWarning
warnings.filterwarnings(action='ignore', category=SpectralCubeWarning,append=True)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore")

import aplpy
from pvextractor import Path
from pvextractor import extract_pv_slice
from pvextractor import PathFromCenter

def calc_ppbeam(header):

    beam_area = np.abs(header['BMAJ']*header['BMIN']*3600.**2.0)*2.*np.pi/(8.*np.log(2.))
    pixel_area=np.abs(header['CDELT1']*header['CDELT2']*3600.**2.0)
    ppbeam=beam_area/pixel_area

    return ppbeam


def gmake_plots_spec1d(fn,roi='icrs; circle(356.5393156, 12.8220309, 1")'):
    """
    1D spectrum diagnostic plot
    e.g.:
        gmake_plots_spec1d('./data_bx610.bb1.cube64x64.iter0.image.fits')
    """
    
    header=fits.getheader(fn)
    ppbeam=calc_ppbeam(header)
    
    data=SpectralCube.read(fn,mode='readonly')
    model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
    mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')

    subdata=data.subcube_from_ds9region(roi) 
    subdata_1d=subdata.sum(axis=(1,2))
    data_1d=data.sum(axis=(1,2))
    
    submodel=model.subcube_from_ds9region(roi) 
    submodel_1d=submodel.sum(axis=(1,2))
    model_1d=model.sum(axis=(1,2))    
    
    submod2d=mod2d.subcube_from_ds9region(roi) 
    submod2d_1d=submod2d.sum(axis=(1,2))
    mod2d_1d=mod2d.sum(axis=(1,2))    
    
    freq=(data.spectral_axis/1e9).value
    
    plt.clf()
    hratio=2.0
    fig,(ax,ax_res)=plt.subplots(2,1,sharex=True,figsize=(8,6),
                                 gridspec_kw = {'height_ratios':[hratio, 1.0]})
    
    ax_res.fill_between(freq,0,subdata_1d.array/ppbeam*1e3-submodel_1d.array/ppbeam*1e3,facecolor='green',step='mid',alpha=1.0)

    ax.fill_between(freq,submod2d_1d.array/ppbeam*1e3,subdata_1d.array/ppbeam*1e3,facecolor='red',step='mid',alpha=0.5)
    ax.plot(freq,freq*0.,color='black',alpha=1.0,lw=1.0,ls='--',dashes=(10,10))
    
    ax.plot(freq,subdata_1d.array/ppbeam*1e3,color='black',alpha=1.0,lw=1.0,drawstyle='steps-mid',label='Data')

    ax.plot(freq,submodel_1d.array/ppbeam*1e3,color='blue',alpha=0.5,lw=2.0,label='Model')
    ax.legend(loc="upper right")
    ax.plot(freq,submod2d_1d.array/ppbeam*1e3,color='blue',alpha=0.5,lw=2.0)
    
    start=np.min(freq)
    end=np.max(freq)
    stepsize=0.5
    ax.xaxis.set_ticks(np.arange(np.floor(start*stepsize)/stepsize, np.ceil(end*stepsize)/stepsize, stepsize))
    ax.xaxis.set_major_formatter(plticker.FormatStrFormatter('%0.1f'))
    ax.minorticks_on()
    ax.set_xlim(start,end)
    ylim=ax.get_ylim()

    ax.set_ylabel('Flux [mJy]')
    fn_basename=os.path.basename(fn)
    ax.set_title(fn_basename)
    ax_res.set_xlabel('Freq [GHz]')
    
    dy_res=(ylim[1]-ylim[0])/hratio/2.0
    ax_res.set_ylim(-dy_res,dy_res)
    
    fig.subplots_adjust(left=0.20,bottom=0.15,right=0.95,top=0.95)
    fig.tight_layout()
    
    fig.savefig('gmake_plots_spec1d_'+fn_basename.replace('.fits','')+'.pdf')    

    plt.close()
    
    
def gmake_plots_yt3d(fn,roi='icrs; circle(356.5393156, 12.8220309, 1")'):
    
    ds=yt.load(fn)
    slc = yt.SlicePlot(ds, "z", ["Intensity"], origin="native")
    slc.show()
    PlotWindowWCS(slc)
    
    """
    header=fits.getheader(fn)
    ppbeam=calc_ppbeam(header)
     
    data=SpectralCube.read(fn)
    ytcube=data.to_yt()
    ds = ytcube.dataset
    #ds=yt.load(fn)
     
    n_v = 10
    vmin = 0.05
    vmax = 4.0
    dv = 0.02
     
    transfer = ColorTransferFunction((vmin, vmax))
    transfer.add_layers(n_v, dv, colormap='RdBu_r')
     
    center = ytcube.world2yt([51.424522,
                          30.723611,
                          5205.18071])
    direction = np.array([1.0, 0.0, 0.0])
    width = 100.  # pixels
    size = 1024
 
    sc = yt.create_scene(ds)
    camera = sc.camera(center, direction, width, size, transfer,
                   fields=['flux'])
 
    # Take a snapshot and save to a file
    snapshot = camera.snapshot()
    write_bitmap(snapshot, 'cube_rendering.png', transpose=True)
    """
    
    
def gmake_plots_makeslice(fn):
    
     #path1 = Path([(0., 0.), (62., 62.)],width=10.0)
     #slice1 = extract_pv_slice(array, path1) 
     ra=356.5393156
     dec=12.8220309
     pa=-45
     radec=SkyCoord(ra,dec,unit="deg")
     cube = SpectralCube.read(fn)
     mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')
     mod3d=SpectralCube.read(fn.replace('data_','cmod3d_'),mode='readonly')
     model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
     cube_contsub=cube-mod2d
     
     for i in [1,2]:
         path = PathFromCenter(center=radec,
                            length=2.5 * u.arcsec,
                            angle=(pa+float(i-1)*90.) * u.deg,
                            width=1 * u.arcsec)
         slice = extract_pv_slice(cube, path)
         slice.writeto(fn.replace('data_','data_slice'+str(i)+'_'),overwrite=True)

         slice = extract_pv_slice(cube_contsub, path)
         slice.writeto(fn.replace('data_','data_contsub_slice'+str(i)+'_'),overwrite=True)
         
         slice = extract_pv_slice(mod3d, path)
         slice.writeto(fn.replace('data_','cmod3d_slice'+str(i)+'_'),overwrite=True)
         
         slice = extract_pv_slice(model, path)
         slice.writeto(fn.replace('data_','cmodel_slice'+str(i)+'_'),overwrite=True)         
         

def gmake_plots_slice(fn,i=1):
    """
        data model res
        contsub version
    """


    fn_basename=os.path.basename(fn)
    header=fits.getheader(fn.replace('data_','data_slice'+str(i)+'_'))
    
    data3d=fits.getdata(fn.replace('data_','cmod3d_slice'+str(i)+'_'))
    if  data3d.sum()==0:
        isline=False
    else:
        isline=True
        
    if  isline==True:
        nx=3
        ny=2
        figsize=(15,10)
    else:
        nx=3
        ny=1
        figsize=(15,5)        
    fig=plt.figure(figsize=figsize) 
    
    #w=WCS(header).celestial
    ax1 = fig.add_subplot(ny,nx,1)
    data1,header=fits.getdata(fn.replace('data_','data_slice'+str(i)+'_'),header=True,memmap=False) 
    ax1.imshow(data1,origin='lower', interpolation='nearest',
               vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
    ax1.set_title(fn_basename)
    if  i==1:
        tx='Major'
    if  i==2:
        tx='Minor'
    ax1.set_xlabel('Position [pix] ('+tx+')')
    ax1.set_ylabel('Freq. [min]')
    
    ax2 = fig.add_subplot(ny,nx,2)
    data2,header=fits.getdata(fn.replace('data_','cmodel_slice'+str(i)+'_'),header=True,memmap=False) 
    ax2.imshow(data2,origin='lower', interpolation='nearest',
               vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
    ax2.set_title('Model')
    
    ax3 = fig.add_subplot(ny,nx,3)
    ax3.imshow(data1-data2, origin='lower', interpolation='nearest',
               vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
    ax3.set_title('Residual')
    
    if  isline==True:
        ax4 = fig.add_subplot(ny,nx,4)
        data4,header=fits.getdata(fn.replace('data_','data_contsub_slice'+str(i)+'_'),header=True,memmap=False) 
        ax4.imshow(data4,origin='lower', interpolation='nearest',
                   vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
        ax4.set_title('Data/Line')
        
        ax5 = fig.add_subplot(ny,nx,5)
        data5,header=fits.getdata(fn.replace('data_','cmod3d_slice'+str(i)+'_'),header=True,memmap=False) 
        ax5.imshow(data5,origin='lower', interpolation='nearest',
                   vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
        ax5.set_title('Model/Line')
        
        ax6 = fig.add_subplot(ny,nx,6)
        ax6.imshow(data1-data2, origin='lower', interpolation='nearest',
                   vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)          
        ax6.set_title('Residual')
        
    out_basename=os.path.basename(fn.replace('data_','data_slice'+str(i)+'_'))
    fig.subplots_adjust(left=0.10,bottom=0.10,right=0.95,top=0.95)
    fig.savefig('gmake_plots_slice_'+out_basename.replace('.fits','')+'.pdf')   
    plt.close() 

    
def gmake_plots_mom0xy(fn,roi='icrs; circle(356.5393156, 12.8220309, 1")'):

    header=fits.getheader(fn)
    ppbeam=calc_ppbeam(header)
    
    data=SpectralCube.read(fn,mode='readonly')
    model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
    mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')
    mod3d=SpectralCube.read(fn.replace('data_','cmod3d_'),mode='readonly')
    if  (mod3d.sum()).value==0.0:
        isline=False
    else:
        isline=True

    ker3d=SpectralCube.read(fn.replace('data_','kernel_'),mode='readonly')
    
    subdata=data.subcube_from_ds9region(roi) 

    
    data_m0=data.moment(order=0)
    #data_m0.write('data_mom0.fits',overwrite=True)  
    
    model_m0=model.moment(order=0)
    mod2d_m0=mod2d.moment(order=0)
    if  isline==True:
        mod3d_m0=mod3d.moment(order=0)
    ker3d_m0=ker3d.moment(order=0)
    #model_m0.write('model_mom0.fits',overwrite=True)
    
#     fig = plt.figure(figsize=(14, 7))
#     
#     f1 = aplpy.FITSFigure(model_m0.array,hdu=model_m0.hdu, figure=fig,
#                           subplot=[0.13, 0.1, 0.35, 0.7])
#     
#     f1.tick_labels.set_font(size='x-small')
#     f1.axis_labels.set_font(size='small')
#     f1.show_grayscale()
#     
#     f2 = aplpy.FITSFigure('model_mom0.fits', figure=fig,
#                           subplot=[0.5, 0.1, 0.35, 0.7])
#     
#     f2.tick_labels.set_font(size='x-small')
#     f2.axis_labels.set_font(size='small')
#     f2.show_grayscale()
#     
#     f2.axis_labels.hide_y()
#     f2.tick_labels.hide_y()
#     
#     fig.savefig('subplots.png', bbox_inches='tight')    
    
    #"""
    #log_model=np.log(model)
    plt.clf()
    if  isline==True:
        figsize=(16,8)
        nx=4
        ny=2
    else:
        figsize=(16,4)
        nx=4
        ny=1
        
    fig=plt.figure(figsize=figsize)
    
    tmp=data_m0.array
    dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
    vmin=np.min(tmp)
    vmax=np.max(tmp)
    #print(vmin,vmax)
    
    w=WCS(header).celestial
    ax1 = fig.add_subplot(ny,nx,1, projection=w)
    ax1.imshow(tmp, origin='lower', interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax1.coords['ra'].set_axislabel('Right Ascension')
    ax1.coords['dec'].set_axislabel('Declination')
    cs1=ax1.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    #print(header['BMAJ'], header['BMIN'],header['BPA'])
    
    wx,wy=w.wcs_pix2world(header['NAXIS1']/8.0,header['NAXIS2']/8.0,0)
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax1.get_transform('icrs'))
    ax1.add_patch(bshape)
    fn_basename=os.path.basename(fn)
    ax1.set_title(fn_basename)
    
    tmp=model_m0.array
    ax2 = fig.add_subplot(ny,nx,2, projection=w)
    ax2.imshow(tmp, origin='lower', interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax2.coords['dec'].set_ticklabel_visible(False)
    ax2.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    ax2.set_title('Model')
    
    
    tmp=data_m0.array-model_m0.array
    ax3 = fig.add_subplot(ny,nx,3, projection=w)
    ax3.imshow(tmp, origin='lower', interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax3.coords['dec'].set_ticklabel_visible(False)
    ax3.contour(tmp,levels=dlevels,colors='white', alpha=0.5)    
    ax3.set_title('Residual')

    tmp_psf=ker3d_m0.array
    dlevels_psf=np.linspace(np.min(tmp_psf),np.max(tmp_psf),12)
    vmin_psf=np.min(tmp_psf)
    vmax_psf=np.max(tmp_psf)
    ax3 = fig.add_subplot(ny,nx,4, projection=w)
    ax3.imshow(tmp_psf, origin='lower', interpolation='nearest',
           vmin=vmin_psf, vmax=vmax_psf)
    ax3.coords['dec'].set_ticklabel_visible(False)
    ax3.contour(tmp_psf,levels=dlevels_psf,colors='white', alpha=0.5)                  
    ax3.set_title('Kernel')

    tmp=data_m0.array-mod2d_m0.array
    dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
    vmin=np.min(tmp)
    vmax=np.max(tmp)
    
    if  isline==True:
        
        ax4 = fig.add_subplot(ny,nx,5, projection=w)
        ax4.imshow(tmp, origin='lower', interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax4.coords['dec'].set_ticklabel_visible(False)
        ax4.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax4.set_title('Data/Line')
        
        tmp=model_m0.array-mod2d_m0.array
        ax5 = fig.add_subplot(ny,nx,6, projection=w)
        ax5.imshow(tmp, origin='lower', interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax5.coords['dec'].set_ticklabel_visible(False)
        ax5.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax5.set_title('Model/Line')
        
        tmp=data_m0.array-mod2d_m0.array-(model_m0.array-mod2d_m0.array)
        ax6 = fig.add_subplot(ny,nx,7, projection=w)
        ax6.imshow(tmp, origin='lower', interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax6.coords['dec'].set_ticklabel_visible(False)
        ax6.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax6.set_title('Residual')



    #fig,ax=plt.subplots(1,1,sharex=True,figsize=(8,8))
     

    #ax.projection=wcs
    #cbar = fig.colorbar(cs1,ax=(ax1,ax2,ax3),orientation='vertical',fraction=.1)
    #cbar.set_label('Log Brightness', rotation=270, labelpad=25)
    #cbar.set_ticks([vmin,vmax])
    
    #fig.tight_layout()
    fig.subplots_adjust(left=0.10,bottom=0.10,right=0.98,top=0.95)
    fig.savefig('gmake_plots_mom0_'+fn_basename.replace('.fits','')+'.pdf')   
    plt.close()
#     #"""
#     
#     f = aplpy.FITSFigure(m0.hdu)  
#     f.show_colorscale()
#     f.save('moment_0.png')

if  __name__=="__main__":
    
    """
    gmake_plots_spec1d('./data_bx610.bb1.cube64x64.iter0.image.fits')
    gmake_plots_spec1d('./data_bx610.bb2.cube64x64.iter0.image.fits')
    gmake_plots_spec1d('./data_bx610.bb3.cube64x64.iter0.image.fits')
    gmake_plots_spec1d('./data_bx610.bb4.cube64x64.iter0.image.fits')
    """
    
    """
    gmake_plots_mom0xy('./data_bx610.bb1.cube64x64.iter0.image.fits')
    gmake_plots_mom0xy('./data_bx610.bb2.cube64x64.iter0.image.fits')
    gmake_plots_mom0xy('./data_bx610.bb3.cube64x64.iter0.image.fits')
    gmake_plots_mom0xy('./data_bx610.bb4.cube64x64.iter0.image.fits')
    """
    
    #gmake_plots_makeslice('./data_bx610.bb1.cube64x64.iter0.image.fits')
    #gmake_plots_makeslice('./data_bx610.bb2.cube64x64.iter0.image.fits')
    #gmake_plots_makeslice('./data_bx610.bb3.cube64x64.iter0.image.fits')
    #gmake_plots_makeslice('./data_bx610.bb4.cube64x64.iter0.image.fits')
    
    gmake_plots_slice('./data_bx610.bb1.cube64x64.iter0.image.fits',i=1)
    gmake_plots_slice('./data_bx610.bb1.cube64x64.iter0.image.fits',i=2)
    
    gmake_plots_slice('./data_bx610.bb2.cube64x64.iter0.image.fits',i=1)
    gmake_plots_slice('./data_bx610.bb2.cube64x64.iter0.image.fits',i=2)
    
    gmake_plots_slice('./data_bx610.bb3.cube64x64.iter0.image.fits',i=1)
    gmake_plots_slice('./data_bx610.bb3.cube64x64.iter0.image.fits',i=2)
    
    gmake_plots_slice('./data_bx610.bb4.cube64x64.iter0.image.fits',i=1)
    gmake_plots_slice('./data_bx610.bb4.cube64x64.iter0.image.fits',i=2)        

    
