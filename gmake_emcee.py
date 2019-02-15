from __future__ import print_function
import re
import time
import os
import numpy as np
from astropy.io import fits
import emcee
import uuid
import random
#import cPickle as pickle
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
import subprocess
import corner
from copy import deepcopy
from astropy.io import ascii
import fnmatch
import sys
import numpy as np 
import matplotlib.pyplot as plt 
import corner 
from astropy.convolution import convolve, Gaussian1DKernel
from astropy.io import fits 
from scipy.interpolate import interp1d
import scipy.integrate as integrate
from scipy.interpolate import Rbf
from scipy.interpolate import interpn
from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans, convolve
from scipy.ndimage.interpolation import shift
from scipy import stats
from astropy.table import Table
from astropy.table import Column
from reproject import reproject_interp
import astropy.convolution as conv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pprint
import shutil
#import commands
import multiprocessing
#import FITS_tools
from scipy._lib._numpy_compat import suppress_warnings
np.warnings.filterwarnings('ignore')


def gmake_emcee_setup(inp_dct,dat_dct):
    
    opt_dct=inp_dct['optimize']
    
    fit_dct={}
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
        fit_dct['p_lo']=np.append(fit_dct['p_lo'],opt_dct[p_name][0])
        fit_dct['p_up']=np.append(fit_dct['p_up'],opt_dct[p_name][1])
        fit_dct['p_iscale']=np.append(fit_dct['p_iscale'],opt_dct[p_name][2])

    gmake_pformat(fit_dct)
    #print(fit_dct['p_name'])
    #print(fit_dct['p_start'])
    #print(fit_dct['p_format'])
    #print(fit_dct['p_format_keys'])
    
    fit_dct['ndim']=len(fit_dct['p_start'])
    fit_dct['nthreads']=multiprocessing.cpu_count()
    fit_dct['nwalkers']=opt_dct['nwalkers']
    fit_dct['outfolder']=opt_dct['outdir']
    
    print('nwalkers:',fit_dct['nwalkers'])
    print('nthreads:',fit_dct['nthreads'])
    print('ndim:    ',fit_dct['ndim'])
    
    np.random.seed(0)
    fit_dct['pos_start'] = \
    [ np.maximum(np.minimum(fit_dct['p_start']+fit_dct['p_iscale']*np.random.randn(fit_dct['ndim']),fit_dct['p_up']),fit_dct['p_lo']) for i in range(fit_dct['nwalkers']) ]
    
    if  not os.path.exists(fit_dct['outfolder']):
        os.makedirs(fit_dct['outfolder'])

    fit_dct['chainfile']=fit_dct['outfolder']+'/emcee_chain.dat'
    f=open(fit_dct['chainfile'], "w")
    output='{0:<5}'.format('it')+' '
    output+='{0:<5}'.format('wk')+' '
    output+=' '.join(('{0:'+fit_dct['p_format_keys'][x]+'}').format(fit_dct['p_name'][x]) for x in range(len(fit_dct['p_name'])))+' '
    output+='{0:<10} {1:<8}'.format('lnprob','chisq')
    output+='\n'
    f.write(output)
    f.close()
    
    fit_dct['pos_last']=deepcopy(fit_dct['pos_start'])
    fit_dct['step_last']=0
    
    np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)   #   fitting metadata
    np.save(fit_dct['outfolder']+'/inp_dct.npy',inp_dct)   #   input metadata

    sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],gmake_model_lnprob,
                                args=(fit_dct,inp_dct,dat_dct),threads=fit_dct['nthreads'],runtime_sortingfn=sort_on_runtime)
                                #args=(data,imsets,disks,fit_dct),threads=fit_dct['nthreads'])

    tic0=time.time()
    lnl,blobs=gmake_model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
                                 savemodel=fit_dct['outfolder']+'/p_start')
    print('Took {0} second for one trial'.format(float(time.time()-tic0))) 
    print('ndata->',blobs['ndata'])
    print('chisq->',blobs['chisq'])
       
    return fit_dct,sampler

def gmake_emcee_savechain(sampler,fitsname,metadata={}):
    """
    save the chains from the emcee sampler
        metadata is a Python dict.
    
    """
    
    t=Table()
    
    blobs=sampler.blobs
    for key in blobs[0][0].keys():
        tmp0=map(lambda v: map(lambda w: w[key], v), blobs)
        t.add_column(Column(name='blobs_'+key, data=[    tmp0    ]))
        (nstep,nwalker)=(np.array(tmp0)).shape
        
    t.add_column(Column(name='chain', data=[    sampler.chain[:,:nstep,:]    ]))                  # nwalker x nstep x npar
    t.add_column(Column(name='acceptance_fraction', data=[    sampler.acceptance_fraction    ]))    # nwalker
    t.add_column(Column(name='lnprobability', data=[    sampler.lnprobability[:,:nstep]    ]))    # nwalker x nstep
        
    if  metadata!={}:
        for key in metadata:
            t.add_column(Column(name=key, data=[    metadata[key]    ]))
    
    dir=os.path.dirname(fitsname)
    if  (not os.path.exists(dir)) and os.path.dirname(dir)!='':
        os.makedirs(dir)
    t.write(fitsname+".fits", overwrite=True)
    
    
def gmake_emcee_iterate(sampler,fit_dct,nstep=100):
    """
        RUN the sampler
    """
    fit_dct['nstep']=nstep
    
    tic=time.time()
    dt=0.0
    
    print("")
    print("Running MCMC...")
    print(">>"+fit_dct['chainfile'])
    print(">>"+fit_dct['outfolder']+"/emcee_chain.fits")
    print("")

    for i,(pos_i,lnprob_i,rstat_i,blobs_i) in enumerate(sampler.sample(fit_dct['pos_last'],iterations=fit_dct['nstep'])):
        """
        http://emcee.readthedocs.io/en/stable/api.html#emcee.EnsembleSampler.sample
            pos    (nwalkers,ndim)
            lnprob (nwalkers,)
            blobs  (nwalkers,)
        """
        fit_dct['step_last']+=1
        fit_dct['pos_last']=pos_i
        
        #   WRITE ASCII TABLE
        tic0=time.time() 
        f = open(fit_dct['chainfile'], "a")
        for k in range(pos_i.shape[0]):
            output='{0:<5}'.format(fit_dct['step_last'])+' '
            output+='{0:<5}'.format(k)+' '
            output+=' '.join(('{0:'+fit_dct['p_format'][x]+'}').format(pos_i[k][x]) for x in range(len(pos_i[k])))+' '
            output+='{0:<10.1f} {1:<8.1f}'.format(lnprob_i[k],blobs_i[k]['chisq'])
            output+='\n'
            f.write(output)
        f.close()
        dt+=float(time.time()-tic0)
        
        if  (i+1) % int(fit_dct['nstep']/10.0) == 0 :
            
            print("")
            print("Completion: {0:8.1f}%".format(float(i+1)/fit_dct['nstep']*100.0))
            print("TimeElapse: {0:8.1f}m".format(float(time.time()-tic)/float(60.)))
            
            fit_dct['acceptfraction']=deepcopy(sampler.acceptance_fraction)
            
        #   WRITE FITS TABLE
        
            tic0=time.time()
            #astable=ascii.read(fit_dct['chainfile'])
            #astable.write(fit_dct['fitstable'],format='fits',overwrite=True)
            #dt+=float(time.time()-tic0)            
            
            #   WRITE NEW-STYLE FITS FILE
            gmake_emcee_savechain(sampler,fit_dct['outfolder']+"/emcee_chain",metadata=fit_dct)
            
            np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)
            
            #p_median,p_error1,p_error2=gmake_emcee_analyze(fit_dct['outfolder'],plotsub=None,burnin=int((i+1)/2.0),plotcorner=False)
            
            fit_tab=gmake_emcee_analyze(fit_dct['outfolder'],plotsub=None,burnin=int((i+1)/2.0),plotcorner=False,
                            verbose=False)
            
            
            dt+=float(time.time()-tic0)
        
        

        
    print("Done.")
    print('Took {0} minutes'.format(float(time.time()-tic)/float(60.)))


def gmake_emcee_analyze(outfolder,
                       burnin=50,
                       modebin=10,
                       plotqtile=True,
                       plotlevel=False,
                       plotsub=None,
                       plotcorner=True,
                       verbose=False,
                       plotburnin=True
                       ):
    """
    # Print out the mean acceptance fraction. In general, acceptance_fraction
    # has an entry for each walker so, in this case, it is a 50-dimensional
    # vector.
    # This number should be between approximately 0.25 and 0.5 if everything went as planned.
    """
    
    
    t=Table.read(outfolder+'/'+'emcee_chain.fits')
    chain_array=t['chain'].data[0]
    acceptfraction=t['acceptance_fraction'].data[0]
    lnprobability=t['lnprobability'].data[0]
    
    blobs_lnprob=t['blobs_lnprob'].data[0]
    blobs_chisq=t['blobs_chisq'].data[0]
    blobs_ndata=t['blobs_ndata'].data[0]
    blobs_npar=t['blobs_npar'].data[0]
    
    #print('##',chain_array.shape) #nwalker x nstep
    #print('##',lnprobability.shape) #nwalker x nstep
    #print('##',blobs_lnprob.shape)  #nstep x nwalker
    #print('##',blobs_chisq.shape)   #nstep x nwalker
    #print('##',blobs_ndata.shape)   #nstep x nwalker
    #print('##',blobs_npar.shape)    #nstep x nwalker
    
    #fit_dct=np.load(outfolder+'/fit_dct.npy').item()
    p_format=t['p_format'].data[0]
    p_name=t['p_name'].data[0]
    p_scale=t['p_iscale'].data[0]
    p_lo=t['p_lo'].data[0]
    p_up=t['p_up'].data[0]
    p_start=t['p_start'].data[0]
    
    
    
    if  verbose==True:
        print("Mean acceptance fraction: ",np.mean(acceptfraction))
    
    #   DO SOME STATS
    
    samples = chain_array[:,burnin:,:].reshape((-1, chain_array.shape[2]))
    fullsamples = chain_array[:,:, :].reshape((-1, chain_array.shape[2]))
    if  verbose==True:
        print('sample shape: ',samples.shape)
        print("MCMC initialize scale / MCMC result:")
    
    p_ptiles=map(lambda v: v,zip(*np.percentile(samples,[2.5,16.,50.,84.,97.5],axis=0)))
    p_median=p_error1=p_error2=p_error3=p_error4=p_int1=p_int2=p_mode=np.array([])    
    
    if  verbose==True:
        print('+'*90)
    
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
        if  verbose==True:
            print(">>>  "+p_name[index]+":")
            print((" median(sigma) = {0:"+p_format[index]+"}"+\
                                 " {1:"+p_format[index]+"}"+\
                                 " {2:"+p_format[index]+"}"+\
                                 " {3:"+p_format[index]+"}"+\
                                 " {4:"+p_format[index]+"}").\
                  format(     p_median[index],p_error3[index],p_error1[index],p_error2[index],p_error4[index]))
            print((" median(ptile) = {0:"+p_format[index]+"}"+\
                                 " {1:"+p_format[index]+"}"+\
                                 " {2:"+p_format[index]+"}"+\
                                 " {3:"+p_format[index]+"}"+\
                                 " {4:"+p_format[index]+"}").\
                  format(     p_ptiles[index][2],p_ptiles[index][0],p_ptiles[index][1],p_ptiles[index][3],p_ptiles[index][4]))            
            print((" start(iscale) ="+\
                                 " {0:"+p_format[index]+"}/{1:"+p_format[index]+"}").\
                  format(        p_start[index],p_scale[index]))            
            print((" mode          ="+\
                                 " {0:"+p_format[index]+"}").\
                  format(        p_mode[index])) 
    
    if  verbose==True:
        print('-'*90)    


    #   ITERATION PARAMETR PLOTS

    figsize=(8.,(len(p_name))*2.5)
    ncol=1
    pl.clf()
    picki=range(len(p_name))
    nrow=int(np.ceil(len(picki)*1.0/ncol))
    fig, axes = pl.subplots(nrow,ncol,sharex=True,figsize=figsize,squeeze=False)
    cc=0
    for i in picki:
        iy=cc % nrow
        ix=(cc - iy)/nrow
        if  plotburnin==False:
            axes[iy,ix].plot(chain_array[:, burnin:, i].T, color="gray", alpha=0.4)
        else:
            axes[iy,ix].plot(chain_array[:, :, i].T, color="gray", alpha=0.4)
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
    figname=outfolder+"/emcee-iteration.png"
    fig.savefig(figname)
    pl.close()
    if  verbose==True:
        print("analyzing outfolder:"+outfolder)
        print("plotting..."+figname)

    #   ITERATION METADATA PLOTS
    
    m_name=['blobs_lnprob','blobs_chisq']
    figsize=(8.,len(m_name)*2.5)
    ncol=1
    pl.clf()
    picki=range(len(m_name))
    nrow=int(np.ceil(len(picki)*1.0/ncol))
    fig, axes = pl.subplots(nrow,ncol,sharex=True,figsize=figsize,squeeze=False)
    cc=0
    for i in picki:
        iy=cc % nrow
        ix=(cc - iy)/nrow
        if  plotburnin==False:
            axes[iy,ix].plot(t[m_name[i]].data[0][burnin:,:], color="k", alpha=0.4)
        else:
            axes[iy,ix].plot(t[m_name[i]].data[0][:,:], color="gray", alpha=0.4)
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
    figname=outfolder+"/emcee-iteration-blobs.png"
    fig.savefig(figname)
    pl.close()
    if  verbose==True:
        print("analyzing outfolder:"+outfolder)
        print("plotting..."+figname)    

    
    
    #   CORNER PLOTS
    
    if  plotcorner==True:
        if  verbose==True:
            print("plotting..."+outfolder+"/line-triangle.png")
            print("input data size:"+str(np.shape(samples)))
        tic=time.time()
        quantiles=None
        if  plotqtile==True:
            quantiles=[0.16, 0.5, 0.84]
        levels=None
        if  plotlevel==True:
            levels=(1-np.exp(-0.5),)        
        fig = corner.corner(samples, labels=p_name,truths=p_start,quantiles=quantiles,levels=levels)
        
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
        
        fig.savefig(outfolder+"/emcee-corner.png")
        pl.close()
        if  verbose==True:
            print('Took {0} seconds'.format(float(time.time()-tic)))
    
    # Make the triangle plot.
    if  plotsub!=None:
        #plotsub is the parameter index array
        if  verbose==True:
            print("plotting..."+outfolder+"/line-triangle-sub.png")
        subsamples = chain_array[:, burnin:, plotsub].reshape((-1, len(plotsub)))
        tic=time.time()
        quantiles=None
        if  plotqtile==True:
            quantiles=[0.16, 0.5, 0.84]
        levels=None
        if  plotlevel==True:
            levels=(1-np.exp(-0.5),)        
        fig = corner.corner(subsamples, labels=p_name[plotsub],truths=p_start[plotsub],quantiles=quantiles,levels=levels)
        fig.savefig(outfolder+"/line-triangle-sub.png")
        pl.close()
        if  verbose==True:
            print('Took {0} seconds'.format(float(time.time()-tic)))    
    
    #fit_dct['p_median']=p_median
    #fit_dct['p_error1']=p_error1
    #fit_dct['p_error2']=p_error2
    #fit_dct['p_error3']=p_error3
    #fit_dct['p_error4']=p_error4
    #fit_dct['p_burnin']=burnin
    #np.save(outfolder+'/fit_dct_analyzed.npy',fit_dct)
    
    t['p_median']=[p_median]
    t['p_error1']=[p_error1]
    t['p_error2']=[p_error2]
    t['p_error3']=[p_error3]
    t['p_error4']=[p_error4]
    t['p_burnin']=[burnin]
    #t.add_column(Column(name='flatchain_samples', data=[  samples  ]),index=0)
    t['flatchain_samples']=[samples]
    t['p_ptiles']=[p_ptiles]
    t['p_mode']=[p_mode]
    
    outname=outfolder+"/emcee_chain_analyzed.fits"
    t.write(outname, overwrite=True)

    
    if  verbose==True:
        print(samples.shape)   
        print('File successfully saved as %s'%(outname))
    
    
    
    return t
    
if  __name__=="__main__":
    
    pass

