import time
import os
import numpy as np
from astropy.io import fits
import emcee
import uuid
import random
import cPickle as pickle
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
import subprocess
import corner
from copy import deepcopy
from astropy.io import ascii
import fnmatch

def py_tirific_analyze(outfolder,
                       burnin=50,
                       plotqtile=True,
                       plotlevel=False,
                       plotsub=None,
                       plotcorner=True,
                       verbose=False
                       ):
    """
    # Print out the mean acceptance fraction. In general, acceptance_fraction
    # has an entry for each walker so, in this case, it is a 50-dimensional
    # vector.
    # This number should be between approximately 0.25 and 0.5 if everything went as planned.
    """

    hdus=fits.open(outfolder+'/'+'chain_mef.fits')
    if  verbose==True:
        print hdus.info()
     
    chain_array=hdus[0].data
    p_keys=hdus[1].data.field('p_keys')
    p_start=hdus[1].data.field('p_start')
    p_lo=hdus[1].data.field('p_lo')
    p_up=hdus[1].data.field('p_up')
    p_scale=hdus[1].data.field('p_scale')
    if  'p_iscale' in hdus[1].columns.names:
        p_scale=hdus[1].data.field('p_iscale')
    acceptfraction=hdus[2].data.field('acceptfraction')
    hdus.close()
    
    mcpars=np.load(outfolder+'/mcpars.npy').item()
    data=np.load(outfolder+'/data.npy').item()
    imsets=np.load(outfolder+'/imsets.npy').item()
    disks=np.load(outfolder+'/disks.npy')
    p_format=mcpars['p_format']
    p_keys=mcpars['p_keys']
    
    p_scale=mcpars['p_scale']
    if  'p_iscale' in mcpars.keys():
        p_scale=mcpars['p_iscale']
    
    if  verbose==True:
        print("Mean acceptance fraction:", np.mean(acceptfraction))
    
    # Estimate the integrated autocorrelation time for the time series in each
    # parameter.
    # print("Autocorrelation time:", sampler.get_autocorr_time())
    #path=os.path.dirname(fitsname)
    path=deepcopy(outfolder)
    objects=mcpars['objects']
    
    for object in sorted(set((','.join(objects)).split(','))):
        if  verbose==True:
            print("analyzing path:"+path)
            print("plotting..."+path+"/line-time-"+object+".png")
        
        picki_main=[]
        picki_vr=[]
        picki_sm1a=[]
        picki_sm1p=[]
        picki_sbr=[]
        picki_vd=[]
        picki_name=[object,object+'_vr',object+'_sm1a',object+'_sm1p',object+'_sbr',object+'_vd']
        for ind in range(len(p_keys)):
            if  fnmatch.fnmatch(p_keys[ind],'*'+object):
                if  fnmatch.fnmatch(p_keys[ind],'vr*'):
                    picki_vr=picki_vr+[ind]
                elif  fnmatch.fnmatch(p_keys[ind],'sm1a*'):
                    picki_sm1a=picki_sm1a+[ind]
                elif  fnmatch.fnmatch(p_keys[ind],'sm1p*'):
                    picki_sm1p=picki_sm1p+[ind]
                elif  fnmatch.fnmatch(p_keys[ind],'sb*'):
                    picki_sbr=picki_sbr+[ind]
                elif  fnmatch.fnmatch(p_keys[ind],'vd*'):
                    picki_vd=picki_vd+[ind]                                                                                           
                else:
                    picki_main=picki_main+[ind]
        for ind in range(len(picki_name)):
            if  ind==0:
                picki=deepcopy(picki_main)
            if  ind==1:
                picki=deepcopy(picki_vr)
            if  ind==2:
                picki=deepcopy(picki_sm1a)
            if  ind==3:
                picki=deepcopy(picki_sm1p)
            if  ind==4:
                picki=deepcopy(picki_sbr)
            if  ind==5:
                picki=deepcopy(picki_vd)                                                                                     
            if  len(picki)!=0:
                pl.clf()
                nrow=int(np.ceil(len(picki)*1.0/2.0))
                fig, axes = pl.subplots(nrow, 2, sharex=True, figsize=(12, 20),squeeze=False)
                cc=0
                for i in picki:
                    iy=cc % nrow
                    ix=(cc - iy)/nrow
                    axes[iy,ix].plot(chain_array[:, :, i].T, color="k", alpha=0.4)
                    axes[iy,ix].yaxis.set_major_locator(MaxNLocator(5))
                    axes[iy,ix].axhline(p_start[i], color="#888888", lw=2)
                    axes[iy,ix].set_ylabel(p_keys[i])
                    if  i==len(p_start)-1:
                        axes[iy,ix].set_xlabel("step number")
                    cc+=1
                if  cc==(nrow*2-1):
                    axes[-1,-1].axis('off')
                fig.tight_layout(h_pad=0.0)
                fig.savefig(path+"/line-time-"+picki_name[ind]+".png")
                pl.close()
        


        
    picki=[]
    for ind in range(len(p_keys)):
        if  fnmatch.fnmatch(p_keys[ind],'lnf*'):
            picki=picki+[ind]
    if  len(picki)!=0:
        pl.clf()
        
        fig, axes = pl.subplots(len(picki), 1, sharex=True, figsize=(12, 12))
        cc=0
        for i in picki:
            if  len(picki)==1:
                axes=[axes]
            axes[cc].plot(chain_array[:, :, i].T, color="k", alpha=0.4)
            axes[cc].yaxis.set_major_locator(MaxNLocator(5))
            axes[cc].axhline(p_start[i], color="#888888", lw=2)
            axes[cc].set_ylabel(p_keys[i])
            if  i==len(p_start)-1:
                axes[cc].set_xlabel("step number")
            cc+=1
        fig.tight_layout(h_pad=0.0)
        fig.savefig(path+"/line-time-lnf.png")
        pl.close()
    # Make the triangle plot.
    
    samples = chain_array[:, burnin:, :].reshape((-1, chain_array.shape[2]))
    if  plotcorner==True:
        if  verbose==True:
            print("plotting..."+path+"/line-triangle.png")
            print("input data size:"+str(np.shape(samples)))
        tic=time.time()
        quantiles=None
        if  plotqtile==True:
            quantiles=[0.16, 0.5, 0.84]
        levels=None
        if  plotlevel==True:
            levels=(1-np.exp(-0.5),)        
        fig = corner.corner(samples, labels=p_keys,truths=p_start,quantiles=quantiles,levels=levels)
        fig.savefig(path+"/line-triangle.png")
        pl.close()
        if  verbose==True:
            print 'Took {0} seconds'.format(float(time.time()-tic))
    
    # Make the triangle plot.
    if  plotsub!=None:
        #plotsub is the parameter index array
        if  verbose==True:
            print("plotting..."+path+"/line-triangle-sub.png")
        subsamples = chain_array[:, burnin:, plotsub].reshape((-1, len(plotsub)))
        tic=time.time()
        quantiles=None
        if  plotqtile==True:
            quantiles=[0.16, 0.5, 0.84]
        levels=None
        if  plotlevel==True:
            levels=(1-np.exp(-0.5),)        
        fig = corner.corner(subsamples, labels=p_keys[plotsub],truths=p_start[plotsub],quantiles=quantiles,levels=levels)
        fig.savefig(path+"/line-triangle-sub.png")
        pl.close()
        if  verbose==True:
            print 'Took {0} seconds'.format(float(time.time()-tic))    
    
    # Compute the sigma
    if  verbose==True:
        print("MCMC initialize scale / MCMC result:")
    ps_mcmc=map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),zip(*np.percentile(samples, [16, 50, 84],axis=0)))
    p_median=np.array([])
    p_median=p_error1=p_error2=p_int1=p_int2=[]
    
    if  verbose==True:
        print('+'*40)
    for index in range(len(ps_mcmc)):
        if  verbose==True:
            print(p_keys[index]+(" p = {0[0]:"+p_format[index]+"} +{0[1]:"+p_format[index]+"} -{0[2]:"+p_format[index]+"} p_start/p_scale = {1:"+p_format[index]+"} / {2:"+p_format[index]+"}").format(ps_mcmc[index],p_start[index],p_scale[index]))
        p_median=np.append(p_median,(ps_mcmc[index])[0])
        p_error1=np.append(p_error1,-ps_mcmc[index][2])
        p_error2=np.append(p_error2,+ps_mcmc[index][1])
        p_int1=np.append(p_int1,(ps_mcmc[index])[0]-ps_mcmc[index][2])
        p_int2=np.append(p_int2,(ps_mcmc[index])[0]+ps_mcmc[index][1])
    if  verbose==True:
        print('-'*40)
        
    ps_mcmc=map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),zip(*np.percentile(samples, [2.5, 50, 97.5],axis=0)))
    p_median=np.array([])
    p_median=p_error3=p_error4=p_int1=p_int2=[]
    
    if  verbose==True:
        print('+'*40)
    for index in range(len(ps_mcmc)):
        if  verbose==True:
            print(p_keys[index]+(" p = {0[0]:"+p_format[index]+"} +{0[1]:"+p_format[index]+"} -{0[2]:"+p_format[index]+"} p_start/p_scale = {1:"+p_format[index]+"} / {2:"+p_format[index]+"}").format(ps_mcmc[index],p_start[index],p_scale[index]))
        p_median=np.append(p_median,(ps_mcmc[index])[0])
        p_error3=np.append(p_error3,-ps_mcmc[index][2])
        p_error4=np.append(p_error4,+ps_mcmc[index][1])
        p_int1=np.append(p_int1,(ps_mcmc[index])[0]-ps_mcmc[index][2])
        p_int2=np.append(p_int2,(ps_mcmc[index])[0]+ps_mcmc[index][1])
    if  verbose==True:
        print('-'*40)
    
    mcpars['p_median']=p_median
    mcpars['p_error1']=p_error1
    mcpars['p_error2']=p_error2
    mcpars['p_error3']=p_error3
    mcpars['p_error4']=p_error4
    mcpars['p_burnin']=burnin
    np.save(outfolder+'/mcpars.npy',mcpars)
    
    return p_median,p_error1,p_error2



