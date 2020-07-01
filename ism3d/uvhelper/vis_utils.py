import logging
from astropy import constants as const
import numpy as np


from .utils import human_unit,human_to_string,get_obj_size,paste_array

import astropy.units as u
from astropy.coordinates import Angle
from ast import literal_eval    
from astropy.io import fits
logger = logging.getLogger(__name__)
import os
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales 
from astropy.coordinates import SkyCoord

from .uvhelper.proc import rmColumns

from .discretize import sample_prep,uv_sample,pickplane
from .model import makepb,advise_imsize

import numexpr as ne
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


def corrupt_ms(vis,
               mode='simplenoise',simplenoise='1mJy',
               inputvis=None,delscratch=True):
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
    
    if  delscratch==True:
        rmColumns(vis,column='MODEL_DATA')
        rmColumns(vis,column='CORRECTED_DATA')
            
    return                

def cpredict_ms(vis,
               fitsimage=None,inputvis=None,pbcor=True,delscratch=True):
    """
    Using casatools.simulator to:
        + generate UV model from a FITS image with primary beam model applied
        + insert it into the data column of MS
        
    the fits image is expected to have the correct flux scaling (true flux)
    pbcor=True will do pbeam rescaling before sending images to FFT; 
        which assume fitsimage is in absolute flux scale
        
    it DOES check interm of frequency gridding
    
    """
    
    if  inputvis is not None:    
        if  inputvis==vis:
            logger.debug("vis and inputvis must be different!")
            return         
        os.system("rm -rf "+vis)
        os.system('cp -rf '+inputvis+' '+vis)
        os.system('rm -rf '+vis+'/dm*fits')    
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
    
    if  delscratch==True:
        rmColumns(vis,column='MODEL_DATA')
        rmColumns(vis,column='CORRECTED_DATA')
        os.system("rm -rf "+fitsimage.replace('.fits','.image'))
    return

def gpredict_ms(vis,fitsimage=None,inputvis=None,pb=None,pbaverage=True,antsize=None,
                method='nufft',ik=5,saveuvgrid=False):
    """
    Using galario to:
        + generate UV model from a FITS image with primary beam model applied
        + insert it into the data column of MS
            
    the fits image is expected to have the correct flux scaling (true flux)
    
    ****pb is assumed to have the same WCS as fitsimage*****
    
    pb!=None or antsize!=None will do pbeam rescaling before sending images to FFT; 
        which assume fitsimage is in absolute flux scale    
    
    it doesn't check interm of frequency gridding
    
    fitsimage:    a list of string or string
    
    
    """
    if  inputvis is not None:   
        if  inputvis==vis:
            logger.debug("vis and inputvis must be different!")
            return 
        os.system("rm -rf "+vis)
        os.system('cp -rf '+inputvis+' '+vis)    
    
    #   READ MS
    
    dat_dct=read_ms(vis=vis,nodata=True)
    uvw=dat_dct['uvw@'+vis]
    phasecenter=dat_dct['phasecenter@'+vis]
    uvweight=dat_dct['weight@'+vis]
    uvflag=dat_dct['flag@'+vis]
    chanfreq=dat_dct['chanfreq@'+vis]
    chanwidth=dat_dct['chanwidth@'+vis]
    wv=chanfreq.to(u.m,equivalencies=u.spectral()).value    # in m
    uvshape=(uvflag.shape)[0:2]
    
    uvmodel=np.zeros((uvflag.shape)[0:2],dtype=np.complex128,order='F')
    
    #   READ MODEL IMAGE
    
    fitsimage_list=list()
    if  isinstance(fitsimage,list):
        fitsimage_list=fitsimage
    else:
        fitsimage_list=[fitsimage]
        
    #   Transform Each Image
    
    for fitsimage0 in fitsimage_list:
         
        im,header=fits.getdata(fitsimage0,header=True)
        w=WCS(header)
        naxis=w._naxis # this is x-y-z    
            
        #   prep for uv_sample()
        
        dRA,dDec,cell,wv_image=sample_prep(w,phasecenter)
        
        print("Image Property: ",fitsimage0)
        print("Phasecenter vs. Image center: ",np.rad2deg(dRA)*3600,np.rad2deg(dDec)*3600)
        print("Image Cell Size: ",np.rad2deg(cell)*3600)
        print("Image Dimension: ",naxis)
        print("Image Wavelength:",wv_image)
        
        iz=int(uvshape[1]/2)
        f_max=2.5
        f_max=2.0
        f_min=5.0
        f_min=2.0
        pbrad=1.22*wv[iz]/25*1.0
        pbrad=0.0
        nxy, dxy = get_image_size(uvw[:,0]/wv[iz], uvw[:,1]/wv[iz],
                                  pb=pbrad,f_max=f_max,f_min=f_min)    
        print("UVW uvw shape:       [nrecord]", uvw.shape)
        print("UVW Sugguested nxy:  [npixel]:", nxy)
        print("UVW Sugguested cell  [arcsec]:", np.rad2deg(dxy)*3600)
        print("UVW UVModel Wavelength:",wv)
        
        if  pb is not None:
            pbeam=fits.getdata(pb,header=False)
            pbeam=np.nan_to_num(pbeam,nan=0.0)
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
        
        for iz in range(uvshape[1]):
            blank=True  
            
            if  pbeam is not None:
                planepb=pickplane(pbeam,iz)  
            else:
                planepb=1.   
            
            plane=pickplane(im,iz)*planepb
            if  method=='nufft':
                plane=np.asfortranarray(plane)
                
            if  np.any(plane):
                blank=False
            if  blank==False:
                uvmodel[:,iz]+=uv_sample(plane,
                                      cell,
                                      (uvw[:,0]/wv[iz]),
                                      (uvw[:,1]/wv[iz]),                               
                                      dRA=dRA,dDec=dDec,
                                      PA=0.,origin='lower',
                                      method=method,ik=ik,saveuvgrid=saveuvgrid)
                #print("predicted plane",iz)        
    
    write_ms(vis,uvmodel,datacolumn='data')
    
    return

    
if  __name__=="__main__":

    pass
 