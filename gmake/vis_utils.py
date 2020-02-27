import logging
from astropy import constants as const
import numpy as np

from galario.single import apply_phase_vis 

from .utils import human_unit
from .utils import human_to_string
from .utils import get_obj_size

import astropy.units as u
from astropy.coordinates import Angle
from ast import literal_eval    

logger = logging.getLogger(__name__)
import os

"""
ref: about taql:
    https://casacore.github.io/casacore-notes/199.html
ref:
     C-contiguous order (last index varies the fastest
     FORTRAN-contiguous order in memory (first index varies the fastest)
"""

# for instance constructed from classes, we use shorter names: tb, msmd, cb, etc...
# see at the end:
#    https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage
from casatools import table
from casatools import msmetadata
from casatools import calibrater
from casatools import simulator 

def read_ms(vis='',
             polaverage=True,dataflag=False,saveflag=True,
             dat_dct=None):
    """
    Note:
        the different output sequence
        casacore.table.getcol():     nrecord x nchan x ncorr
        casatools.table.getcol():    ncorr x nchan x nrecord
        
    dataflag: default=False
        set flagged data value to np.nan, which may lead to troubles of calculating chisq2
    saveflag: default=True
        save flagging (bool) column, which is need to figure out channel-wise bad data
        
    """
    
    if  dat_dct is None:
        dat_dct_out={}
    else:
        dat_dct_out=dat_dct    
    
    # set order='F' for the quick access of u/v/w seperately
    # assuming xx/yy, we decide to save data as stokes=I to reduce the data size by x2
    # then the data/weight in numpy as nrecord x nchan / nrecord    


    textout='\nREADing: '+vis
    logger.debug(textout)
    logger.debug('-'*len(textout))
        
    t=table()
    t.open(vis)    
    dat_dct_out['uvw@'+vis]=(t.getcol('UVW')).T.astype(np.float32,order='F')
    dat_dct_out['type@'+vis]='vis'
    # spectrum_weight is not considered here
    dat_dct_out['weight@'+vis]=(t.getcol('WEIGHT')).T.astype(np.float32,order='F')
    dat_dct_out['data@'+vis]=(t.getcol('DATA')).T.astype(np.complex64,order='F')
    dat_dct_out['flag@'+vis]=(t.getcol('FLAG')).T
    if  dataflag==True:
        dat_dct_out['data@'+vis][dat_dct_out['flag@'+vis]==True]=np.nan  
    t.close()
    
    if  polaverage==True:
        dat_dct_out['data@'+vis]=np.mean(dat_dct_out['data@'+vis],axis=-1)
        dat_dct_out['weight@'+vis]=np.sum(dat_dct_out['weight@'+vis],axis=-1)
        dat_dct_out['flag@'+vis]=np.any(dat_dct_out['flag@'+vis],axis=-1)    
    
    # flag all data with zero weight
    dat_dct_out['flag@'+vis][dat_dct_out['weight@'+vis]==0,:]=1
    # set weight=0 record with weight=1 for speeding log(wt)
    dat_dct_out['weight@'+vis][dat_dct_out['weight@'+vis]==0]=1
    
    #   use the "last" and "only" spw in the SPECTRAL_WINDOW table
    #   We don't handle mutipl-spw MS here.
    ts=table()
    ts.open(vis+'/SPECTRAL_WINDOW')
    dat_dct_out['chanfreq@'+vis]=ts.getcol('CHAN_FREQ')[:,-1]*u.Hz
    dat_dct_out['chanwidth@'+vis]=ts.getcol('CHAN_WIDTH')[:,-1]*u.Hz
    ts.close()
    
    #   use the "last" and "only" field phase center in the FIELD table
    
    mymsmd=msmetadata()
    mymsmd.open(vis)
    phasecenter=mymsmd.phasecenter(0)
    radec=[phasecenter['m0']['value'],phasecenter['m1']['value']]
    mymsmd.close()
    
    phase_dir=Angle(radec*u.rad).to(unit=u.deg)
    phase_dir[0]=phase_dir[0].wrap_at(360.0*u.deg)
    dat_dct_out['phasecenter@'+vis]=phase_dir    

    count_flag=np.count_nonzero(dat_dct_out['flag@'+vis])
    count_record=np.size(dat_dct_out['data@'+vis])
    logger.debug('flagging fraction: {0:.0%}'.format(count_flag*1./count_record))    

    
    vars=['data','uvw','weight','flag']
    for var in vars:
        if  saveflag==False and var=='flag':
            del dat_dct_out['flag@'+vis]        
        if  var+'@'+vis not in dat_dct_out.keys():
            continue
        size=human_unit(get_obj_size(dat_dct_out[var+'@'+vis])*u.byte)
        size=human_to_string(size,format_string='{0:3.0f} {1}')
        textout='{:60} {:15} {:20} {:20}'.format(
            var+'@'+vis,str(dat_dct_out[var+'@'+vis].dtype),str(dat_dct_out[var+'@'+vis].shape),
            size)
        if  var=='weight':
            pickweight=np.broadcast_to(dat_dct_out['weight@'+vis][:,np.newaxis],dat_dct_out['data@'+vis].shape)
            pickweight=pickweight[np.where(dat_dct_out['flag@'+vis]==False)]
            pt_select=[0,16,50,84,100]
            pt_level=np.percentile(pickweight,pt_select)
            for pt_ind in range(len(pt_select)):
                textout+='\n{:60} {:15} {:<20.0%} {:<20f}'.format('','ptile:',pt_select[pt_ind]*0.01,pt_level[pt_ind]) 
        logger.debug(textout)                                   
    
    vars=['chanfreq','chanwidth']
    for ind in range(2):
        tag=vars[ind]+'@'+vis
        if  tag not in dat_dct_out.keys():
            continue
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
    logger.debug('-'*118)

    if  dat_dct is None:
        return dat_dct_out
    else:
        return 

def write_ms(vis,value,
             datacolumn='corrected',inputvis=None):
    """
    attach new visibility data/model values into an MS
    
    if the specified datacolumn doesn't exist, it will be created on-the-fly.
    
    note:
        the input data shape is nrecord x nchan x ncorr following the rule in casacore.table.getcol(),
        which is reversed from casa6.casatools.table.getcol() (ncorr x nchan x nrecord)
        alternatively, ncrecord x nchan (stokes-I) is also fine and will be broadcasted to all correlations 
        (assumed to be RR, LL, XX, or YY) 
    
    """
    
    if  inputvis is not None:
        
        os.system("rm -rf "+vis)
        os.system('cp -rf '+inputvis+' '+vis)
    
    addcorr=addmodel=False
    if  datacolumn=='data':
        colname='DATA'
    if  datacolumn=='corrected':
        colname='CORRECTED_DATA'
        addcorr=True
    if  datacolumn=='model':
        colname='MODEL_DATA'
        addmodel=True
    
    tb=table()
    
    if  datacolumn=='corrected' or datacolumn=='model':    
        tb.open(vis)
        colnames=tb.colnames()
        tb.close()
        if  colnames.count(colname)==0:
            cb=calibrater()
            cb.open(vis,addcorr=addcorr,addmodel=addmodel)
            cb.close()
            
    tb.open(vis,nomodify=False)
    
    colshape=tb.getcolshapestring(colname)
    colshape=tuple(literal_eval(colshape[0]))+(len(colshape),)
    if  value.ndim<len(colshape):
        value_in=(value.T)[np.newaxis,:,:]
    else:
        value_in=(value.T)
        
    tb.putcol(colname,np.broadcast_to(value_in,colshape))
    tb.close()

    return 

def corrupt_ms(vis,
               mode='simplenoise',simplenoise='1mJy',
               inputvis=None):
    """
    use simulated tool
    """
    if  inputvis is not None:    
        os.system("rm -rf "+vis)
        os.system('cp -rf '+inputvis+' '+vis)

    sm=simulator()    
    sm.openfromms(vis)
    sm.setnoise(mode=mode,simplenoise=simplenoise)
    sm.corrupt()
    sm.done()
    
    return                
               

if  __name__=="__main__":

    pass
 