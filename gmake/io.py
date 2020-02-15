from .vis_utils import read_ms
#from .ms import read_ms0
from sys import getsizeof
import logging
import time
from .utils import *
import os
from astropy.io import fits 
from astropy.table import Table
from astropy.table import Column
from .vis_utils import write_ms

logger = logging.getLogger(__name__)


import warnings
import hickle as hkl
from hickle.hickle import SerializedWarning   
warnings.filterwarnings("ignore",category=SerializedWarning)  

#from memory_profiler import profile
#@profile
def read_data(inp_dct,
              save_data=False,
              fill_mask=False,fill_error=False,                                   # for FITS/image
              polaverage=True,dataflag=False,saveflag=True):     # for MS/visibilities
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
    logger.info('read data (may take some time..)')
    start_time = time.time()    
    
    dat_dct={}

    for tag in inp_dct.keys():
                                
        if  'vis' in inp_dct[tag].keys():
            
            obj=inp_dct[tag]
            vis_list=obj['vis'].split(",")
            
            for ind in range(len(vis_list)):
                
                if  ('data@'+vis_list[ind] not in dat_dct) and 'vis' in obj:
                    
                    read_ms(vis_list[ind],
                            polaverage=polaverage,dataflag=dataflag,saveflag=saveflag,
                            dat_dct=dat_dct)
                        
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
                if  isinstance(obj['psf'],str):
                    pf_list=obj['psf'].split(",")          
                else:
                    if  isinstance(obj['psf'],tuple):
                        pf_list=[]
                        pf_list.append(obj['psf'])
                    else:
                        pf_list=obj['psf']
                        
            if  'pmodel' in obj:
                
                data,hd=fits.getdata(obj['pmodel'],header=True,memmap=False) 
                dat_dct['pmodel@'+tag]=data
                dat_dct['pheader@'+tag]=hd                
                
                logger.debug('loading: '+obj['pmodel']+' to ')
                logger.debug('pmodel@'+tag)       
                logger.debug(str(data.shape)+str(human_unit(getsizeof(data)*u.byte)))              

            for ind in range(len(im_list)):
                
                if  ('data@'+im_list[ind] not in dat_dct) and 'image' in obj:
                    data,hd=fits.getdata(im_list[ind],header=True,memmap=False)
                    dat_dct['data@'+im_list[ind]]=data
                    dat_dct['header@'+im_list[ind]]=hd
                    dat_dct['type@'+im_list[ind]]='image'
                    
                    logger.debug('loading: '+im_list[ind]+' to ')
                    logger.debug('data@'+im_list[ind]+' '+'header@'+im_list[ind])
                    logger.debug(str(data.shape)+str(human_unit(getsizeof(data)*u.byte)))
                    
                if  ('error@'+im_list[ind] not in dat_dct) and 'error' in obj:
                    data=fits.getdata(em_list[ind],memmap=False)
                    dat_dct['error@'+im_list[ind]]=data
                    
                    logger.debug('loading: '+em_list[ind]+' to ')
                    logger.debug('error@'+im_list[ind])
                    logger.debug(str(data.shape)+str(human_unit(getsizeof(data)*u.byte)))
                    
                if  ('mask@'+im_list[ind] not in dat_dct) and 'mask' in obj:
                    data=fits.getdata(mk_list[ind],memmap=False)                
                    dat_dct['mask@'+im_list[ind]]=data
                    
                    logger.debug('loading: '+mk_list[ind]+' to ')
                    logger.debug('mask@'+im_list[ind])
                    logger.debug(str(data.shape)+str(human_unit(getsizeof(data)*u.byte)))
                if  ('sample@'+im_list[ind] not in dat_dct) and 'sample' in obj:
                    data=fits.getdata(sp_list[ind],memmap=False)                
                    # sp_index; 3xnp array (px index of sampling data points)
                    dat_dct['sample@'+im_list[ind]]=np.squeeze(data['sp_index'])
                    
                    logger.debug('loading: '+sp_list[ind]+' to ')
                    logger.debug('sample@'+im_list[ind])
                    logger.debug(str(data.shape)+str(human_unit(getsizeof(data)*u.byte)))
                if  ('psf@'+im_list[ind] not in dat_dct) and 'psf' in obj:
                    if  isinstance(pf_list[ind],str):
                        data=fits.getdata(pf_list[ind],memmap=False)                
                        dat_dct['psf@'+im_list[ind]]=data
                        logger.debug('loading: '+pf_list[ind]+' to ')
                        logger.debug('psf@'+im_list[ind])       
                        logger.debug(str(data.shape)+str(human_unit(getsizeof(data)*u.byte)))
                    else:
                        dat_dct['psf@'+im_list[ind]]=pf_list[ind]
                     
                            
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
                        
                        
    
    logger.info('-'*80)
    dat_size=human_unit(get_obj_size(dat_dct)*u.byte)
    
    logger.info("--- dat_dct size {:0.2f} ---".format(dat_size))
    logger.info("--- took {0:<8.5f} seconds ---".format(time.time()-start_time))
    
    
    if  save_data==True:
        outdir='./'
        if  'general' in inp_dct:
            if  'outdir' in inp_dct['general']:
                outdir=inp_dct['general']['outdir']+'/'
        hkl.dump(dat_dct, outdir+'dat_dct.h5', mode='w')
        logger.info('--- save to: '+outdir+'dat_dct.h5')
    
    
    return dat_dct

def dct2npy(dct,outname='dct2npy'):
    np.save(outname+'.npy',dct)
    return

def npy2dct(npyname):
    return np.load(npyname,allow_pickle=True).item()
    
def dct2hdf(dct,outname='dct2hdf'):
    """
    write a Python dictionary object into a HDF5 file.
    slashes are not allowed in HDF5 object names
    We repalce any "/" in keys with "|" to avoid a confusion with HDF5 internal structures
    """
    
    
    dct0=dct.copy()
    keys=list(dct0.keys())
    for key in keys:
        if  '/' in key:
            dct0[key.replace('/','|')]=dct0.pop(key)
    outpath=outname
    if  outname.endswith('.h5') or outname.endswith('.hdf5'):
        outpath=outname
    else:
        outpath=outname+'.h5'
    hkl.dump(dct0, outpath, mode='w')#,compression='gzip')      
    logger.info('--- save to: '+outpath)
    
    return

def hdf2dct(hdf):
    """
    read a Python dictionary object from a HDF5 file
    slashes are not allowed in HDF5 object names
    We repalce any "|" in keys with "/" to recover the potential file directory paths in keysst   
    """
    dct=hkl.load(hdf)
    keys=list(dct.keys())
    for key in keys:
        if  '|' in key:
            dct[key.replace('|','/')]=dct.pop(key)    
    
    return dct

    
def fits2dct(fits):
    """
    read a fits table into a none-nested dictionary
    the fits table must be the "1-row" version from gmake.dct2fits 
    
    References
      + about FITS byteorder: https://github.com/astropy/astropy/issues/4069
    
    note: we decide to save dct to HDF5 by default for a couple of reasons from now.
          FITS is always stored in big-endian byte order, will cause some troubles with casacore/galario
          I/O performance is worse
          The "table" approach doesn't support nesting / DatType may changed during the dct2fits->fits2dct process
          
    """
    t=Table()
    tb=t.read(fits)
    sys_byteorder = ('>', '<')[sys.byteorder == 'little']

    dct={}
    for col in tb.colnames:
        dct[col]=(tb[col][0])
        try:
            dorder=dct[col].dtype.byteorder
            if  dorder not in ('=', sys_byteorder):
                dct[col]=dct[col].byteswap().newbyteorder(sys_byteorder)        
        except:
            pass
        #try:
        #    
        #    #col,type(dct[col].dtype.byteorder),len(dct[col].dtype.byteorder))
        #
        #except:
        #    pass
    
    return dct 

def dct2fits(dct,outname='dct2fits'):
    """
        save a non-nested dictionary into a FITS binary table
        note:  not every Python object can be dumped into a FITS column, 
               e.g. a dictionary type can be aded into a column of a astropy/Table, but
               the Table can'be saved into FITS.
        example:
            gmake.dct2fits(dat_dct,save_npy=True)
        for npy np.save(outname.replace('.fits','.npy'),dct)
        
    note: we decide to save dct to HDF5 by default for a couple of reasons from now.
          FITS is always stored in big-endian byte order, will cause some troubles with casacore/galario
          I/O performance is worse
          The "table" approach doesn't support nesting / DatType may changed during the dct2fits->fits2dct process        
    """
    
    t=Table()
    
    for key in dct:
        #   the value is wrapped into a one-element list
        #   so the saved FITS table will "technically" have one row.
        t.add_column(Column(name=key,data=[dct[key]]))
    if  outname.endswith('.fits'):
        outname_full=outname
    else:
        outname_full=outname+'.fits'
    t.write(outname_full,overwrite=True)    

    
    return



def export_model(models,outdir='./',
                 includedata=False,
                 outname_exclude=None,outname_replace=None):
    """
        export a model set into FITS images or Measurement Sets
        shortname:    a string list to get rid of from the original data image name
        
    """
    logger.info('export the model set: {0:^50}'.format(outdir)+' (may take some time..)')
    start_time = time.time()
    
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
            
            versions=['imodel','imod2d','imod3d','pbeam']        
            hd=models[key.replace('data@','header@')]
            for version in versions:             
                if  key.replace('data@',version+'@') in models.keys():
                    if  models[key.replace('data@',version+'@')] is not None:
                        logger.debug(key.replace('data@',version+'@'))
                        tmp=(models[key.replace('data@',version+'@')]).copy()
                        if  tmp.ndim==2:
                            tmp=tmp[np.newaxis,np.newaxis,:,:]
                        fitsname=outdir+'/'+version+'_'+basename+'.fits'
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
                    fitsname=outdir+'/'+outname+basename+'.fits'   
                    logger.debug("write reference model profile: ")
                    logger.debug("    "+prof+' to '+fitsname)
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
                write_ms(newms,models[key.replace('data@','uvmodel@')],
                            datacolumn='data')
            else:
                logger.debug("    "+key.replace('data@','uvmodel@')+' to '+'corrected@'+newms)
                write_ms(newms,models[key.replace('data@','uvmodel@')],
                            datacolumn='corrected')
            
            oldms_path=os.path.abspath(oldms)
            newms=outdir+'/data_'+basename
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
            write_ms(newms,models[key.replace('data@','uvmod3d@')],
                        datacolumn='corrected',delmod=False)
            logger.debug("write ms column: "+key.replace('data@','uvmod2d@')+' to '+'data@'+newms)
            write_ms(newms,models[key.replace('data@','uvmod2d@')],
                        datacolumn='data',delmod=True)
            """
            
            #write_ms(newms,models[key.replace('data@','uvmod3d@')])             
            
            
            #logger.debug("copy "+key.replace('data@','uvmod2d@')+' to '+'model@'+newms)
            #write_ms(newms,models[key.replace('data@','uvmod2d@')],
            #            datacolumn='model')
            #logger.debug("copy "+key.replace('data@','uvmod3d@')+' to '+'corrected@'+newms)
            #write_ms(newms,models[key.replace('data@','uvmod3d@')],
            #            datacolumn='corrected')            
            
            #newms=outdir+'/data_'+basename.replace('.fits','.ms.cont')
            #logger.debug("copy "+oldms+'  to  '+newms)
            #os.system("rm -rf "+newms)
            #os.system('cp -rf '+oldms+' '+newms)
            #write_ms(newms,models[key.replace('data@','uvmod2d@')])         
            
            #newms=outdir+'/data_'+basename.replace('.fits','.ms.contsub')
            #logger.debug("copy "+oldms+'  to  '+newms)
            #os.system("rm -rf "+newms)
            #os.system('cp -rf '+oldms+' '+newms)
            #write_ms(newms,models[key.replace('data@','uvmod3d@')])       
            
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
    
    logger.info('-'*80)
    logger.info("--- took {0:<8.5f} seconds ---".format(time.time()-start_time))

    
    