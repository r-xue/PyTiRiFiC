
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
    if  len(freq)==1:
        return 
    
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
    odir=os.path.dirname(fn)+'/pls_spec1d'
    if not os.path.exists(odir):
        os.makedirs(odir)        
    fig.savefig(odir+'/'+fn_basename.replace('.fits','')+vname+'.pdf')    

    plt.close()
    
    return 

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
    
    
def gmake_plots_makeslice(fn,
                          radec=[356.53932576899575,12.822017913507711],
                          linechan=None,
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
     if  linechan is not None:
         data_line = SpectralCube.read(fn.replace('data_','data_line_'),mode='readonly')
     
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

def gmake_plots_slice(fn,i=1):
    """
        data model res
        contsub version
    """


    fn_basename=os.path.basename(fn)
    header=fits.getheader(fn.replace('data_','data_slice'+str(i)+'_'))
    if  header['NAXIS2']==1:
        return

    
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
        data5,header=fits.getdata(fn.replace('data_','data_line_slice'+str(i)+'_'),header=True,memmap=False) 
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

    odir=os.path.dirname(fn)+'/pls_slice'
    if not os.path.exists(odir):
        os.makedirs(odir)          
    fig.savefig(odir+'/'+out_basename.replace('.fits','')+'.pdf')   
    plt.close() 
    
    return

    
def gmake_plots_mom0xy(fn,linechan=None):


    dirname=os.path.dirname(fn)
    #mod_dct=np.load(dirname+'/mod_dct.npy').item()
    #print(mod_dct.keys())
    header=fits.getheader(fn)
    ppbeam=calc_ppbeam(header)
    
    data=SpectralCube.read(fn,mode='readonly')
    model=SpectralCube.read(fn.replace('data_','cmodel_'),mode='readonly')
    mod2d=SpectralCube.read(fn.replace('data_','cmod2d_'),mode='readonly')
    mod3d=SpectralCube.read(fn.replace('data_','cmod3d_'),mode='readonly')
    imodel=SpectralCube.read(fn.replace('data_','imodel_'),mode='readonly')
    imod2d=SpectralCube.read(fn.replace('data_','imod2d_'),mode='readonly')
    imod3d=SpectralCube.read(fn.replace('data_','imod3d_'),mode='readonly')
    
    plane0=imodel.unmasked_data[0,:,:].value
    tmp0=np.where(plane0==np.max(plane0))
    cxy=((list(zip(*tmp0)))[0])[::-1]
    nxy=(plane0.shape)[::-1]

    
    if  (mod3d.sum()).value==0.0:
        isline=False
    else:
        isline=True

    ker3d=SpectralCube.read(fn.replace('data_','kernel_'),mode='readonly')
    
    data_m0=data.moment(order=0)
    #data_m0.write(fn.replace('.fits','mom0test.fits'),overwrite=True)  
    
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
        figsize=(24,12)
        nx=6
        ny=3
    else:
        figsize=(24,4)
        nx=6
        ny=1
        
    fig=plt.figure(figsize=figsize)
    
    w=WCS(header).celestial
    
    
    tmp=data_m0.array
    dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
    rms=sigma_clipped_stats(tmp, sigma=3, maxiters=5)
    rms=rms[2]
    dlevels=rms*np.arange(-3-3*10,3+3*10,6)

     
    vmin=np.min(tmp)
    vmax=np.max(tmp)
    ax1 = fig.add_subplot(ny,nx,1, projection=w)
    ax1.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax1.coords['ra'].set_axislabel('Right Ascension')
    ax1.coords['dec'].set_axislabel('Declination')
    cs1=ax1.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    ax1.contour(tmp,levels=0,colors='gray', alpha=0.5)
    wx,wy=w.wcs_pix2world(header['NAXIS1']/8.0,header['NAXIS2']/8.0,0)
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax1.get_transform('icrs'))
    ax1.add_patch(bshape)
    fn_basename=os.path.basename(fn)
    ax1.set_title(fn_basename)
    ax1.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
    ax1.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")
    
    tmp=model_m0.array
    ax2 = fig.add_subplot(ny,nx,2, projection=w)
    ax2.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax2.coords['dec'].set_ticklabel_visible(False)
    ax2.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    ax2.contour(tmp,levels=0,colors='gray', alpha=0.5)
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax2.get_transform('icrs'))    
    ax2.add_patch(bshape)
    ax2.set_title('Model')
    ax2.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
    ax2.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")
    
    tmp=data_m0.array-model_m0.array
    ax3 = fig.add_subplot(ny,nx,3, projection=w)
    ax3.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax3.coords['dec'].set_ticklabel_visible(False)
    ax3.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
    ax3.contour(tmp,levels=0,colors='gray', alpha=0.5)
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax3.get_transform('icrs'))            
    ax3.add_patch(bshape)
    ax3.set_title('Residual')
    ax3.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
    ax3.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")

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
    ax4.contour(tmp_psf,levels=0,colors='gray', alpha=0.5)
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax4.get_transform('icrs'))                          
    ax4.add_patch(bshape)
    ax4.set_title('Kernel')
    
    
    tmp=imodel_m0.array
    #imodel_m0.write(fn.replace('.fits','mom0test.fits'),overwrite=True)  
    vmin=np.min(tmp)
    vmax=np.max(tmp)
    vmax=np.partition(tmp.flatten(), -2)[-2]
    dlevels=np.linspace(vmin,vmax,6)
    ax5 = fig.add_subplot(ny,nx,5, projection=w)
    ax5.imshow(tmp, interpolation='nearest',
           vmin=vmin, vmax=vmax)
    ax5.coords['dec'].set_ticklabel_visible(False)
    ax5.contour(tmp,levels=dlevels,colors='white', alpha=0.5,origin='image')
    ax5.contour(tmp,levels=[vmax*0.1,vmax*0.5],colors='yellow', alpha=0.5,origin='image')
    bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax5.get_transform('icrs'))                          
    ax5.add_patch(bshape)
    ax5.set_title('iModel')
    ax5.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
    ax5.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")    

    tmp=data_m0.array-mod2d_m0.array
    dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
    vmin=np.min(tmp)
    vmax=np.max(tmp)
    
    if  isline==True:
        
        imcontsub(fn,
                  linefile=fn.replace('data_','data_line_'),
                  contfile=fn.replace('data_','data_cont_'),
                  linechan=linechan)
        data_line=SpectralCube.read(fn.replace('data_','data_line_'),mode='readonly')
        data_line_m0=data_line.moment(order=0)
        tmp=data_line_m0.array
        dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
        vmin=np.min(tmp)
        vmax=np.max(tmp)
        
        ### LINE
        
        dlevels=rms*np.arange(-3-3*10,3+3*10,6)
        ax4 = fig.add_subplot(ny,nx,1+6, projection=w)
        ax4.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax4.coords['dec'].set_ticklabel_visible(False)
        ax4.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax4.contour(tmp,levels=0,colors='gray', alpha=0.5)
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax4.get_transform('icrs'))                          
        ax4.add_patch(bshape)        
        ax4.set_title('Data/Line')
        ax4.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
        ax4.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")           
        
        
        tmp=model_m0.array-mod2d_m0.array
        ax5 = fig.add_subplot(ny,nx,2+6, projection=w)
        ax5.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax5.coords['dec'].set_ticklabel_visible(False)
        ax5.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax5.contour(tmp,levels=0,colors='gray', alpha=0.5)
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax5.get_transform('icrs'))                          
        ax5.add_patch(bshape)
        ax5.set_title('Model/Line')
        ax5.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
        ax5.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")
            
        
        tmp=data_line_m0.array-(model_m0.array-mod2d_m0.array)
        ax6 = fig.add_subplot(ny,nx,3+6, projection=w)
        ax6.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax6.coords['dec'].set_ticklabel_visible(False)
        ax6.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax6.contour(tmp,levels=0,colors='gray', alpha=0.5)
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax6.get_transform('icrs'))                          
        ax6.add_patch(bshape)        
        ax6.set_title('Residual/LINE')
        ax6.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
        ax6.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")
        
        tmp=imod3d_m0.array
        vmin=np.min(tmp)
        vmax=np.max(tmp)
        vmax=np.partition(tmp.flatten(), -2)[-2]
    
        dlevels=np.linspace(vmin,vmax,6)
        ax10 = fig.add_subplot(ny,nx,5+6, projection=w)
        ax10.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax10.coords['dec'].set_ticklabel_visible(False)
        ax10.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax10.contour(tmp,levels=[vmax*0.1,vmax*0.5],colors='yellow', alpha=0.5)
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax10.get_transform('icrs'))                          
        ax10.add_patch(bshape)
        ax10.set_title('Model/Line') 
        ax10.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
        ax10.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")
        
        
        ### CONT
        
        data_cont=fits.getdata(fn.replace('data_','data_cont_'))
        tmp=data_cont.copy()
        dlevels=np.linspace(np.min(tmp),np.max(tmp),12)
        vmin=np.min(tmp)
        vmax=np.max(tmp)
        
        dlevels=rms*np.arange(-3-3*10,3+3*10,6)
        ax11 = fig.add_subplot(ny,nx,1+12, projection=w)
        ax11.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax11.coords['dec'].set_ticklabel_visible(False)
        ax11.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax11.contour(tmp,levels=0,colors='gray', alpha=0.5)
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax11.get_transform('icrs'))                          
        ax11.add_patch(bshape)        
        ax11.set_title('Data/CONT')
        ax11.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
        ax11.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")           
        
        
        tmp=(mod2d.mean(axis=0)).array
        ax12 = fig.add_subplot(ny,nx,2+12, projection=w)
        ax12.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax12.coords['dec'].set_ticklabel_visible(False)
        ax12.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax12.contour(tmp,levels=0,colors='gray', alpha=0.5)
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax12.get_transform('icrs'))                          
        ax12.add_patch(bshape)
        ax12.set_title('Model/CONT')
        ax12.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
        ax12.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")
            
        
        tmp=data_cont-tmp
        ax13 = fig.add_subplot(ny,nx,3+12, projection=w)
        ax13.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax13.coords['dec'].set_ticklabel_visible(False)
        ax13.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax13.contour(tmp,levels=0,colors='gray', alpha=0.5)
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax13.get_transform('icrs'))                          
        ax13.add_patch(bshape)        
        ax13.set_title('Residual/CONT')
        ax13.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
        ax13.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")
        
        tmp=(imod2d.mean(axis=0)).array
        vmin=np.min(tmp)
        vmax=np.max(tmp)
        vmax=np.partition(tmp.flatten(), -2)[-2]
    
        dlevels=np.linspace(vmin,vmax,6)
        ax14 = fig.add_subplot(ny,nx,5+12, projection=w)
        ax14.imshow(tmp, interpolation='nearest',
               vmin=vmin, vmax=vmax)
        ax14.coords['dec'].set_ticklabel_visible(False)
        ax14.contour(tmp,levels=dlevels,colors='white', alpha=0.5)
        ax14.contour(tmp,levels=[vmax*0.1,vmax*0.5],colors='yellow', alpha=0.5)
        bshape=mpl.patches.Ellipse((wx,wy), header['BMIN'], header['BMAJ'], angle=-header['BPA'], 
                               edgecolor='cyan', facecolor='cyan',
                               transform=ax14.get_transform('icrs'))                          
        ax14.add_patch(bshape)
        ax14.set_title('Model/Line') 
        ax14.plot([cxy[0]+10,cxy[0]+25],[cxy[1],cxy[1]],color="yellow")
        ax14.plot([cxy[0],cxy[0]],[cxy[1]+10,cxy[1]+25],color="yellow")                              

    #fig.tight_layout()
    
    
    fig.subplots_adjust(left=0.07,bottom=0.07,right=0.98,top=0.95)
    
    odir=os.path.dirname(fn)+'/pls_mom0xy'
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

    wd=fn.replace('data','imodrp*')

    flist=glob.glob(wd)
    
    if  len(flist)>0:
        
        fig=plt.figure(figsize=(8.,5.*len(flist))) 
        cc=0
        for fn0 in flist:
            print(fn0)
            cc=cc+1
            ax = fig.add_subplot(len(flist),1,cc)
            
            t=Table.read(fn0)
            ax.plot(t['sbrad'].data[0],t['sbprof'].data[0],color='black',label='S.B. (diff)')
            ymin,ymax=ax.get_ylim()
            
            cog=scipy.integrate.cumtrapz(t['sbprof'].data[0]*2.*np.pi*t['sbrad'].data[0],t['sbrad'].data[0],initial=0.)
            cog /= np.max(cog) 
            ax.plot(t['sbrad'].data[0],cog*ymax,linestyle='--',color='black',label='S.B. (cog)')
            
            ax.set_xlim(np.min(t['sbrad'].data[0]),np.max(t['sbrad'].data[0]))
            
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
            y1=t['vdis'].data[0]
            ax1.plot(x1,y1,color='red',label='Vdist')
            ax1.plot(t['vrad_node'].data[0],t['vdis_node'].data[0],marker='o',linestyle='none',color='red',mfc='none',label='Vdist-N')
            ax1.set_ylabel('Vrot/Vdis [km/s]')
        
            ax1.legend(loc="lower right")
        
        odir=os.path.dirname(fn)+'/pls_radprof'
        if not os.path.exists(odir):
            os.makedirs(odir)   
            
        fig.savefig(odir+'/'+os.path.basename(fn).replace('.fits','')+'.pdf') 

if  __name__=="__main__":

    pass


    
