from .gmake_init import *
from .gmake_utils import *

from .fit_amoeba import *
from .fit_emcee import *
from .fit_lmfit import *

logger = logging.getLogger(__name__)

def fit_setup(inp_dct,dat_dct):
    
    sampler={'inp_dct':inp_dct,'dat_dct':dat_dct}

    if  'amoeba' in inp_dct['optimize']['method']:
        fit_dct=amoeba_setup(inp_dct,dat_dct)
    if  'emcee' in inp_dct['optimize']['method']:
        fit_dct,sampler=emcee_setup(inp_dct,dat_dct)
    if  'lmfit' in inp_dct['optimize']['method']:
        fit_dct=lmfit_setup(inp_dct,dat_dct)            

    #   for method='emcee': sampler is an emcee object
    #   for method=others: sampler is a dict

    return fit_dct,sampler

def fit_iterate(fit_dct,sampler,nstep=100):
    
    if  'amoeba' in fit_dct['optimize']['method']:
        amoeba_iterate(fit_dct,sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)
        return
    if  'emcee' in fit_dct['optimize']['method']:
        emcee_iterate(sampler,fit_dct,nstep=nstep)
        return
    if  'lmfit' in fit_dct['optimize']['method']:
        lmfit_iterate(fit_dct,sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)
        return

def fit_analyze(inpfile,burnin=None):
    
    
    #inp_dct=np.load(outfolder+'/inp_dct.npy',allow_pickle=True).item()
    
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
    
    dat_dct=np.load(outfolder+'/dat_dct.npy',allow_pickle=True).item()
    

    lnl,blobs=model_lnprob(theta_start,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_start')
    logger.debug('p_start:    ')
    logger.debug(pformat(blobs))
    write_inp(inp_dct,inpfile=outfolder+'/p_start.inp',overwrite=True,
                    writepar=(fit_dct['p_name'],theta_start))
    
    lnl,blobs=model_lnprob(theta_end,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_fits')
    logger.debug('p_fits: ')
    logger.debug(pformat(blobs))
    write_inp(inp_dct,inpfile=outfolder+'/p_fits.inp',overwrite=True,
                    writepar=(fit_dct['p_name'],theta_end))  
    

           