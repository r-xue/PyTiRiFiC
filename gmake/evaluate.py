from .model_dynamics import model_vrot
from .io import *

logger = logging.getLogger(__name__)

import builtins
import gc
import os
import psutil
process = psutil.Process(os.getpid())

#from .meta import dat_dct_global
import gmake.meta as meta

from memory_profiler import profile
from gmake import pprint
from gmake.model import clouds_fill

from gmake.model import model_setup
from gmake.discretizer import chi2uv,chi2im

from .model_dynamics import *
from .io import *


#from galario.double import get_image_size
#from galario.double import sampleImage
#from galario.double import chi2Image


logger = logging.getLogger(__name__)


from astropy.modeling.models import Gaussian2D

from memory_profiler import profile

from .model import model_setup
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

    # build model container
    
    if  models is None:
        models=model_setup(inp2mod(mod_dct),dat_dct,decomp=decomp,verbose=verbose)

    # calculate chisq 
           
    for tag in list(models.keys()):
        
        if  'imodel@' in tag:
            
            if  models[tag.replace('imodel@','type@')]=='vis':
                
                objs=[mod_dct[obj] for obj in models[tag.replace('imodel@','objs@')]]
                
                chi2=chi2uv(objs,
                            models[tag.replace('imodel@','header@')],
                            dat_dct[tag.replace('imodel@','data@')],
                            dat_dct[tag.replace('imodel@','uvw@')],
                            dat_dct[tag.replace('imodel@','phasecenter@')],
                            dat_dct[tag.replace('imodel@','weight@')],
                            dat_dct[tag.replace('imodel@','flag@')])

            if  models[tag.replace('imodel@','type@')]=='image':
                
                objs=[mod_dct[obj] for obj in models[tag.replace('imodel@','objs@')]]
                
                chi2=chi2im(objs,
                            models[tag.replace('imodel@','header@')],
                            dat_dct[tag.replace('imodel@','data@')],
                            models[tag.replace('imodel@','psf@')],
                            models[tag.replace('imodel@','error@')])
            chisq+=chi2                

    # lnl is not implementaed yet
    
    if  returnwdev==True:
        return ll,chisq,wdev
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
    return ll,chisq



"""
Convinient Functions, which

    + require argument is number rather quantities
    + large dataset is from meta.X
    
"""


def calc_lnprob(p,fit_dct,inp_dct,models=None,
                savemodel=None,decomp=False,nsamps=1e5,
                verbose=False):
    """
    this is the evaluating function for emcee
    use internal database (meta.dat_dct_global) to avoid coping during threading
    """
    theta=[p[i]<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
    
    out=log_probability(theta,fit_dct,inp_dct,meta.dat_dct_global,
                        models=models,
                      savemodel=savemodel,decomp=decomp,nsamps=nsamp,
                      verbose=verbose)
    return out    


def calc_chisq(p,fit_dct=None,inp_dct=None,dat_dct=None,
               models=None,
               savemodel=None):
    """
    this is the evaluating function for amoeba and warpping around model_lnprop
    
    For the compaibility purpose, p is number rather than quatity in units of p_start  
    """
    theta=[p[i]<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
    
    lnl,chisq=log_probability(theta,fit_dct,inp_dct,dat_dct,
                              models=models,
                              savemodel=savemodel)

    
    return chisq   





