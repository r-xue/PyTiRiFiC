import builtins
from multiprocessing import Pool
import socket
import emcee
from matplotlib.colors import LogNorm
from matplotlib.ticker import MaxNLocator
import gmake.meta as meta
import corner
from numpy.lib import recfunctions as rfn
from matplotlib import cm
from lmfit import minimize
from lmfit import report_fit
from .evaluate import *
import numpy as np
import copy
import sys
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)
from galario.single import threads as galario_threads
import os
from memory_profiler import profile
from .evaluate import calc_chisq
from .evaluate import log_likelihood
import pyfftw
from .meta import *

def opt_analyze(inpfile,burnin=None,copydata=True,export=False):
    
    inp_dct=read_inp(inpfile)
    outfolder=inp_dct['general']['outdir']
    if  'analyze' in inp_dct:
        if  'burnin' in inp_dct['analyze']:
            burnin=inp_dct['analyze']['burnin']
    
    if  'amoeba' in inp_dct['optimize']['method']:
        chisq_analyze(outfolder,burnin=burnin)
        #fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        #fit_dct=hdf2dct(outfolder+'/fit.h5')
        #theta_start=fit_dct['p_start']
        #theta_end=fit_dct['p_best']        
    
    if  'emcee' in inp_dct['optimize']['method']:
        emcee_analyze(outfolder,burnin=burnin)
        #fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        #fit_dct=hdf2dct(outfolder+'/fit.h5')
        #theta_start=fit_dct['p_start']
        #theta_end=fit_dct['p_median']
    
    if  'lmfit-nelder' in inp_dct['optimize']['method']:
        chisq_analyze(outfolder,burnin=burnin)
        #fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        #theta_start=fit_dct['p_start']
        #theta_end=np.array(list(fit_dct['p_lmfit_result'].params.valuesdict().values()))  
    
    if  'lmfit-brute' in inp_dct['optimize']['method']:
        brute_analyze(outfolder)
        #fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
        #theta_start=fit_dct['p_start']
        #theta_end=fit_dct['p_lmfit_result'].brute_x0                
    
    
    if  export==True:
        
        dat_dct_path=outfolder+'/data.h5'
        if  os.path.isfile(dat_dct_path):
            logger.debug('reading data from'+str(dat_dct_path))
            dat_dct=hdf2dct(dat_dct_path)
        else:
            dat_dct=read_data(inp_dct,fill_mask=True,fill_error=True)
            if  copydata==True:
                dct2hdf(dat_dct,outname=dat_dct_path)
        
        for i in range(2):
            if  i==0:
                theta=theta_start
            if  i==1:
                theta=theta_end
                
            models,inp_dct,mod_dct=model_mapper(theta,fit_dct,inp_dct,dat_dct)
            
            outname_exclude=None
            if  'shortname' in inp_dct['general'].keys():
                outname_exclude=inp_dct['general']['shortname']
            if  'outname_exclude' in inp_dct['general'].keys():
                outname_exclude=inp_dct['general']['outname_exclude']
            outname_replace=None
            if  'outname_replace' in inp_dct['general'].keys():
                outname_replace=inp_dct['general']['outname_replace']
    
            export_model(models,outdir=outfolder+'/model_'+str(i),
                         outname_exclude=outname_exclude,
                         outname_replace=outname_replace)
            
            models_keys=list(models.keys())
            data_keys=list(dat_dct.keys())
            for key in models_keys:
                if  key in data_keys:
                    del models[key]
            dct2hdf(models,outfolder+'/model_'+str(i)+'/'+'models.h5')
            write_inp(inp_dct,inpfile=outfolder+'/model_'+str(i)+'/model.inp',overwrite=True)          
            
            
            #models_1=model_mapper(theta_end,fit_dct,inp_dct,dat_dct)
            #lnl,blobs=model_lnprob(theta_start,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/model_0',packblobs=True)
            #logger.debug('model_0: ')
            #logger.debug(pformat(blobs))
            
            #lnl,blobs=model_lnprob(theta_end,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/model_1',packblobs=True)
            #logger.debug('model_1: ')
            #logger.debug(pformat(blobs))


def chisq_analyze(outfolder,burnin=None):
    
    
    
    """
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
    """

    fit_dct=hdf2dct(outfolder+'/fit.h5')
    p_name=fit_dct['p_name']
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    p_start=fit_dct['p_start']
    p_format=fit_dct['p_format']
    p_unit=[q.unit for q in fit_dct['p_start']]
    p_format_prec=fit_dct['p_format_prec']
    
    
    p_chisq=hdf2dct(outfolder+'/chisq_chain.h5')
    chi2=p_chisq['blobs']['chi2']/p_chisq['ndata']
    pars=p_chisq['blobs']['pars']
    p_best=p_chisq['p_best']
    
    fit_dct['p_best']=p_best    
    dct2hdf(fit_dct,outfolder+'/'+'fit.h5')
    
    ndim=(pars.shape)[0]
    niter=(pars.shape)[1]

    if  burnin is None:
        burnin=int(niter*0.8)
    if  burnin>=niter:
        burnin=niter-10
    
    #   print out parameter shifting
    
    logger.debug("+"*80)
    logger.debug("Check optimized parameters:")
    maxlen=len(max(fit_dct['p_name'],key=len))
    for ind  in range(len(p_name)):
        textout=' {:{align}{width}} '.format(ind,align='<',width=2)
        textout+=' {:{align}{width}} '.format(p_name[ind],align='<',width=maxlen)
        textout+=' = {:{align}{width}{prec}} '.format(p_best[ind],align='^',width=13,prec=p_format_prec[ind])
        textout+=' <- {:{align}{width}{prec}} '.format(p_start[ind],align='^',width=13,prec=p_format_prec[ind])
        textout+=' ( {:{align}{width}{prec}}, '.format(p_lo[ind],align='^',width=13,prec=p_format_prec[ind])
        textout+=' {:{align}{width}{prec}} )'.format(p_up[ind],align='^',width=13,prec=p_format_prec[ind])
        logger.debug(textout)    
    logger.debug("-"*80)  
    
    #   PLOT PARAMETERS
    
    figsize=(20.0,ndim*3.0)
    plt.clf()
    ncol=4
    nrow=int(np.ceil(ndim*1.0/1))
    fig, axes = plt.subplots(nrow+1,ncol,figsize=figsize,squeeze=True)
    
    for i in range(ndim):
        
        offset=0
        scale=1
        p_unit_display=p_unit[i]
        if  'xypos.ra' in p_name[i] or 'xypos.dec' in p_name[i]:
            offset=p_start[i].value
            scale=3600 # deg -> sec
            p_unit_display=u.arcsec
        
        for j in [0,1]:
            
            step_start=0 if j==0 else burnin
            
            axes[i,j].plot(np.arange(step_start,niter),((pars[i,step_start:]).T-offset)*scale, color="gray", alpha=0.4)
            ymin, ymax = axes[i,j].get_ylim()
            axes[i,j].set_ylim(ymin, ymax)
            axes[i,j].set_xlim(step_start, niter)
            
            if  j==1:
                axes[i,j-1].axvspan(step_start,niter,color='whitesmoke')
            
            axes[i,j].axhline(((p_lo[i].value-offset)*scale), color="r", lw=0.8,ls='-')
            axes[i,j].axhline(((p_up[i].value-offset)*scale), color="r", lw=0.8,ls='-')
            
            label_start=label_best=''
            if  j==0:
                label_start='Initial: '+("{0:"+p_format[i]+"}").format(p_start[i]*p_unit[i])
            else:
                label_best='Optimized:'+("{0:"+p_format[i]+"}").format(p_best[i]*p_unit[i])
            
            axes[i,j].axhline(((p_start[i].value-offset)*scale),color="b", lw=9,ls='-',label=label_start,alpha=0.4)
            axes[i,j].axhline(((p_best[i].value-offset)*scale),color="g", lw=3,ls='-',label=label_best)
            #axes[i,0].set_ylabel(("{0:"+p_format[i]+"}").format(p_start[i]*p_unit[i]),color="b")
            if  j==0:
                axes[i,j].set_title(p_name[i]+' ['+(p_unit_display.to_string())+']')
            
            show_labels=''
            axes[i,j].legend(loc='upper right')

            chi2_selected=chi2[step_start:]

            ymin=np.min(chi2_selected[np.isfinite(chi2_selected)])
            ymax=np.max(chi2_selected[np.isfinite(chi2_selected)])    
            axes[i,j+2].set_ylim(ymin, ymax)
            if  j==0:
                axes[i,j+2].set_ylabel('$\chi^2_{red}$')
            if  j==1:
                axes[i,j+2-1].axhspan(ymin,ymax,color='whitesmoke')
            #axes[i,j+2].text(0.9,0.8,'$\chi^2_{red}<$'+str(ymax),transform=axes[i,j+2].transAxes)
            
            pick_ind=np.where(np.logical_and(chi2 < ymax,chi2 > ymin))
            axes[i,j+2].plot((pars[i,pick_ind].T-offset)*scale,chi2[pick_ind],'o',color="gray", alpha=0.4,)        
            
            
            axes[i,j+2].axvline(((p_start[i].value-offset)*scale), ls='-', color='b',lw=9,alpha=0.4)
            axes[i,j+2].axvline(((p_best[i].value-offset)*scale), ls='-', color='g',lw=3)
            axes[i,j+2].set_xlabel(p_name[i]+' ['+(p_unit_display.to_string())+']')
                     

    axes[i+1,0].plot(np.arange(0,niter),chi2)
    axes[i+1,0].set_xlim(0, niter)
    axes[i+1,1].plot(np.arange(burnin,niter),chi2[burnin:])
    axes[i+1,1].set_xlim(step_start, niter)
    #axes[i+1,1].set_title(("{0}").format(np.nanmin(chi2)),color="g")
    fig.delaxes(axes[i+1,2])
    fig.delaxes(axes[i+1,3])
    axes[i+1,0].set_ylabel('Goodness Scale')
    axes[i+1,1].set_ylabel('Goodness Scale')
    axes[i+1,0].set_xlabel("Iteration")
    axes[i+1,1].set_xlabel("Iteration")
                    
                
    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/chisq-iteration.pdf"
    fig.savefig(figname)
    plt.close()       
    logger.debug("analyzing outfolder:"+outfolder)
    logger.debug("plotting..."+figname)  

def emcee_analyze(outfolder,
                  burnin=None,
                  modebin=10,
                  plotqtile=True,
                  plotlevel=False,
                  plotsub=None,
                  plotcorner=True,
                  plotburnin=True):
    """
    # Print out the mean acceptance fraction. In general, acceptance_fraction
    # has an entry for each walker so, in this case, it is a 50-dimensional
    # vector.
    # This number should be between approximately 0.25 and 0.5 if everything went as planned.
    """
    h5name=outfolder+'/'+'emcee_chain.h5'
    reader = emcee.backends.HDFBackend(h5name,read_only=True)
    tau=reader.get_autocorr_time(quiet=True)
    thin=1
    
    chain_array=reader.get_chain(flat=False,discard=0,thin=thin)

    fullsamples = reader.get_chain(flat=True,discard=0,thin=thin)
    if  burnin is None:
        burnin=int((chain_array.shape)[0]*0.5)
    logger.debug("select burnin:   {0}".format(burnin))    
    niter=(chain_array.shape)[0]
    logger.debug("chain shape  :   {0}".format(chain_array.shape))
    
    # gether info
    samples = reader.get_chain(flat=True,discard=burnin,thin=thin)
    log_prob_samples = reader.get_log_prob(discard=burnin, flat=True, thin=thin)
    #print(samples.shape,log_prob_samples.shape)
    samples_with_logprob=np.concatenate((samples,log_prob_samples[:,None]),axis=1)
    blobs_samples = reader.get_blobs(discard=0, thin=thin)
    
    # add lnprob to blobs_samples
    lnprob=reader.get_log_prob(thin=thin)
    dt=np.dtype(blobs_samples.dtype.descr+[('lnprob',float)])
    new_blobs_samples = np.zeros(blobs_samples.shape, dtype=dt)
    new_blobs_samples['chisq']=blobs_samples['chisq']
    new_blobs_samples['lnprob']=lnprob
    blobs_samples=new_blobs_samples
    
    #   chain_array # (nstep-discard)/thin x nwalker x npar     when flat==False
    #   blobs       # (nstep-discard)/thin x nwalker            when flat==False
    
    fit_dct=hdf2dct(outfolder+'/'+'fit.h5')
    p_format=fit_dct['p_format']
    p_name=fit_dct['p_name']
    p_scale=np.array([q.value for q in fit_dct['p_scale']])
    p_lo=np.array([q.value for q in fit_dct['p_lo']])
    p_up=np.array([q.value for q in fit_dct['p_up']])
    p_start=np.array([q.value for q in fit_dct['p_start']])
    
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
    plt.clf()
    picki=range(len(p_name))
    nrow=int(np.ceil(len(picki)*1.0/1))
    fig, axes = plt.subplots(nrow,2,sharex=False,figsize=figsize,squeeze=False)
    cc=0
    for i in picki:
        
        for j in [0,1]:
            iy=i
            #ix=int((cc - iy)/nrow)
            ix=j
            if  ix==0:
                axes[iy,ix].plot(np.arange(0,niter),chain_array[:, :, i], color="gray", alpha=0.4)
                #axes[iy,ix].axvline(burnin, color="c", lw=2,ls=':')
                ymin, ymax = axes[iy,ix].get_ylim()
                axes[iy,ix].set_ylim(ymin, ymax)
                axes[iy,ix].set_xlim(0,niter)
            if  ix==1:
                axes[iy,ix].plot(np.arange(burnin,niter),chain_array[burnin:, :, i], color="gray", alpha=0.4)
                axes[iy,ix].set_xlim(burnin,niter)
                ymin, ymax = axes[iy,ix].get_ylim()
                axes[iy,ix].set_ylim(ymin, ymax)
                axes[iy,ix].set_xlim(burnin,niter)
            axes[iy,ix].yaxis.set_major_locator(MaxNLocator(5))
            
            xmin, xmax = axes[iy,ix].get_xlim()
            bfrac=(burnin-xmin)/(xmax-xmin)
            axes[iy,ix].axhline(p_start[i],xmax=bfrac, color="b", lw=2,ls='-')
            axes[iy,ix].axhline(p_start[i]+p_scale[i],xmax=bfrac, color="b", lw=2,ls='--')
            axes[iy,ix].axhline(p_start[i]-p_scale[i],xmax=bfrac, color="b", lw=2,ls='--')
            
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
        logger.debug("plotting..."+outfolder+"/emcee-corner.pdf")
        logger.debug("input data size:"+str(np.shape(samples)))
        tic=time.time()
        quantiles=None
        if  plotqtile==True:
            quantiles=[0.16, 0.5, 0.84]
        levels=None
        if  plotlevel==True:
            levels=(1-np.exp(-0.5),) 
        #print(samples.shape)       #
        #fig = corner.corner(samples_with_logprob, labels=p_name+['logprob'],quantiles=quantiles,levels=levels,quiet=False)
        fig = corner.corner(samples, labels=p_name,truths=p_start,quantiles=quantiles,levels=levels,quiet=False)
        ndim=len(p_start)
        #axes = np.array(fig.axes).reshape((ndim+1, ndim+1))
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


    
    
def brute_analyze(outfolder):
    
    
    fit_dct=hdf2dct(outfolder+'/fit.h5')
    p_name=fit_dct['p_name']
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    p_start=fit_dct['p_start']
    p_format=fit_dct['p_format']
    p_unit=[q.unit for q in fit_dct['p_start']]
    p_format_prec=fit_dct['p_format_prec']
    
    
    p_chisq=hdf2dct(outfolder+'/chisq_chain.h5')
    chi2=p_chisq['blobs']['chi2']/p_chisq['ndata']
    pars=p_chisq['blobs']['pars']
    p_best=p_chisq['p_best']

    fit_dct['p_best']=p_best    
    dct2hdf(fit_dct,outfolder+'/'+'fit.h5')    
    result=p_chisq['result']
    
    # min position
    # result.brute_x0
    # min value
    # result.brute_fval
    # fval grid
    # result.brute_Jout
    
    # p1_grid= np.unique(result.brute_grid[0].ravel())
    # p2_grid= np.unique(result.brute_grid[1].ravel())
    #grid_x, grid_y = [np.unique(par.ravel()) for par in result.brute_grid]
    
    
    #   iteration plot
    
    print(result.brute_grid.shape)
    ndim=result.brute_x0.size
    bt_grid=result.brute_grid
    if  ndim==1:
        bt_grid=result.brute_grid[np.newaxis]
        bt_x0=result.brute_x0[np.newaxis]
        
    else:
        bt_grid=result.brute_grid
        bt_x0=result.brute_x0
    
    
    figsize=(4.*2.0,ndim*2.5)
    plt.clf()
    ncol=2
    nrow=int(np.ceil(ndim*1.0/1))
    fig, axes = plt.subplots(nrow,ncol,figsize=figsize,squeeze=True)
    if  ndim==1:
        axes=axes[np.newaxis,:]
    print(result.brute_Jout.shape)
    print(result.brute_grid.shape)

    
    for i in range(ndim):

        pchain=(bt_grid[i,:]).ravel()
        axes[i,0].plot(np.arange(1,pchain.size+1),pchain, color="gray", alpha=0.4)
        axes[i,0].set_ylabel(fit_dct['p_name'][i])               
                       
        axes[i,1].plot(pchain,
                     result.brute_Jout.ravel(),
                     'o', color="gray", alpha=0.4)
        axes[i,1].axvline(bt_x0[i], ls='-', color='g',lw=3)
        axes[i,1].set_xlabel(fit_dct['p_name'][i]) 
        
        if  i==ndim-1:
            axes[i,0].set_xlabel('$feval_grid_index$') 
            
    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/brute-iteration.pdf"
    fig.savefig(figname)
    plt.close()     

    #   corner plot
    
    best_vals=True
    output=outfolder+"/brute-corner.pdf"
    figsize=(8,8)
    npars = len(result.var_names)
    fig, axes = plt.subplots(npars, npars,figsize=figsize)
    varlabels=p_name
    
    if  best_vals and isinstance(best_vals, bool):
        best_vals = result.params

    for i, par1 in enumerate(result.var_names):
        for j, par2 in enumerate(result.var_names):

            # parameter vs chi2 in case of only one parameter
            if  npars == 1:
                axes.plot(result.brute_grid, result.brute_Jout, 'o', ms=3)
                axes.set_ylabel(r'$\chi^{2}$')
                axes.set_xlabel(varlabels[i])
                if  best_vals:
                    axes.axvline(best_vals[par1].value, ls='dashed', color='r')

            # parameter vs chi2 profile on top
            elif i == j and j < npars-1:
                if i == 0:
                    axes[0, 0].axis('off')
                ax = axes[i, j+1]
                red_axis = tuple([a for a in range(npars) if a != i])
                ax.plot(np.unique(result.brute_grid[i]),
                        np.minimum.reduce(result.brute_Jout, axis=red_axis),
                        'o', ms=3)
                ax.set_ylabel(r'$\chi^{2}$')
                ax.yaxis.set_label_position("right")
                ax.yaxis.set_ticks_position('right')
                ax.set_xticks([])
                if  best_vals:
                    ax.axvline(best_vals[par1].value, ls='dashed', color='r')

            # parameter vs chi2 profile on the left
            elif j == 0 and i > 0:
                ax = axes[i, j]
                red_axis = tuple([a for a in range(npars) if a != i])
                ax.plot(np.minimum.reduce(result.brute_Jout, axis=red_axis),
                        np.unique(result.brute_grid[i]), 'o', ms=3)
                ax.invert_xaxis()
                ax.set_ylabel(varlabels[i])
                if i != npars-1:
                    ax.set_xticks([])
                elif i == npars-1:
                    ax.set_xlabel(r'$\chi^{2}$')
                if  best_vals:
                    ax.axhline(best_vals[par1].value, ls='dashed', color='r')

            # contour plots for all combinations of two parameters
            elif j > i:
                ax = axes[j, i+1]
                red_axis = tuple([a for a in range(npars) if a != i and a != j])
                X, Y = np.meshgrid(np.unique(result.brute_grid[i]),
                                   np.unique(result.brute_grid[j]))
                lvls1 = np.linspace(result.brute_Jout.min(),
                                    np.median(result.brute_Jout),10, dtype='int')
                lvls2 = np.linspace(np.median(result.brute_Jout),
                                    np.max(result.brute_Jout), 10, dtype='int')
                lvls = np.unique(np.concatenate((lvls1, lvls2)))
                local_brute=np.minimum.reduce(result.brute_Jout, axis=red_axis)
                local_max=np.max(local_brute)
                global_max=np.max(result.brute_Jout)
                #lvls1 = np.linspace(result.brute_Jout.min(),
                #                    local_max=,10, dtype='int')
                #lvls2 = np.linspace(np.median(result.brute_Jout),
                #                    np.max(result.brute_Jout), 10, dtype='int')               
                ax.contourf(X.T, Y.T, local_brute,
                            cmap=cm.coolwarm,levels=10) #, norm=LogNorm(),lvls
                print(par1,par2,lvls)
                ax.set_yticks([])
                if  best_vals:
                    ax.axvline(best_vals[par1].value, ls='dashed', color='r')
                    ax.axhline(best_vals[par2].value, ls='dashed', color='r')
                    ax.plot(best_vals[par1].value, best_vals[par2].value, 'rs', ms=3)
                if  j != npars-1:
                    ax.set_xticks([])
                elif j == npars-1:
                    ax.set_xlabel(varlabels[i])
                if  j - i >= 2:
                    axes[i, j].axis('off')
                    
    if output is not None:
        plt.savefig(output)  
        print(output)  
    

    return

 

