import logging
import casacore.tables as ctb
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
from galario.single import apply_phase_vis 

logger = logging.getLogger(__name__)

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


