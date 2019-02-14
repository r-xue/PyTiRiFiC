from __future__ import print_function

import numpy as np
from astropy.modeling.models import Sersic2D
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.io import fits
from astropy.convolution import convolve_fft
from astropy.convolution import convolve
import pprint

def gmake_model_api(mod_dct,dat_dct,
                      decomp=False,
                      verbose=False):
    
    models={}
    
    #   FIRST PASS: add models OBJECT by OBJECT
    
    for tag in mod_dct.keys():
        
        obj=mod_dct[tag]
        
        #   skip if no "method"
        
        if  'method' not in obj.keys():
            continue    
        if  verbose==True:
            print("+"*40); print('@',tag); print('method:',obj['method']) ; print("-"*40)

        

        image_list=mod_dct[tag]['image'].split(",")
        
        for image in image_list:
            
            data=dat_dct['data@'+image]
            hd=dat_dct['header@'+image]
            error=dat_dct['error@'+image]
            mask=dat_dct['mask@'+image]
            sample=dat_dct['sample@'+image]
            if  'psf@'+image in dat_dct.keys():
                psf=dat_dct['psf@'+image]
            else:
                psf=None
            
            if  'disk2d' in obj['method'].lower():
            
                imodel=gmake_model_disk2d(hd,obj['xypos'][0],obj['xypos'][1],
                                         r_eff=obj['sbser'][0],n=obj['sbser'][1],posang=obj['pa'],
                                         ellip=1.-np.cos(np.deg2rad(obj['inc'])),
                                         intflux=obj['intflux'],restfreq=obj['restfreq'],alpha=obj['alpha'])

            if  'kimspy' in obj['method'].lower():
                
                imodel=gmake_model_kinmspy(hd,obj)
                

            if  'imodel@'+image in models.keys():
                models['imodel@'+image]+=imodel
            else:
                models['imodel@'+image]=imodel.copy()
                models['header@'+image]=hd
                models['data@'+image]=data
                models['error@'+image]=error     
                models['mask@'+image]=mask
                models['sample@'+image]=sample
                models['psf@'+image]=psf
                
    #   SECOND PASS: simulate observations IMAGE BY IMAGE
    
    for tag in models.keys():
        
        if  'imodel@' in tag:
            cmodel,kernel=gmake_model_simobs(models[tag],
                                             models[tag.replace('imodel@','header@')],
                                             psf=models[tag.replace('imodel@','psf@')],
                                             returnkernel=True)
            models[tag.replace('imodel@','cmodel@')]=cmodel.copy()
            models[tag.replace('imodel@','kernel@')]=kernel.copy()
            
    return models                

def gmake_model_lnlike(theta,fit_dct,inp_dct,dat_dct,
                         savemodel='',
                         verbose=False):
    """
    the likelihood function
    """
    
    blobs={'lnprob':0.0,'chisq':0.0,'ndata':0.0,'npar':len(theta)}
     
    inp_dct0=deepcopy(inp_dct)
    for ind in range(len(fit_dct['p_name'])):
        #print("")
        #print('modify par: ',fit_dct['p_name'][ind],theta[ind])
        #print(gmake_readpar(inp_dct0,fit_dct['p_name'][ind]))
        gmake_writepar(inp_dct0,fit_dct['p_name'][ind],theta[ind])
        #print(">>>")
        #print(gmake_readpar(inp_dct0,fit_dct['p_name'][ind]))
        #print("")
    #gmake_listpars(inp_dct0)
    #tic0=time.time()
    mod_dct=gmake_inp2mod(inp_dct0)
    #print('Took {0} second on inp2mod'.format(float(time.time()-tic0))) 
    
    #tic0=time.time()
    #models=gmake_kinmspy_api(mod_dct,dat_dct=dat_dct)
    if  savemodel!='':
        cleanout=True
    else:
        cleanout=False
    models=gmake_model_api(mod_dct,dat_dct=dat_dct,
                           decomp=False,cleanout=cleanout,verbose=False)
    #print('Took {0} second on one API run'.format(float(time.time()-tic0))) 
    #gmake_listpars(mod_dct)
     
    
    for key in models.keys(): 
        
        if  'data@' not in key:
            continue
        
        im=models[key]
        hd=models[key.replace('data@','header@')]        
        mo=models[key.replace('data@','model@')]
        em=models[key.replace('data@','error@')]
        mk=models[key.replace('data@','mask@')]
        sp=models[key.replace('data@','sample@')]
        if  key.replace('data@','cmodel@') in models.keys():
            cm=models[key.replace('data@','cmodel@')]        
        if  key.replace('data@','psf@') in models.keys():
            pf=models[key.replace('data@','psf@')]
        
        #tic0=time.time()

        
        """
        sigma2=em**2
        #lnl1=np.sum( (im-mo)**2/sigma2*mk )
        #lnl2=np.sum( (np.log(sigma2)+np.log(2.0*np.pi))*mk )
        lnl1=np.sum( ((im-mo)**2/sigma2)[mk==1] )
        lnl2=np.sum( (np.log(sigma2)+np.log(2.0*np.pi))[mk==1] )
        lnl=-0.5*(lnl1+lnl2)
        blobs['lnprob']+=lnl
        blobs['chisq']+=lnl1
        blobs['ndata']+=np.sum(mk)
        """
        
        #print(im.shape)
        #print(sp.shape)
        #print(sp[:,2:0:-1].shape)
        #"""
        imtmp=np.squeeze(em)
        nxyz=np.shape(imtmp)
        if  len(nxyz)==3:
            imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1]),np.arange(nxyz[2])),\
                                        imtmp,sp[:,::-1],method='linear')
        else:
            imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1])),\
                                        imtmp,sp[:,1::-1],method='linear')
        sigma2=imtmp**2.0
        imtmp=np.squeeze(im-mo)
        
        if  len(nxyz)==3:
            imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1]),np.arange(nxyz[2])),\
                                        imtmp,sp[:,::-1],method='linear')
        else:
            imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1])),\
                                        imtmp,sp[:,1::-1],method='linear')
        
        #print(sp[:,1::-1])
        lnl1=np.sum( (imtmp)**2/sigma2 )
        lnl2=np.sum( np.log(sigma2*2.0*np.pi) )
        lnl=-0.5*(lnl1+lnl2)
        
        blobs['lnprob']+=lnl
        blobs['chisq']+=lnl1
        blobs['ndata']+=(np.shape(sp))[0]
        
        if  savemodel!='':
            basename=key.replace('data@','')
            basename=os.path.basename(basename)
            if  not os.path.exists(savemodel):
                os.makedirs(savemodel)
            fits.writeto(savemodel+'/data_'+basename,im,hd,overwrite=True)
            fits.writeto(savemodel+'/model_'+basename,mo,hd,overwrite=True)
            fits.writeto(savemodel+'/error_'+basename,em,hd,overwrite=True)
            fits.writeto(savemodel+'/mask_'+basename,mk,hd,overwrite=True)
            fits.writeto(savemodel+'/residual_'+basename,im-mo,hd,overwrite=True)
            if  key.replace('data@','cmodel@') in models.keys():
                fits.writeto(savemodel+'/cmodel_'+basename,cm,hd,overwrite=True)            
            if  key.replace('data@','psf@') in models.keys():
                fits.writeto(savemodel+'/psf_'+basename,pf,hd,overwrite=True)
        #"""
        #print('Took {0} second on calculating lnl/blobs'.format(float(time.time()-tic0)),key)
    lnl=blobs['lnprob']
    
    return lnl,blobs


def gmake_model_lnprior(theta,fit_dct):
    """
    pass through the likelihood prior function (limiting the parameter space)
    """
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    for index in range(len(theta)):
        if  theta[index]<p_lo[index] or theta[index]>p_up[index]:
            return -np.inf
    return 0.0

    
def gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,
                         savemodel='',
                         verbose=False):
    """
    this is the evaluating function for emcee 
    """
    lp = gmake_model_lnprior(theta,fit_dct)
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        return -np.inf,blobs
    if  verbose==True:
        print("try ->",theta)
    lnl,blobs=gmake_model_lnlike(theta,fit_dct,inp_dct,dat_dct,savemodel=savemodel)
    return lp+lnl,blobs        


if  __name__=="__main__":
    
    pass


    """
    log_model=np.log(model)
    plt.figure()
    plt.imshow(np.log(model), origin='lower', interpolation='nearest',
           vmin=np.min(log_model), vmax=np.max(log_model))
    plt.xlabel('x')
    plt.ylabel('y')
    cbar = plt.colorbar()
    cbar.set_label('Log Brightness', rotation=270, labelpad=25)
    cbar.set_ticks([np.min(log_model),np.max(log_model)], update_ticks=True)
    plt.savefig('test/test_model_disk2d.eps')
    """


