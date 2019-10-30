"""
A Module used as an abstract layer for different optimization algorithms
"""
from .utils import *

from .opt_amoeba import *
from .opt_emcee import *
from .opt_lmfit import *
from .io import *

import logging
logger = logging.getLogger(__name__)

def fit_setup(inp_dct,dat_dct,initial_model=True,copydata=False):
    """
    for method='emcee': sampler is an emcee object
    for method=others: sampler is a dict
    """


    if  'amoeba' in inp_dct['optimize']['method']:
        fit_dct=amoeba_setup(inp_dct,dat_dct)
    if  'emcee' in inp_dct['optimize']['method']:
        fit_dct=emcee_setup(inp_dct,dat_dct)
    if  'lmfit' in inp_dct['optimize']['method']:
        fit_dct=lmfit_setup(inp_dct,dat_dct)
    
    outfolder=fit_dct['outfolder']
    
    if  copydata==True:
    
        dat_dct_path=outfolder+'/data.h5'
        dct2hdf(dat_dct,outname=dat_dct_path)    
    
    if  initial_model==True:

        start_time = time.time()
        lnl,lnprob,chisq,ndata,npar=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
                                                 savemodel=None)
        #lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,packblobs=True,
        #                       savemodel='')     
        logger.debug("{0:50} : {1:<8.5f} seconds".format('one trial',time.time()-start_time))
        logger.debug('ndata->'+str(ndata))
        logger.debug('chisq->'+str(chisq))
        """
        lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
                               savemodel=fit_dct['outfolder']+'/model_0')
        logger.debug('p_start:    ')
        logger.debug(pformat(blobs))
        """    
    #print('++')
    dct2hdf(fit_dct,outname=outfolder+'/fit.h5')
    #print('--')

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

def fit_analyze(inpfile,burnin=None,copydata=True):
    
    inp_dct=read_inp(inpfile)
    outfolder=inp_dct['general']['outdir']
    
    if  'amoeba' in inp_dct['optimize']['method']:
        amoeba_analyze(outfolder,burnin=burnin)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        theta_start=fit_dct['p_amoeba']['p0']
        theta_end=fit_dct['p_amoeba']['p_best']
    
    if  'emcee' in inp_dct['optimize']['method']:
        emcee_analyze(outfolder,burnin=burnin)
        #fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        fit_dct=hdf2dct(outfolder+'/fit.h5')
        theta_start=fit_dct['p_start']
        theta_end=fit_dct['p_median']
    
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
    
    dat_dct_path=outfolder+'/data.h5'
    if  os.path.isfile(dat_dct_path):
        dat_dct=hdf2dct(dat_dct_path)
    else:
        dat_dct=read_data(inp_dct,fill_mask=True,fill_error=True)
        if  copydata==True:
            dct2hdf(dat_dct,outname=dat_dct_path)
    
    lnl,blobs=model_lnprob(theta_start,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/model_0',packblobs=True)
    logger.debug('model_0: ')
    logger.debug(pformat(blobs))
    
    lnl,blobs=model_lnprob(theta_end,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/model_1',packblobs=True)
    logger.debug('model_1: ')
    logger.debug(pformat(blobs))
    

           