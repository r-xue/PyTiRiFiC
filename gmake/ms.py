import logging
import casacore.tables as ctb
#import scipy.constants as const
from astropy import constants as const
import numpy as np

from galario.single import apply_phase_vis 

from sys import getsizeof
from .utils import human_unit
from .utils import human_to_string

import astropy.units as u
from astropy.coordinates import Angle


logger = logging.getLogger(__name__)

#from memory_profiler import profile
#from copy import deepcopy
#import numexpr as ne

def getcolnp(t,colname):
    """
    use casacore.table.getcolnp rather than casacore.table.getcol()
    to reduce the memory footprint
    
    this is a drop-in replacement for table.getcol() without memory comsumption spike:
    
    #https://github.com/casacore/python-casacore/issues/9
    #https://github.com/casacore/python-casacore/issues/38
    #https://github.com/casacore/python-casacore/issues/130
    getslicenp/getcolnp/getcellnp
    
    the below calls should give the same results beside the peak memory comsumption  different
        
        getcolnp(t,'DATA')
        vs.
        t.getcol('DATA') 
    
    in-place like operation
    for more complicated case, you probally want to use tqsl
    """
    record0=t.getcell(colname,0)
    arr=np.empty(shape=(t.nrows(),)+record0.shape,dtype=record0.dtype)
    t.getcolnp(colname,arr)
    
    return arr
       
#@profile
def read_ms(vis='',
            polaverage=True,dataflag=False,saveflag=False,memorytable=False,
            dat_dct=None):
    """
    Read a Measurement Set into a Dictionary only containing useful UV variables.
    
    vis:           MS file name
        We assume that only a single field/spw exist in this MS, so the MS needs to 
        be carefully prepared.
    
    polaverage:    True
        averging different polarization variable to reduce data size by 2
    dataflag:      True
        set the flagged chan-vis to np.nan (so no extra flag array is needed)
    saveflag:      False
        save the flag array
    
    dat_dct:       pre-defined container for saving memory usages. 
    
    
    DATA:    nrecord x nchan
    UVW:     nrecord x 3
    WEIGHT:  nrecord,
    
    note:
        currently, the implemetation may not work for MS with flagging uneven across the spectrum domain:
        use checkchflag to check the channel-wise flagging consistancy
    
    make sure:
        the flagging/missing data doesn't lead to chi^2=Nan
        UVW is valid
        
    """
    
    if  dat_dct is None:
        dat_dct_out={}
    else:
        dat_dct_out=dat_dct    
    
    # set order='F' for the quick access of u/v/w seperately
    # assuming xx/yy, we decide to save data as stokes=I to reduce the data size by x2
    # then the data/weight in numpy as nrecord x nchan / nrecord    
    
    
    with ctb.table(vis,ack=False,memorytable=memorytable) as t:
        
        dat_dct_out['uvw@'+vis]=(t.getcol('UVW')).astype(np.float32,order='F')
        dat_dct_out['type@'+vis]='vis'
        
        if  polaverage==False:
            dat_dct_out['data@'+vis]=getcolnp(t,'DATA')
            dat_dct_out['weight@'+vis]=getcolnp(t,'WEIGHT')
        else:
            tmp=ctb.taql('SELECT means(DATA,1) as DATA_I C4 from $t')
            dat_dct_out['data@'+vis]=getcolnp(tmp,'DATA_I')
            tmp.done()
            # the WEIGHT value is a single channel weight (not the bandwidth weight)
            # the mstransform() opertation will do the WEIGHT summming when do channel 
            # averging in my data prep procedure
            # 
            # the above imlememntation requires avaiable memory of 1xdata
            # the below will requires memort of 2.0xdata 
            #dat_dct_out['data@'+vis]=np.mean(getcolnp(t,'DATA'),axis=-1)    
            dat_dct_out['weight@'+vis]=np.sum(getcolnp(t,'WEIGHT'),axis=-1)          

        
        
        #if  dataflag==True:
        #    dat_dct_out['data@'+vis][np.nonzero(t.getcol('FLAG')==True)]=np.nan
        #if  saveflag==True:
        #    dat_dct_out['flag@'+vis]=t.getcol('FLAG')
        
        if  polaverage==True:       
            if  saveflag==True:
                dat_dct_out['flag@'+vis]=np.any(dat_dct_out['flag@'+vis],axis=-1)
        
    
    #   for auto-corr uvw=[0,0,0], which will not work right now
    
    """
    #   mstransform.timeaverging data may show some short-integration record with uvw set to = [0,0,0]
    irecord_bad=np.where(dat_dct_out['uvw@'+vis][:,0]==0)

    dat_dct_out['data@'+vis]=np.delete(dat_dct_out['data@'+vis],irecord_bad,axis=0)
    dat_dct_out['weight@'+vis]=np.delete(dat_dct_out['weight@'+vis],irecord_bad,axis=0)
    dat_dct_out['uvw@'+vis]=np.delete(dat_dct_out['uvw@'+vis],irecord_bad,axis=0)
    if  saveflag==True:
        dat_dct_out['flag@'+vis]=np.delete(dat_dct_out['flag@'+vis],irecord_bad,axis=0)
    #dat_dct_out['@'+vis]=np.delete(dat_dct_out['data@'+vis],irecord_bad,axis=0)
    """
    
    #   use the "last" and "only" spw in the SPECTRAL_WINDOW table
    #   We don't handle mutipl-spw MS here.
    
    ts=ctb.table(vis+'/SPECTRAL_WINDOW',ack=False)
    dat_dct_out['chanfreq@'+vis]=ts.getcol('CHAN_FREQ')[-1]*u.Hz
    dat_dct_out['chanwidth@'+vis]=ts.getcol('CHAN_WIDTH')[-1]*u.Hz
    ts.close()
    
    #   use the "last" and "only" field phase center in the FIELD table
    
    tf=ctb.table(vis+'/FIELD',ack=False) 
    phase_dir=tf.getcol('PHASE_DIR')
    tf.close()
    phase_dir=phase_dir[-1][0]
    phase_dir=Angle(phase_dir*u.rad).to(unit=u.deg)
    phase_dir[0]=phase_dir[0].wrap_at(360.0*u.deg)
    dat_dct_out['phasecenter@'+vis]=phase_dir
    #np.rad2deg(phase_dir)
    #if  phase_dir[0]<0:
    #    phase_dir[0]+=360.0    
    
    
    #"""
    logger.debug('\nRead: '+vis+'\n')
    vars=['data','uvw','weight']
    for var in vars:
        if  var+'@'+vis not in dat_dct_out.keys():
            continue
        #print(getsizeof(dat_dct_out[var+'@'+vis])*u.byte)
        size=human_unit(getsizeof(dat_dct_out[var+'@'+vis])*u.byte)
        size=human_to_string(size,format_string='{0:3.0f} {1}')
        textout='{:60} {:15} {:20} {:20}'.format(
            var+'@'+vis,str(dat_dct_out[var+'@'+vis].dtype),str(dat_dct_out[var+'@'+vis].shape),
            size)
        if  var=='weight':
            textout+='\n  >>percentiles (0,16,50,84,100)%: '+str(np.percentile(dat_dct_out['weight@'+vis],[0,16,50,84,100]))
        logger.debug(textout)                                   
    
    vars=['chanfreq','chanwidth']
    for ind in range(2):
        tag=vars[ind]+'@'+vis
        textout='{:60} {:10} {:10.4f} {:10.4f}'.format(
            tag,
            str(dat_dct_out[tag].shape),
            human_unit(np.min(dat_dct_out[tag])),
            human_unit(np.max(dat_dct_out[tag])))
        logger.debug(textout)

    radec=phase_dir[0].to_string(unit=u.hr,sep='hms') # print(phase_dir[0].hms)
    radec+='  '
    radec+=phase_dir[1].to_string(unit=u.degree,sep='dms') # print(phase_dir[1].dms)
    
    logger.debug('{:60} {:10}'.format('phasecenter@'+vis,radec))
    #"""
    
    
    
    
    if  dataflag==True:
        count_flag=np.count_nonzero(np.isnan(dat_dct_out['data@'+vis]))
        count_record=np.size(dat_dct_out['data@'+vis])
        logger.debug('data flagging fraction: {}'.format(count_flag*1./count_record))
    
    return


    

def ms_read(vis,datacolumn='corrected',
          figname=None):
    """
    Annular averages a uv dataset in bins, return and plots results.
    mimicking the function of miriad/uvamp
    note:    
        uvdist_kl:     np.array    klambda
        uvw:                       meter 
        uvdata:        np.array    Jy
    """
    
    
    tm=ctb.table(vis)
    if  'corrected' in datacolumn.lower():
        uvdata=tm.getcol('CORRECTED_DATA')
    if  'data' in datacolumn.lower():
        uvdata=tm.getcol('DATA')        
    if  'model' in datacolumn.lower():
        uvdata=tm.getcol('MODEL_DATA')
    logger.debug(str(uvdata.shape))
    
    uvw=tm.getcol('UVW').astype(np.float32)     # in meter nrecord x 3 -> float32 for galario.single
    weight=tm.getcol('WEIGHT')                  # ideally, 1/sigma^2, or in 1/Jy^2
    
    ts=ctb.table(vis+'/SPECTRAL_WINDOW')
    chan_freq=ts.getcol('CHAN_FREQ')    # nspw x nchan
    chan_freq=chan_freq[0]              # nchan

    #logger.debug(str(chan_freq.shape))
    #logger.debug(str(uvw.shape))
    
    chan_wv=const.c.value/chan_freq
    
    nrecord=(uvw.shape)[0]
    nchan=(chan_freq.shape)[0]
    ncorr=(uvdata.shape)[2]

    uvw_kl=np.broadcast_to(uvw[:,np.newaxis,:],(nrecord,nchan,3))/np.broadcast_to(chan_wv[np.newaxis,:,np.newaxis]*1e3,(nrecord,nchan,3))
    #logger.debug(str(uvw_kl.shape))
    
    #   uvdata.shape:                   # nrecord x nchan x ncorr
    #   uvw_kl.shape:                   # nrecord x nchan x 3
    
    return (uvw_kl,uvdata)


 

if  __name__=="__main__":

    pass


