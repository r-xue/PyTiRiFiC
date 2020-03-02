import numpy as np


import astropy.units as u
from astropy.wcs import WCS
from astropy import constants as const
from astropy.cosmology import Planck13
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from astropy.io import fits 
from astropy.coordinates import SkyCoord
import numexpr as ne
from galario.single import sampleImage
from astropy.convolution import convolve_fft
import pyfftw
from scipy.sparse import csr_matrix
import fast_histogram as fh
import mkl_fft
import scipy
pyfftw.interfaces.cache.enable()
pyfftw.interfaces.cache.set_keepalive_time(5)
from copy import deepcopy
from .io import *
from .model_dynamics import model_vrot
from .model import clouds_fill
from .model import model_setup
from .model import clouds_discretize_2d

"""
*mapper / *chisq share some degrees of coding;
However, *chisq is setup for max performance while *mapper is configurated to saving model data.

"""

def pix2sky(obj,w,px=None,py=None,pz=None):
    """
    convert pixel index (zero-based to a "relative" "sky" frame (centered around the object xypos)
        "sky-frame" could be (angular,angular,velocity) or (distance,distance,velocity)
        while typically the sky-frame is defined in angular units;
        if the sky frame is defined in length the angular seperation will be converted to physical angular size.
        the object redshift is required
        
        We assume:
            inverse-RA (and pixel-x) aligns along with x
            DEC (and pixel-y) aligns along with y 
        The functin dosn't consider pixel rotation at this moment
    """
    
    #   wz  : galaxy zero systematic velocity in the hz or wavelength 
    
    if  'Hz' in w.wcs.cunit[2].name:
        wz=(obj['restfreq']/(1.0+obj['z'])*(1.-obj['vsys']/const.c)).to(u.Hz)
        dv=(-const.c*w.wcs.cdelt[2]*u.Hz/(obj['restfreq']/(1.0+obj['z']))).to(u.km/u.s)
    if  'angstrom' in w.wcs.cunit[2].name:
        wz=(obj['restwave']*(1.0+obj['z'])*(1.+obj['vsys']/const.c)).to(u.m)
        dv=(const.c*w.wcs.cdelt[2]*u.angstrom/(obj['restwave']*(1.0+obj['z']))).to(u.km/u.s)
    if  'm/s' in w.wcs.cunit[2].name:
        wz=obj['vsys']
        dv=(w.wcs.cdelt[2]*u.m/u.s).to(u.km/u.s)    
    
    #   get 0-based pix-index of galactic center in the spectral cube
    
    if  w.naxis==4:
        fpx,fpy,fpz,fps=w.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,wz,1,0)
    if  w.naxis==3:
        fpx,fpy,fpz=w.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,wz.si,0)    


    cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0*u.arcsec
    kps=Planck13.kpc_proper_per_arcmin(obj['z']).to(u.kpc/u.arcsec)
    dp=cell*kps
    
    if  px is None:
        # if px/py/pz is not specified, will be 1d vector from 0 to naxiy
        # the sx will tell you the sky-value for px=0/px=1/px=2...
        pp=w._naxis
        px=np.arange(pp[0])
        py=np.arange(pp[1])
        pz=np.arange(pp[2])
        
    sx=(px-fpx)*dp
    sy=(py-fpy)*dp
    sz=(pz-fpz)*dv
    
    return sx,sy,sz

def channel_split(objs,w,return_v=False):
    """
    Divivd the cloudlet model by channel in advance
    to avoid doing it during channel looping
    
    Ref:
        The implemented method is analogous to IDL histogram's reverse_indices:
        https://stackoverflow.com/questions/26783719/efficiently-get-indices-of-histogram-bins-in-python
        https://stackoverflow.com/questions/2754905/vectorized-approach-to-binning-with-numpy-scipy-in-python
        https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)

    Note:
        returned v has a flip sign from V_los
        vrange[0] first channel velocity and vrange[1] last channel velocity 
    """

    fluxscale_list=[]
    xrange_list=[]
    yrange_list=[]
    x_list=[]
    y_list=[]
    wt_list=[]
    
    if  return_v==True:
        v_list=[]
    #cof_list=[]
    
    for i in range(len(objs)):
        
        # return coordinate transform info
        
        sx,sy,sv=pix2sky(objs[i],w)

        # calculate eqavelent flux density contribution per cloud within one channel
        
        dv=sv[1]-sv[0] 
        fluxscale=objs[i]['lineflux']/objs[i]['clouds_loc'].size/np.abs(dv)
        fluxscale_list.append(fluxscale.to_value('Jy'))
        
        vrange=[sv[0]-dv/2,sv[-1]+dv/2]
        nbins=sv.size
        ch=((-nbins/(vrange[1]-vrange[0]))*objs[i]['clouds_loc'].differentials['s'].d_z+\
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
        
        N=objs[i]['clouds_loc'].size
        
        # for x_/y_list: first/last element saving cloudlets beyond the data channel coverage
        # so len(x_list)=2+nbins  
        
        # we use csr_matrix to performance partial sorting over the entire dgitized velocity range
        # the row index (irow) of the cloudlet in the CSR storage
        irow=ch-ch_of_firstrow  
        icol=np.arange(N)

        # we can also return csr_matrix and do slicing in mapper/chi2uv/chi2im
        # but there is no signature performance benefits
        csr_x = csr_matrix((objs[i]['clouds_loc'].x.value, (irow, icol)), shape=(nrow, N))
        csr_y = csr_matrix((objs[i]['clouds_loc'].y.value, (irow, icol)), shape=(nrow, N))
        x_list.append(np.split(csr_x.data, csr_x.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ]))
        y_list.append(np.split(csr_y.data, csr_y.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ]))
        
        if  return_v==True:
            csr_v = csr_matrix((objs[i]['clouds_loc'].differentials['s'].d_z.value, (irow, icol)), shape=(nrow, N))
            v_list.append(np.split(csr_v.data, csr_v.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ]))           
 
        dx=sx[1]-sx[0]
        xrange_list.append([sx[0].value-dx.value/2,sx[-1].value+dx.value/2])
        dy=sy[1]-sy[0]
        yrange_list.append([sy[0].value-dy.value/2,sy[-1].value+dy.value/2])
        
        if  objs[i]['clouds_wt'] is None:
            wt_list.append(None)
        else:
            csr_wt = csr_matrix((objs[i]['clouds_wt'], (irow, icol)), shape=(nrow, N))
            wt_list.append(np.split(csr_wt.data, csr_wt.indptr[  (1-ch_of_firstrow)  : (nbins+2-ch_of_firstrow)   ]))    
    
    if  return_v==True:
        return fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list,v_list
    else:
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

##########################################################################


    

##########################################################################

def xy_mapper(objs,w,psf=None,pb=None,normalize_kernel=False):
           
    """
    map a cloudlets-based model into a gridd data model (i.a FITS image-like for exporting or XY->UV tranform)
    
    obj:        target metadata (galactic center position (ra,dec), redshift, vsys, etc.)
                whatever information nesscarity to convert WCS units to physical units
    header:     data frame
    loc:        cloudlet position and velocity in the physical car on-sky frame
    weights:    cloudlet weights 
    
    convert pixel index wthin a WCS to a position in the on-sky galactic coordinates defined in the cloudlet model (ppv)
    
    
    #   get the coordinate of tl tr pix in the galactic frame
    
    #   x/y_sky is along x/y_pix
    #   here we directly map x/y_gal into x/y_pix without considering RA/DEC
        
    """
    
    convol_fft_pad=False
    convol_psf_pad=False
    convol_complex_dtype=np.complex64    
    
    cc=0
    naxis=w._naxis
    
    cube=np.zeros((naxis[2],naxis[1],naxis[0]),dtype=np.float32)
    if  psf is not None:
        scube=np.zeros((naxis[2],naxis[1],naxis[0]),dtype=np.float32)

    #   gather information per object before going into the channel loop,
    #   so it won't need to reapt for each chanel
    fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=\
        channel_split(objs,w,return_v=False)        
    
    for iz in range(naxis[2]):
        
        blank=True
        for i in range(len(objs)): 
            if  x_list[i][iz+1].size!=0:
                blank=False
                wt=wt_list[i][iz] if wt_list[i] is not None else None
                if  pb is not None:
                    if  pb.ndim==2:
                        planepb=pb
                    if  pb.ndim==3:
                        planepb=pb[iz,:,:]
                    if  pb.ndim==4:
                        planepb=pb[0,iz,:,:]
                else:
                    planepb=1                  
                cube[iz,:,:]+=fh.histogram2d(y_list[i][iz+1],x_list[i][iz+1],                                             
                                             range=[yrange_list[i],xrange_list[i]],
                                             bins=(naxis[1],naxis[0]),
                                             weights=wt)*fluxscale_list[i]*planepb
                                             
        if  psf is not None and blank==False :
            if  psf.ndim==2:
                planepsf=psf
            if  psf.ndim==3:
                planepsf=psf[iz,:,:]
            if  psf.ndim==4:
                planepsf=psf[0,iz,:,:]               
            scube[iz,:,:]=convolve_fft(cube[iz,:,:],planepsf,
                                      fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
                                      complex_dtype=convol_complex_dtype,
                                      #fftn=np.fft.fftn, ifftn=np.fft.ifftn,
                                      #fftn=mkl_fft.fftn, ifftn=mkl_fft.ifftn,
                                      #nan_treatment='fill',fill_value=0.0,
                                      #fftn=scipy.fftpack.fftn, ifftn=scipy.fftpack.ifftn,
                                      fftn=pyfftw.interfaces.numpy_fft.fftn, ifftn=pyfftw.interfaces.numpy_fft.ifftn,
                                      normalize_kernel=normalize_kernel)
            cc+=1       
            
    if  psf is None:
        return cube
    else:
        return cube,scube



def uv_mapper(objs,w,
              uvdata,uvw,phasecenter,uvweight,uvflag,pb=None):
    """
    map mutiple component into one header and calculate chisq
    
    models:    a list of model to be mapped into the visibility model for the chisq calculation
    header:    pesudo fits header
    uv...:     visibility data 
    
    """
    
    cc=0
    chi2=0
    naxis=w._naxis    
    
    phasecenter_sc = SkyCoord(phasecenter[0], phasecenter[1], frame='icrs')
    refimcenter_sc = SkyCoord(w.wcs.crval[0]*u.deg,w.wcs.crval[1]*u.deg, frame='icrs')
    dra, ddec = phasecenter_sc.spherical_offsets_to(refimcenter_sc)    
    dRA=dra.to_value(u.rad)
    dDec=ddec.to_value(u.rad)
    cell=np.mean(proj_plane_pixel_scales(w.celestial))
    cell=(np.deg2rad(cell)).astype(np.float32)
    wspec=w.sub(['spectral'])  
    wv=wspec.pixel_to_world(np.arange(naxis[2])).to(u.m,equivalencies=u.spectral()).value.astype(np.float32) 
    
    #   gather information per object before going into the channel loop,
    #   so it won't need to reapt for each chanel
    fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=\
        channel_split(objs,w,return_v=False) 
    
    vis=np.zeros((uvdata.shape)[0:2],dtype=uvdata.dtype,order='F')
        
    for iz in range(naxis[2]):
        blank=True  
        for i in range(len(objs)): 
            if  x_list[i][iz].size!=0:
                wt=wt_list[i][iz] if wt_list[i] is not None else None
                if  pb is not None:
                    if  pb.ndim==2:
                        planepb=pb
                    if  pb.ndim==3:
                        planepb=pb[iz,:,:]
                    if  pb.ndim==4:
                        planepb=pb[0,iz,:,:]                      
                else:
                    planepb=1
                if  blank==True:
                    plane=fh.histogram2d(y_list[i][iz+1],x_list[i][iz+1],
                                         range=[yrange_list[i],xrange_list[i]],
                                         bins=(naxis[1],naxis[0]),
                                         weights=wt)*fluxscale_list[i]*planepb
                    blank=False
                else:
                    plane+=fh.histogram2d(y_list[i][iz+1],x_list[i][iz+1],
                                         range=[yrange_list[i],xrange_list[i]],
                                         bins=(naxis[1],naxis[0]),
                                         weights=wt)*fluxscale_list[i]*planepb                    
        if  blank==False:
            vis[:,iz]=sampleImage(plane.astype(np.float32),
                                  cell,
                                  (uvw[:,0]/wv[iz]),
                                  (uvw[:,1]/wv[iz]),                               
                                  dRA=dRA,dDec=dDec,
                                  PA=0.,check=False,origin='lower')
            
    return vis

##########################################################################

def model_mapper(theta,fit_dct,inp_dct,dat_dct,
                 models=None,
                 savemodel=None,decomp=False,nsamps=1e5,
                 verbose=False,test_threading=False):
    """
    the likelihood function
    
        step:    + fill the varying parameter into inp_dct
                 + convert inp_dct to mod_dct
                 + use mod_dct to regenerate RC
    
    theta can be quanitity here
    
    returnwdev=True is a special mode reserved for lmfit
    
    retired option: returnwdev=True
    models,inp_dct0,mod_dct0=model_mapper(theta,fit_dct,inp_dct,meta.dat_dct_global,models=models,returnwdev=True)
    wdev=[]
    for tag in list(models.keys()):
        if  'imodel@' in tag:
            dname=tag.replace('imodel@','')
            wdev.append(models['model@'+dname].ravel().astype(np.float32))
    
    """

    
    ll=0
    chisq=0
    wdev=np.array([])

    # copy and modify model input dct
    
    inp_dct0=deepcopy(inp_dct)
    p_num=len(fit_dct['p_name']) 
    for ind in range(p_num):
        write_par(inp_dct0,fit_dct['p_name'][ind],theta[ind],verbose=False)
    
    mod_dct=inp2mod(inp_dct0)   # in physical units
    model_vrot(mod_dct)         # in natural (default internal units)

    # attach the cloudlet (reference) model to mod_dct
    
    clouds_fill(mod_dct,
                nc=100000,nv=20,seeds=[None,None,None,None])

    # build model container (skipped during iteration)
    if  models is None:
        models=model_setup(inp2mod(mod_dct),dat_dct,decomp=decomp,verbose=verbose)

    # calculate chisq 
           
    for tag in list(models.keys()):
        
        if  'imodel@' in tag:
            
            dname=tag.replace('imodel@','')
            objs=[mod_dct[obj] for obj in models[tag.replace('imodel@','objs@')]]
            w=models['wcs@'+dname]
            if  models[tag.replace('imodel@','type@')]=='vis':                
                model_one=uv_mapper(objs,w,
                                    dat_dct['data@'+dname],
                                    dat_dct['uvw@'+dname],
                                    dat_dct['phasecenter@'+dname],
                                    dat_dct['weight@'+dname],
                                    dat_dct['flag@'+dname])
            if  models[tag.replace('imodel@','type@')]=='image':
                imodel,model_one=xy_mapper(objs,w,
                                    psf=models['psf@'+dname],normalize_kernel=False)

            models['model@'+dname]=model_one

    return models,inp_dct0,mod_dct




