from .model_func import *
from .model_func2 import *
from .model_build import *
from .model_build2 import *
from .model_eval import *
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


def model_lnlike2(theta,fit_dct,inp_dct,dat_dct,
                 savemodel=None,decomp=False,nsamps=1e5,
                 returnwdev=False,
                 verbose=False,test_threading=False):
    """
    the likelihood function
    
        step:    + fill the varying parameter into inp_dct
                 + convert inp_dct to mod_dct
                 + use mod_dct to regenerate RC
    """

    
    blobs={'lnprob':0.0,
           'chisq':0.0,
           'ndata':0.0,
           'wdev':np.array([]),
           'npar':len(theta)}
    if  returnwdev==False:
        del blobs['wdev']

    #models_size=human_unit(get_obj_size(fit_dct)*u.byte)
    #logger.info("before models size {:0.2f} ---".format(models_size))
    #models_size=human_unit(get_obj_size(inp_dct)*u.byte)
    #logger.info("before models size {:0.2f} ---".format(models_size))    
    

    
    """
    if  test_threading==True:
        #   don't actually calculate model
        #   used for testing threading overheads.
        x=dat_dct       
        t = time.time() + np.random.uniform(0.1, 0.2)
        while True:
            if time.time() >= t:
                break
        return 0.0,blobs
    """
    
    inp_dct0=deepcopy(inp_dct)

        
    for ind in range(len(fit_dct['p_name'])):
        #print(fit_dct['p_name'][ind],theta[ind],fit_dct['p_unit'][ind],type(fit_dct['p_unit'][ind]))
        write_par(inp_dct0,fit_dct['p_name'][ind],theta[ind]*fit_dct['p_unit'][ind],verbose=False)
    
 
        
    #tic0=time.time()
    mod_dct=inp2mod(inp_dct0)   # in physical units
    model_vrot(mod_dct)         # in natural (default internal units)
    #print('Took {0} second on inp2mod'.format(float(time.time()-tic0))) 


    if  test_threading==True:
        #   don't actually calculate model
        #   used for testing threading overheads.
        x=dat_dct       
        t = time.time() + np.random.uniform(1.1, 1.2)
        while True:
            if time.time() >= t:
                break
        return 0.0,blobs         
        
    
    #tic0=time.time()
    #models=gmake_kinmspy_api(mod_dct,dat_dct=dat_dct)

    #if  savemodel is not None:
    #    nsamps=nsamps*10

    #print('before',process.memory_info().rss/1024/1024)
    #logger.info("before models size {:0.2f} ---".format(models_size))    
     
    models=model_init2(mod_dct,dat_dct,decomp=decomp,verbose=verbose)
    models_size=human_unit(get_obj_size(models)*u.byte)

       
    model_fill2(models,decomp=decomp,nsamps=nsamps,verbose=verbose)
    #print(get_obj_size(models,to_string=True))
    #print('before',process.memory_info().rss/1024/1024)
      
    
    #models_size=human_unit(get_obj_size(models)*u.byte)
    #logger.info("--- models size {:0.2f} ---".format(models_size))      
    
    #models_size=human_unit(get_obj_size(models)*u.byte)
    #logger.info("before models size {:0.2f} ---".format(models_size))
    #for key in models:
    #    print(key,get_obj_size(models[key])/1024/1024)    
    


    
    
    #print(get_obj_size(models))
    #print(blobs['lnprob'])
    #models_size=human_unit(get_obj_size(models)*u.byte)
    #logger.info("after models size {:0.2f} ---".format(models_size))    
    

        
    
    #models_size=human_unit(get_obj_size(models)*u.byte)
    #logger.info("--- models size {:0.2f} ---".format(models_size))
    

    
        
    #for key in models:
    #    print(key,get_obj_size(models[key])/1024/1024)
        
    for tag in list(models.keys()):
        
        if  'imodel@' in tag:
            
            if  models[tag.replace('imodel@','type@')]=='vis':
                #print(models[tag])
                chi2=model_uvchi2(models[tag],#*models[tag.replace('imod3d@','pbeam@')],
                                     #models[tag.replace('imod3d@','imod2d@')],#*models[tag.replace('imod3d@','pbeam@')],
                                     models[tag.replace('imodel@','header@')],
                                     dat_dct[tag.replace('imodel@','data@')],
                                     dat_dct[tag.replace('imodel@','uvw@')],
                                     dat_dct[tag.replace('imodel@','phasecenter@')],
                                     dat_dct[tag.replace('imodel@','weight@')],
                                     average=True,
                                     verbose=verbose)
                #print(chi2)
                blobs['chisq']+=chi2
                #logger.debug("{0} {1}".format(tag,chi2))
    
    lnl=blobs['lnprob']
    #print('after',process.memory_info().rss/1024/1024)
    #logger.debug("{0} {1}".format('-->',blobs['chisq']))
    return lnl,blobs    
    


def model_lnprob2(theta,fit_dct,inp_dct,dat_dct,
                 savemodel=None,decomp=False,nsamps=1e5,
                 packblobs=False,
                 verbose=False):
    """
    this is the evaluating function for emcee
    packblobs=True:
        lnl,blobs
    packblobs=False:
        lnl,lnp,chisq,ndata,npar
    """

    if  verbose==True:
        start_time = time.time()
        
    lp = model_lnprior(theta,fit_dct)
    
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        if  packblobs==True:
            return -np.inf,blobs
        else:
            return -np.inf,-np.inf,+np.inf,0.0,len(theta)

       
    lnl,blobs=model_lnlike2(theta,fit_dct,inp_dct,dat_dct,
                           savemodel=savemodel,decomp=decomp,nsamps=nsamps,
                           verbose=verbose)
    
    if  verbose==True:
        print("try ->",theta)
        print("---{0:^10} : {1:<8.5f} seconds ---".format('lnprob',time.time()-start_time))    
    
    # np.array: to creat a zero-d object array 
    if  packblobs==True:
        return lp+lnl,blobs
    else:
        return lp+lnl,blobs['lnprob'],blobs['chisq'],blobs['ndata'],blobs['npar']


def model_lnprob_global2(theta,fit_dct,inp_dct,
                 savemodel=None,decomp=False,nsamps=1e5,
                 packblobs=False,
                 verbose=False):
    """
    this is the evaluating function for emcee
    packblobs=True:
        lnl,blobs
    packblobs=False:
        lnl,lnp,chisq,ndata,npar
    """

    if  verbose==True:
        start_time = time.time()
        
    lp = model_lnprior(theta,fit_dct)
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        if  packblobs==True:
            return -np.inf,blobs
        else:
            return -np.inf,-np.inf,+np.inf,0.0,len(theta)
    
    lnl,blobs=model_lnlike2(theta,fit_dct,inp_dct,meta.dat_dct_global,
                           savemodel=savemodel,decomp=decomp,nsamps=nsamps,
                           verbose=verbose)
    if  verbose==True:
        print("try ->",theta)
        print("---{0:^10} : {1:<8.5f} seconds ---".format('lnprob',time.time()-start_time))    
    
    # np.array: to creat a zero-d object array 
    if  packblobs==True:
        return lp+lnl,blobs
    else:
        return lp+lnl,blobs['lnprob'],blobs['chisq'],blobs['ndata'],blobs['npar']    
      


def model_chisq2(theta,
                      fit_dct=None,inp_dct=None,dat_dct=None,
                      savemodel=None,
                      verbose=False):
    """
    this is the evaluating function for amoeba 
    """
    #print(theta)
    if  verbose==True:
        start_time = time.time()
        
    lp = model_lnprior(theta,fit_dct)
    if  lp!=0:
        lp=+np.inf
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        #return +np.inf,blobs
        return +np.inf
    
    lnl,blobs=model_lnlike2(theta,fit_dct,inp_dct,dat_dct,savemodel=savemodel)
    
    if  verbose==True:
        print("try ->",theta)
        print("---{0:^10} : {1:<8.5f} seconds ---".format('lnprob',time.time()-start_time))    
    
    #print('-->',lp+blobs['chisq'])
    return lp+blobs['chisq']   


if  __name__=="__main__":
    
    pass




