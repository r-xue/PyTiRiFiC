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

mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"

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


def gmake_plots_spec1d(fn,roi='icrs; circle(356.53932576899575,12.822017913507711 , 1") # text={example}'):
    """
    1D spectrum diagnostic plot
    e.g.:
        gmake_plots_spec1d('./data_bx610.bb1.cube64x64.iter0.image.fits')
    """
    
    header=fits.getheader(fn)
    ppbeam=calc_ppbeam(header)
    
    data=SpectralCube.read(fn,mode='readonly')
    model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
    imodel=SpectralCube.read(fn.replace('data_','imodel_'),mode='readonly')
    mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')

    subdata=data.subcube_from_ds9region(roi) 
    subdata_1d=subdata.sum(axis=(1,2))
    data_1d=data.sum(axis=(1,2))
    
    submodel=model.subcube_from_ds9region(roi) 
    submodel_1d=submodel.sum(axis=(1,2))
    model_1d=model.sum(axis=(1,2))
    
    subimodel=imodel.subcube_from_ds9region(roi) 
    subimodel_1d=subimodel.sum(axis=(1,2))
    imodel_1d=imodel.sum(axis=(1,2))            
    
    submod2d=mod2d.subcube_from_ds9region(roi) 
    submod2d_1d=submod2d.sum(axis=(1,2))
    mod2d_1d=mod2d.sum(axis=(1,2))    
    
    freq=(data.spectral_axis/1e9).value
    
    plt.clf()
    hratio=2.00
    fig,(ax,ax_res)=plt.subplots(2,1,sharex=True,figsize=(12,8),
                                 gridspec_kw = {'height_ratios':[hratio, 1.0]})
    
    ax_res.fill_between(freq,0,subdata_1d.array/ppbeam*1e3-submodel_1d.array/ppbeam*1e3,facecolor='green',step='mid',alpha=1.0)
    ax_res.plot(freq,freq*0.,color='black',alpha=1.0,lw=1.0,ls='--',dashes=(10,10))
    ax_res.plot(freq,subdata_1d.array/ppbeam*1e3-submodel_1d.array/ppbeam*1e3,color='black',alpha=2.0,lw=1.0,drawstyle='steps-mid',label='Residual')
    
    res_mean=np.mean(subdata_1d.array/ppbeam*1e3-submodel_1d.array/ppbeam*1e3)

    ax_res.plot(freq,freq*0.+res_mean,color='blue',alpha=0.5,lw=1.0,label='Residual-Mean')
    ax_res.legend(loc="upper right")
    

    ax.fill_between(freq,submod2d_1d.array/ppbeam*1e3,subdata_1d.array/ppbeam*1e3,facecolor='red',step='mid',alpha=0.5)
    ax.plot(freq,freq*0.,color='black',alpha=1.0,lw=1.0,ls='--',dashes=(10,10))
    
    ax.plot(freq,subdata_1d.array/ppbeam*1e3,color='black',alpha=2.0,lw=1.0,drawstyle='steps-mid',label='Data')
    

    # note: only in clean map these two will match as ppbeam was calculated from a Gaussian kernel
    ax.plot(freq,submodel_1d.array/ppbeam*1e3,color='blue',alpha=0.5,lw=2.0,label='Model')
    ax.plot(freq,subimodel_1d.array*1e3,color='cyan',alpha=0.5,lw=2.0,label='iModel')

    
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
    ax.set_title(fn_basename+'\n'+roi.replace('icrs','').replace(';',''))
    ax_res.set_xlabel('Freq [GHz]')
    
    dy_res=(ylim[1]-ylim[0])/hratio/2.0
    ax_res.set_ylim(-dy_res,dy_res)
    
    fig.subplots_adjust(left=0.20,bottom=0.15,right=0.95,top=0.95)
    fig.tight_layout()
    
    vname=''
    if  'text={' in roi:
        vname='_'+(roi.split("text={"))[1].replace("}",'')
    odir='gmake_plots_spec1d'
    if not os.path.exists(odir):
        os.makedirs(odir)        
    fig.savefig(odir+'/'+fn_basename.replace('.fits','')+vname+'.pdf')    

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
    
    
def gmake_plots_makeslice(fn,width=1.0,length=2.5,pa=-45):
    
     #path1 = Path([(0., 0.), (62., 62.)],width=10.0)
     #slice1 = extract_pv_slice(array, path1) 
     
     radec=[356.53932576899575,12.822017913507711]

     pa=-45
     
     radec=SkyCoord(radec[0],radec[1],unit="deg",frame='icrs')
     cube = SpectralCube.read(fn)
     mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')
     mod3d=SpectralCube.read(fn.replace('data_','cmod3d_'),mode='readonly')
     model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
     imodel=SpectralCube.read(fn.replace('data_','imodel_'),mode='readonly')
     imod3d=SpectralCube.read(fn.replace('data_','imod3d_'),mode='readonly')
     cube_contsub=cube-mod2d
     
     for i in [1,2]:
         path = PathFromCenter(center=radec,
                            length=length*u.arcsec,
                            angle=(pa+float(i-1)*90.) * u.deg,
                            width=width*u.arcsec)
         slice = extract_pv_slice(cube, path)
         slice.writeto(fn.replace('data_','data_slice'+str(i)+'_'),overwrite=True)

         slice = extract_pv_slice(cube_contsub, path)
         slice.writeto(fn.replace('data_','data_contsub_slice'+str(i)+'_'),overwrite=True)
         
         slice = extract_pv_slice(mod3d, path)
         slice.writeto(fn.replace('data_','cmod3d_slice'+str(i)+'_'),overwrite=True)
         
         slice = extract_pv_slice(model, path)
         slice.writeto(fn.replace('data_','cmodel_slice'+str(i)+'_'),overwrite=True)         

         slice = extract_pv_slice(imodel, path)
         slice.writeto(fn.replace('data_','imodel_slice'+str(i)+'_'),overwrite=True)
         
         slice = extract_pv_slice(imod3d, path)
         slice.writeto(fn.replace('data_','imod3d_slice'+str(i)+'_'),overwrite=True)                   

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
        nx=4
        ny=2
        figsize=(20,10)
    else:
        nx=4
        ny=1
        figsize=(20,5)        
    fig=plt.figure(figsize=figsize) 
    
    #w=WCS(header).celestial
    ax1 = fig.add_subplot(ny,nx,1)
    data1,header=fits.getdata(fn.replace('data_','data_slice'+str(i)+'_'),header=True,memmap=False) 
    ax1.imshow(data1, interpolation='nearest',
               vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
    ax1.set_title(fn_basename)
    if  i==1:
        tx='Major'
    if  i==2:
        tx='Minor'
    ax1.set_xlabel('Position [pix] ('+tx+')')
    ax1.set_ylabel('Freq. [pix]')
    
    ax2 = fig.add_subplot(ny,nx,2)
    data2,header=fits.getdata(fn.replace('data_','cmodel_slice'+str(i)+'_'),header=True,memmap=False) 
    ax2.imshow(data2, interpolation='nearest',
               vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
    ax2.set_title('Model')
    
    ax3 = fig.add_subplot(ny,nx,3)
    ax3.imshow(data1-data2, interpolation='nearest',
               vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
    ax3.set_title('Residual')
    
    ax4 = fig.add_subplot(ny,nx,4)
    data4,header=fits.getdata(fn.replace('data_','imodel_slice'+str(i)+'_'),header=True,memmap=False) 
    ax4.imshow(data4, interpolation='nearest',
               vmin=np.min(data4), vmax=np.max(data4),aspect=0.25)
    ax4.set_title('Model')
    
    if  isline==True:
        ax5 = fig.add_subplot(ny,nx,5)
        data5,header=fits.getdata(fn.replace('data_','data_contsub_slice'+str(i)+'_'),header=True,memmap=False) 
        ax5.imshow(data5, interpolation='nearest',
                   vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
        ax5.set_title('Data/Line')
        
        ax6 = fig.add_subplot(ny,nx,6)
        data6,header=fits.getdata(fn.replace('data_','cmod3d_slice'+str(i)+'_'),header=True,memmap=False) 
        ax6.imshow(data6, interpolation='nearest',
                   vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)
        ax6.set_title('Model/Line')
        
        ax7 = fig.add_subplot(ny,nx,7)
        ax7.imshow(data1-data2, interpolation='nearest',
                   vmin=np.min(data1), vmax=np.max(data1),aspect=0.25)          
        ax7.set_title('Residual')
        
        ax8 = fig.add_subplot(ny,nx,8)
        data8,header=fits.getdata(fn.replace('data_','imod3d_slice'+str(i)+'_'),header=True,memmap=False) 
        ax8.imshow(data8, interpolation='nearest',
                   vmin=np.min(data8), vmax=np.max(data8),aspect=0.25)
        ax8.set_title('Model/Line')        
        
    out_basename=os.path.basename(fn.replace('data_','data_slice'+str(i)+'_'))
    fig.subplots_adjust(left=0.07,bottom=0.07,right=0.95,top=0.95)

    odir='gmake_plots_slice'
    if not os.path.exists(odir):
        os.makedirs(odir)          
    fig.savefig(odir+'/'+out_basename.replace('.fits','')+'.pdf')   
    plt.close() 

    
def gmake_plots_mom0xy(fn):

    header=fits.getheader(fn)
    ppbeam=calc_ppbeam(header)
    
    data=SpectralCube.read(fn,mode='readonly')
    model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
    mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')
    mod3d=SpectralCube.read(fn.replace('data_','cmod3d_'),mode='readonly')
    imodel=SpectralCube.read(fn.replace('data_','imodel_'),mode='readonly')
    imod3d=SpectralCube.read(fn.replace('data_','imod3d_'),mode='readonly')
    
    if  (mod3d.sum()).value==0.0:
        isline=False
    else:
        isline=True

    ker3d=SpectralCube.read(fn.replace('data_','kernel_'),mode='readonly')
    

    
    data_m0=data.moment(order=0)
    #data_m0.write('data_mom0.fits',overwrite=True)  
    
    model_m0=model.moment(order=0)
    imodel_m0=imodel.moment(order=0)
    mod2d_m0=mod2d.moment(order=0)
    if  isline==True:
        mod3d_m0=mod3d.moment(order=0)
        imod3d_m0=imod3d.moment(order=0)
    ker3d_m0=ker3d.moment(order=0)
    ker3d_m0=ker3d[0,:,:]

    plt.clf()
    if  isline==True:
        figsize=(20,8)
        nx=5
        ny=2
    else:
        figsize=(20,4)
        nx=5
        ny=1
        
    fig=plt.figure(figsize=figsize)
    
    tmp=data_m0.array
    dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
    vmin=np.min(tmp)
    vmax=np.max(tmp)
    #print(vmin,vmax)
    
    w=WCS(header).celestial
    ax1 = fig.add_subplot(ny,nx,1, projection=w)
    ax1.imshow(tmp, interpolation='nearest',
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
    ax2.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax2.coords['dec'].set_ticklabel_visible(False)
    ax2.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax2.get_transform('icrs'))    
    ax2.add_patch(bshape)
    ax2.set_title('Model')
    
    
    tmp=data_m0.array-model_m0.array
    ax3 = fig.add_subplot(ny,nx,3, projection=w)
    ax3.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax3.coords['dec'].set_ticklabel_visible(False)
    ax3.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax3.get_transform('icrs'))            
    ax3.add_patch(bshape)
    ax3.set_title('Residual')

    tmp_psf=ker3d_m0.array
    dlevels_psf=np.linspace(np.min(tmp_psf),np.max(tmp_psf),12)
    vmin_psf=np.min(tmp_psf)
    vmax_psf=np.max(tmp_psf)
    ax4 = fig.add_subplot(ny,nx,4, projection=w)
    ax4.imshow(tmp_psf, interpolation='nearest',
           vmin=vmin_psf, vmax=vmax_psf)
    ax4.coords['dec'].set_ticklabel_visible(False)
    ax4.contour(tmp_psf,levels=dlevels_psf,colors='white', alpha=0.5)
    ax4.contour(tmp_psf,levels=[0.5],colors='yellow', alpha=0.5)
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax4.get_transform('icrs'))                          
    ax4.add_patch(bshape)
    ax4.set_title('Kernel')
    
    tmp=imodel_m0.array
    dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
    vmin=np.min(tmp)
    vmax=np.max(tmp)
    ax5 = fig.add_subplot(ny,nx,5, projection=w)
    ax5.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax5.coords['dec'].set_ticklabel_visible(False)
    ax5.contour(tmp,levels=dlevels,colors='white', alpha=0.5,origin='image')
    ax5.contour(tmp,levels=[np.max(tmp)*0.1,np.max(tmp)*0.5],colors='yellow', alpha=0.5,origin='image')
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax5.get_transform('icrs'))                          
    ax5.add_patch(bshape)
    ax5.set_title('iModel')    

    tmp=data_m0.array-mod2d_m0.array
    dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
    vmin=np.min(tmp)
    vmax=np.max(tmp)
    
    if  isline==True:
        
        ax4 = fig.add_subplot(ny,nx,6, projection=w)
        ax4.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax4.coords['dec'].set_ticklabel_visible(False)
        ax4.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax4.set_title('Data/Line')
        
        tmp=model_m0.array-mod2d_m0.array
        ax5 = fig.add_subplot(ny,nx,7, projection=w)
        ax5.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax5.coords['dec'].set_ticklabel_visible(False)
        ax5.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax5.set_title('Model/Line')
        
        tmp=data_m0.array-mod2d_m0.array-(model_m0.array-mod2d_m0.array)
        ax6 = fig.add_subplot(ny,nx,8, projection=w)
        ax6.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax6.coords['dec'].set_ticklabel_visible(False)
        ax6.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax6.set_title('Residual')
        
        tmp=imod3d_m0.array
        dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
        ax10 = fig.add_subplot(ny,nx,10, projection=w)
        ax10.imshow(tmp, interpolation='nearest',
               vmin=np.min(tmp), vmax=np.max(tmp))
        ax10.coords['dec'].set_ticklabel_visible(False)
        ax10.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax10.contour(tmp,levels=[np.max(tmp)*0.1,np.max(tmp)*0.5],colors='yellow', alpha=0.5)
        ax10.set_title('Model/Line')    

    #fig.tight_layout()
    
    
    fig.subplots_adjust(left=0.07,bottom=0.07,right=0.98,top=0.95)
    
    odir='gmake_plots_mom0xy'
    if not os.path.exists(odir):
        os.makedirs(odir)        
    fig.savefig(odir+'/'+fn_basename.replace('.fits','')+'.pdf')   
    plt.close()
#     #"""
#     
#     f = aplpy.FITSFigure(m0.hdu)  
#     f.show_colorscale()
#     f.save('moment_0.png')


def gmake_plots_radprof(fn):

    wd=fn.replace('data','imod3d_prof*')

    flist=glob.glob(wd)
    
    fig=plt.figure(figsize=(8.,4.*len(flist))) 
    
    cc=0
    for fn0 in flist:
        print(fn0)
        cc=cc+1
        ax = fig.add_subplot(len(flist),1,cc)
        
        t=Table.read(fn0)
        ax.plot(t['sbrad'].data[0],t['sbprof'].data[0],color='black')
        ymin,ymax=ax.get_ylim()
        
        cog=scipy.integrate.cumtrapz(t['sbprof'].data[0]*2.*np.pi*t['sbrad'].data[0],t['sbrad'].data[0],initial=0.)
        cog /= np.max(cog) 
        ax.plot(t['sbrad'].data[0],cog*ymax,linestyle='--',color='black')
        
        ax.set_xlim(np.min(t['sbrad'].data[0]),np.max(t['sbrad'].data[0]))
        
        ax.set_title(os.path.basename(fn0))
        ax.set_ylabel('SB')
        if  cc==len(flist):
            ax.set_xlabel('Radius [arcsec]')
        
        ax1 = ax.twinx()
        x1=t['velrad'].data[0]
        y1=t['velprof'].data[0]
        ax1.plot(x1,y1,color='blue')
        ax1.plot(t['velrad_node'].data[0],t['velprof_node'].data[0],marker='o',linestyle='none',color='blue',mfc='none')
        y1=t['gassigma'].data[0]
        ax1.plot(x1,y1,color='red')
        ax1.plot(t['velrad_node'].data[0],t['gassigma_node'].data[0],marker='o',linestyle='none',color='red',mfc='none')
        ax1.set_ylabel('Vrot/Vdis [km/s]')
        
    odir='gmake_plots_radprof'
    if not os.path.exists(odir):
        os.makedirs(odir)   
        
    fig.savefig(odir+'/'+os.path.basename(fn).replace('.fits','')+'.pdf') 

if  __name__=="__main__":
    
    #"""
    cen1='icrs; circle(356.53932576899575,12.822017913507711,1.00") # text={cen1}'
    cen2='icrs; circle(356.53932576899575,12.822017913507711,0.05") # text={cen2}'
    slice1='icrs; box(356.53932576899575,12.822017913507711,0.20",0.75",135) # text={slice1}'
    slice2='icrs; box(356.53932576899575,12.822017913507711,0.20",0.75",45)  # text={slice2}'
    rois=[cen1,cen2,slice1,slice2]
    
    bbs=['bb1','bb2','bb3','bb4']
    bbs=['bb2']

    fn_name_tmp='./data_bx610.bbx.cube64x64.iterx.image.fits'
    
    for bb in bbs:
        fn_name=fn_name_tmp.replace('bbx',bb).replace('iterx','iter0')
        
        """
        for roi in rois:
            print('plots_spec1d: ',fn_name)
            gmake_plots_spec1d(fn_name,roi=roi)
        """
        
        """
        print('plots_mom0xy: ',fn_name)
        gmake_plots_mom0xy(fn_name)
        """

        """
        gmake_plots_makeslice(fn_name,width=2.0,pa=-45)
        gmake_plots_slice(fn_name,i=1)
        gmake_plots_slice(fn_name,i=2)        
        """
        #"""
        gmake_plots_radprof(fn_name)
        #"""

    
