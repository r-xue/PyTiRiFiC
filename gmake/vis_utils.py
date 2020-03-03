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
from astropy.io import fits
logger = logging.getLogger(__name__)
import os
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from galario.single import sampleImage
from .discretize import sample_prep
from .model import makepb

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
from casatasks import importfits

def read_ms(vis='',
             polaverage=True,dataflag=False,saveflag=True,
             nodata=False,
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
        
        
    nodata=True:
        only read the MS "framework" from MS, not the actual dataset
    
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
    if  nodata==False:
        dat_dct_out['data@'+vis]=(t.getcol('DATA')).T.astype(np.complex64,order='F')
    
    dat_dct_out['flag@'+vis]=(t.getcol('FLAG')).T
    if  dataflag==True:
        dat_dct_out['data@'+vis][dat_dct_out['flag@'+vis]==True]=np.nan  
    t.close()
    
    if  polaverage==True:
        dat_dct_out['data@'+vis]=np.mean(dat_dct_out['data@'+vis],axis=-1)
        dat_dct_out['weight@'+vis]=np.sum(dat_dct_out['weight@'+vis],axis=-1)
        dat_dct_out['flag@'+vis]=np.any(dat_dct_out['flag@'+vis],axis=-1)    
        
        for colname in ['data','weight','flag']:
            if  colname+'@'+vis in dat_dct_out:
                if  colname=='data':
                    dat_dct_out[colname+'@'+vis]=np.mean(dat_dct_out[colname+'@'+vis],axis=-1)
                if  colname=='flag':
                    dat_dct_out[colname+'@'+vis]=np.any(dat_dct_out[colname+'@'+vis],axis=-1)
                if  colname=='weight':
                    dat_dct_out[colname+'@'+vis]=np.sum(dat_dct_out[colname+'@'+vis],axis=-1)                    
    
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
    count_record=np.size(dat_dct_out['flag@'+vis])
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
            pickweight=np.broadcast_to(dat_dct_out['weight@'+vis][:,np.newaxis],dat_dct_out['flag@'+vis].shape)
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
        if  inputvis==vis:
            logger.debug("vis and inputvis must be different!")
            return          
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
        if  inputvis==vis:
            logger.debug("vis and inputvis must be different!")
            return          
        os.system("rm -rf "+vis)
        os.system('cp -rf '+inputvis+' '+vis)

    sm=simulator()    
    sm.openfromms(vis)
    sm.setnoise(mode=mode,simplenoise=simplenoise)
    sm.corrupt()
    sm.done()
    
    return                

def cpredict_ms(vis,
               fitsimage=None,inputvis=None,pbcor=True):
    """
    Using casatools.simulator to:
        + generate UV model from a FITS image with primary beam model applied
        + insert it into the data column of MS
        
    the fits image is expected to have the correct flux scaling (true flux)
    pbcor=True will do pbeam rescaling before sending images to FFT; 
        which assume fitsimage is in absolute flux scale
    """
    
    if  inputvis is not None:    
        if  inputvis==vis:
            logger.debug("vis and inputvis must be different!")
            return         
        os.system("rm -rf "+vis)
        os.system('cp -rf '+inputvis+' '+vis)    
    """
    data,header=fits.getdata('im.fits',header=True)
    data=np.expand_dims(data,axis=0)
    print(data.shape)
    fits.writeto('im.4d.fits',data,header,overwrite=True)
    """
    importfits(fitsimage,
               imagename=fitsimage.replace('.fits','.image'),
               overwrite=True,
               defaultaxes=True,defaultaxesvalues=[None,None,None,None])
    
    sm=simulator()
    sm.openfromms(vis)
    # this will look up vptable from ms metadata
    if  pbcor==True:
        sm.setvp(dovp=True,usedefaultvp=True,dosquint=True,pblimit=0.01)
    sm.predict(imagename=fitsimage.replace('.fits','.image'))
    sm.done
    
    return

def gpredict_ms(vis,
               fitsimage=None,inputvis=None,pb=None,pbaverage=True,antsize=None):
    """
    Using galario to:
        + generate UV model from a FITS image with primary beam model applied
        + insert it into the data column of MS
            
    the fits image is expected to have the correct flux scaling (true flux)
    
    ****pb is assumed to have the same WCS as fitsimage*****
    
    pb!=None or antsize!=None will do pbeam rescaling before sending images to FFT; 
        which assume fitsimage is in absolute flux scale    
    
    """
    if  inputvis is not None:   
        if  inputvis==vis:
            logger.debug("vis and inputvis must be different!")
            return 
        os.system("rm -rf "+vis)
        os.system('cp -rf '+inputvis+' '+vis)    
    
    im,header=fits.getdata(fitsimage,header=True)
    dat_dct=read_ms(vis=vis,nodata=True)
    uvw=dat_dct['uvw@'+vis]
    phasecenter=dat_dct['phasecenter@'+vis]
    uvweight=dat_dct['weight@'+vis]
    uvflag=dat_dct['flag@'+vis]
    
    w=WCS(header)
    naxis=w._naxis # this is x-y-z
    
    #   prep for sampleImage()    
    dRA,dDec,cell,wv=sample_prep(w,phasecenter)
    
    uvmodel=np.zeros((uvflag.shape)[0:2],dtype=np.complex64,order='F')
    
    if  pb is not None:
        pbeam=fits.getdata(pb,header=False)
        if  pbaverage==True:
            if  pbeam.ndim==3:
                pbeam=np.mean(pbeam,axis=(0))
            if  pbeam.ndim==4:
                pbeam=np.mean(pbeam,axis=(0,1))
    else:
        pbeam=None

    if  antsize is not None:
        # just one plane
        pbeam=makepb(header,phasecenter=phasecenter,antsize=antsize)
        
    for iz in range(naxis[2]):
        blank=True  
        
        if  pbeam is not None:
            if  pbeam.ndim==2:
                planepb=pbeam
            if  pbeam.ndim==3:
                planepb=pbeam[iz,:,:]
            if  pbeam.ndim==4:
                planepb=pbeam[0,iz,:,:]   
        else:
            planepb=1                
        
        if  im.ndim==2:
            plane=im*planepb
        if  im.ndim==3:
            plane=im[iz,:,:]*planepb
        if  im.ndim==4:
            plane=im[0,iz,:,:]*planepb         
        
        if  np.any(plane):
            blank=False
                  
        if  blank==False:
            uvmodel[:,iz]=sampleImage(plane.astype(np.float32),
                                  cell,
                                  (uvw[:,0]/wv[iz]),
                                  (uvw[:,1]/wv[iz]),                               
                                  dRA=dRA,dDec=dDec,
                                  PA=0.,check=False,origin='lower')
        
    write_ms(vis,uvmodel,datacolumn='data')
    
    return

    
if  __name__=="__main__":

    pass
 