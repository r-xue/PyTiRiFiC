
from .model_eval import * 

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


def amoeba_iterate(fit_dct,inp_dct,dat_dct,nstep=100):
    """
    calling amoeba
    """
    
    logger.debug(" ")
    logger.debug("Running AMOEBA...")
    logger.debug(">>"+fit_dct['outfolder']+"/amoeba_chain.h5")
    logger.debug(" ")    

    host_nthread=multiprocessing.cpu_count()
    galario_threads(host_nthread)
    os.environ["OMP_NUM_THREADS"] = str(host_nthread)

    p_amoeba=amoeba_sa(model_chisq,fit_dct['p_start'],fit_dct['p_scale'],
                       p_lo=fit_dct['p_lo'],p_up=fit_dct['p_up'],
                       funcargs={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct},
                       ftol=1e-10,temperature=0,
                       maxiter=nstep,verbose=True)
    lnl,blobs=model_lnlike(p_amoeba['p_best'],fit_dct,inp_dct,dat_dct)
    p_amoeba['blobs']=blobs
    dct2hdf(p_amoeba,outname=fit_dct['outfolder']+'/amoeba_chain.h5')
    
    return

def amoeba_analyze(outfolder,
                         burnin=None):
    
    
    
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
    p_unit=fit_dct['p_unit']
    p_format_prec=fit_dct['p_format_prec']
    
    #t=Table.read(outfolder+'/'+'amoeba_chain.fits')
    #chi2=t['chi2'].data[0]
    #pars=t['pars'].data[0]
    #p_best=t['p_best'].data[0]
    
    p_amoeba=hdf2dct(outfolder+'/amoeba_chain.h5')
    
    blobs=p_amoeba['blobs']
    ndp=blobs['ndata']
    chi2=p_amoeba['chi2']/blobs['ndata']
    pars=p_amoeba['pars']
    p_best=p_amoeba['p_best']
    
    fit_dct['p_best']=p_best
    
    dct2hdf(fit_dct,outfolder+'/'+'fit.h5')
    
                             
    
    ndim=(pars.shape)[0]
    niter=(pars.shape)[1]
    if  burnin is None:
        burnin=int(niter*0.8)
    
    #   print out parameter shifting
    
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
            offset=p_start[i]
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
            
            axes[i,j].axhline((p_lo[i]-offset)*scale, color="r", lw=0.8,ls='-')
            axes[i,j].axhline((p_up[i]-offset)*scale, color="r", lw=0.8,ls='-')
            
            label_start=label_best=''
            if  j==0:
                label_start='Initial: '+("{0:"+p_format[i]+"}").format(p_start[i]*p_unit[i])
            else:
                label_best='Optimized:'+("{0:"+p_format[i]+"}").format(p_best[i]*p_unit[i])
            
            axes[i,j].axhline((p_start[i]-offset)*scale,color="b", lw=9,ls='-',label=label_start,alpha=0.4)
            axes[i,j].axhline((p_best[i]-offset)*scale,color="g", lw=3,ls='-',label=label_best)
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
            
            
            axes[i,j+2].axvline((p_start[i]-offset)*scale, ls='-', color='b',lw=9,alpha=0.4)
            axes[i,j+2].axvline((p_best[i]-offset)*scale, ls='-', color='g',lw=3)
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
    figname=outfolder+"/iteration.pdf"
    fig.savefig(figname)
    plt.close()       
    logger.debug("analyzing outfolder:"+outfolder)
    logger.debug("plotting..."+figname)      


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