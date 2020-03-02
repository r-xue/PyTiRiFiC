"""
A Module used as an abstract layer for different optimization algorithms
"""
from .utils import *
from .io import *
from .meta import read_inp
from .evaluate import calc_chisq,log_probability
from .model import model_setup
from pprint import pformat
from .utils import pprint
from .discretize import model_mapper


import logging
logger = logging.getLogger(__name__)

from numpy.random import Generator,SFC64,PCG64
from lmfit import Parameters
#from .utils import *
#import os
import gmake.meta as meta

#from memory_profiler import profile
#@profile

#from .meta import db_global
#print('opt',hex(id(db_global)))

from .evaluate import *

import logging
logger = logging.getLogger(__name__) 

from lmfit import minimize
from lmfit import report_fit
from galario.single import threads as galario_threads
import copy
import emcee
#from multiprocessing import Pool
#import pickle
#pickle.DEFAULT_PROTOCOL=3
import multiprocessing as mp
Pool = mp.get_context('fork').Pool



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
    fit_dct['p_scale']=[]   # use to normalize the parameter range (roughly (p_max-p_min))
    fit_dct['p_unit']=[]
    
    for p_name in opt_dct.keys():
        
        if  '@' not in p_name:
            continue
        #   lognsigma doesn't work with method!='emcee'
        if  ('emcee' not in opt_dct['method']) and 'lognsigma' in p_name:
            continue
        
        p_value=read_par(inp_dct,p_name)
        fit_dct['p_name'].append(p_name)
        fit_dct['p_start'].append(u.Quantity(np.mean(p_value)))
        
        mode=opt_dct[p_name][0]
        lims=opt_dct[p_name][1]
        fit_dct['p_lo'].append(u.Quantity(
                                read_range(center=fit_dct['p_start'][-1],
                                          delta=lims[0],
                                          mode=mode)))
        fit_dct['p_up'].append(u.Quantity(read_range(center=fit_dct['p_start'][-1],
                                          delta=lims[1],
                                          mode=mode)))                         
        
        scale_def=max((abs(fit_dct['p_lo'][-1]-fit_dct['p_start'][-1]),abs(fit_dct['p_up'][-1]-fit_dct['p_start'][-1])))
        if  len(lims)<=2:
            scale=scale_def
        else:
            scale_value=(lims[2]).to_value(unit=p_unit)
            if  mode=='a' or mode=='o':
                scale=scale_value
            if  mode=='r':
                scale=abs(fit_dct['p_start'][-1]*scale_value)
            scale=min(scale_def,scale)
        fit_dct['p_scale'].append(u.Quantity(scale))
        
    gmake_pformat(fit_dct)
    
    fit_dct['ndim']=len(fit_dct['p_start'])
    fit_dct['outfolder']=gen_dct['outdir']   
    if  (not os.path.exists(fit_dct['outfolder'])) and fit_dct['outfolder']!='':
        os.makedirs(fit_dct['outfolder'])         
    logger.debug('ndim:    '+str(fit_dct['ndim']))
    logger.debug('outdir:  '+str(fit_dct['outfolder']))
    
    models=model_setup(inp2mod(inp_dct),dat_dct)
    ndata=0
    
    for tag in list(models.keys()):
        if  'imodel@' in tag:
            if  models[tag.replace('imodel@','type@')]=='vis':
                ndata+=np.sum(~dat_dct[tag.replace('imodel@','flag@')]) 
            if  models[tag.replace('imodel@','type@')]=='image':
                if  tag.replace('imodel@','sample@') in models:
                    ndata+=(models[tag.replace('imodel@','sample@')].shape)[0] 
                else:
                    ndata+=dat_dct[tag.replace('imodel@','data@')].size                                
    npar=len(fit_dct['p_start'])
    
    fit_dct['ndata']=ndata
    fit_dct['npar']=npar
    logger.debug('npar ->'+str(npar))        
    logger.debug('ndata->'+str(ndata))     
    
    #   this is optimizer threads
    #   if >1, then OMP will be set to one (which is dne in itertion()
    if  'nthreads' in opt_dct:
        fit_dct['nthreads']=opt_dct['nthreads'] # doens't reallyt matter if method='emcee'
    else:
        fit_dct['nthreads']=1
        # for emcee/brute, it might be faster to set fit_dct['nthreads']=multiprocessing.cpu_count()
        if  fit_dct['method']=='emcee' or fit_dct['method']=='lmfit-brute':
            fit_dct['nthreads']=multiprocessing.cpu_count()
    
    #######################################################
    # pack additional setup for mpfit/lmfit
    #######################################################
    
    parinfo = [{'value':0.,
                'fixed':0,
                'limited':[0,0],
                'limits':[0.,0.],
                'parname':'',
                'step':0,
                'relstep':0,
                'mpside':0,
                'mpmaxstep':0,
                'mpminstep':0,
                } for i in range(len(fit_dct['p_name']))]
    params=Parameters()
    for i in range(len(fit_dct['p_name'])):
        parinfo[i]['parname']=fit_dct['p_name'][i]
        parinfo[i]['limited']=[1,1]
        parinfo[i]['value']=fit_dct['p_start'][i]
        parinfo[i]['step']=fit_dct['p_scale'][i]
        parinfo[i]['relstep']=fit_dct['p_scale'][i]
        parinfo[i]['limits']=[fit_dct['p_lo'][i],fit_dct['p_up'][i]]
        params.add('p_'+str(i+1),
                   value=fit_dct['p_start'][i].value,
                   vary=True,
                   min=fit_dct['p_lo'][i].value,
                   max=fit_dct['p_up'][i].value)
                   #brute_step=fit_dct['p_scale'][i].value)
    fit_dct['mpfit_parinfo']=parinfo
    fit_dct['lmfit_params']=params   

    #######################################################
    # pack additional setup for emcee
    #######################################################
    if  fit_dct['method']=='emcee':
        if  'nwalkers' in opt_dct:
            fit_dct['nwalkers']=opt_dct['nwalkers']
        else:
            fit_dct['nwalkers']=10            
        # emcee requires the vector position to be an array rather than quanities
        rng = Generator(SFC64(None))
        p_start=rng.normal(size=(fit_dct['nwalkers'],fit_dct['ndim']))
        p_start*=np.array([q.value*0.01 for q in fit_dct['p_scale']])
        p_start+=np.array([q.value for q in fit_dct['p_start']])
        p_start=np.minimum(p_start,np.array([q.value for q in fit_dct['p_up']]))
        p_start=np.maximum(p_start,np.array([q.value for q in fit_dct['p_lo']]))
        fit_dct['pos_start']=p_start.copy()
        fit_dct['pos_last']=p_start.copy()
        fit_dct['step_last']=0
    
    
    #######################################################
    
    dct2hdf(fit_dct,outname=fit_dct['outfolder']+'/fit.h5')    
    meta.db_global['dat_dct']=dat_dct
    meta.db_global['models']=models

    if  copydata==True:
        dat_dct_path=outfolder+'/data.h5'
        dct2hdf(dat_dct,outname=dat_dct_path)    

    if  initial_model==True:
        start_time = time.time()
        lnl,chisq=log_probability(fit_dct['p_start'],
                                                    fit_dct,inp_dct,dat_dct,
                                                    models=models)
        logger.debug('chisq->'+str(chisq))
        logger.debug('lnl  ->'+str(lnl))
        logger.debug("{0:50} : {1:<8.5f} seconds".format('one trial',time.time()-start_time))
        
    return fit_dct,models

def opt_iterate(fit_dct,inp_dct,dat_dct,models,resume=False):

    method=fit_dct['method'].split('-')[0]
    
    if  method=='emcee':
        opt_name='emcee'
    else:
        opt_name='chisq'
    
    logger.debug('max_iteration:'+str(inp_dct['optimize']['niter']))
    globals()[opt_name+'_iterate'](fit_dct,inp_dct,dat_dct,models,
                                   nstep=inp_dct['optimize']['niter'],
                                   resume=resume)

    return

def chisq_iterate(fit_dct,inp_dct,dat_dct,models,nstep=20,resume=None):
    """
    call lmfit or amoeba (scalar optimizer)
    
    reference: https://docs.scipy.org/doc/scipy/reference/optimize.html
    """
    
    logger.debug(" ")
    logger.debug("Running Optimizer: "+fit_dct['method'])
    logger.debug(">>"+fit_dct['outfolder']+"/chisq_chain.h5")
    logger.debug(" ")     

    ndim=len(fit_dct['p_name'])
    blobs={'pars':[],            # matching amoeba_sa.py (ndim+1+niter)
           'chi2':[],
           'logp':[]}
    
    #   using AMOEBA **obselete built-in method**
    if  fit_dct['method']=='amoeba':
        p_lo=np.array([q.value for q in fit_dct['p_lo']])
        p_up=np.array([q.value for q in fit_dct['p_up']])
        p0=[q.value for q in fit_dct['p_start']]
        scale=[q.value for q in fit_dct['p_scale']]
        #p0=(p_lo+p_up)/2.0
        #scale=(p_up-p_lo)/2.0      
        result=amoeba_sa(calc_chisq,p0,scale,
                           p_lo=[q.value for q in fit_dct['p_lo']],
                           p_up=[q.value for q in fit_dct['p_up']],
                           funcargs={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct,'models':models,'blobs':blobs},
                           ftol=1e-10,temperature=0,
                           maxiter=nstep,verbose=False)
    
    #   LMFIT https://lmfit.github.io/lmfit-py/fitting.html#lmfit.minimizer.MinimizerResult
    #   Essentially it's a wrapper around: https://docs.scipy.org/doc/scipy/reference/optimize.html
    
    if  '-nelder' in fit_dct['method']:
        # https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html#optimize-minimize-neldermead
        p_lo=np.array([q.value for q in fit_dct['p_lo']])
        p_up=np.array([q.value for q in fit_dct['p_up']])
        
        p0=np.array([q.value for q in fit_dct['p_start']])
        scale=np.array([q.value for q in fit_dct['p_scale']])
        
        p0=(p_lo+p_up)/2.0
        scale=(p_up-p_lo)/2.0
        
        """
        note: 
            do not set intial_simplex and min/max at the same time due to prameter mapping in lmfit
            two workaround methods:
                + remove min/max (commented out)
                + also mapping initial_simplex (used below)
                  see: https://lmfit.github.io/lmfit-py/bounds.html
        p = np.outer(p0, np.ones(fit_dct['npar']+1))
        for i in range(fit_dct['npar']):
            p[i][i+1]+=scale[i]        
        for i in range(len(fit_dct['p_name'])):
            fit_dct['lmfit_params']['p_'+str(i+1)].set(min=-np.inf)
            fit_dct['lmfit_params']['p_'+str(i+1)].set(max=+np.inf)
        """
        
        p0_internal=np.arcsin(2*(p0-p_lo)/(p_up-p_lo)-1)
        p1_internal=np.arcsin(2*(p0+scale-p_lo)/(p_up-p_lo)-1)
        sim = np.zeros((fit_dct['npar'] + 1, fit_dct['npar']), dtype=p0.dtype)
        sim[0] = p0_internal
        for k in range(fit_dct['npar']):
            y = np.array(p0_internal, copy=True)
            y[k] = p1_internal[k]
            sim[k + 1] = y        
        fit_kws={'options':{'maxiter':nstep,'adaptive':False,'fatol':1e-7,
                            'disp':True,'initial_simplex':sim}} #'maxfev':nstep,,
        func=calc_chisq
    
    if  '-leastsq' in fit_dct['method']:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.leastsq.html
        fit_kws={'epsfcn':0.01,'maxfev':100}
        func=calc_wdev
        
    if  '-least_squares' in fit_dct['method']:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
        fit_kws={'diff_step':np.ones(len(fit_dct['p_name']))*0.01,'max_nfev':nstep}
        func=calc_wdev
        
    if  '-brute' in fit_dct['method']:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brute.html
        if  'nthreads' not in fit_dct:
            fit_dct['nthreads']=1
        fit_kws={'Ns':10,'keep':'all','workers':fit_dct['nthreads']}
        func=calc_chisq
    
    kws={'fit_dct':fit_dct,'inp_dct':inp_dct,'models':models,'blobs':blobs}
    
    # turn on/off mutiple-threading
    set_omp_threads()
    if  '-brute' in fit_dct['method']:
        if  fit_kws['workers']>=2 or fit_kws['workers']==-1:
            del kws['blobs']
            set_omp_threads(1)
    
    if  'lmfit-' in fit_dct['method']:
        result=minimize(func,fit_dct['lmfit_params'],
                        kws=kws,
                        calc_covar=True,
                        method=fit_dct['method'].replace('lmfit-',''),
                        **fit_kws)

    #   collect the results
    
    p_chisq={}
    p_chisq['result']=result
    #   for amoeba, thereis another copy of chi2/pars
    #   result['chi2']  (ndim+1+iter)
    #   result['pars']  (ndim,ndim+1+iter)
    
    if  'lmfit' in fit_dct['method']:
        report_fit(p_chisq['result'])
        p_best=np.array(list(p_chisq['result'].params.valuesdict().values()))
        p_best=[p_best[i]<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))] 
    else:
        p_best=[result['p_best'][i]<<fit_dct['p_start'][i].unit for i in range(len(fit_dct['p_name']))]
        
    blobs['chi2']=np.array(blobs['chi2'])       # (ndim)            
    blobs['pars']=np.array(blobs['pars']).T     # (ndim,ieval)      

    p_chisq['blobs']=blobs                      # evaluation history for post analysis
    p_chisq['ndata']=fit_dct['ndata']           # ndata
    p_chisq['npar']=fit_dct['npar']             # npar
    p_chisq['p_best']=p_best                    # p_best

    dct2hdf(p_chisq,outname=fit_dct['outfolder']+'/chisq_chain.h5')
    #lnl,chisq=log_probability(p_best,fit_dct,inp_dct,dat_dct)   
    
    return 

def emcee_iterate(fit_dct,inp_dct,dat_dct,models,nstep=100,resume=False):
    """
        RUN the sampler
    """
    fit_dct['nstep']=nstep
    
    tic=time.time()
    dt=0.0
    
    logger.debug(" ")
    logger.debug("Running MCMC...")
    logger.debug(">>"+fit_dct['outfolder']+"/emcee_chain.h5")
    logger.debug(" ")
    logger.info('Hostname:      {0}'.format(socket.gethostname()))
    logger.info('CPU No. :      {0}'.format(multiprocessing.cpu_count()))
    logger.info('nthreads:      {0}'.format(fit_dct['nthreads']))
    logger.info('nwalkers:      {0}'.format(fit_dct['nwalkers']))            
    
    """
    emcee v3
        https://emcee.readthedocs.io/en/latest/tutorials/monitor/
    """
    index=0
    autocorr=np.empty(fit_dct['nstep'])
    old_tau=np.inf
    
    h5name=fit_dct['outfolder']+'/emcee_chain.h5'
    
    if  resume==False:
        backup(h5name,move=True)
        backend = emcee.backends.HDFBackend(h5name)
        backend.reset(fit_dct['nwalkers'],fit_dct['ndim'])
        last_state=fit_dct['pos_last']
    else:
        backend = emcee.backends.HDFBackend(h5name)
        last_state=backend.get_last_sample()
        
    # initilize the sampler
    
    dtype = [("chisq",float)] 
    if  fit_dct['nthreads']==1:
        set_omp_threads()
        sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                    calc_lnprob,backend=backend,blobs_dtype=dtype,
                                    args=(fit_dct,inp_dct),
                                    runtime_sortingfn=sort_on_runtime)
        sampler.run_mcmc(last_state,fit_dct['nstep'],progress=True)
    else:
        set_omp_threads(1)
        """
        from .evaluate import calc_lnprob2_initializer
        from .evaluate import calc_lnprob2
        with Pool(processes=fit_dct['nthreads'],initializer=calc_lnprob2_initializer,initargs=(dat_dct,models)) as pool:
            #   use model_lnprob_globe without the keyword dat_dct to avoid redundant data pickling  
            sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                        calc_lnprob2,backend=backend,blobs_dtype=dtype,
                                        args=(fit_dct,inp_dct),
                                        runtime_sortingfn=sort_on_runtime,pool=pool)
            sampler.run_mcmc(last_state,fit_dct['nstep'],progress=True)        
        """
    
        with Pool(processes=fit_dct['nthreads']) as pool:
            #   use model_lnprob_globe without the keyword dat_dct to avoid redundant data pickling  
            sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                        calc_lnprob,backend=backend,blobs_dtype=dtype,
                                        args=(fit_dct,inp_dct),
                                        runtime_sortingfn=sort_on_runtime,pool=pool)
            sampler.run_mcmc(last_state,fit_dct['nstep'],progress=True)
        
        
        """    
        with mp.Manager() as manager:
            mg_dat_dct = manager.dict(dat_dct)
            mg_models=manager.dict(models)            
            with manager.Pool(processes=fit_dct['nthreads']) as pool:
                sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                            calc_lnprob,backend=backend,blobs_dtype=dtype,
                                            args=(fit_dct,inp_dct,mg_dat_dct,mg_models),
                                            runtime_sortingfn=sort_on_runtime,pool=pool)
                sampler.run_mcmc(last_state,fit_dct['nstep'],progress=True)                
        """
                        
    """    
    for sample in sampler.sample(fit_dct['pos_last'],iterations=fit_dct['nstep'],
                                 progress=True,store=True):
        
        # Only check convergence every 100 steps
        if  sampler.iteration % int(fit_dct['nstep']/10.0):
            continue
    
        # Compute the autocorrelation time so far
        tau=sampler.get_autocorr_time(tol=0)    # (npar.)
        autocorr[index]=np.mean(tau)
        index+=1
        
        # Check convergence
        converged = np.all(tau * 100 < sampler.iteration)
        converged &= np.all(np.abs(old_tau - tau) / tau < 0.01)
        if  converged:
            break
        old_tau = tau
    """
    
    set_omp_threads()

    logger.debug("Done.")
    logger.debug('Took {0} minutes'.format(float(time.time()-tic)/float(60.)))

    return




"""
built-in method obselete
"""


def amoeba_sa(func,p0,scale, 
              p_lo=None,p_up=None,
              funcargs=None,
              ftol=1e-5,
              maxiter=5000,
              temperature=0.,
              format_prec='10.0f',
              verbose=False): 
    """


    A Python implementation of the AMOEBA / Nelder-Mead downhill-simplex algorithm for
    minizing a model function
    
        loosely based on amoeba_sa.pro (IDL) from E.Rolosky with the improvements from H.Fu
    
    reference:
        https://github.com/fchollet/nelder-mead/blob/master/nelder_mead.py
        https://docs.scipy.org/doc/scipy/reference/optimize.html#module-scipy.optimize
        https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html
        https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method
    
    note:
        for using it as a module:
        >sys.path.append("/PATH_TO_SCRIPTS/")
        >from amoeba_sa import amoeba_sa
    
    history:
        20171215    RX      introduced
        20171216    RX      return the result as dict

    Keywords:
        func:         name of the function to be evaluate
        scale:        the search scale for each variable, a list with one
                      element for each variable.
        funcargs:     unction optional parameters packed (dict)
        p0:           initial values (ndarray)
        scale:        initial scale (ndarray)
        p_lo:         p_lo limit for p (ndarray)
        p_up:         p_up limit for p (ndarray)
    
    return
    
        dict
    
    """
    #from scipy.stats.distributions import chi2
    np.seterr(divide='ignore', invalid='ignore')
    
    if  p_lo is None:
        p_lo=p0-np.inf
    if  p_up is None:
        p_up=p0+np.inf

    # (i,i+1) array for SIMPLEX
    # IDL and Python have different indexing orders
    # https://docs.scipy.org/doc/numpy/user/basics.indexing.html
    ndim=len(p0)
    p = np.outer(p0, np.ones(ndim+1))
    for i in range(ndim):
        p[i][i+1]+=scale[i]

    y=np.zeros(ndim+1)+func(p[:, 0],**funcargs)
    for i in range(1,ndim+1):
        y[i]=func(p[:, i],**funcargs)
    
    # list holding your trying route
    pars=copy.deepcopy(p)    # p: (ndim,ndim+1) positions of each simplex vertex
    chi2=copy.deepcopy(y)    # y: (ndim+1) chi2 at each simplex vertex
    
    niter=0
    psum=np.sum(p, axis=1)

    while niter<=maxiter:
        
        y=y-temperature*np.log(np.random.random(ndim+1))

        s=np.argsort(y)
        ilo=s[0]                            # index to Lowest chi^2
        ihi=s[-1]                           # index to Highest chi^2
        inhi=s[-2]                          # index to Next highest chi^2
        d=np.abs(y[ihi])+np.abs(y[ilo])     # denominator = interval
        
        if  verbose==True:
            #print(niter,np.abs(y[ilo]),np.abs(y[ihi]))
            logger.debug('{}'.format(pars[:,np.argmin(chi2)]))
            logger.debug(('{0:>6d} {1:>'+format_prec+'} {2:>'+format_prec+'}')
                  .format(int(niter),np.abs(y[ilo]),np.abs(y[ihi])))
        
        if  d!=0.0:                         # compute fractional change in chi^2
            rtol=2.0*np.abs(y[ihi]-y[ilo])/d
        else:                               # terminate if denominator is 0
            rtol=ftol/2.  

        if  rtol<ftol or niter==maxiter:
            #print rtol,ftol
            break

        niter=niter+2
        #print '->',psum
        p,psum,pars,chi2,ytry=amotry_sa(func,p,psum,ihi,-1.0,y,
                       temperature=temperature,
                       p_up=p_up,p_lo=p_lo,
                       pars=pars,chi2=chi2,funcargs=funcargs)
        #print '<-',psum
        if  ytry<=y[ilo]:
            p,psum,pars,chi2,ytry=amotry_sa(func,p,psum,ihi,2.0,y,
                           temperature=temperature,
                           p_up=p_up,p_lo=p_lo,
                           pars=pars,chi2=chi2,funcargs=funcargs)
        else: 
            if  ytry>=y[inhi]:
                ysave=y[ihi] 
                p,psum,pars,chi2,ytry=amotry_sa(func,p,psum,ihi,0.5,y,
                               temperature= temperature,
                               p_up=p_up,p_lo=p_lo,
                               pars=pars,chi2=chi2,funcargs=funcargs)
                if  ytry>=ysave:
                    for i in range(ndim+1):
                        if  i!=ilo:
                            psum=0.5*(p[:, i] + p[:, ilo])
                            p[:, i] = psum
                            y[i] = func(psum,**funcargs)
                            pars=np.append(pars,np.expand_dims(psum,axis=1),axis=1)
                            chi2=np.append(chi2,y[i])
                    niter=niter + ndim
                    psum=np.sum(p, axis=1)
            else: 
                niter=niter-1
    
    dict={}
    #print chi2
    #print chi2[np.argmin(chi2)]
    dict['p_best']=pars[:,np.argmin(chi2)]
    dict['p0']=p0
    dict['niter']=niter
    dict['maxiter']=maxiter
    dict['ftol']=ftol
    dict['chi2']=chi2       # (ndim+1+niter)        chi2 at each simplex vertex
    dict['pars']=pars       # (ndim,ndim+1+niter)   positions of each simplex vertex
    dict['temperature']=temperature
    dict['p_up']=p_up
    dict['p_up']=p_lo
    
    np.seterr(divide='warn', invalid='warn')
    
    return  dict

def amotry_sa(func,p,psum,ihi,fac,y, 
              temperature=0.0, 
              p_up=+np.inf,p_lo=-np.inf,
              pars=None,chi2=None,
              funcargs=None):
    # we can return modified parameters via mutable variales
    # but it's not safe in general
    # we return stack variables instead
    fac1=(1.0-fac)/len(psum)
    fac2=fac1-fac
    ptry=np.maximum(np.minimum(psum*fac1-p[:,ihi]*fac2,p_up),p_lo)
    
    ytry=func(ptry,**funcargs)

    
    pars=np.append(pars,np.expand_dims(ptry,axis=1),axis=1)
    chi2=np.append(chi2,ytry)
 
    ytry = ytry+temperature*np.log(np.random.random())  
    if  ytry<y[ihi]:
        y[ihi]=ytry
        #psum=psum+ptry-p[:, ihi] #(don't use this as we don't want to change psum id (just modify it) 
        psum+=ptry-p[:, ihi]
        p[:,ihi] = ptry
        
    return  p,psum,pars,chi2,ytry
           