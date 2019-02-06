from __future__ import print_function

import numpy as np
from astropy.modeling.models import Sersic2D
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.io import fits
from astropy.convolution import convolve_fft
import pprint

def gmake_model_api(mod_dct,dat_dct={},
                      outname='',
                      decomp=False,
                      cleanout=False,
                      verbose=False):
    
    models={}
    
    for tag in mod_dct.keys():
        
        obj=mod_dct[tag]
        if  'method' not in obj.keys():
            continue
        elif 'disk2d' not in obj['method'].lower():
            continue
    
        if  verbose==True:
            print("+"*40)
            print('@',tag)
            print("-"*40)
        
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
            beamsize=[0.2,0.2,0.]
            
            if  'BMAJ' in hd.keys():
                beamsize[0]=hd['BMAJ']*3600.
            if  'BMIN' in hd.keys():
                beamsize[1]=hd['BMIN']*3600.
            if  'BPA' in hd.keys():
                beamsize[2]=hd['BPA']
                
            xypos=obj['xypos']
            restfreq=obj['restfreq']
            intflux=obj['intflux']*(hd['CRVAL3']/1e9/obj['restfreq'])**obj['alpha']                                        
            posang=obj['pa']
            inc=obj['inc']
            ellip=1.-np.cos(np.deg2rad(inc))
            ser=obj['sbser']
            if  verbose==True:
                print('beamsize->',beamsize)
                print(image,hd['CRVAL3']/1e9,intflux)
                
            model=gmake_model_disk2d(hd,
                                     xypos[0],xypos[1],beamsize,
                                     psf=psf,
                                     r_eff=ser[0],
                                     n=ser[1],                                     
                                     cleanout=False,
                                     intflux=intflux,
                                     posang=posang,
                                     ellip=ellip)
            if  cleanout==True:
                cmodel=gmake_model_disk2d(hd,
                                         xypos[0],xypos[1],beamsize,
                                         psf=psf,
                                         r_eff=ser[0],
                                         n=ser[1],                                     
                                         cleanout=True,
                                         intflux=intflux,
                                         posang=posang,
                                         ellip=ellip)            
            
            if  decomp==True:
                models[tag+'@'+image]=model
            
            if  'model@'+image in models.keys():
                models['model@'+image]+=model
                if  cleanout==True:
                    models['cmodel@'+image]+=cmodel
            else:
                models['model@'+image]=model.copy()
                if  cleanout==True:
                    models['cmodel@'+image]=cmodel.copy()
                models['header@'+image]=hd
                models['data@'+image]=data
                models['error@'+image]=error     
                models['mask@'+image]=mask
                models['sample@'+image]=sample            
                models['psf@'+image]=psf
                
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
    models=gmake_model_api(mod_dct,dat_dct=dat_dct)
    #print('Took {0} second on one API run'.format(float(time.time()-tic0))) 
    #gmake_listpars(mod_dct)
     
    
    for key in models.keys(): 
        
        if  'data@' not in key:
            continue
        
        im=models[key]
        mo=models[key.replace('data@','model@')]
        if  'cmodel@' in key:
            cm=models[key.replace('data@','cmodel@')]
        em=models[key.replace('data@','error@')]
        mk=models[key.replace('data@','mask@')]
        sp=models[key.replace('data@','sample@')]
        hd=models[key.replace('data@','header@')]
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
            if  'cmodel@' in key:
                fits.writeto(savemodel+'/cmodel_'+basename,cm,hd,overwrite=True)
            fits.writeto(savemodel+'/error_'+basename,em,hd,overwrite=True)
            fits.writeto(savemodel+'/mask_'+basename,mk,hd,overwrite=True)
            fits.writeto(savemodel+'/residual_'+basename,im-mo,hd,overwrite=True)
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
    
    #pass

    execfile('gmake_model_func.py')
    execfile('gmake_utils.py')
    execfile('gmake_emcee.py')

    """
    inp_dct=gmake_readinp('examples/bx610/bx610xy_cont.inp',verbose=False)
    #pprint.pprint(inp_dct)
    dat_dct=gmake_read_data(inp_dct,verbose=False,fill_mask=True,fill_error=True)

    fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
    gmake_emcee_iterate(sampler,fit_dct,nstep=500)
    """
    
    
    #"""
    
    #outfolder='bx610xy_cont_emcee_working1'
    outfolder='bx610xy_emcee'
    fit_tab=gmake_emcee_analyze(outfolder,plotsub=None,burnin=250,plotcorner=True,
                        verbose=True)
    
    """
    outfolder='bx610xy_cont_cm_emcee'
    fit_dct=np.load(outfolder+'/fit_dct.npy').item()
    inp_dct=np.load(outfolder+'/inp_dct.npy').item()
    fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
    theta=fit_tab['p_median'].data[0]
    print(theta)
    lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_median')
    print(lnl,blobs)
    """
    #"""
    
    #print(fit_dct['p_name'])
    
    #print(fit_dct['p_start'])
    #gmake_model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,data_dct,savemodel='test',verbose=True)
    
    #pprint.pprint(models)
    #print(models.keys())
    
    """
    data,hd=fits.getdata('examples/bx610/bx610_spw25.mfs.fits',header=True,memmap=False)
    
    model=gmake_model_disk2d(hd,356.539321,12.8220179445,[0.2,0.2,0.0],
                             cleanout=False)
    
    fits.writeto('test_model_disk2d.fits',model,hd,overwrite=True)
    
    log_model=np.log(model)
    plt.figure()
    plt.imshow(np.log(model), origin='lower', interpolation='nearest',
           vmin=np.min(log_model), vmax=np.max(log_model))
    plt.xlabel('x')
    plt.ylabel('y')
    cbar = plt.colorbar()
    cbar.set_label('Log Brightness', rotation=270, labelpad=25)
    cbar.set_ticks([np.min(log_model),np.max(log_model)], update_ticks=True)
    plt.savefig('test_model_disk2d.eps')
    
    """



