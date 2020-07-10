#from .utils import imcontsub

import logging
logger = logging.getLogger(__name__)
from pprint import pformat
from astropy.coordinates import SkyCoord

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from astropy.wcs import WCS
# mpl.rcParams['xtick.direction'] = 'in'
# mpl.rcParams['ytick.direction'] = 'in'
# mpl.rcParams.update({'font.size': 12})
# mpl.rcParams["font.family"] = "serif"
# mpl.rcParams["image.origin"]="lower"
# mpl.rc('text', usetex=True)

mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"
mpl.rcParams['agg.path.chunksize'] = 10000
#mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#mpl.rc('font',**{'family':'serif','serif':['Palatino']})
#mpl.rc('text',usetex=True)
import astropy.units as u
import numpy as np
#from .model import pots_to_vcirc

from ..utils.misc import prepdir
from ..xyhelper.sky import linear_offset_coords
from ..arts.dynamics import vrot_from_rcProf
from astropy.units import Quantity

def plt_rc0(pots,
           pscorr=None,
           rrange=[1e-3,1e1]*u.kpc,num=50,
           figname='plt_rc.pdf'):
    """
    plot rc from galpy.potential
    also try:
        https://galpy.readthedocs.io/en/v1.5.0/getting_started.html
        from galpy.potential import plotRotcurve
        
    pscorr=(80*u.km/u.s,10*u.kpc)
    """
    
    rho=np.geomspace(rrange[0],rrange[1],num=num)
    rho=rho[np.where(rho>0)]
    
    vcirc,vname=pots_to_vcirc(pots,rho,pscorr=pscorr)
    
    plt.clf()
    fig,ax=plt.subplots(1,1,figsize=(10,10))
    
    nc=vcirc.shape[0]
    for i in range(nc): 
        ax.plot(rho,vcirc[i,:],label=vname[i])
    #ax.plot(rc['rrad']/rc['kps'],rc['vcirc_dp'],color='blue',label='ThinExpDisk')
    #ax.plot(rc['rrad']/rc['kps'],rc['vcirc_tt'],color='black',label='All')
    ax.set_xlabel('Radius [kpc]')
    ax.set_ylabel('V [km/s]')
    ax.legend()
    #ax1.loglog(rad,vcirc_tp)
    #ax1.loglog(rad,vcirc_tp,color='black')
    #ax2.loglog(rad,cmass_tp)
    fig.savefig(figname)    

def plt_rcProf(rcProf,
           rrange=[1e-3,2e1]*u.kpc,num=100,
           figname='plt_rc.pdf',showplot=False):    
    """
    plot rotation curve from the keyword:rcProf
    """
    
    rho=np.geomspace(rrange[0],rrange[1],num=num)
    rho=rho[np.where(rho>0)]
    
    vcirc=vrot_from_rcProf(rcProf,rho)    
    vname='Potential'
    
    name=[]
    for v0 in rcProf:
        if  isinstance(v0,Quantity):
            name.append("{0.value}{0.unit:latex_inline}".format(v0))
        else:
            name.append("{}".format(v0))
    name=','.join(name)
    name='('+name+')'

    
    if  showplot==False:
        plt.clf()
    fig,ax=plt.subplots(1,1,figsize=(5,5))
    
    ax.plot(rho,vcirc,label=name)
    #ax.plot(rc['rrad']/rc['kps'],rc['vcirc_dp'],color='blue',label='ThinExpDisk')
    #ax.plot(rc['rrad']/rc['kps'],rc['vcirc_tt'],color='black',label='All')
    ax.set_xlabel('Radius [kpc]')
    ax.set_ylabel('V [km/s]')
    #ax.legend()
    ax.set_title(name)
    #ax1.loglog(rad,vcirc_tp)
    #ax1.loglog(rad,vcirc_tp,color='black')
    #ax2.loglog(rad,cmass_tp)
    prepdir(figname) 
    fig.savefig(figname)  
    if  showplot==False:
        plt.close() # don't show it in ipynb         
    
    return

def im_grid(images,header,
            offset=False,
            units=None,titles=None,nxy=(3,3),
            figsize=(9,9),figname='im_grid.pdf',
            vmins=None,vmaxs=None,
            showplot=False):
    """
    display fits-images in a basic grid layout, with colorbar
    some interesting features:
        optionally make maps in an offset coordinates
    
    images: list can be non
    nxy:
    figname
    w: projection
    """
    if  offset==True:
        w=WCS(header).celestial
        coord = SkyCoord(header['CRVAL1'], header['CRVAL2'], unit="deg")
        #coord = SkyCoord(w.wcs.crval[0],w.wcs.crval[1], unit="deg")
        w_use=linear_offset_coords(w,coord)
        xlabel=r'$\Delta~\alpha$ ["]'
        ylabel=r'$\Delta~\delta$ ["]'
    else:
        w_use=WCS(header).celestial
        xlabel=r'$\alpha$ ["]'
        ylabel=r'$\delta$ ["]'        
    
    if  not isinstance(images,list):
        images=[images]
    if  not isinstance(images,list):
        images=[header]        

    plt.clf()
    
    fig, axs = plt.subplots(nxy[1],nxy[0], figsize=figsize,subplot_kw={'projection':w_use})
    axs=np.array(axs).reshape(-1)
    #fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2,hspace=0.2)
    
    for ii in range(nxy[0]*nxy[1]):
        
        if ii>=len(images):
            fig.delaxes(axs[ii])
            continue

        if images[ii] is None:
            fig.delaxes(axs[iy,ix])
            continue    
        vmin=vmins[ii] if  vmins is not None else None
        vmax=vmaxs[ii] if  vmaxs is not None else None
        im = axs[ii].imshow(images[ii],origin='lower',vmin=vmin,vmax=vmax);

        #divider = make_axes_locatable(axs[iy,ix])
        #cax = divider.append_axes("right", size="7%", pad=0.05)
        clb=fig.colorbar(im, ax=axs[ii]);
        if  units is not None:
            clb.ax.set_title(units[ii])
        if  titles is not None:
            axs[ii].set_title(titles[ii])
        axs[ii].set_xlabel(xlabel)
        axs[ii].set_ylabel(ylabel)
        #aa[iy,ix].set_title(os.path.basename(name).replace('_','.'))
        #aa[iy,ix].set_aspect('auto')

    #fig.tight_layout() 
    #; plt.show()
    prepdir(figname)    
    fig.savefig(figname)
    
    if  showplot==False:
        plt.close() # don't show it in ipynb
    #clear_output(wait=True) ; display(fig)
    



def plt_spec1d(fn,roi='icrs; circle(356.53932576899575,12.822017913507711 , 1") # text={example}'):
    """
    1D spectrum diagnostic plot
    e.g.:
        plt_spec1d('./data_bx610.bb1.cube64x64.iter0.image.fits')
    """
    

    
    header=fits.getheader(fn)
    ppbeam=calc_ppbeam(header)

    #   Hz->GHz / angstrom->Angstrom / m/s->km/s
    xu_scale=1.
    stepsize=0.5
    if  'Hz' in header['CUNIT3']:
        xu_scale=1e9
        stepsize=0.5
        xlabel='Freq [GHz]'
    if  'angstrom' in header['CUNIT3']:
        xu_scale=1.
        stepsize=1000.0
        #xlabel='Wavelength ['+"{0.unit:latex}".format(1*u.angstrom)+']'
        xlabel="$\lambda \, [\AA]$"
    if  'm/s' in header['CUNIT3']:
        xu_scale=1e3
    #   Jy->mJy
    yu_scale=1e-3
    if  'angstrom' in header['CUNIT3']:
        yu_scale=1.

    
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
    
    freq=(data.spectral_axis/xu_scale).value
    if  len(freq)==1:
        return 
    
    logger.debug("plt_spec1d <<<  fn ="+str(fn))
    logger.debug("plt_spec1d <<<  roi="+str(roi))    
    
    plt.clf()
    hratio=2.00
    fig,(ax,ax_res)=plt.subplots(2,1,sharex=True,figsize=(12,8),
                                 gridspec_kw = {'height_ratios':[hratio, 1.0]})
    
    ax_res.fill_between(freq,0,subdata_1d.array/ppbeam/yu_scale-submodel_1d.array/ppbeam/yu_scale,facecolor='green',step='mid',alpha=1.0)
    ax_res.plot(freq,freq*0.,color='black',alpha=1.0,lw=1.0,ls='--',dashes=(10,10))
    ax_res.plot(freq,subdata_1d.array/ppbeam/yu_scale-submodel_1d.array/ppbeam/yu_scale,color='black',alpha=2.0,lw=1.0,drawstyle='steps-mid',label='Residual')
    
    res_mean=np.mean(subdata_1d.array/ppbeam/yu_scale-submodel_1d.array/ppbeam/yu_scale)

    ax_res.plot(freq,freq*0.+res_mean,color='blue',alpha=0.5,lw=1.0,label='Residual-Mean')
    ax_res.legend(loc="upper right")
    

    ax.fill_between(freq,submod2d_1d.array/ppbeam/yu_scale,subdata_1d.array/ppbeam/yu_scale,facecolor='red',step='mid',alpha=0.5)
    ax.plot(freq,freq*0.,color='black',alpha=1.0,lw=1.0,ls='--',dashes=(10,10))
    
    ax.plot(freq,subdata_1d.array/ppbeam/yu_scale,color='black',alpha=2.0,lw=1.0,drawstyle='steps-mid',label='Data')
    

    # note: only in clean map these two will match as ppbeam was calculated from a Gaussian kernel
    ax.plot(freq,submodel_1d.array/ppbeam/yu_scale,color='blue',alpha=0.5,lw=2.0,label='Model')
    ax.plot(freq,subimodel_1d.array/yu_scale,color='cyan',alpha=0.5,lw=2.0,label='iModel')

    
    ax.legend(loc="upper right")
    ax.plot(freq,submod2d_1d.array/ppbeam/yu_scale,color='blue',alpha=0.5,lw=2.0)
    
    start=np.nanmin(freq)
    end=np.nanmax(freq)
    ax.xaxis.set_ticks(np.arange(np.floor(start*stepsize)/stepsize, np.ceil(end*stepsize)/stepsize, stepsize))
    ax.xaxis.set_major_formatter(plticker.FormatStrFormatter('%0.1f'))
    ax.minorticks_on()
    ax.set_xlim(start,end)
    ylim=ax.get_ylim()

    ax.set_ylabel('Flux [mJy]')
    fn_basename=os.path.basename(fn)
    ax.set_title(fn_basename+'\n'+roi.replace('icrs','').replace(';',''))
    ax_res.set_xlabel(xlabel)
    
    dy_res=(ylim[1]-ylim[0])/hratio/2.0
    ax_res.set_ylim(-dy_res,dy_res)
    
    fig.subplots_adjust(left=0.20,bottom=0.15,right=0.95,top=0.95)
    fig.tight_layout()
    
    vname=''
    if  'text={' in roi:
        vname='_'+(roi.split("text={"))[1].replace("}",'')
    odir=os.path.dirname(fn)+'/plt_spec1d'

    if  not os.path.exists(odir):
        os.makedirs(odir)        
    fig.savefig(odir+'/'+fn_basename.replace('.fits','')+vname+'.pdf')    

    plt.close()
    logger.debug("plt_spec1d >>> "+odir+'/'+fn_basename.replace('.fits','')+vname+'.pdf\n')
    
    return 

def plt_yt3d(fn,roi='icrs; circle(356.5393156, 12.8220309, 1")'):
    
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
    
    
def plt_makeslice(fn,
                          radec=[356.53932576899575,12.822017913507711],
                          linechan=None,
                          slicechan=None,
                          width=1.0,length=2.5,pa=-45):
    
     #path1 = Path([(0., 0.), (62., 62.)],width=10.0)
     #slice1 = extract_pv_slice(array, path1) 


    pa=-45
    radec=SkyCoord(radec[0],radec[1],unit="deg",frame='icrs')
     
    data = SpectralCube.read(fn)
    mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')
    mod3d=SpectralCube.read(fn.replace('data_','cmod3d_'),mode='readonly')
    model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
    imodel=SpectralCube.read(fn.replace('data_','imodel_'),mode='readonly')
    imod3d=SpectralCube.read(fn.replace('data_','imod3d_'),mode='readonly')

    if  slicechan is not None:
        data=data.spectral_slab(slicechan[0],slicechan[1])
        mod2d=mod2d.spectral_slab(slicechan[0],slicechan[1])
        mod3d=mod3d.spectral_slab(slicechan[0],slicechan[1])
        model=model.spectral_slab(slicechan[0],slicechan[1])
        imodel=imodel.spectral_slab(slicechan[0],slicechan[1])
        imod3d=imod3d.spectral_slab(slicechan[0],slicechan[1])

    if  linechan is not None:
        data_line = SpectralCube.read(fn.replace('data_','data_line_'),mode='readonly')
        if  slicechan is not None:
            data_line=data_line.spectral_slab(slicechan[0],slicechan[1])          
     
    for i in [1,2]:
         path = PathFromCenter(center=radec,
                            length=length*u.arcsec,
                            angle=(pa+float(i-1)*90.) * u.deg,
                            width=width*u.arcsec)
         slice = extract_pv_slice(data, path)
         slice.writeto(fn.replace('data_','data_slice'+str(i)+'_'),overwrite=True)

         if  linechan is not None:
             slice = extract_pv_slice(data_line, path)
             slice.writeto(fn.replace('data_','data_line_slice'+str(i)+'_'),overwrite=True)
         
         slice = extract_pv_slice(mod3d, path)
         slice.writeto(fn.replace('data_','cmod3d_slice'+str(i)+'_'),overwrite=True)
         
         slice = extract_pv_slice(model, path)
         slice.writeto(fn.replace('data_','cmodel_slice'+str(i)+'_'),overwrite=True)         

         slice = extract_pv_slice(imodel, path)
         slice.writeto(fn.replace('data_','imodel_slice'+str(i)+'_'),overwrite=True)
         
         slice = extract_pv_slice(imod3d, path)
         slice.writeto(fn.replace('data_','imod3d_slice'+str(i)+'_'),overwrite=True)                   

def plt_slice(fn,i=1):
    """
        data model res
        contsub version
    """

    
    
    fn_basename=os.path.basename(fn)
    header=fits.getheader(fn.replace('data_','data_slice'+str(i)+'_'))
    if  header['NAXIS2']==1:
        return

    logger.debug("plt_slice <<< "+str(fn)+str(i))
    
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
               vmin=np.nanmin(data1), vmax=np.nanmax(data1),aspect=0.25)
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
               vmin=np.nanmin(data1), vmax=np.nanmax(data1),aspect=0.25)
    ax2.set_title('Model')
    
    ax3 = fig.add_subplot(ny,nx,3)
    ax3.imshow(data1-data2, interpolation='nearest',
               vmin=np.nanmin(data1), vmax=np.nanmax(data1),aspect=0.25)
    ax3.set_title('Residual')
    
    ax4 = fig.add_subplot(ny,nx,4)
    data4,header=fits.getdata(fn.replace('data_','imodel_slice'+str(i)+'_'),header=True,memmap=False) 
    ax4.imshow(data4, interpolation='nearest',
               vmin=np.nanmin(data4), vmax=np.nanmax(data4),aspect=0.25)
    ax4.set_title('Model')
    
    if  isline==True:
        ax5 = fig.add_subplot(ny,nx,5)
        data5,header=fits.getdata(fn.replace('data_','data_line_slice'+str(i)+'_'),header=True,memmap=False) 
        ax5.imshow(data5, interpolation='nearest',
                   vmin=np.nanmin(data1), vmax=np.nanmax(data1),aspect=0.25)
        ax5.set_title('Data/Line')
        
        ax6 = fig.add_subplot(ny,nx,6)
        data6,header=fits.getdata(fn.replace('data_','cmod3d_slice'+str(i)+'_'),header=True,memmap=False) 
        ax6.imshow(data6, interpolation='nearest',
                   vmin=np.nanmin(data1), vmax=np.nanmax(data1),aspect=0.25)
        ax6.set_title('Model/Line')
        
        ax7 = fig.add_subplot(ny,nx,7)
        ax7.imshow(data1-data2, interpolation='nearest',
                   vmin=np.nanmin(data1), vmax=np.nanmax(data1),aspect=0.25)          
        ax7.set_title('Residual')
        
        ax8 = fig.add_subplot(ny,nx,8)
        data8,header=fits.getdata(fn.replace('data_','imod3d_slice'+str(i)+'_'),header=True,memmap=False) 
        ax8.imshow(data8, interpolation='nearest',
                   vmin=np.nanmin(data8), vmax=np.nanmax(data8),aspect=0.25)
        ax8.set_title('Model/Line')        
        
    out_basename=os.path.basename(fn.replace('data_','data_slice'+str(i)+'_'))
    fig.subplots_adjust(left=0.07,bottom=0.07,right=0.95,top=0.95)

    odir=os.path.dirname(fn)+'/plt_slice'

    if not os.path.exists(odir):
        os.makedirs(odir)          
    fig.savefig(odir+'/'+out_basename.replace('.fits','')+'.pdf')   
    plt.close() 
    logger.debug("plt_slice >>> "+odir+'/'+out_basename.replace('.fits','')+'.pdf\n') 
    
    return

    
def plt_mom0xy(fn,linechan=None):

    logger.debug("plt_mom0xy <<< "+fn)
    
    dirname=os.path.dirname(fn)
    
    #   load data/cmodel
    header=fits.getheader(fn)
    ppbeam=calc_ppbeam(header)
    data=SpectralCube.read(fn,mode='readonly')
    model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
    mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')
    mod3d=SpectralCube.read(fn.replace('data_','cmod3d_'),mode='readonly')
    
    #   load imodel (i.a., reference models,which may have different WCS)
    ref_header=fits.getheader(fn.replace('data_','imodel_'))
    imodel=SpectralCube.read(fn.replace('data_','imodel_'),mode='readonly')
    imod2d=SpectralCube.read(fn.replace('data_','imod2d_'),mode='readonly')
    imod3d=SpectralCube.read(fn.replace('data_','imod3d_'),mode='readonly')

    if  os.path.isfile(fn.replace('data_','mask_')):
        mask=SpectralCube.read(fn.replace('data_','mask_'),mode='readonly')
        data=data.with_mask(mask.unitless_filled_data[:,:,:]==0)
    
    if  (mod3d.sum()).value==0.0:
        isline=False
    else:
        isline=True

    ker3d=SpectralCube.read(fn.replace('data_','kernel_'),mode='readonly')
    
    data_m0=data.moment(order=0)
    #data_m0.write(fn.replace('.fits','mom0test.fits'),overwrite=True)  
    
    model_m0=model.moment(order=0)
    
    mod2d_m0=mod2d.moment(order=0)
    if  isline==True:
        mod3d_m0=mod3d.moment(order=0)
        imod3d_m0=imod3d.moment(order=0)
    ker3d_m0=ker3d.moment(order=0)
    ker3d_m0=ker3d[0,:,:]
    imodel_m0=imodel.moment(order=0)




    plt.clf()
    if  isline==True:
        figsize=(24,12)
        nx=6
        ny=3
    else:
        figsize=(24,4)
        nx=6
        ny=1
        
    fig=plt.figure(figsize=figsize)
    
    w=WCS(header).celestial
    ref_w=WCS(ref_header).celestial

    tmp=data_m0.array
    dlevels=np.linspace(np.nanmin(tmp),np.nanmax(tmp),12)
    rms=sigma_clipped_stats(tmp, sigma=3, maxiters=5)
    rms=rms[2]
    dlevels=rms*np.arange(-3-3*10,3+3*10,6)

     
    vmin=np.nanmin(tmp)
    vmax=np.nanmax(tmp)
    ax1 = fig.add_subplot(ny,nx,1, projection=w)
    ax1.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    
    xlim=ax1.get_xlim()
    ylim=ax1.get_ylim()
    xlim=(xlim[0]+0,xlim[1]-0)
    ylim=(ylim[0]+0,ylim[1]-0)
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    wxlim,wylim=w.wcs_pix2world(xlim,ylim,0)
    
    plane0=model_m0.value
    tmp0=np.where(plane0==np.nanmax(plane0))
    cxy=((list(zip(*tmp0)))[0])[::-1]
    nxy=(plane0.shape)[::-1]
    wcx,wcy=w.wcs_pix2world(cxy[0],cxy[1],0)    
    
    ax1.coords['ra'].set_axislabel('Right Ascension')
    ax1.coords['dec'].set_axislabel('Declination')
    cs1=ax1.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    ax1.contour(tmp,levels=0,colors='gray', alpha=0.5)
    wx,wy=w.wcs_pix2world(header['NAXIS1']/8.0,header['NAXIS2']/8.0,0)
    if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax1.get_transform('icrs'))
        ax1.add_patch(bshape)
    fn_basename=os.path.basename(fn)
    ax1.set_title(fn_basename)
    #ax1.plot([cxy[0]+10,cxy[0]+21],[cxy[1],cxy[1]],color="yellow",transform=ax1.get_transform('icrs'))
    ax1.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax1.get_transform('icrs'))
    ax1.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax1.get_transform('icrs'))
    
    xlim=ax1.get_xlim()
    ylim=ax1.get_ylim()
    wxlim,wylim=w.wcs_pix2world(xlim,ylim,0)

    tmp=model_m0.array
    ax2 = fig.add_subplot(ny,nx,2, projection=w)
    ax2.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax2.coords['dec'].set_ticklabel_visible(False)
    ax2.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    ax2.contour(tmp,levels=0,colors='gray', alpha=0.5)
    if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax2.get_transform('icrs'))    
        ax2.add_patch(bshape)
    ax2.set_title('Model')
    ax2.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax2.get_transform('icrs'))
    ax2.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax2.get_transform('icrs'))
    
    tmp=data_m0.array-model_m0.array
    ax3 = fig.add_subplot(ny,nx,3, projection=w)
    ax3.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax3.coords['dec'].set_ticklabel_visible(False)
    ax3.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    ax3.contour(tmp,levels=0,colors='gray', alpha=0.5)
    if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax3.get_transform('icrs'))            
        ax3.add_patch(bshape)
    ax3.set_title('Residual')
    ax3.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax3.get_transform('icrs'))
    ax3.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax3.get_transform('icrs'))

    
    tmp_psf=ker3d_m0.array
    dlevels_psf=np.linspace(np.nanmin(tmp_psf),np.nanmax(tmp_psf),12)
    vmin_psf=np.nanmin(tmp_psf)
    vmax_psf=np.nanmax(tmp_psf)
    ax4 = fig.add_subplot(ny,nx,4, projection=w)
    ax4.imshow(tmp_psf, interpolation='nearest',
           vmin=vmin_psf, vmax=vmax_psf)
    ax4.coords['dec'].set_ticklabel_visible(False)
    ax4.contour(tmp_psf,levels=dlevels_psf,colors='white', alpha=0.5)
    ax4.contour(tmp_psf,levels=[0.5],colors='yellow', alpha=0.5)
    ax4.contour(tmp_psf,levels=0,colors='gray', alpha=0.5)
    if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax4.get_transform('icrs'))                          
        ax4.add_patch(bshape)
    ax4.set_title('Kernel')
    
    
    tmp=imodel_m0.array
    #imodel_m0.write(fn.replace('.fits','mom0test.fits'),overwrite=True)  
    vmin=np.nanmin(tmp)
    vmax=np.nanmax(tmp)
    vmax=np.partition(tmp.flatten(), -2)[-2]
    dlevels=np.linspace(vmin,vmax,6)
    ax5 = fig.add_subplot(ny,nx,5, projection=ref_w)
    ax5.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax5.coords['dec'].set_ticklabel_visible(False)
    ax5.contour(tmp,levels=dlevels,colors='white', alpha=0.5,origin='image')
    ax5.contour(tmp,levels=[vmax*0.1,vmax*0.5],colors='yellow', alpha=0.5,origin='image')
    if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax5.get_transform('icrs'))                          
        ax5.add_patch(bshape)
    ax5.set_title('Ref.Model')
    ax5.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax5.get_transform('icrs'))
    ax5.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax5.get_transform('icrs'))
    ref_w=WCS(ref_header).celestial
    ref_xlim,ref_ylim=ref_w.wcs_world2pix(wxlim,wylim,0)
    ax5.set_xlim(ref_xlim)
    ax5.set_ylim(ref_ylim)    


    tmp=data_m0.array-mod2d_m0.array
    dlevels=np.linspace(np.nanmin(tmp),np.nanmax(tmp),12)
    vmin=np.nanmin(tmp)
    vmax=np.nanmax(tmp)


    if  isline==True:
        
        imcontsub(fn,
                  linefile=fn.replace('data_','data_line_'),
                  contfile=fn.replace('data_','data_cont_'),
                  linechan=linechan)
        data_line=SpectralCube.read(fn.replace('data_','data_line_'),mode='readonly')
        data_line_m0=data_line.moment(order=0)
        tmp=data_line_m0.array
        dlevels=np.linspace(np.nanmin(tmp),np.nanmax(tmp),12)
        vmin=np.nanmin(tmp)
        vmax=np.nanmax(tmp)
        
        ### LINE
        
        dlevels=rms*np.arange(-3-3*10,3+3*10,6)
        ax4 = fig.add_subplot(ny,nx,1+6, projection=w)
        ax4.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax4.coords['dec'].set_ticklabel_visible(False)
        ax4.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax4.contour(tmp,levels=0,colors='gray', alpha=0.5)
        if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
            bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax4.get_transform('icrs'))                          
            ax4.add_patch(bshape)        
        ax4.set_title('Data/Line')
        ax4.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax4.get_transform('icrs'))
        ax4.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax4.get_transform('icrs'))          
        
        
        tmp=model_m0.array-mod2d_m0.array
        ax5 = fig.add_subplot(ny,nx,2+6, projection=w)
        ax5.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax5.coords['dec'].set_ticklabel_visible(False)
        ax5.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax5.contour(tmp,levels=0,colors='gray', alpha=0.5)
        if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
            bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax5.get_transform('icrs'))                          
            ax5.add_patch(bshape)
        ax5.set_title('Model/Line')
        ax5.plot([cxy[0]+10,cxy[0]+21],[cxy[1],cxy[1]],color="yellow")
        ax5.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+21],color="yellow")
            
        
        tmp=data_line_m0.array-(model_m0.array-mod2d_m0.array)
        ax6 = fig.add_subplot(ny,nx,3+6, projection=w)
        ax6.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax6.coords['dec'].set_ticklabel_visible(False)
        ax6.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax6.contour(tmp,levels=0,colors='gray', alpha=0.5)
        if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
            bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax6.get_transform('icrs'))                          
            ax6.add_patch(bshape)        
        ax6.set_title('Residual/LINE')
        ax6.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax6.get_transform('icrs'))
        ax6.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax6.get_transform('icrs'))
        
        tmp=imod3d_m0.array
        vmin=np.nanmin(tmp)
        vmax=np.nanmax(tmp)
        vmax=np.partition(tmp.flatten(), -2)[-2]
    
        dlevels=np.linspace(vmin,vmax,6)
        ax10 = fig.add_subplot(ny,nx,5+6, projection=ref_w)
        ax10.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax10.coords['dec'].set_ticklabel_visible(False)
        ax10.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax10.contour(tmp,levels=[vmax*0.1,vmax*0.5],colors='yellow', alpha=0.5)
        if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
            bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax10.get_transform('icrs'))                          
            ax10.add_patch(bshape)
        ax10.set_title('Model/Line') 
        ref_xlim,ref_ylim=ref_w.wcs_world2pix(wxlim,wylim,0)
        ax10.set_xlim(ref_xlim)
        ax10.set_ylim(ref_ylim)           
        ax10.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax10.get_transform('icrs'))
        ax10.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax10.get_transform('icrs'))
        
        
        ### CONT
        
        data_cont=fits.getdata(fn.replace('data_','data_cont_'))
        tmp=data_cont.copy()
        dlevels=np.linspace(np.nanmin(tmp),np.nanmax(tmp),12)
        vmin=np.nanmin(tmp)
        vmax=np.nanmax(tmp)
        
        dlevels=rms*np.arange(-3-3*10,3+3*10,6)
        ax11 = fig.add_subplot(ny,nx,1+12, projection=w)
        ax11.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax11.coords['dec'].set_ticklabel_visible(False)
        ax11.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax11.contour(tmp,levels=0,colors='gray', alpha=0.5)
        if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
            bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax11.get_transform('icrs'))                          
            ax11.add_patch(bshape)        
        ax11.set_title('Data/CONT') 
        ax11.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax11.get_transform('icrs'))
        ax11.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax11.get_transform('icrs'))        
        
        
        tmp=(mod2d.mean(axis=0)).array
        ax12 = fig.add_subplot(ny,nx,2+12, projection=w)
        ax12.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax12.coords['dec'].set_ticklabel_visible(False)
        ax12.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax12.contour(tmp,levels=0,colors='gray', alpha=0.5)
        if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
            bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax12.get_transform('icrs'))                          
            ax12.add_patch(bshape)
        ax12.set_title('Model/CONT')
        ax12.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax12.get_transform('icrs'))
        ax12.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax12.get_transform('icrs'))  
            
        
        tmp=data_cont-tmp
        ax13 = fig.add_subplot(ny,nx,3+12, projection=w)
        ax13.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax13.coords['dec'].set_ticklabel_visible(False)
        ax13.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax13.contour(tmp,levels=0,colors='gray', alpha=0.5)
        if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
            bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax13.get_transform('icrs'))                          
            ax13.add_patch(bshape)        
        ax13.set_title('Residual/CONT') 
        ax13.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax13.get_transform('icrs'))
        ax13.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax13.get_transform('icrs'))  
        
        tmp=(imod2d.mean(axis=0)).array
        vmin=np.nanmin(tmp)
        vmax=np.nanmax(tmp)
        vmax=np.partition(tmp.flatten(), -2)[-2]
    
        dlevels=np.linspace(vmin,vmax,6)
        ax14 = fig.add_subplot(ny,nx,5+12, projection=ref_w)
        ax14.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax14.coords['dec'].set_ticklabel_visible(False)
        ax14.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax14.contour(tmp,levels=[vmax*0.1,vmax*0.5],colors='yellow', alpha=0.5)
        if  'BMIN' in header.keys() and 'BMAJ' in header.keys():
            bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax14.get_transform('icrs'))                          
            ax14.add_patch(bshape)
        ax14.set_title('Ref.Model/Line')
        ref_xlim,ref_ylim=ref_w.wcs_world2pix(wxlim,wylim,0)
        ax14.set_xlim(ref_xlim)
        ax14.set_ylim(ref_ylim)   
        ax14.plot([wcx+0.4/3600,wcx+0.8/3600],[wcy,wcy],color="yellow",transform=ax14.get_transform('icrs'))
        ax14.plot([wcx,wcx],[wcy+0.4/3600,wcy+0.9/3600],color="yellow",transform=ax14.get_transform('icrs'))                             

    #fig.tight_layout()

    
    fig.subplots_adjust(left=0.01,bottom=0.01,right=0.99,top=0.99)
    odir=os.path.dirname(fn)+'/plt_mom0xy'

    if not os.path.exists(odir):
        os.makedirs(odir)        
    fig.savefig(odir+'/'+fn_basename.replace('.fits','')+'.pdf')   
    plt.close()
    logger.debug("plt_mom0xy >>> "+odir+'/'+os.path.basename(fn).replace('.fits','')+'.pdf\n') 
#     #"""
#     
#     f = aplpy.FITSFigure(m0.hdu)  
#     f.show_colorscale()
#     f.save('moment_0.png')


def plt_radprof(fn):

    wd=fn.replace('data','imodrp*')
    flist=glob.glob(wd)

    if  len(flist)>0:
        
        fig=plt.figure(figsize=(8.,5.*len(flist))) 
        cc=0
        for fn0 in flist:
            logger.debug("plt_radprof <<< "+fn0)
            
            cc=cc+1
            ax = fig.add_subplot(len(flist),1,cc)
            
            t=Table.read(fn0)
            ax.plot(t['sbrad'].data[0],t['sbprof'].data[0],color='black',label='S.B. (diff)')
            ymin,ymax=ax.get_ylim()
            
            cog=scipy.integrate.cumtrapz(t['sbprof'].data[0]*2.*np.pi*t['sbrad'].data[0],t['sbrad'].data[0],initial=0.)
            cog /= np.nanmax(cog) 
            ax.plot(t['sbrad'].data[0],cog*ymax,linestyle='--',color='black',label='S.B. (cog)')
            
            ax.set_xlim(np.nanmin(t['sbrad'].data[0]),np.nanmax(t['sbrad'].data[0]))
            
            ax.set_title(os.path.basename(fn0))
            ax.set_ylabel('SB')
            
            ax.legend(loc="upper right")
            
            if  cc==len(flist):
                ax.set_xlabel('Radius [arcsec]')
            
            ax1 = ax.twinx()
            x1=t['vrad'].data[0]
            y1=t['vrot'].data[0]
            ax1.plot(x1,y1,color='blue',label='Vrot')
            ax1.plot(t['vrad_node'].data[0],t['vrot_node'].data[0],marker='o',linestyle='none',color='blue',mfc='none',label='Vrot-N')
            
            if  'vrot_halo_node' in t:
                ax1.plot(t['vrad_node'].data[0],t['vrot_halo_node'].data[0],marker='v',linestyle='none',color='blue',mfc='none',label='Vrot-Halo-N')
            if  'vrot_disk_node' in t:
                ax1.plot(t['vrad_node'].data[0],t['vrot_disk_node'].data[0],marker='^',linestyle='none',color='blue',mfc='none',label='Vrot-Disk-N')
            
            y1=t['vdis'].data[0]
            ax1.plot(x1,y1,color='red',label='Vdist')
            
            ax1.plot(t['vrad_node'].data[0],t['vdis_node'].data[0],marker='o',linestyle='none',color='red',mfc='none',label='Vdist-N')
            
            ax1.set_ylabel('Vrot/Vdis [km/s]')
        
            ax1.legend(loc="lower right")
        
        odir=os.path.dirname(fn)+'/plt_radprof'
        if not os.path.exists(odir):
            os.makedirs(odir)   
            
        fig.savefig(odir+'/'+os.path.basename(fn).replace('.fits','')+'.pdf')
        logger.debug("plt_radprof >>> "+odir+'/'+os.path.basename(fn).replace('.fits','')+'.pdf\n') 



if  __name__=="__main__":

    pass


    
