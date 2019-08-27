from .gmake_init import *
from .gmake_amoeba import *
from .gmake_emcee import *
from .gmake_lmfit import *

def gmake_fit_setup(inp_dct,dat_dct):
    
    sampler={'inp_dct':inp_dct,'dat_dct':dat_dct}

    if  'amoeba' in inp_dct['optimize']['method']:
        fit_dct=gmake_amoeba_setup(inp_dct,dat_dct)
    if  'emcee' in inp_dct['optimize']['method']:
        fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
    if  'lmfit' in inp_dct['optimize']['method']:
        fit_dct=gmake_lmfit_setup(inp_dct,dat_dct)            

    #   for method='emcee': sampler is an emcee object
    #   for method=others: sampler is a dict

    return fit_dct,sampler

def gmake_fit_iterate(fit_dct,sampler,nstep=100):
    
    if  'amoeba' in fit_dct['optimize']['method']:
        gmake_amoeba_iterate(fit_dct,sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)
        return
    if  'emcee' in fit_dct['optimize']['method']:
        gmake_emcee_iterate(sampler,fit_dct,nstep=nstep)
        return
    if  'lmfit' in fit_dct['optimize']['method']:
        gmake_lmfit_iterate(fit_dct,sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)
        return

def gmake_fit_analyze(outfolder,burnin=None):
    
    
    inp_dct=np.load(outfolder+'/inp_dct.npy',allow_pickle=True).item()
    
    
    if  'amoeba' in inp_dct['optimize']['method']:
        gmake_amoeba_analyze(outfolder,burnin=burnin)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        theta_start=fit_dct['p_amoeba']['p0']
        theta_end=fit_dct['p_amoeba']['p_best']
    
    if  'emcee' in inp_dct['optimize']['method']:
        gmake_emcee_analyze(outfolder,burnin=burnin)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        theta_start=fit_dct['p_start']
        theta_end=fit_dct['p_median']
    
    if  'lmfit-nelder' in inp_dct['optimize']['method']:
        gmake_lmfit_analyze_nelder(outfolder,burnin=burnin)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        theta_start=fit_dct['p_start']
        theta_end=np.array(list(fit_dct['p_lmfit_result'].params.valuesdict().values()))  
    
    if  'lmfit-brute' in inp_dct['optimize']['method']:
        gmake_lmfit_analyze_brute(outfolder)
        fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        theta_start=fit_dct['p_start']
        theta_end=fit_dct['p_lmfit_result'].brute_x0                
              
    
    #"""
    dat_dct=np.load(outfolder+'/dat_dct.npy',allow_pickle=True).item()
    lnl,blobs=gmake_model_lnprob(theta_start,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_start')
    logging.debug('p_start:    ')
    logging.debug(pformat(blobs))
    
    gmake_write_inp(inp_dct,inpfile=outfolder+'/p_start.inp',overwrite=True,
                    writepar=(fit_dct['p_name'],theta_start))

    lnl,blobs=gmake_model_lnprob(theta_end,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_fits')
    logging.debug('p_fits: ')
    logging.debug(pformat(blobs))
    
    gmake_write_inp(inp_dct,inpfile=outfolder+'/p_fits.inp',overwrite=True,
                    writepar=(fit_dct['p_name'],theta_end))  
    #"""

           