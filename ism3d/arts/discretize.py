import numpy as np
import scipy
import astropy.units as u
from astropy.wcs import WCS
from astropy import constants as const
from astropy.cosmology import Planck13
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.convolution import convolve_fft
import numexpr as ne
import pyfftw
pyfftw.interfaces.cache.enable()
pyfftw.interfaces.cache.set_keepalive_time(5)
from scipy.sparse import csr_matrix
import fast_histogram as fh
from .. import fft_use
from galario.single import sampleImage
from copy import deepcopy
#from .io import *
#from .dynamics import model_vrot
#from .utils import write_par
#from .utils import inp2mod
import operator
from scipy.interpolate import RectBivariateSpline
import scipy.fft as scipy_fft
import finufftpy  as nufft
"""
Note:    
    discretize.*render and evaluate.*chisq share similar codebase in some degree.
    However, evaluate.*chisq is written for max performance with less memory impact, 
    while evaluate.*render is configurated for saving all model metadata.

"""
import logging
logger = logging.getLogger(__name__)







def clouds_perchan(clouds_loc,clouds_wt,sv,return_v=False):
    """
    split clouds_loc by its LOS velocity 
    
    clouds_loc 6D cloud location
    sv:    LOS velocity sampling vector
    
    note: sv and clouds_loc.d_z are defined by flipped sign;
          so we consider sv <-> -d_z  
          
    Ref:
        The implemented method is analogous to IDL histogram's reverse_indices:
        https://stackoverflow.com/questions/26783719/efficiently-get-indices-of-histogram-bins-in-python
        https://stackoverflow.com/questions/2754905/vectorized-approach-to-binning-with-numpy-scipy-in-python
        https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)
        
    return:
        list of cloudsset: each elements contain the clouds located within each channel plane
    
    """
    
    dv=sv[1]-sv[0]
    vrange=[sv[0]-dv/2,sv[-1]+dv/2]
    nbins=sv.size
    ch=((-nbins/(vrange[1]-vrange[0]))*clouds_loc.differentials['s'].d_z+\
        (vrange[1]-nbins*vrange[0]-vrange[0])/(vrange[1]-vrange[0])).astype(int)

    ##########################################################
    # Note:  ch=1 represents cloudlets within the first data channel
    #        ch=nbins represents cloudlets within the last data channel
    #       (-0.1/0.1).astype(int):
    #        making ch=0 ambigous in terms of representation in the data frame.
    ##########################################################
    
    ch_of_firstrow=np.minimum(np.min(ch),1)
    ch_of_lastrow=np.maximum(np.max(ch),nbins)
    nrow=ch_of_lastrow-ch_of_firstrow+1
    
    N=clouds_loc.size
    
    # for x_/y_list: first/last element saving cloudlets beyond the data channel coverage
    # so len(x_list)=2+nbins  
    
    # we use csr_matrix to performance partial sorting over the entire dgitized velocity range
    # the row index (irow) of the cloudlet in the CSR storage
    irow=ch-ch_of_firstrow  
    icol=np.arange(N)

    # we can also return csr_matrix and do slicing in mapper/chi2uv/chi2im
    # but there is no signature performance benefits
    csr_x = csr_matrix((clouds_loc.x.value, (irow, icol)), shape=(nrow, N))
    csr_y = csr_matrix((clouds_loc.y.value, (irow, icol)), shape=(nrow, N))
    x_perchan=np.split(csr_x.data, csr_x.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ])
    y_perchan=np.split(csr_y.data, csr_y.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ])
    if  clouds_wt is None:
        wt_perchan=None
    else:
        csr_wt = csr_matrix((clouds_wt, (irow, icol)), shape=(nrow, N))
        wt_perchan=np.split(csr_wt.data, csr_wt.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ])
        
    if  return_v==True:
        csr_v = csr_matrix((objs[i]['clouds_loc'].differentials['s'].d_z.value, (irow, icol)), shape=(nrow, N))
        v_perchan=np.split(csr_v.data, csr_v.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ])
        return x_perchan,y_perchan,wt_perchan,v_perchan
    else:
        return x_perchan,y_perchan,wt_perchan

def channel_split(objs,w):
    """
    Divivd the cloudlet model by channel in advance
    to avoid doing it during channel looping
    


    Note:
        returned v has a flip sign from V_los
        vrange[0] first channel velocity and vrange[1] last channel velocity 
        
        The returned list should have a element number of N(objs)
    
    for ccloudlet model: fluxscale is the flux per cloud
    for continuum model: fluxscale is the flux of the object within a plane
    """

    fluxscale_list=[]   # in Jy
    xrange_list=[]      # in kpc
    yrange_list=[]      # in kpc
    x_list=[]           # in kpc
    y_list=[]           # in kpc
    wt_list=[]          # arbitary

    for i in range(len(objs)):
        
        # return coordinate transform info
        
        sx,sy,sz=pix2sky(objs[i],w)

        #   for line component, we group clouds by their channel locations
        
        if  'lineflux' in objs[i]:
            
            # eqavelent flux density contribution per cloud within one channel
            
            dv=sz[1]-sz[0] 
            fluxscale=objs[i]['lineflux']/objs[i]['clouds_loc'].size/np.abs(dv)
            fluxscale_list.append(fluxscale.to_value('Jy'))
            
            x_perchan,y_perchan,wt_perchan=\
                clouds_perchan(objs[i]['clouds_loc'],objs[i]['clouds_wt'],sz,return_v=False)        
            x_list.append(x_perchan)
            y_list.append(y_perchan)
            wt_list.append(wt_perchan)
            
        #   fpr continuum componnet, we derive the frequency-dependent-scaling and 
        #   attached the channel-indepdent clouds location. 
        
        if  objs[i]['type'] not in ['apmodel'] and 'contflux' in objs[i]:
            
            # flux density contribution per cloud within each channel
            fluxscale=objs[i]['contflux']/objs[i]['clouds_loc'].size
            fluxscale=fluxscale*((sz/objs[i]['contfreq'])**objs[i]['alpha'])
            fluxscale_list.append(fluxscale.to_value('Jy'))
            x_list.append(objs[i]['clouds_loc'].x.value)
            y_list.append(objs[i]['clouds_loc'].y.value)
            wt_list.append(objs[i]['clouds_wt'])
            
        if  objs[i]['type']=='apmodel':
            
            # flux density contribution per cloud within each channel
            fluxscale=objs[i]['contflux']
            fluxscale=fluxscale*((sz/objs[i]['contfreq'])**objs[i]['alpha'])
            fluxscale_list.append(fluxscale.to_value('Jy'))
            x_list.append(sx)
            y_list.append(sy)
            wt_list.append(None)            

        dx=sx[1]-sx[0]
        xrange_list.append([sx[0].value-dx.value/2,sx[-1].value+dx.value/2])
        dy=sy[1]-sy[0]
        yrange_list.append([sy[0].value-dy.value/2,sy[-1].value+dy.value/2])

    return fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list


def lognsigma_lookup(objs,dname):
    """
    update some model parameters related to likelihood calculation
        In the model properties, we have some keywords related to configing the likelihood
    model and calculate log_propeorbaility:
        lognsigma: used to scale noise level (in case it's overunder estimated)
    They are actually related to data (one value per dataset)
    But it's setup per object due to the input file layout (repeated for different objects, like PSF)
    # we expected lognsigma is the same for one dname from all objs 
    """
    
    lognsigma=0
    for i in range(len(objs)):
        if  ('vis' in objs[i] or 'image' in objs[i]) and ('lognsigma' in objs[i]):
            if  'vis' in objs[i]:
                dname_list=objs[i]['vis'].split(",")
            if  'image' in objs[i]:
                dname_list=objs[i]['image'].split(",")
            for j in range(len(dname_list)):
                if  dname==dname_list[j]:
                    if  isinstance(objs[i]['lognsigma'],(list,tuple)):
                        lognsigma=objs[i]['lognsigma'][j]
                    else:
                        lognsigma=objs[i]['lognsigma']
    
    return lognsigma










