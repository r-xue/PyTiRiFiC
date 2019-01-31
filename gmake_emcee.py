from __future__ import print_function
import re

import time
import os
import sys

import numpy as np 
import matplotlib.pyplot as plt 
import emcee
import corner 
import uuid
import random
import cPickle as pickle

from astropy.convolution import convolve, Gaussian1DKernel

from astropy.io import ascii
from astropy.io import fits 

from scipy.interpolate import interp1d
import scipy.integrate as integrate
from scipy.interpolate import Rbf
from scipy.interpolate import interpn
from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans, convolve
from scipy.ndimage.interpolation import shift

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
from scipy import stats
from astropy.table import Table
from astropy.table import Column

from copy import deepcopy

import uuid
import random
import cPickle as pickle
from reproject import reproject_interp
import astropy.convolution as conv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import subprocess

import fnmatch
import pprint
import shutil
import commands
import multiprocessing
import numpy as np

import FITS_tools

import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator


from scipy._lib._numpy_compat import suppress_warnings
np.warnings.filterwarnings('ignore')


def gmake_emcee_setup(inp_dct):
    
    #print(inp_dct['optimize'])
    opt_dct=inp_dct['optimize']
    
    fit_dct={}
    fit_dct['p_start']=[]
    fit_dct['p_lo']=[]
    fit_dct['p_up']=[]
    fit_dct['p_name']=[]
    fit_dct['p_iscale']=[]   
    #fit_dct['p_scale']=[]
    
    for p_name in opt_dct.keys():
        
        fit_dct['p_name']=np.append(fit_dct['p_name'],[p_name])
        fit_dct['p_start']=np.append(fit_dct['p_start'],np.mean(gmake_readpar(inp_dct,p_name)))
        fit_dct['p_lo']=np.append(fit_dct['p_lo'],opt_dct[p_name][0])
        fit_dct['p_up']=np.append(fit_dct['p_up'],opt_dct[p_name][1])
        fit_dct['p_iscale']=np.append(fit_dct['p_iscale'],opt_dct[p_name][2])

    gmake_pformat(fit_dct)
    print(fit_dct['p_name'])
    print(fit_dct['p_start'])
    print(fit_dct['p_format'])
    print(fit_dct['p_format_keys'])
    
    fit_dct['ndim']=len(fit_dct['p_start'])
    fit_dct['nthreads']=multiprocessing.cpu_count()
    fit_dct['nwalkers']=40
    fit_dct['outfolder']='test_emcee'
    
    print('nwalkers:',fit_dct['nwalkers'])
    print('nthreads:',fit_dct['nthreads'])
    print('ndim:    ',fit_dct['ndim'])
    
    np.random.seed(0)
    fit_dct['pos_start'] = \
    [ np.maximum(np.minimum(fit_dct['p_start']+fit_dct['p_iscale']*np.random.randn(fit_dct['ndim']),fit_dct['p_up']),fit_dct['p_lo']) for i in range(fit_dct['nwalkers']) ]
    
    if  not os.path.exists(fit_dct['outfolder']):
        os.makedirs(fit_dct['outfolder'])
    
    fit_dct['fitstable']=fit_dct['outfolder']+'/chain.fits'
    
    fit_dct['chainfile']=fit_dct['outfolder']+'/chain.dat'
    f=open(fit_dct['chainfile'], "w")
    output='{0:<5}'.format('#is')
    output+=' {0:<5}'.format('iw')
    output+=' '.join(('{0:'+fit_dct['p_format_keys'][x]+'}').format(fit_dct['p_name'][x]) for x in range(len(fit_dct['p_name'])))
    output+=' {0:<6} {1:<6}'.format('lnprob','chisq')
    output+='\n'
    f.write(output)
    f.close()
    
    fit_dct['pos_last']=deepcopy(fit_dct['pos_start'])
    fit_dct['step_last']=0
    
    np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)   #   fitting metadata
    np.save(fit_dct['outfolder']+'/inp_dct.npy',inp_dct)   #   input metadata

    sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],gmake_kinmspy_lnprob,
                                args=(fit_dct,inp_dct),threads=fit_dct['nthreads'],runtime_sortingfn=sort_on_runtime)
                                #args=(data,imsets,disks,fit_dct),threads=fit_dct['nthreads'])

    tic0=time.time()
    lnl,blobs=gmake_kinmspy_lnprob(fit_dct['p_start'],fit_dct,inp_dct)
    print('ndata->',blobs['ndata'])
    print('chisq->',blobs['chisq'])
    print('Took {0} second for one trial'.format(float(time.time()-tic0)))    
    
    return fit_dct,sampler
    
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
    print(">>"+fit_dct['outfolder']+"/chain_mef.fits")
    print(">>"+fit_dct['outfolder']+"/chain.fits")
    print("")

    for i,(pos_i,lnprob_i,rstat_i,blobs_i) in enumerate(sampler.sample(fit_dct['pos_last'],iterations=fit_dct['nstep'])):
        """
        http://emcee.readthedocs.io/en/stable/api.html#emcee.EnsembleSampler.sample
            pos    (nwalkers,ndim)
            lnprob (nwalkers,)
            blobs  (nwalkers,)
        """
        fit_dct['step_last']+=1
        
        #   WRITE ASCII TABLE
        tic0=time.time() 
        f = open(fit_dct['chainfile'], "a")
        for k in range(pos_i.shape[0]):
            output='{0:<5}'.format(fit_dct['step_last'])
            output+=' {0:<5}'.format(k)
            output+=' '.join(('{0:'+fit_dct['p_format'][x]+'}').format(pos_i[k][x]) for x in range(len(pos_i[k])))
            output+=' {0:<6.2f} {1:<6.0f}'.format(lnprob_i[k],blobs_i[k]['chisq'])
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
            
            #   WRITE NEW-STYLE BTABLE FILE
            
            t=Table()
            for key in fit_dct:
                    t.add_column(Column(name=key, data=[fit_dct[key]]))
                # param x step x walker (note: fits/idl array dimension sequence is reversed)    
            tmpcol=Column(name='chain_array', data=[ sampler.chain[:,0:fit_dct['step_last'],:]  ])
            t.add_column(tmpcol)
            t.write(fit_dct['outfolder']+"/chain.fits", overwrite=True)
            
            np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)
            
            #p_median,p_error1,p_error2=gmake_emcee_analyze(fit_dct['outfolder'],plotsub=None,burnin=int((i+1)/2.0),plotcorner=False)
            
            
            dt+=float(time.time()-tic0)
        
        fit_dct['pos_last']=pos_i

        
    print("Done.")
    print('Took {0} minutes'.format(float(time.time()-tic)/float(60.)))
    
if  __name__=="__main__":
    
    execfile('gmake_kinmspy.py')
    execfile('gmake_utils.py')
    execfile('gmake_emcee_analyze.py')
    
    #inp_dct=gmake_readinp('examples/bx610/bx610xy.inp',verbose=False)
    #fit_dct,sampler=gmake_emcee_setup(inp_dct)
    #gmake_emcee_iterate(sampler,fit_dct,nstep=20)
    
    
    fit_dct=gmake_emcee_analyze('test_emcee/',plotsub=None,burnin=10,plotcorner=True,
                                verbose=True)

    #op_dct=inp_dct['optimize']
    #print(inp_dct['optimize'])
    
    """
    opt_dct=inp_dct['optimize']

    for par_name in opt_dct.keys():
        po_str=key.split("@")
        pi_str=re.findall("\[(.*?)\]", po_str[0])
        #print(pi_str,po_str)
        if  len(pi_str)==0:
            par_str=po_str[0]
            obj_str=po_str[1]
            print(key,input[obj_str][par_str])
        else:
            par_str=(po_str[0].split("["))[0]
            obj_str=po_str[1]
            ind_str=pi_str[0]
            print(key,input[obj_str][par_str][make_slice(ind_str)])
            #print(input[po_str[1]][po_str[0]][make_slice(pi_str[0])])
    """        
    """
    x=range(20)
    print(x)
    print(x[make_slice('0:1')])
    print(x[make_slice('10:2:-1')])
    print(x[make_slice('1')])
    x[make_slice('0:1')]=[2]
    x[make_slice('1:4')]=[3,2,1]
    print(x)
    """
#mcpars['mode']='emcee'
#mcpars['nthreads']=multiprocessing.cpu_count()
