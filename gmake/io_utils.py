from .gmake_init import *
from .gmake_utils import *


logger = logging.getLogger(__name__)

def read_data(inp_dct,
              fill_mask=False,fill_error=False,                                   # for FITS/image
              memorytable=True,polaverage=True,dataflag=True,saveflag=False):     # for MS/visibilities
    """
    read FITS/image or MS/visibilities into the dictionary
    
        + we set data=
        
        note: 
              DATA column shape in nrecord x nchan x ncorr
              WEIGHT column shape in nrecord x ncorr( supposely this is the "average" value of WEIGHT_SPECTRUM along the channle-axis
              WEIGHT_SPECTRUM SHAPE in nrecord x nchan x ncorr
              FLAGS shape in nrecord x nchan x ncorr
              (so WEIGHT_SPECTRUM is likely ~WEIGHT/NCHAN?) depending on the data model / calibration script
              
              data@ms in complex64 (not complex128)
        
        For space-saving, we 
            + set DATA-values=np.nan when flag=True (so there is no a "flag" variable for flagging in dat_dct
            + when polaverage=True, we only derive stokes-I if both XX/YY (or RR/YY) are Good. If one of them are flagged, Data-Values set to np.nan
                this follows the principle in the tclean()/stokes parameter 
                https://casa.nrao.edu/casadocs-devel/stable/global-task-list/task_tclean/parameters
                http://casacore.github.io/casacore/StokesConverter_8h_source.html
            + weight doesn't include the channel-axis (assuming the channel-wise weight variable is neligible   
            
            XX=I+Q YY=I-Q ; RR=I+V LL=I-V => I=(XX+YY)/2 or (RR+LL)/2
                
    """
    
    dat_dct={}

    for tag in inp_dct.keys():
                                
        if  'vis' in inp_dct[tag].keys():
            
            obj=inp_dct[tag]
            vis_list=obj['vis'].split(",")
            
            for ind in range(len(vis_list)):
                
                if  ('data@'+vis_list[ind] not in dat_dct) and 'vis' in obj:
                    
    
                    t=ctb.table(vis_list[ind],ack=False,memorytable=memorytable)
                    # set order='F' for the quick access of u/v/w 
                    dat_dct['uvw@'+vis_list[ind]]=(t.getcol('UVW')).astype(np.float32,order='F')
                    dat_dct['type@'+vis_list[ind]]='vis'
                    
                    if  polaverage==True:
                        # assuming xx/yy, we decide to save data as stokes=I to reduce the data size by x2
                        # then the data/weight in numpy as nrecord x nchan / nrecord
                        dat_dct['data@'+vis_list[ind]]=np.mean(t.getcol('DATA'),axis=-1)
                        dat_dct['weight@'+vis_list[ind]]=np.sum(t.getcol('WEIGHT'),axis=-1)
                        if  dataflag==True:
                            dat_dct['data@'+vis_list[ind]][np.where(np.any(t.getcol('FLAG'),axis=-1))]=np.nan
                        if  saveflag==True:
                            dat_dct['flag@'+vis_list[ind]]=np.any(t.getcol('FLAG'),axis=-1)         
                    else:
                        dat_dct['data@'+vis_list[ind]]=t.getcol('DATA')
                        dat_dct['weight@'+vis_list[ind]]=t.getcol('WEIGHT')
                        if  dataflag==True:
                            dat_dct['data@'+vis_list[ind]][np.nonzero(t.getcol('FLAG')==True)]=np.nan
                        if  saveflag==True:
                            dat_dct['flag@'+vis_list[ind]]=t.getcol('FLAG')
                    t.close()
                    
                    #   use the last spw in the SPECTRAL_WINDOW table
                    ts=ctb.table(vis_list[ind]+'/SPECTRAL_WINDOW',ack=False)
                    dat_dct['chanfreq@'+vis_list[ind]]=ts.getcol('CHAN_FREQ')[-1]
                    dat_dct['chanwidth@'+vis_list[ind]]=ts.getcol('CHAN_WIDTH')[-1]
                    ts.close()
                    
                    #   use the last field phasecenter in the FIELD table
                    tf=ctb.table(vis_list[ind]+'/FIELD',ack=False) 
                    phase_dir=tf.getcol('PHASE_DIR')
                    tf.close()
                    phase_dir=phase_dir[-1][0]
                    phase_dir=np.rad2deg(phase_dir)
                    if  phase_dir[0]<0:
                        phase_dir[0]+=360.0
                    dat_dct['phasecenter@'+vis_list[ind]]=phase_dir
                    

                    logger.debug('\nloading: '+vis_list[ind]+'\n')
                    logger.debug('data@'+vis_list[ind]+'>>'+str(dat_dct['data@'+vis_list[ind]].shape)+str(convert_size(getsizeof(dat_dct['data@'+vis_list[ind]]))))
                    logger.debug('uvw@'+vis_list[ind]+'>>'+str(dat_dct['uvw@'+vis_list[ind]].shape)+str(convert_size(getsizeof(dat_dct['uvw@'+vis_list[ind]]))))
                    logger.debug('weight@'+vis_list[ind]+'>>'+\
                          str(dat_dct['weight@'+vis_list[ind]].shape)+str(convert_size(getsizeof(dat_dct['weight@'+vis_list[ind]])))+\
                          str(np.median(dat_dct['weight@'+vis_list[ind]])))
                    if  saveflag==True:
                        logger.debug('flag@'+vis_list[ind]+'>>'+\
                              str(dat_dct['flag@'+vis_list[ind]].shape)+str(convert_size(getsizeof(dat_dct['flag@'+vis_list[ind]])))+\
                              str(np.median(dat_dct['weight@'+vis_list[ind]])))                                      
                    logger.debug('chanfreq@'+vis_list[ind]+'>> [GHz]'+\
                          str(np.min(dat_dct['chanfreq@'+vis_list[ind]])/1e9)+\
                          str(np.max(dat_dct['chanfreq@'+vis_list[ind]])/1e9)+\
                          str(np.size(dat_dct['chanfreq@'+vis_list[ind]])))
                    logger.debug('chanwidth@'+vis_list[ind]+'>> [GHz]'+\
                          str(np.min(dat_dct['chanwidth@'+vis_list[ind]])/1e9)+\
                          str(np.max(dat_dct['chanwidth@'+vis_list[ind]])/1e9)+\
                          str(np.mean(dat_dct['chanwidth@'+vis_list[ind]])/1e9))
                    logger.debug('phasecenter@'+vis_list[ind]+'>>'+str(dat_dct['phasecenter@'+vis_list[ind]]))
                        
        if  'image' in inp_dct[tag].keys():
        
            obj=inp_dct[tag]
            im_list=obj['image'].split(",")
            if  'mask' in obj:
                mk_list=obj['mask'].split(",")
            if  'error' in obj:
                em_list=obj['error'].split(",")
            if  'sample' in obj:
                sp_list=obj['sample'].split(",")
            if  'psf' in obj:
                pf_list=obj['psf'].split(",")          
            
            
            if  'pmodel' in obj:
                
                data,hd=fits.getdata(obj['pmodel'],header=True,memmap=False) 
                dat_dct['pmodel@'+tag]=data
                dat_dct['pheader@'+tag]=hd                
                
                logger.debug('loading: '+obj['pmodel']+' to ')
                logger.debug('pmodel@'+tag)       
                logger.debug(str(data.shape)+str(convert_size(getsizeof(data))))              
            
            for ind in range(len(im_list)):
                
                if  ('data@'+im_list[ind] not in dat_dct) and 'image' in obj:
                    data,hd=fits.getdata(im_list[ind],header=True,memmap=False)
                    dat_dct['data@'+im_list[ind]]=data
                    dat_dct['header@'+im_list[ind]]=hd
                    dat_dct['type@'+im_list[ind]]='image'
                    
                    logger.debug('loading: '+im_list[ind]+' to ')
                    logger.debug('data@'+im_list[ind],'header@'+im_list[ind])
                    logger.debug(str(data.shape)+str(convert_size(getsizeof(data))))
                    
                if  ('error@'+im_list[ind] not in dat_dct) and 'error' in obj:
                    data=fits.getdata(em_list[ind],memmap=False)
                    dat_dct['error@'+im_list[ind]]=data
                    
                    logger.debug('loading: '+em_list[ind]+' to ')
                    logger.debug('error@'+im_list[ind])
                    logger.debug(str(data.shape)+str(convert_size(getsizeof(data))))
                    
                if  ('mask@'+im_list[ind] not in dat_dct) and 'mask' in obj:
                    data=fits.getdata(mk_list[ind],memmap=False)                
                    dat_dct['mask@'+im_list[ind]]=data
                    
                    logger.debug('loading: '+mk_list[ind]+' to ')
                    logger.debug('mask@'+im_list[ind])
                    logger.debug(str(data.shape)+str(convert_size(getsizeof(data))))
                if  ('sample@'+im_list[ind] not in dat_dct) and 'sample' in obj:
                    data=fits.getdata(sp_list[ind],memmap=False)                
                    # sp_index; 3xnp array (px index of sampling data points)
                    dat_dct['sample@'+im_list[ind]]=np.squeeze(data['sp_index'])
                    
                    logger.debug('loading: '+sp_list[ind]+' to ')
                    logger.debug('sample@'+im_list[ind])
                    logger.debug(str(data.shape)+str(convert_size(getsizeof(data))))
                if  ('psf@'+im_list[ind] not in dat_dct) and 'psf' in obj:
                    data=fits.getdata(pf_list[ind],memmap=False)                
                    dat_dct['psf@'+im_list[ind]]=data
                    logger.debug('loading: '+pf_list[ind]+' to ')
                    logger.debug('psf@'+im_list[ind])       
                    logger.debug(str(data.shape)+str(convert_size(getsizeof(data))))
                        
                     
                            
                tag='data@'+im_list[ind]
                
                if  fill_mask==True or fill_error==True:
                    if  (tag.replace('data@','mask@') not in dat_dct) and fill_mask==True:
                        data=dat_dct[tag]
                        dat_dct[tag.replace('data@','mask@')]=data*0.0+1.
                        logger.debug('fill '+tag.replace('data@','mask@')+str(1.0))
                    if  (tag.replace('data@','error@') not in dat_dct) and fill_error==True:
                        data=dat_dct[tag]
                        dat_dct[tag.replace('data@','error@')]=data*0.0+np.std(data)
                        logger.debug('fill '+tag.replace('data@','error@')+str(np.std(data)))                
  
    
    return dat_dct

def dct2fits(dct,outname='dct2fits',save_npy=False):
    """
        save a non-nested dictionary into a FITS binary table
        note:  not every Python object can be dumped into a FITS column, 
               e.g. a dictionary type can be aded into a column of a astropy/Table, but
               the Table can'be saved into FITS.
        example:
            gmake.dct2fits(dat_dct,save_npy=True)
    """
    

    t=Table()
    
    for key in dct:
        #   the value is wrapped into a one-element list
        #   so the saved FITS table will "technically" have one row.
        t.add_column(Column(name=key,data=[dct[key]]))
    t.write(outname+'.fits',overwrite=True)    
    if  save_npy==True:
        np.save(outname+'.npy',dct)

def add_uvmodel(vis,uvmodel,
                datacolumn='corrected',
                delwt=True,
                delmod=False,delcal=False):
    """
    + add corrected column to vis
    + remove model_data column in vis
    + remove imaging_weight in vis
    
    """
    
    ctb.addImagingColumns(vis, ack=False)
    #ctb.removeImagingColumns(vis)
    
    t=ctb.table(vis,ack=False,readonly=False)
    tmp=t.getcol('DATA')
    
    if  'corrected' in datacolumn.lower():
        t.putcol('CORRECTED_DATA',np.broadcast_to(uvmodel[:,:,np.newaxis],tmp.shape))
    if  'data' in datacolumn.lower():
        t.putcol('DATA',np.broadcast_to(uvmodel[:,:,np.newaxis],tmp.shape))
    if  'model' in datacolumn.lower():
        t.putcol('MODEL_DATA',np.broadcast_to(uvmodel[:,:,np.newaxis],tmp.shape))
                    
    #print('add_uvmodel',vis)
    #print(np.sum(uvmodel,axis=0))
    if  delwt==True:
        t.removecols('IMAGING_WEIGHT')
    if  delmod==True:
        t.removecols('MODEL_DATA')
    if  delcal==True:
        t.removecols('MODEL_DATA')
        t.removecols('CORRECTED_DATA')
    
    t.unlock()

    return 

def export_model(models,outdir='./',
                 includedata=False,
                 outname_exclude=None,outname_replace=None):
    """
        export a model set into FITS images or Measurement Sets
        shortname:    a string list to get rid of from the original data image name
        
    """
    for key in list(models.keys()): 
        
        if  'data@' not in key:
            continue

        
        if  models[key.replace('data@','type@')]=='vis':
        
            basename=key.replace('data@','')
            #   name string replacement
            if  outname_replace is not None:
                for ostring, rstring in outname_replace:
                    basename=basename.replace(ostring,rstring)
            #   name string exclusion
            if  outname_exclude is not None:
                for ostring in outname_exclude:
                    basename=basename.replace(ostring,'')            
            basename=os.path.basename(basename)
            logger.debug(" ")
            logger.debug('-->'+'data_'+basename)
            logger.debug(" ")
            
            if  not os.path.exists(outdir):
                os.makedirs(outdir)
            
            versions=['imodel','imod2d','imod3d']        
            hd=models[key.replace('data@','header@')]
            for version in versions:             
                if  key.replace('data@',version+'@') in models.keys():
                    if  models[key.replace('data@',version+'@')] is not None:
                        logger.debug(key.replace('data@',version+'@'))
                        tmp=(models[key.replace('data@',version+'@')]).copy()
                        if  tmp.ndim==2:
                            tmp=tmp[np.newaxis,np.newaxis,:,:]
                        fitsname=(outdir+'/'+version+'_'+basename).replace('.ms','.fits')
                        logger.debug("write reference model image: ")
                        logger.debug("    "+key.replace('data@',version+'@')+' to '+fitsname)
                        fits.writeto(fitsname,
                                     tmp,
                                     models[key.replace('data@','header@')],
                                     overwrite=True)
            
            for prof in list(models.keys()):
                
                if  'imod3d_prof@' in prof  and key.replace('data@','') in prof:
                    outname=prof.replace(key.replace('data@',''),'')
                    outname=outname.replace('imod3d_prof@','imodrp_').replace('@','_')
                    fitsname=outdir+'/'+outname+basename.replace('.ms','')   
                    logger.debug("write reference model profile: ")
                    logger.debug("    "+prof+' to '+fitsname+'.fits')
                    dct2fits(models[prof],outname=fitsname)
            
            ###############
            # data  -> data@outms                          
            # model -> corrected@outms                   
            # mod2d -> data@outms.contsub
            # mod3d -> corrected@outms.contsub
            ###############
            oldms=key.replace('data@','')
            newms=outdir+'/model_'+basename.replace('.ms','.ms')
            
            
            logger.debug("copy ms container: ")
            logger.debug("    "+oldms+'  to  '+newms)
            os.system("rm -rf "+newms)
            os.system('cp -rf '+oldms+' '+newms)
            logger.debug("write ms column: ")
            if  includedata==False:
                logger.debug("    "+key.replace('data@','uvmodel@')+' to '+'data@'+newms)
                add_uvmodel(newms,models[key.replace('data@','uvmodel@')],
                            datacolumn='data',delcal=True)
            else:
                logger.debug("    "+key.replace('data@','uvmodel@')+' to '+'corrected@'+newms)
                add_uvmodel(newms,models[key.replace('data@','uvmodel@')],
                            datacolumn='corrected',delmod=True)
            
            oldms_path=os.path.abspath(oldms)
            newms=outdir+'/data_'+basename.replace('.ms','.ms')
            logger.debug("create symlink:")
            logger.debug("    "+oldms_path+'  to  '+newms)
            os.system('rm -rf '+newms) 
            os.system('ln -s '+oldms_path+' '+newms)      
                        
            """
            newms=outdir+'/data_'+basename.replace('.ms','.ms.contsub')
            logger.debug("copy ms container: "+oldms+'  to  '+newms)
            os.system("rm -rf "+newms)
            os.system('cp -rf '+oldms+' '+newms)
            logger.debug("write ms column: "+key.replace('data@','uvmod3d@')+' to '+'corrected@'+newms)
            add_uvmodel(newms,models[key.replace('data@','uvmod3d@')],
                        datacolumn='corrected',delmod=False)
            logger.debug("write ms column: "+key.replace('data@','uvmod2d@')+' to '+'data@'+newms)
            add_uvmodel(newms,models[key.replace('data@','uvmod2d@')],
                        datacolumn='data',delmod=True)
            """
            
            #add_uvmodel(newms,models[key.replace('data@','uvmod3d@')])             
            
            
            #logger.debug("copy "+key.replace('data@','uvmod2d@')+' to '+'model@'+newms)
            #add_uvmodel(newms,models[key.replace('data@','uvmod2d@')],
            #            datacolumn='model')
            #logger.debug("copy "+key.replace('data@','uvmod3d@')+' to '+'corrected@'+newms)
            #add_uvmodel(newms,models[key.replace('data@','uvmod3d@')],
            #            datacolumn='corrected')            
            
            #newms=outdir+'/data_'+basename.replace('.fits','.ms.cont')
            #logger.debug("copy "+oldms+'  to  '+newms)
            #os.system("rm -rf "+newms)
            #os.system('cp -rf '+oldms+' '+newms)
            #add_uvmodel(newms,models[key.replace('data@','uvmod2d@')])         
            
            #newms=outdir+'/data_'+basename.replace('.fits','.ms.contsub')
            #logger.debug("copy "+oldms+'  to  '+newms)
            #os.system("rm -rf "+newms)
            #os.system('cp -rf '+oldms+' '+newms)
            #add_uvmodel(newms,models[key.replace('data@','uvmod3d@')])       
            
        if  models[key.replace('data@','type@')]=='image':
            
            basename=key.replace('data@','')
            #   name string replacement
            if  outname_replace is not None:
                for ostring, rstring in outname_replace:
                    basename=basename.replace(ostring,rstring)
            #   name string exclusion
            if  outname_exclude is not None:
                for ostring in outname_exclude:
                    basename=basename.replace(ostring,'')            
            basename=os.path.basename(basename)
            
            logger.debug('-->data_'+basename)
            
            if  not os.path.exists(outdir):
                os.makedirs(outdir)
            versions=['data','imodel','cmodel','error','mask','kernel','psf','residual',
                      'imod2d','imod3d','cmod2d','cmod3d']
            hd=models[key.replace('data@','header@')]
            for version in versions:
                if  version=='residual' and key.replace('data@','cmodel@') in models.keys():
                    if  models[key.replace('data@','cmodel@')] is not None:
                        fits.writeto(outdir+'/'+version+'_'+basename,
                                     models[key]-models[key.replace('data@','cmodel@')],
                                     models[key.replace('data@','header@')],
                                     overwrite=True)                
                if  key.replace('data@',version+'@') in models.keys():
                    if  models[key.replace('data@',version+'@')] is not None:
                        tmp=(models[key.replace('data@',version+'@')]).copy()
                        if  tmp.ndim==2:
                            tmp=tmp[np.newaxis,np.newaxis,:,:]
                        fits.writeto(outdir+'/'+version+'_'+basename,
                                     tmp,
                                     models[key.replace('data@','header@')],
                                     overwrite=True)
            
            for prof in list(models.keys()):
                
                if  'imod3d_prof@' in prof  and key.replace('data@','') in prof:
    
                    outname=prof.replace(key.replace('data@',''),'')
                    outname=outname.replace('imod3d_prof@','imodel_').replace('@','_')
                    dct2fits(models[prof],outname=outdir+'/'+outname+basename.replace('.fits','.rp'))            
        

    np.save(outdir+'/'+'mod_dct.npy',models['mod_dct'])