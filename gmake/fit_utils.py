from .gmake_init import *
from .gmake_utils import *

from .fit_amoeba import *
from .fit_emcee import *
from .fit_lmfit import *
from .io_utils import *

logger = logging.getLogger(__name__)

def fit_setup(inp_dct,dat_dct,initial_model=True,copydata=True):
    """
    for method='emcee': sampler is an emcee object
    for method=others: sampler is a dict
    """
    
    sampler={'inp_dct':inp_dct,'dat_dct':dat_dct}

    if  'amoeba' in inp_dct['optimize']['method']:
        fit_dct=amoeba_setup(inp_dct,dat_dct)
    if  'emcee' in inp_dct['optimize']['method']:
        fit_dct,sampler=emcee_setup(inp_dct,dat_dct)
    if  'lmfit' in inp_dct['optimize']['method']:
        fit_dct=lmfit_setup(inp_dct,dat_dct)            
    
    if  copydata==True:
        
        outfolder=inp_dct['optimize']['outdir']
        dat_dct_path=outfolder+'/data.h5'
        dct2hdf(dat_dct,outname=dat_dct_path)    
    
    if  initial_model==True:

        start_time = time.time()
        lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
                               savemodel='')
        logger.debug("{0:50} : {1:<8.5f} seconds".format('one trial',time.time()-start_time))
        logger.debug('ndata->'+str(blobs['ndata']))
        logger.debug('chisq->'+str(blobs['chisq']))
        """
        lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
                               savemodel=fit_dct['outfolder']+'/model_0')
        logger.debug('p_start:    ')
        logger.debug(pformat(blobs))
        """    


    return fit_dct,sampler

def fit_iterate(fit_dct,sampler,nstep=100):
    
    if  'amoeba' in fit_dct['method']:
        amoeba_iterate(fit_dct,sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)
        return
    if  'emcee' in fit_dct['method']:
        emcee_iterate(sampler,fit_dct,nstep=nstep)
        return
    if  'lmfit' in fit_dct['method']:
        lmfit_iterate(fit_dct,sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)
        return

def fit_analyze(inpfile,burnin=None,copydata=True):
    
    inp_dct=read_inp(inpfile)
    outfolder=inp_dct['optimize']['outdir']
    
    if  'amoeba' in inp_dct['optimize']['method']:
        amoeba_analyze(outfolder,burnin=burnin)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        theta_start=fit_dct['p_amoeba']['p0']
        theta_end=fit_dct['p_amoeba']['p_best']
    
    if  'emcee' in inp_dct['optimize']['method']:
        emcee_analyze(outfolder,burnin=burnin)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
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
    
    lnl,blobs=model_lnprob(theta_start,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/model_0')
    logger.debug('model_0: ')
    logger.debug(pformat(blobs))
    
    lnl,blobs=model_lnprob(theta_end,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/model_1')
    logger.debug('model_1: ')
    logger.debug(pformat(blobs))
    

           