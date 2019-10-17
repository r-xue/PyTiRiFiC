import logging
import casacore.tables as ctb
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
from galario.single import apply_phase_vis 

from sys import getsizeof
from .gmake_utils import human_unit
from .gmake_utils import human_to_string

import astropy.units as u

logger = logging.getLogger(__name__)

def read_ms(vis='',
            polaverage=True,dataflag=True,saveflag=False,memorytable=True,
            dat_dct=None):
    
    if  dat_dct is None:
        dat_dct_out={}
    else:
        dat_dct_out=dat_dct    
    
    t=ctb.table(vis,ack=False,memorytable=memorytable)
    # set order='F' for the quick access of u/v/w 
    dat_dct_out['uvw@'+vis]=(t.getcol('UVW')).astype(np.float32,order='F')
    dat_dct_out['type@'+vis]='vis'
    
    if  polaverage==True:
        # assuming xx/yy, we decide to save data as stokes=I to reduce the data size by x2
        # then the data/weight in numpy as nrecord x nchan / nrecord
        dat_dct_out['data@'+vis]=np.mean(t.getcol('DATA'),axis=-1)
        dat_dct_out['weight@'+vis]=np.sum(t.getcol('WEIGHT'),axis=-1)
        if  dataflag==True:
            dat_dct_out['data@'+vis][np.where(np.any(t.getcol('FLAG'),axis=-1))]=np.nan
        if  saveflag==True:
            dat_dct_out['flag@'+vis]=np.any(t.getcol('FLAG'),axis=-1)         
    else:
        dat_dct_out['data@'+vis]=t.getcol('DATA')
        dat_dct_out['weight@'+vis]=t.getcol('WEIGHT')
        if  dataflag==True:
            dat_dct_out['data@'+vis][np.nonzero(t.getcol('FLAG')==True)]=np.nan
        if  saveflag==True:
            dat_dct_out['flag@'+vis]=t.getcol('FLAG')
    t.close()
    
    #   use the last spw in the SPECTRAL_WINDOW table
    ts=ctb.table(vis+'/SPECTRAL_WINDOW',ack=False)
    dat_dct_out['chanfreq@'+vis]=ts.getcol('CHAN_FREQ')[-1]
    dat_dct_out['chanwidth@'+vis]=ts.getcol('CHAN_WIDTH')[-1]
    ts.close()
    
    #   use the last field phasecenter in the FIELD table
    tf=ctb.table(vis+'/FIELD',ack=False) 
    phase_dir=tf.getcol('PHASE_DIR')
    tf.close()
    phase_dir=phase_dir[-1][0]
    phase_dir=np.rad2deg(phase_dir)
    if  phase_dir[0]<0:
        phase_dir[0]+=360.0
    dat_dct_out['phasecenter@'+vis]=phase_dir
    
    logger.debug('\nRead: '+vis+'\n')
    vars=['data','uvw','weight']
    for var in vars:
        if  var+'@'+vis not in dat_dct_out.keys():
            continue
        size=human_unit(getsizeof(dat_dct_out[var+'@'+vis])*u.byte)
        size=human_to_string(size,format_string='{0:3.0f} {1}')
        textout='{:60} {:20} {:20}'.format(
            var+'@'+vis,str(dat_dct_out[var+'@'+vis].shape),
            size)
        if  var=='weight':
            textout+=str(np.median(dat_dct_out['weight@'+vis]))
        logger.debug(textout)                                   
    
    key=['chanfreq','chanwidth']
    uts=['GHz','MHz']
    scale=[1e9,1e6]
    for ind in range(2):
        fmin=human_unit(np.min(dat_dct_out[key[ind]+'@'+vis])*u.Hz)
        fmax=human_unit(np.max(dat_dct_out[key[ind]+'@'+vis])*u.Hz)
        print(fmin,fmax)
        textout='{:60} {:20} {:10.4f} {:10.4f}'.format(
            'chanfreq@'+vis,
            str(dat_dct_out[key[ind]+'@'+vis].shape),
            fmin,fmax)
        logger.debug(textout)

    logger.debug('phasecenter@'+vis+'>>'+str(dat_dct_out['phasecenter@'+vis]))
    
    return dat_dct_out

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
    
    chan_wv=const.c/chan_freq
    
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


