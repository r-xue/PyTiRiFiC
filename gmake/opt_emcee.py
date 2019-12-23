
from .model_eval import * 
from .model_eval2 import *

import builtins
from multiprocessing import Pool
import os
import socket
import emcee

from galario.single import threads as galario_threads

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import logging
logger = logging.getLogger(__name__)

import gmake.meta as meta
import corner 

    
def emcee_iterate(fit_dct,inp_dct,dat_dct,nstep=100,
                  mctest=False):
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

    """
    emcee v3
        https://emcee.readthedocs.io/en/latest/tutorials/monitor/
    """
    index=0
    autocorr=np.empty(fit_dct['nstep'])
    old_tau=np.inf
    
    h5name=fit_dct['outfolder']+'/emcee_chain.h5'
    os.system('rm -rf '+h5name)
    fit_dct['backend']=h5name
    backend = emcee.backends.HDFBackend(h5name)
    backend.reset(fit_dct['nwalkers'],fit_dct['ndim'])
    
    # initilize the sampler
    dtype = [("lnprob",float),("chisq",float),("ndata",int),("npar",int)]    
    
    host_nthread=multiprocessing.cpu_count()
    
    logger.info('hostname: {0}; {1} CPU cores'.format(socket.gethostname(),host_nthread))
    logger.info('emcee threading: {0}'.format(fit_dct['nthreads']))
    
    omp_nthread=1 if fit_dct['nthreads']>=2 else host_nthread
    logger.info('OpenMP threading: {0}'.format(omp_nthread))
    galario_threads(omp_nthread)
    os.environ["OMP_NUM_THREADS"] = str(omp_nthread)        
    
    
    if  fit_dct['nthreads']==1:
        sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                    model_lnprob,backend=backend,blobs_dtype=dtype,
                                    args=(fit_dct,inp_dct,dat_dct),
                                    runtime_sortingfn=sort_on_runtime)
        sampler.run_mcmc(fit_dct['pos_last'],fit_dct['nstep'],progress=True)
    else:
        print("try pool")
        with Pool(processes=fit_dct['nthreads']) as pool:
            #   use model_lnprob_globe without the keyword dat_dct to avoid redundant data pickling  
            sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                        model_lnprob_global2,backend=backend,blobs_dtype=dtype,
                                        args=(fit_dct,inp_dct),
                                        runtime_sortingfn=sort_on_runtime,pool=pool)
            sampler.run_mcmc(fit_dct['pos_last'],fit_dct['nstep'],progress=True)            
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
    
    galario_threads(host_nthread)
    os.environ["OMP_NUM_THREADS"] = str(host_nthread)        

    logger.debug("Done.")
    logger.debug('Took {0} minutes'.format(float(time.time()-tic)/float(60.)))

    return

def emcee_analyze(outfolder,
                       burnin=None,
                       modebin=10,
                       plotqtile=True,
                       plotlevel=False,
                       plotsub=None,
                       plotcorner=True,
                       plotburnin=True
                       ):
    """
    # Print out the mean acceptance fraction. In general, acceptance_fraction
    # has an entry for each walker so, in this case, it is a 50-dimensional
    # vector.
    # This number should be between approximately 0.25 and 0.5 if everything went as planned.
    """
    h5name=outfolder+'/'+'emcee_chain.h5'
    reader = emcee.backends.HDFBackend(h5name,read_only=True)
    
    thin=1
    
    chain_array=reader.get_chain(flat=False,discard=0,thin=thin)
    fullsamples = reader.get_chain(flat=True,discard=0,thin=thin)
    if  burnin is None:
        burnin=int((chain_array.shape)[0]*0.5)    
    
    samples = reader.get_chain(flat=True,discard=burnin,thin=thin)
    log_prob_samples = reader.get_log_prob(discard=burnin, flat=True, thin=thin)
    blobs_samples = reader.get_blobs(discard=0, thin=thin)
    
    
    #   chain_array # (nstep-discard)/thin x nwalker x npar     when flat==False
    #   blobs       # (nstep-discard)/thin x nwalker            when flat==False
    
    fit_dct=hdf2dct(outfolder+'/'+'fit.h5')
    p_format=fit_dct['p_format']
    p_name=fit_dct['p_name']
    p_scale=fit_dct['p_scale']
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    p_start=fit_dct['p_start']
    
    p_ptiles=list(map(lambda v: v,zip(*np.percentile(samples,[2.5,16.,50.,84.,97.5],axis=0))))
    p_median=p_error1=p_error2=p_error3=p_error4=p_int1=p_int2=p_mode=np.array([])    
    
    logger.debug('+'*90)
    
    for index in range(len(p_ptiles)):
        
        #tmp0=stats.mode(np.around(samples[:,index],decimals=3))
        hist,bin_edges=np.histogram(samples[:,index],modebin)
        bin_cent=.5*(bin_edges[:-1] + bin_edges[1:])
        tmp0=bin_cent[np.argmax(hist)]
        
        p_mode=np.append(p_mode,tmp0)
        p_median=np.append(p_median,p_ptiles[index][2])
        p_error1=np.append(p_error1,p_ptiles[index][1]-p_ptiles[index][2])
        p_error2=np.append(p_error2,p_ptiles[index][3]-p_ptiles[index][2])
        p_error3=np.append(p_error3,p_ptiles[index][0]-p_ptiles[index][2])
        p_error4=np.append(p_error4,p_ptiles[index][4]-p_ptiles[index][2])        
        p_int1=np.append(p_int1,p_ptiles[index][3]-p_ptiles[index][1])
        p_int2=np.append(p_int2,p_ptiles[index][4]-p_ptiles[index][0])
        p_ptiles[index]=list(p_ptiles[index])
        
        logger.debug(">>>  "+p_name[index]+":")
        logger.debug((" median(sigma) = {0:"+p_format[index]+"}"+\
                             " {1:"+p_format[index]+"}"+\
                             " {2:"+p_format[index]+"}"+\
                             " {3:"+p_format[index]+"}"+\
                             " {4:"+p_format[index]+"}").\
              format(     p_median[index],p_error3[index],p_error1[index],p_error2[index],p_error4[index]))
        logger.debug((" median(ptile) = {0:"+p_format[index]+"}"+\
                             " {1:"+p_format[index]+"}"+\
                             " {2:"+p_format[index]+"}"+\
                             " {3:"+p_format[index]+"}"+\
                             " {4:"+p_format[index]+"}").\
              format(     p_ptiles[index][2],p_ptiles[index][0],p_ptiles[index][1],p_ptiles[index][3],p_ptiles[index][4]))            
        logger.debug((" start(iscale) ="+\
                             " {0:"+p_format[index]+"}/{1:"+p_format[index]+"}").\
              format(        p_start[index],p_scale[index]))            
        logger.debug((" mode          ="+\
                             " {0:"+p_format[index]+"}").\
              format(        p_mode[index])) 
    
    logger.debug('-'*90)    


    #   ITERATION PARAMETR PLOTS

    figsize=(8.,(len(p_name))*2.5)
    ncol=1
    plt.clf()
    picki=range(len(p_name))
    nrow=int(np.ceil(len(picki)*1.0/ncol))
    fig, axes = plt.subplots(nrow,ncol,sharex=True,figsize=figsize,squeeze=False)
    cc=0
    for i in picki:
        iy=int(cc % nrow)
        ix=int((cc - iy)/nrow)
        if  plotburnin==False:
            axes[iy,ix].plot(chain_array[burin:, :, i], color="gray", alpha=0.4)
        else:
            axes[iy,ix].plot(chain_array[:, :, i], color="gray", alpha=0.4)
            axes[iy,ix].axvline(burnin, color="c", lw=2,ls=':')
        axes[iy,ix].yaxis.set_major_locator(MaxNLocator(5))
        ymin, ymax = axes[iy,ix].get_ylim()
        xmin, xmax = axes[iy,ix].get_xlim()
        bfrac=(burnin-xmin)/(xmax-xmin)
        axes[iy,ix].axhline(p_start[i],xmax=bfrac, color="b", lw=2,ls='-')
        axes[iy,ix].axhline(p_start[i]+p_scale[i],xmax=bfrac, color="b", lw=2,ls='--')
        axes[iy,ix].axhline(p_start[i]-p_scale[i],xmax=bfrac, color="b", lw=2,ls='--')
        axes[iy,ix].set_ylim(ymin, ymax)
        axes[iy,ix].axhline(p_lo[i], color="r", lw=0.8,ls='-')
        axes[iy,ix].axhline(p_up[i], color="r", lw=0.8,ls='-')
        axes[iy,ix].axhline(p_median[i]+p_error1[i],xmin=bfrac, color="g", lw=2,ls='--')
        axes[iy,ix].axhline(p_median[i]+p_error2[i],xmin=bfrac, color="g", lw=2,ls='--')
        axes[iy,ix].axhline(p_median[i]+p_error3[i],xmin=bfrac, color="g", lw=2,ls=':')
        axes[iy,ix].axhline(p_median[i]+p_error4[i],xmin=bfrac, color="g", lw=2,ls=':')
        axes[iy,ix].axhline(p_median[i],xmin=bfrac, color="g", lw=3,ls='-')
        axes[iy,ix].axhline(p_mode[i],xmin=bfrac, color="cyan", lw=3,ls='-')
        axes[iy,ix].set_ylabel(p_name[i])
        if  i==len(p_start)-1:
            axes[iy,ix].set_xlabel("step number")
        cc+=1
    if  cc==(nrow*2-1):
        axes[-1,-1].axis('off')

    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/emcee-iteration.pdf"
    fig.savefig(figname)
    plt.close()

    logger.debug("analyzing outfolder:"+outfolder)
    logger.debug("plotting..."+figname)

    #   ITERATION METADATA PLOTS
    
    m_name=['lnprob','chisq']
    t=blobs_samples
    
    figsize=(8.,8.)
    ncol=1
    plt.clf()
    picki=range(len(m_name))
    nrow=int(np.ceil(len(picki)*1.0/ncol))
    fig, axes = plt.subplots(nrow,ncol,sharex=True,figsize=figsize,squeeze=False)
    cc=0
    for i in picki:
        iy=int(cc % nrow)
        ix=int((cc - iy)/nrow)
        if  plotburnin==False:
            axes[iy,ix].plot(t[m_name[i]][burnin:,:], color="k", alpha=0.4)
        else:
            axes[iy,ix].plot(t[m_name[i]][:,:], color="gray", alpha=0.4)
            axes[iy,ix].axvline(burnin, color="c", lw=2,ls=':')
        axes[iy,ix].yaxis.set_major_locator(MaxNLocator(5))
        ymin, ymax = axes[iy,ix].get_ylim()
        xmin, xmax = axes[iy,ix].get_xlim()
        bfrac=(burnin-xmin)/(xmax-xmin)
        axes[iy,ix].set_ylim(ymin, ymax)
        axes[iy,ix].set_ylabel(m_name[i])
        
        if  m_name[i]=='blobs_chisq':
            axes[iy,ix].axhline(np.mean(t['blobs_ndata'].data[0][:,:]), color="r", lw=0.8,ls='-')
        if  i==len(m_name)-1:
            axes[iy,ix].set_xlabel("step number")
        cc+=1
    if  cc==(nrow*2-1):
        axes[-1,-1].axis('off')

    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/emcee-iteration-blobs.pdf"
    fig.savefig(figname)
    plt.close()
    logger.debug("analyzing outfolder:"+outfolder)
    logger.debug("plotting..."+figname)    

    
    
    #   CORNER PLOTS
    
    if  plotcorner==True:
        logger.debug("plotting..."+outfolder+"/line-triangle.pdf")
        logger.debug("input data size:"+str(np.shape(samples)))
        tic=time.time()
        quantiles=None
        if  plotqtile==True:
            quantiles=[0.16, 0.5, 0.84]
        levels=None
        if  plotlevel==True:
            levels=(1-np.exp(-0.5),)        
        fig = corner.corner(samples, labels=p_name,truths=p_start,quantiles=quantiles,levels=levels,quiet=True)
        
        ndim=len(p_start)
        axes = np.array(fig.axes).reshape((ndim, ndim))
        
        # Loop over the diagonal
        value1=p_start
        value2=p_median
        for i in range(ndim):
            ax = axes[i, i]
            ax.axvline(value1[i], color="b")
            ax.axvline(value2[i], color="g")
        
        # Loop over the histograms
        for yi in range(ndim):
            for xi in range(yi):
                ax = axes[yi, xi]
                ax.axvline(value1[xi], color="b")
                ax.axvline(value2[xi], color="g")
                ax.axhline(value1[yi], color="b")
                ax.axhline(value2[yi], color="g")
                ax.plot(value1[xi], value1[yi], "sg")
                ax.plot(value2[xi], value2[yi], "sr")
        
        fig.savefig(outfolder+"/emcee-corner.pdf")
        plt.close()
        logger.debug('Took {0} seconds'.format(float(time.time()-tic)))
    
    # Make the triangle plot.
    if  plotsub!=None:
        #plotsub is the parameter index array
        logger.debug("plotting..."+outfolder+"/line-triangle-sub.pdf")
        subsamples = chain_array[:, burnin:, plotsub].reshape((-1, len(plotsub)))
        tic=time.time()
        quantiles=None
        if  plotqtile==True:
            quantiles=[0.16, 0.5, 0.84]
        levels=None
        if  plotlevel==True:
            levels=(1-np.exp(-0.5),)        
        fig = corner.corner(subsamples, labels=p_name[plotsub],truths=p_start[plotsub],quantiles=quantiles,levels=levels,quiet=True)
        fig.savefig(outfolder+"/line-triangle-sub.pdf")
        plt.close()
        logger.debug('Took {0} seconds'.format(float(time.time()-tic)))    

    
    
    fit_dct['p_median']=p_median
    fit_dct['p_error1']=p_error1
    fit_dct['p_error2']=p_error2
    fit_dct['p_error3']=p_error3
    fit_dct['p_error4']=p_error4
    fit_dct['p_burnin']=burnin
    #t.add_column(Column(name='flatchain_samples', data=[  samples  ]),index=0)
    fit_dct['flatchain_samples']=samples
    fit_dct['p_ptiles']=p_ptiles
    fit_dct['p_mode']=p_mode
    
    dct2hdf(fit_dct,outfolder+'/'+'fit.h5')
    
    return 


