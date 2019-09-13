from .gmake_init import *
from .model_utils import * 

import numpy as np
import copy
import sys
import logging

logger = logging.getLogger(__name__)

def amoeba_setup(inp_dct,dat_dct,initial_model=False):
    
    
    opt_dct=inp_dct['optimize']
    
    fit_dct={'optimize':opt_dct.copy()}
    fit_dct['p_start']=[]
    fit_dct['p_lo']=[]
    fit_dct['p_up']=[]
    fit_dct['p_name']=[]
    fit_dct['p_iscale']=[]
    
    
    for p_name in opt_dct.keys():
        if  '@' not in p_name:
            continue
        fit_dct['p_name']=np.append(fit_dct['p_name'],[p_name])
        fit_dct['p_start']=np.append(fit_dct['p_start'],np.mean(gmake_readpar(inp_dct,p_name)))

        if  opt_dct[p_name][0]=='a' or opt_dct[p_name][0]=='r' or opt_dct[p_name][0]=='o': 
            si=1 ; mode=deepcopy(opt_dct[p_name][0])
        else:
            si=0 ; mode='a'
        fit_dct['p_lo']=np.append(fit_dct['p_lo'],
                                  gmake_read_range(center=fit_dct['p_start'][-1],
                                                   delta=opt_dct[p_name][si+0],
                                                   mode=mode))
        fit_dct['p_up']=np.append(fit_dct['p_up'],
                                  gmake_read_range(center=fit_dct['p_start'][-1],
                                                   delta=opt_dct[p_name][si+1],
                                                   mode=mode))                                  
        fit_dct['p_iscale']=np.append(fit_dct['p_iscale'],
                                  gmake_read_range(center=fit_dct['p_start'][-1],
                                                   delta=opt_dct[p_name][si+2],
                                                   mode=mode))

    gmake_pformat(fit_dct)    
    
    fit_dct['ndim']=len(fit_dct['p_start'])
    fit_dct['nthreads']=1
    fit_dct['outfolder']=opt_dct['outdir']
    
    if  (not os.path.exists(fit_dct['outfolder'])) and fit_dct['outfolder']!='':
        os.makedirs(fit_dct['outfolder'])

    
    fit_dct['ndim']=len(fit_dct['p_start'])
    #   turn off mutiple-processing since mkl_fft has been threaded.
    fit_dct['nthreads']=1   #multiprocessing.cpu_count()
    #fit_dct['nwalkers']=opt_dct['nwalkers']
    fit_dct['outfolder']=opt_dct['outdir']
    
    #print('nwalkers:',fit_dct['nwalkers'])
    #print('nthreads:',fit_dct['nthreads'])
    logger.debug('ndim:    '+str(fit_dct['ndim']))
    logger.debug('outdir:  '+str(fit_dct['outfolder']))    
    
    np.save(fit_dct['outfolder']+'/dat_dct.npy',dat_dct)
    #np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)   #   fitting metadata
    #np.save(fit_dct['outfolder']+'/inp_dct.npy',inp_dct)   #   input metadata    
    
    if  initial_model==True:
        theta_start=fit_dct['p_start']
        lnl,blobs=gmake_model_lnprob(theta_start,fit_dct,inp_dct,dat_dct,savemodel=fit_dct['outfolder']+'/p_start')
        logger.debug('p_start:    ')
        logger.debug(pformat(blobs))
        #pprint.pprint(blobs)    
    
    return fit_dct

def amoeba_iterate(fit_dct,inp_dct,dat_dct,nstep=500):
    """
    calling amoeba
    """

    p_amoeba=amoeba_sa(model_chisq,fit_dct['p_start'],fit_dct['p_iscale'],
                       p_lo=fit_dct['p_lo'],p_up=fit_dct['p_up'],
                       funcargs={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct},
                       ftol=1e-10,temperature=0,
                       maxiter=nstep,verbose=True)

    fit_dct['p_amoeba']=p_amoeba
    
    np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)
    dct2fits(p_amoeba,outname=fit_dct['outfolder']+'/amoeba_chain')
    
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
    fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
    p_name=fit_dct['p_name']
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    p_start=fit_dct['p_start']
    p_format=fit_dct['p_format']
    p_format_prec=fit_dct['p_format_prec']
    
    #t=Table.read(outfolder+'/'+'amoeba_chain.fits')
    #chi2=t['chi2'].data[0]
    #pars=t['pars'].data[0]
    #p_best=t['p_best'].data[0]
    
    chi2=fit_dct['p_amoeba']['chi2']
    pars=fit_dct['p_amoeba']['pars']
    p_best=fit_dct['p_amoeba']['p_best']
                             
    
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
    
    figsize=(8.*2.0,ndim*2.5)
    pl.clf()
    ncol=3
    nrow=int(np.ceil(ndim*1.0/1))
    fig, axes = pl.subplots(nrow+1,ncol,figsize=figsize,squeeze=True)
    
    for i in range(ndim):
        
        axes[i,0].plot(np.arange(niter),(pars[i,:]).T, color="gray", alpha=0.4)
        ymin, ymax = axes[i,0].get_ylim()
        axes[i,0].set_ylim(ymin, ymax)
        axes[i,0].set_xlim(0, niter)
        axes[i,0].axhline(p_lo[i], color="r", lw=0.8,ls='-')
        axes[i,0].axhline(p_up[i], color="r", lw=0.8,ls='-')
        axes[i,0].axhline(p_start[i],color="b", lw=2,ls='-')
        axes[i,0].set_ylabel(p_name[i])
        axes[i,0].axhline(p_best[i],color="g", lw=3,ls='-')
        axes[i,0].set_title(("{0:"+p_format[i]+"}").format(p_start[i]),color="b")
        
        if  i==ndim-1:
            axes[i,0].set_xlabel("step number")

        
        axes[i,1].plot(np.arange(burnin,niter),pars[i,burnin:].T, color="gray", alpha=0.4)
        ymin, ymax = axes[i,1].get_ylim()
        axes[i,1].set_ylim(ymin, ymax)
        axes[i,1].set_xlim(burnin, niter)
        axes[i,1].axhline(p_lo[i], color="r", lw=0.8,ls='-')
        axes[i,1].axhline(p_up[i], color="r", lw=0.8,ls='-')
        axes[i,1].axhline(p_start[i],color="b", lw=2,ls='-')
        axes[i,1].axhline(p_best[i],color="g", lw=3,ls='-')
        axes[i,1].set_title(("{0:"+p_format[i]+"}").format(p_best[i]),color="g")
        
        if  i==ndim-1:
            axes[i,1].set_xlabel("step number")
            
        
        ymin=np.nanmin(chi2[burnin:])
        ymax=np.nanmax(chi2[burnin:])
        axes[i,2].set_ylim(ymin, ymax)
        
        pick_ind=np.where(np.logical_and(chi2 < ymax,chi2 > ymin))
        axes[i,2].plot(pars[i,pick_ind].T,chi2[pick_ind],'o',color="gray", alpha=0.4,)        
        
        axes[i,2].axvline(p_best[i], ls='-', color='g',lw=3)
        axes[i,2].axvline(p_start[i], ls='-', color='b',lw=3)
        axes[i,2].set_xlabel(fit_dct['p_name'][i])         

    axes[i+1,0].plot(np.arange(niter),chi2)
    axes[i+1,1].plot(np.arange(burnin,niter),chi2[burnin:])
    axes[i+1,1].set_title(("{0}").format(np.nanmin(chi2)),color="g")
    
    fig.delaxes(axes[i+1,2])
    axes[i+1,0].set_ylabel('Goodness Scale')
                    
                
    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/iteration.pdf"
    fig.savefig(figname)
    pl.close()       


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