"""
A Module used as an abstract layer for different optimization algorithms
"""
from .utils import *

from .opt_amoeba import *
from .opt_emcee import *
from .opt_lmfit import *
from .io import *
from .meta import read_inp
from .evaluate import calc_chisq,log_probability
from .model import model_setup
from pprint import pformat

import logging
logger = logging.getLogger(__name__)

#from .utils import *
#import os
#import gmake.meta as meta

#from memory_profiler import profile
#@profile

def opt_setup(inp_dct,dat_dct,initial_model=False,copydata=False):
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

    for method='emcee': sampler is an emcee object
    for method=others: sampler is a dict
    
    generate:
        fit_dct:    fitting metadata
        models:     model container + initilize some modeling metadata (header for vis; psf model; PB model etc.)
                    so we don't repeat it during iteration.
                
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
        
        p_value=read_par(inp_dct,p_name)
        fit_dct['p_name'].append(p_name)
        fit_dct['p_start'].append(np.mean(p_value))
        
        mode=opt_dct[p_name][0]
        lims=opt_dct[p_name][1]
        fit_dct['p_lo'].append(read_range(center=fit_dct['p_start'][-1],
                                          delta=lims[0],
                                          mode=mode))
        fit_dct['p_up'].append(read_range(center=fit_dct['p_start'][-1],
                                          delta=lims[1],
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
        fit_dct['p_scale'].append(scale)

    gmake_pformat(fit_dct)

    
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

    
    models=model_setup(inp2mod(inp_dct),dat_dct)
    ndata=0
    for tag in list(models.keys()):
        if  'imodel@' in tag:
            if  models[tag.replace('imodel@','type@')]=='vis':
                ndata+=np.sum(~dat_dct[tag.replace('imodel@','flag@')]) 
            if  models[tag.replace('imodel@','type@')]=='image':
                ndata+=dat_dct[tag.replace('imodel@','data@')].size                                
    npar=len(fit_dct['p_start'])
    
    fit_dct['ndata']=ndata
    fit_dct['npar']=npar
    logger.debug('npar ->'+str(npar))        
    logger.debug('ndata->'+str(ndata))        
    
    if  initial_model==True:
        
        start_time = time.time()
        lnl,chisq=log_probability(fit_dct['p_start'],
                                                    fit_dct,inp_dct,dat_dct,
                                                    models=models)
        logger.debug('chisq->'+str(chisq))
        logger.debug('lnl  ->'+str(lnl))
        logger.debug("{0:50} : {1:<8.5f} seconds".format('one trial',time.time()-start_time))


    dct2hdf(fit_dct,outname=fit_dct['outfolder']+'/fit.h5')    

    meta.dat_dct_global=dat_dct
    
    if  copydata==True:
    
        dat_dct_path=outfolder+'/data.h5'
        dct2hdf(dat_dct,outname=dat_dct_path)    

    return fit_dct,models

def fit_iterate(fit_dct,inp_dct,dat_dct,models):
    
    globals()[fit_dct['method']+'_iterate'](fit_dct,inp_dct,dat_dct,models,
                                            nstep=inp_dct['optimize']['niter'])

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
    

           