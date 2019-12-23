"""
A Module used as an abstract layer for different optimization algorithms
"""
from .utils import *

from .opt_amoeba import *
from .opt_emcee import *
from .opt_lmfit import *
from .io import *
from .meta import read_inp

from pprint import pformat

import logging
logger = logging.getLogger(__name__)

#from .utils import *

#import os
#import gmake.meta as meta

#from memory_profiler import profile
#@profile
def fit_setup(inp_dct,dat_dct,initial_model=False,save_model=False,copydata=False):
    """
    for method='emcee': sampler is an emcee object
    for method=others: sampler is a dict
    """

    fit_dct=opt_setup(inp_dct,dat_dct)
    
    outfolder=fit_dct['outfolder']
    
    if  copydata==True:
    
        dat_dct_path=outfolder+'/data.h5'
        dct2hdf(dat_dct,outname=dat_dct_path)    
    
    if  initial_model==True:

        start_time = time.time()
        if  save_model==True:
            savemodel=outfolder+'/model_0'
        else:
            savemodel=None
        
        lnl,lnprob,chisq,ndata,npar=model_lnprob2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
                                             savemodel=savemodel)          
        #lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,packblobs=True,
        #                       savemodel=savemodel)
             
        logger.debug("{0:50} : {1:<8.5f} seconds".format('one trial',time.time()-start_time))
        
        #logger.debug('ndata->'+str(ndata))
        #logger.debug('chisq->'+str(chisq))
        """
        lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
                               savemodel=fit_dct['outfolder']+'/model_0')
        logger.debug('p_start:    ')
        logger.debug(pformat(blobs))
        """    

    dct2hdf(fit_dct,outname=outfolder+'/fit.h5')

    return fit_dct

def opt_setup(inp_dct,dat_dct):
    """
    Notes:
        + nthreads
            if the calling function uses the CPU multiple-threading functon for calculations, 
            turn on threading in emcee may have adverse effects actually
            
            log:
                * didn't find clear way to turn off threading for mkl_fft
                * mkl_num_threads doesn't apply here
                mkl_fft/threads=8 emecee-threads=1
                    iteration:  1
                    Took 1.22294176419576 minutes
                mkl_fft/threads=8 emecee-threads=4
                    iteration:  1
                    Took 2.3464738647143046 minutes
                mkl_fft/threads=8 emecee-threads=8
                    iteration:  1
                    Took 2.845475753148397 minutes
                pyfftw/threads=1 emecee-threads=1
                    iteration:  1
                    Took 2.0895618041356405 minutes
                pyfftw/threads=8 emecee-threads=8
                    iteration:  1
                    Took 2.9587043801943462 minutes                  
                pyfftw/threads=8 emecee-threads=1
                    iteration:  1
                    Took 2.0195618041356405 minutes
    
    20190923:
        update the dependency to emcee>3.0rc2
        the setup follows the guideline here:
            https://emcee.readthedocs.io/en/latest/tutorials/monitor/?highlight=sampler.sample
    
    Note:
        emcee-threading vs model-threading
        model-threading may be ineffecient if the calculation process is not truely/fully parameliized
        but some overhead can be avoid
        emcee-threading will require more memory and carefully arrange input parameter to avoid heavy pickling
        
        if memory allowed, using emcee-threading may be the better option generally 
            
    """
    
    opt_dct=inp_dct['optimize']
    gen_dct=inp_dct['general']
    
    fit_dct={'optimize':opt_dct.copy()}
    fit_dct={'method':opt_dct['method']}
    fit_dct['p_start']=[]
    fit_dct['p_lo']=[]
    fit_dct['p_up']=[]
    fit_dct['p_name']=[]
    fit_dct['p_scale']=[]
    fit_dct['p_unit']=[]
    
    for p_name in opt_dct.keys():
        if  '@' not in p_name:
            continue
        fit_dct['p_name'].append(p_name)
        p_value,p_unit=read_par(inp_dct,p_name,to_value=True)
        fit_dct['p_unit'].append(p_unit)
        #print(p_name,p_unit,p_value)
        fit_dct['p_start']=np.append(fit_dct['p_start'],np.mean(p_value))
        
        mode=opt_dct[p_name][0]
        lims=opt_dct[p_name][1]
        
        if  isinstance(lims[0],u.Quantity):
            p_lo_value=(lims[0]).to_value(unit=p_unit)
        else:
            p_lo_value=lims[0]
        fit_dct['p_lo']=np.append(fit_dct['p_lo'],
                                  read_range(center=fit_dct['p_start'][-1],
                                                   delta=p_lo_value,
                                                   mode=mode))
        if  isinstance(lims[1],u.Quantity):
            p_up_value=(lims[1]).to_value(unit=p_unit)
        else:
            p_up_value=lims[1]
        
        fit_dct['p_up']=np.append(fit_dct['p_up'],
                                  read_range(center=fit_dct['p_start'][-1],
                                                   delta=p_up_value,
                                                   mode=mode))                                  
        
        scale_def=max((abs(fit_dct['p_lo'][-1]-fit_dct['p_start'][-1]),abs(fit_dct['p_up'][-1]-fit_dct['p_start'][-1])))
        if  len(lims)<=2:
            if  fit_dct['method']=='emcee':
                scale=scale_def*0.01
            else:
                scale=scale_def*1.0
        else:
            scale_value=(lims[2]).to_value(unit=p_unit)
            if  mode=='a' or mode=='o':
                scale=scale_value
            if  mode=='r':
                scale=abs(fit_dct['p_start'][-1]*scale_value)
            scale=min(scale_def,scale)
        fit_dct['p_scale']=np.append(fit_dct['p_scale'],scale)


    gmake_pformat(fit_dct)
    #print(fit_dct['p_name'])
    #print(fit_dct['p_start'])
    #print(fit_dct['p_format'])
    #print(fit_dct['p_format_keys'])
    
    fit_dct['ndim']=len(fit_dct['p_start'])
    #   turn off mutiple-processing since mkl_fft has been threaded.
    fit_dct['nthreads']=multiprocessing.cpu_count()
    if  'nthreads' in opt_dct:
        fit_dct['nthreads']=opt_dct['nthreads'] # doens't reallyt matter if method='emcee'
    if  'nwalkers' in opt_dct:
        fit_dct['nwalkers']=opt_dct['nwalkers']
    fit_dct['outfolder']=gen_dct['outdir']
    
    
    if  fit_dct['method']=='emcee':
        logger.debug('nthreads:'+str(fit_dct['nthreads']))
        logger.debug('nwalkers:'+str(fit_dct['nwalkers']))
    
    logger.debug('ndim:    '+str(fit_dct['ndim']))
    logger.debug('outdir:  '+str(fit_dct['outfolder']))
    
    if  fit_dct['method']=='emcee':
        np.random.seed(0)
        fit_dct['pos_start'] = \
        [ np.maximum(np.minimum(fit_dct['p_start']+fit_dct['p_scale']*np.random.randn(fit_dct['ndim']),fit_dct['p_up']),fit_dct['p_lo']) for i in range(fit_dct['nwalkers']) ]
        fit_dct['pos_last']=deepcopy(fit_dct['pos_start'])
    if  (not os.path.exists(fit_dct['outfolder'])) and fit_dct['outfolder']!='':
        os.makedirs(fit_dct['outfolder'])

    fit_dct['step_last']=0
    
    #np.save(fit_dct['outfolder']+'/dat_dct.npy',dat_dct)
    #np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)   #   fitting metadata
    #np.save(fit_dct['outfolder']+'/inp_dct.npy',inp_dct)   #   input metadata
    
    # setup backend

    
    """
    sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                    model_lnprob,backend=backend,blobs_dtype=dtype,
                                    args=(fit_dct,inp_dct,dat_dct),
                                    runtime_sortingfn=sort_on_runtime)
                                    #args=(data,imsets,disks,fit_dct),threads=fit_dct['nthreads'],threads=fit_dct['nthreads'])
    """

    meta.dat_dct_global=dat_dct
    #print(dat_dct_global)
    
                               

                                    #args=(data,imsets,disks,fit_dct),threads=fit_dct['nthreads']threads=fit_dct['nthreads'],)                                    
    #"""

    return fit_dct

def fit_iterate(fit_dct,inp_dct,dat_dct):
    
    if  'amoeba' in fit_dct['method']:
        amoeba_iterate(fit_dct,inp_dct,dat_dct,nstep=inp_dct['optimize']['niter'])
        return
    if  'emcee' in fit_dct['method']:
        emcee_iterate(fit_dct,inp_dct,dat_dct,nstep=inp_dct['optimize']['niter'])
        return
    if  'lmfit' in fit_dct['method']:
        lmfit_iterate(fit_dct,inp_dct,dat_dct,nstep=inp_dct['optimize']['niter'])
        return

def fit_analyze(inpfile,burnin=None,copydata=True,export=False):
    
    inp_dct=read_inp(inpfile)
    outfolder=inp_dct['general']['outdir']
    
    if  'amoeba' in inp_dct['optimize']['method']:
        amoeba_analyze(outfolder,burnin=burnin)
        #fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        fit_dct=hdf2dct(outfolder+'/fit.h5')
        theta_start=fit_dct['p_start']
        theta_end=fit_dct['p_best']        
    
    if  'emcee' in inp_dct['optimize']['method']:
        emcee_analyze(outfolder,burnin=burnin)
        #fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        #fit_dct=hdf2dct(outfolder+'/fit.h5')
        #theta_start=fit_dct['p_start']
        #theta_end=fit_dct['p_median']
    
    if  'lmfit-nelder' in inp_dct['optimize']['method']:
        lmfit_analyze_nelder(outfolder,burnin=burnin)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        theta_start=fit_dct['p_start']
        theta_end=np.array(list(fit_dct['p_lmfit_result'].params.valuesdict().values()))  
    
    if  'lmfit-brute' in inp_dct['optimize']['method']:
        lmfit_analyze_brute(outfolder)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        theta_start=fit_dct['p_start']
        theta_end=fit_dct['p_lmfit_result'].brute_x0                
    
    
    if  export==True:
        dat_dct_path=outfolder+'/data.h5'
        if  os.path.isfile(dat_dct_path):
            dat_dct=hdf2dct(dat_dct_path)
        else:
            dat_dct=read_data(inp_dct,fill_mask=True,fill_error=True)
            if  copydata==True:
                dct2hdf(dat_dct,outname=dat_dct_path)
        
        #lnl,blobs=model_lnprob(theta_start,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/model_0',packblobs=True)
        #logger.debug('model_0: ')
        #logger.debug(pformat(blobs))
        
        #lnl,blobs=model_lnprob(theta_end,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/model_1',packblobs=True)
        #logger.debug('model_1: ')
        #logger.debug(pformat(blobs))
    

           