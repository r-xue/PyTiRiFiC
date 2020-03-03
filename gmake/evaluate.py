from .model_dynamics import model_vrot
import builtins
import gc
import os
import psutil
process = psutil.Process(os.getpid())

from .utils import pprint
from .model import clouds_fill
from .model_dynamics import *
from .io import *
from astropy.wcs import WCS
#from galario.double import get_image_size
#from galario.double import sampleImage
#from galario.double import chi2Image
logger = logging.getLogger(__name__)
from astropy.modeling.models import Gaussian2D
from memory_profiler import profile
from .model import model_setup
from .discretize import uv_mapper,xy_mapper
from .discretize import channel_split
from .discretize import sample_prep
from .discretize import lognsigma_lookup
import fast_histogram as fh
import numexpr as ne
from galario.single import sampleImage
from astropy.convolution import convolve_fft
import pyfftw
from .discretize import model_mapper
from lmfit import Parameters
from scipy.interpolate import interpn
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales

import gmake.meta as meta

"""
Cores Functions

log_prior + log_likelihood -> log_probability
:
->calc_chisq
->calc_lnprob

"""

def log_prior(theta,fit_dct):
    """
    pass through the likelihood prior function (limiting the parameter space)
    """
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    for index in range(len(theta)):
        if  theta[index]<p_lo[index] or theta[index]>p_up[index]:
            return -np.inf
    return 0.0

def log_likelihood(theta,fit_dct,inp_dct,dat_dct,
                   models=None,
                   savemodel=None,decomp=False,nsamps=1e5,
                   returnwdev=False,
                   verbose=False,test_threading=False):
    """
    the likelihood function
    
        step:    + fill the varying parameter into inp_dct
                 + convert inp_dct to mod_dct
                 + use mod_dct to regenerate RC
    
    theta can be quanitity here
    
    """
    #logger.debug(str(theta))
    
    ll=0
    chisq=0
    wdev=[]

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
    #print(mod_dct['co21']['rcProf'])
    #print(mod_dct['co21']['sbProf'])
    # build model container (skipped during iteration)
    
    if  models is None:
        models=model_setup(inp2mod(mod_dct),dat_dct,decomp=decomp,verbose=verbose)
        
    # calculate chisq 
           
    for tag in list(models.keys()):
        
        if  'imodel@' in tag:
            
            dname=tag.replace('imodel@','')
            objs=[mod_dct[obj] for obj in models[tag.replace('imodel@','objs@')]]
            
            if  models[tag.replace('imodel@','type@')]=='vis':
                chi2_one,ll_one=uv_chisq(objs,dname,dat_dct,models)
            if  models[tag.replace('imodel@','type@')]=='image':
                if  returnwdev==True:
                    chi2_one,ll_one,wdev_one=xy_chisq(objs,dname,dat_dct,models,returnwdev=True)
                    wdev.append(wdev_one.ravel())
                else:
                    chi2_one,ll_one=xy_chisq(objs,dname,dat_dct,models,returnwdev=False)
            chisq+=chi2_one
            ll+=ll_one
            
    # lnl is not implementaed yet

    if  returnwdev==True:
        return ll,chisq,np.hstack(wdev)
    else:
        return ll,chisq   


def log_probability(theta,
                    fit_dct,inp_dct,dat_dct,
                    models=None,
                    savemodel=None,decomp=False,nsamps=1e5,
                    verbose=False):
    """
    ll+lq
    """
    
    lp = log_prior(theta,fit_dct)
    if  not np.isfinite(lp):
        return -np.inf,+np.inf

    ll,chisq=log_likelihood(theta,fit_dct,inp_dct,dat_dct,
                             models=models,returnwdev=False,
                             savemodel=savemodel,decomp=decomp,nsamps=nsamps,
                             verbose=verbose)
    #logger.debug(str(theta))
    return ll+lp,chisq


"""
Convinient Functions, which

    + require argument is number rather quantities
    + large dataset is from X
    
"""

def calc_lnprob2_initializer(dat_dct,models):
    
    global global_dat_dct
    global global_models
    
    global_dat_dct=dat_dct
    global_models=models
    
    return

def calc_lnprob2(p,fit_dct,inp_dct,#dat_dct,models,
                savemodel=None,decomp=False,nsamps=1e5,
                verbose=False):
    """
    this is the evaluating function for emcee
    use internal read-only database (meta.db_global['dat_dct']/meta.db_global['models']) to avoid coping during threading
    """
    #print('1',meta.db_global['dat_dct'])
    #print('2',meta.db_global['models'])
    #print('-->',hex(id(global_dat_dct)))
    theta=[p[i]<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
    ll,chisq=log_probability(theta,fit_dct,inp_dct,
                             global_dat_dct,
                             models=global_models,
                             #dat_dct,
                             #models=models,
                             savemodel=savemodel)
    return ll,chisq 


def calc_lnprob(p,fit_dct,inp_dct,#dat_dct,models,
                savemodel=None,decomp=False,nsamps=1e5,
                verbose=False):
    """
    this is the evaluating function for emcee
    use internal read-only database (meta.db_global['dat_dct']/meta.db_global['models']) to avoid coping during threading
    """
    #print('1',meta.db_global['dat_dct'])
    #print('2',meta.db_global['models'])
    #print('-->',hex(id(meta.db_global['dat_dct'])))
    theta=[p[i]<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
    ll,chisq=log_probability(theta,fit_dct,inp_dct,
                             meta.db_global['dat_dct'],
                             models=meta.db_global['models'],
                             #dat_dct,
                             #models=models,
                             savemodel=savemodel)
    return ll,chisq    


def calc_chisq(p,
               fit_dct=None,inp_dct=None,dat_dct=None,
               models=None,blobs=None,
               savemodel=None):
    """
    this is the evaluating function for amoeba/lmfit and warpping around log_probalilibity()
    For the compaibility purpose, p is number rather than quatity in units of p_start  
    """
    theta=[]    # with units for log_probability
    pars=[]     # without units for bookkeeping  
    
    if  isinstance(p,Parameters):
        theta=[p['p_'+str(i+1)].value<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
        pars=[p['p_'+str(i+1)].value for i in range(len(fit_dct['p_name']))]
    else:
        theta=[p[i]<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
        pars=[p[i] for i in range(len(fit_dct['p_name']))]
    
    ll,chisq=log_probability(theta,fit_dct,inp_dct,meta.db_global['dat_dct'],
                              models=models,
                              savemodel=savemodel)
    if  isinstance(blobs,dict):
        if  'chi2' in blobs:
            blobs['chi2'].append(chisq)
        if  'logp' in blobs:
            blobs['logp'].append(ll)
        if  'pars' in blobs:
            blobs['pars'].append(pars)

    logger.debug(str(theta)+' '+str(chisq))
    return chisq

def calc_wdev(p,
              fit_dct=None,inp_dct=None,
              models=None,blobs=None,
              savemodel=None):
    """
    this might be slightly slower than calc_chisq due to memory usage to hold entire models
    it's not ideal for parallel calculation as the models are saved in the same object "models"
    """
    theta=[]    # with units for log_probability
    pars=[]     # without units for bookkeeping  
    
    if  isinstance(p,Parameters):
        theta=[p['p_'+str(i+1)].value<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
        pars=[p['p_'+str(i+1)].value for i in range(len(fit_dct['p_name']))]
    else:
        theta=[p[i]<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
        pars=[p[i] for i in range(len(fit_dct['p_name']))]
    logger.debug(str(theta))
    
    models,inp_dct0,mod_dct0=model_mapper(theta,fit_dct,inp_dct,
                                          meta.db_global['dat_dct'],
                                          models=models)
    wdev=[]
    for tag in list(models.keys()):
        if  'imodel@' in tag:
            dname=tag.replace('imodel@','')
            if  models['type@'+dname]=='vis':
                wdev_one=np.abs(models['model@'+dname]-meta.db_global['dat_dct']['data@'+dname])*np.sqrt(meta.db_global['dat_dct']['weight@'+dname][:,None])
                wdev.append(wdev_one[meta.db_global['dat_dct']['flag@'+dname]==False].ravel())
            if  models['type@'+dname]=='image':
                if  'sample@'+dname in models:
                    naxis=models['wcs@'+dname]._naxis
                    scube=interpn(  (np.arange(naxis[2]),np.arange(naxis[1]),np.arange(naxis[0])),
                                    np.squeeze(models['model@'+dname]),
                                    models['sample@'+dname][:,::-1],method='linear')
                    error=models['error-sp@'+dname]
                    imdata=models['data-sp@'+dname]
                else:
                    scube=models['model@'+dname]
                    error=models['error@'+dname]
                    imdata=models['data@'+dname]
                wdev_one=(scube-imdata)/error
                wdev.append(wdev_one.ravel())           
    
    wdev=np.hstack(wdev)
    
    logger.debug(str(theta)+' '+str(np.sum(wdev**wdev))+' '+str(wdev.size))
    return wdev

    """
    #obselet: only works for xy-optimiztion
    ll,chisq,wdev=log_likelihood(theta,fit_dct,inp_dct,meta.db_global['dat_dct'],
                              models=models,
                              savemodel=savemodel,returnwdev=True) 
    return wdev   
    """


#######################################################################################
# optimized for iteration performance / though sharing codes with xy/uv_mapper
#######################################################################################

def uv_chisq(objs,dname,dat_dct,models):
    """
    map multiple component into one header and also calculate chisq
    
    models:    a list of model to be mapped into the visibility model for the chisq calculation
    header:    pesudo fits header
    uv...:     visibility data 
    
    """

                            
    w=models['wcs@'+dname]
    uvdata=dat_dct['data@'+dname]
    uvw=dat_dct['uvw@'+dname]
    phasecenter=dat_dct['phasecenter@'+dname]
    uvweight=dat_dct['weight@'+dname]
    uvflag=dat_dct['flag@'+dname]
    pb=models['pbeam@'+dname]
    
    cc=0
    naxis=w._naxis    

    #   prep for sampleImage()    
    dRA,dDec,cell,wv=sample_prep(w,phasecenter)

    #   gather information per object before going into the channel loop,
    #   so it won't need to reapt for each chanel
    fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=\
        channel_split(objs,w,return_v=False) 
    lognsigma=lognsigma_lookup(objs,dname)
    
    chi2=0
    for iz in range(naxis[2]):
        
        blank=True  
        for i in range(len(objs)): 
            if  x_list[i][iz].size!=0:
                wt=wt_list[i][iz] if wt_list[i] is not None else None
                if  pb.ndim==2:
                    planepb=pb
                if  pb.ndim==3:
                    planepb=pb[iz,:,:]
                if  pb.ndim==4:
                    planepb=pb[0,iz,:,:]  
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
            uvdiff=ne.evaluate('a-b',
                     local_dict={'a':sampleImage(plane.astype(np.float32),
                                            cell,
                                            (uvw[:,0]/wv[iz]),
                                            (uvw[:,1]/wv[iz]),
                                            #ne.evaluate('a/b',local_dict={'a':uvw[:,0],'b':wv[iz]}),
                                            #ne.evaluate('a/b',local_dict={'a':uvw[:,1],'b':wv[iz]}),                                   
                                            dRA=dRA,dDec=dDec,
                                            PA=0.,check=False,origin='lower'),
                                 'b':uvdata[:,iz]})
            cc+=1
        else:
            uvdiff=uvdata[:,iz]
        
        # ll pt1
        chi2+=ne.evaluate('sum( ( (a.real)**2+(a.imag)**2 ) * (~b*c) )', #'sum( abs(a)**2*c)'
                         local_dict={'a':uvdiff,
                                     'b':uvflag[:,iz],
                                     'c':uvweight})/((np.exp(lognsigma))**2)  
    
    # ll pt2
    uvweight[uvweight==0]=1
    ll=np.sum(~uvflag)*(np.log(2*np.pi)+2*lognsigma)+\
        2*(-0.5)*ne.evaluate('sum( ~b*log(wt) )',local_dict={'wt':uvweight[:,np.newaxis],'b':uvflag})    
    # -1/2*(ll1+ll2)
    ll=-0.5*(chi2+ll)
    
    return chi2,ll

def xy_chisq(objs,dname,dat_dct,models,returnwdev=False):
    """
    map mutiple component into one header and calculate chisq
    
    models:    a list of model to be mapped into the visibility model for the chisq calculation
    header:    pesudo fits header
    uv...:     visibility data 
    
    """
    w=models['wcs@'+dname]
    imdata=dat_dct['data@'+dname]
    psf=models['psf@'+dname]
    error=models['error@'+dname]
    pb=models['pbeam@'+dname]
    
    convol_fft_pad=False
    convol_psf_pad=False
    convol_complex_dtype=np.complex64 
        
    cc=0
    naxis=w._naxis

    #   gather information per object before going into the channel loop,
    #   so it won't need to reapt for each chanel
    fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=\
        channel_split(objs,w,return_v=False)  
    lognsigma=lognsigma_lookup(objs,dname)
    
    # note: DO NOT USE np.float32 here as we are dealing with large numbers in numexpr()
    #   https://stackoverflow.com/questions/12596695/why-does-a-float-variable-stop-incrementing-at-16777216-in-c
    
    #   we create a model cube here with some memory ppanelty
    #   however, interpn will work faster in one shot
    scube=np.zeros((naxis[2],naxis[1],naxis[0]),dtype=np.float64)
    chi2=0
    for iz in range(naxis[2]):
        
        blank=True                    
        for i in range(len(objs)): 
            obj=objs[i]
            if  x_list[i][iz+1].size!=0:
                wt=wt_list[i][iz] if wt_list[i] is not None else None
                if  pb.ndim==2:
                    planepb=pb
                if  pb.ndim==3:
                    planepb=pb[iz,:,:]
                if  pb.ndim==4:
                    planepb=pb[0,iz,:,:]                  
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
        if  blank==False :
            if  psf.ndim==2:
                planepsf=psf
            if  psf.ndim==3:
                planepsf=psf[iz,:,:]
            if  psf.ndim==4:
                planepsf=psf[0,iz,:,:]            
            scube[iz,:,:]=convolve_fft(plane,planepsf,
                                      fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
                                      #complex_dtype=convol_complex_dtype,
                                      #fftn=np.fft.fftn, ifftn=np.fft.ifftn,
                                      #fftn=mkl_fft.fftn, ifftn=mkl_fft.ifftn,
                                      #nan_treatment='fill',fill_value=0.0,
                                      #fftn=scipy.fftpack.fftn, ifftn=scipy.fftpack.ifftn,
                                      fftn=pyfftw.interfaces.numpy_fft.fftn, ifftn=pyfftw.interfaces.numpy_fft.ifftn,
                                      normalize_kernel=False)
            cc+=1
  
    # assemble comparison pair
    
    if  'sample@'+dname in models:
        scube=interpn(  (np.arange(naxis[2]),np.arange(naxis[1]),np.arange(naxis[0])),
                        np.squeeze(scube),
                        models['sample@'+dname][:,::-1],method='linear')
        error=models['error-sp@'+dname]
        imdata=models['data-sp@'+dname]

    # ll pt1
    chi2=ne.evaluate('sum( ((a-b)/c)**2 )', 
                      local_dict={'a':scube,'b':imdata,'c':error})/((np.exp(lognsigma))**2)     
    # ll pt2
    ll=imdata.size*(np.log(2*np.pi)+2*lognsigma)+\
        2*ne.evaluate('sum( log(a) )',local_dict={'a':error})
    # -1/2*(ll1+ll2)
    ll=-0.5*(chi2+ll)
    
    if  returnwdev==False:
        return chi2,ll
    else:
        wdev=ne.evaluate('(a-b)/c',local_dict={'a':scube,'b':imdata,'c':error})
        return chi2,ll,wdev



#######################################################################################
# obselete 
#######################################################################################


def xy_chisq0(objs,dname,dat_dct,models):
    """
    **replaced by the current xy_chisq()**
    
    map mutiple component into one header and calculate chisq 
    
    models:    a list of model to be mapped into the visibility model for the chisq calculation
    header:    pesudo fits header
    uv...:     visibility data 
    
    """
    w=models['wcs@'+dname]
    imdata=dat_dct['data@'+dname]
    psf=models['psf@'+dname]
    error=models['error@'+dname]
    
    convol_fft_pad=False
    convol_psf_pad=False
    convol_complex_dtype=np.complex64    
        
    cc=0
    naxis=w._naxis

    #   gather information per object before going into the channel loop,
    #   so it won't need to reapt for each chanel
    fluxscale_list,xrange_list,yrange_list,x_list,y_list,wt_list=\
        channel_split(objs,w,return_v=False)  
    lognsigma=lognsigma_lookup(objs,dname)   

    chi2=0
    for iz in range(naxis[2]):
        
        blank=True                    
        for i in range(len(objs)): 
            obj=objs[i]
            if  x_list[i][iz+1].size!=0:
                wt=wt_list[i][iz] if wt_list[i] is not None else None
                if  blank==True:
                    plane=fh.histogram2d(y_list[i][iz+1],x_list[i][iz+1],
                                         range=[yrange_list[i],xrange_list[i]],
                                         bins=(naxis[1],naxis[0]),
                                         weights=wt)*fluxscale_list[i]
                    blank=False
                else:
                    plane+=fh.histogram2d(y_list[i][iz+1],x_list[i][iz+1],
                                         range=[yrange_list[i],xrange_list[i]],
                                         bins=(naxis[1],naxis[0]),
                                         weights=wt)*fluxscale_list[i]
            
        if  blank==False :
            if  psf.ndim==2:
                planepsf=psf
            if  psf.ndim==3:
                planepsf=psf[iz,:,:]
            if  psf.ndim==4:
                planepsf=psf[0,iz,:,:]            
            imdiff=ne.evaluate('a-b',
                     local_dict={'a':convolve_fft(plane,planepsf,
                                                    fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
                                                    #complex_dtype=convol_complex_dtype,
                                                    #fftn=np.fft.fftn, ifftn=np.fft.ifftn,
                                                    #fftn=mkl_fft.fft2, ifftn=mkl_fft.ifft2,
                                                    #nan_treatment='fill',fill_value=0.0,
                                                    #fftn=scipy.fftpack.fftn, ifftn=scipy.fftpack.ifftn,
                                                    fftn=pyfftw.interfaces.numpy_fft.fftn, ifftn=pyfftw.interfaces.numpy_fft.ifftn,
                                                    normalize_kernel=False),
                                 'b':imdata[iz,:,:]})
            cc+=1
        else:
            imdiff=-imdata[iz,:,:]
        
        # ll pt1
        chi2+=ne.evaluate('sum( ( a**2 ) * (1/c)**2 )', 
                         local_dict={'a':imdiff,'c':error[iz,:,:]})/((np.exp(lognsigma))**2)     
    
    # ll pt2
    ll=imdata.size*(np.log(2*np.pi)+2*lognsigma)+\
        2*ne.evaluate('sum( log(a) )',local_dict={'a':error})
    
    # -1/2*(ll1+ll2)
    ll=-0.5*(chi2+ll)

    return chi2,ll
