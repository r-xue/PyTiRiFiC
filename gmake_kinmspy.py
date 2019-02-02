from __future__ import print_function
from KinMS import KinMS
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import scipy.constants as const
import time

def gmake_kinmspy_api(mod_dct,dat_dct={},
                      outname='',
                      decomp=False,
                      verbose=True):
    """
    handle modeling parameters to kinmspy and generate the model cubes embeded into 
    a dictionary nest
    
    """
    
    models={}
    
    for tag in mod_dct.keys():
        
        if  tag=='optimize' or tag=='cont':
            continue
        
        if  verbose==True:
            print("+"*40)
            print('@',tag)
            print("-"*40)
        
        obj=mod_dct[tag]
        
        #tic=time.time()
        if  'data@'+obj['image'] not in dat_dct:
            data,hd=fits.getdata(obj['image'],header=True)
        else:
            data=dat_dct['data@'+obj['image']]
            hd=dat_dct['header@'+obj['image']]
        if  'error@'+obj['image'] not in dat_dct:
            error=fits.getdata(obj['error'])
        else:
            error=dat_dct['error@'+obj['image']]
        if  'mask@'+obj['image'] not in dat_dct:
            mask=fits.getdata(obj['mask'])
        else:
            mask=dat_dct['mask@'+obj['image']]
        if  'sample@'+obj['image'] not in dat_dct:
            sample=fits.getdata(obj['sample'])
            sample=sample['sp_index']
        else:
            sample=dat_dct['sample@'+obj['image']]       
                                                           
        #print('Took {0} seconds to read FITS'.format(float(time.time()-tic)/float(1)))
        
        if  verbose==True:
            print(hd['NAXIS1'],hd['NAXIS2'],hd['NAXIS3'])
        
        psize=np.sqrt(np.abs(hd['CDELT1']*hd['CDELT2']))*3600.0         #   arcsec
        
        cdelt3=hd['CDELT3']     # hz or m/s
        crval3=hd['CRVAL3']     # hz or m/s
        crpix3=hd['CRPIX3']     # pix
        
        #   vector description of the z-axis: 
        #       vdelt3/vrval3/crpix3
        rfreq=obj['restfreq']/(1.0+obj['z'])                            #   GHz
        if  'Hz' in hd['CUNIT3']:   # by freq
            vdelt3=-const.c*cdelt3/(1.0e9*rfreq)/1000.                  #   km/s
            vrval3=const.c*((1.0e9*rfreq)-crval3)/(1.0e9*rfreq)/1000.0  #   km/s
        else:                       # by velo
            vdelt3=cdelt3/1000.0
            vrval3=crval3/1000.0
        
        if  verbose==True:
            print(psize,vdelt3,vrval3,crpix3)
        
        xs=psize*hd['NAXIS1']
        ys=psize*hd['NAXIS2']
        vs=abs(vdelt3)*hd['NAXIS3']
        cell=psize
        dv=abs(vdelt3)
        
        beamsize=[0.2,0.2,0.]
        
        if  'BMAJ' in hd.keys():
            beamsize[0]=hd['BMAJ']*3600.
        if  'BMIN' in hd.keys():
            beamsize[1]=hd['BMIN']*3600.
        if  'BPA' in hd.keys():
            beamsize[2]=hd['BPA']                        
        if  verbose==True:
            print('beamsize->',beamsize)
        
        inc=obj['inc']
        gassigma=np.array(obj['vdis'])
        
        sbrad=np.array(obj['radi'])
        sbprof=obj['sbexp'][0]*np.exp(-sbrad/obj['sbexp'][1])
        
        velrad=obj['radi']
        velprof=obj['vrot']
        posang=obj['pa']
        intflux=0.01
        filename='test'
        
        xypos=obj['xypos']
        restfreq=115.271e9
        restfreq=obj['restfreq']
        
        vsys=obj['vsys']
        
        fsys=(1.0-vsys/(const.c/1000.0))*rfreq # line systematic frequency in the observer frame
        
        
        #   ra    ----      xi_data     ----    (xSize-1.)/2.+phasecen[0]/cell
        #   dec   ----      yi_data     ----    (ySize-1.)/2.+phasecen[1]/cell
        #   vsys  ----      vi_data     ----    (vSize-1.)/2.+voffset/dv
       
        #
        # collect the world coordinates of the disk center (ra,dec,freq/wave)
        # note: vsys is defined in the radio(freq)/optical(wave) convention, 
        #       within the rest frame set at obj['z']/
        #       the convention doesn't really matter, as long as vsys << c
        #
        w=WCS(hd)
        wx=xypos[0]
        wy=xypos[1]
        ws=1    # stokes
        wo=0    # 0-based or 1-based index
        if  'Hz' in hd['CUNIT3']:
            wz=obj['restfreq']*1e9/(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
            dv=-const.c*cdelt3/(1.0e9*obj['restfreq']/(1.0+obj['z']))/1000.
        if  'Angstrom' in hd['CUNIT3']:
            wz=obj['restwave']*(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
            dv=const.c*cdelt3/(obj['restwave']*(1.0+obj['z']))/1000.
        if  'm/s' in hd['CUNIT3']:
            wz=obj['vsys']/1000.
            dv=cdelt3/1000.        

        px,py,pz,ps=w.wcs_world2pix(wx,wy,wz,ws,wo)
        
        px_int=round(px)
        py_int=round(py)
        pz_int=round(pz)
        phasecen=np.array([px-px_int,py-py_int])*cell
        voffset=(pz-pz_int)*dv
        
        #print(phasecen,voffset)
        #print('<-->',tag,px_int,py_int,pz_int,ps)
        #print('hz:',int(xs/cell*0.5))
        phasecen=[0.,0.]
        
        
        
        xs=np.max(sbrad)*2.0*2.0
        ys=np.max(sbrad)*2.0*2.0
        vs=np.max(velprof)*1.5*2.0
        
        px_o=px_int-int(xs/cell*0.5)
        py_o=py_int-int(ys/cell*0.5)
        pz_o=pz_int-int(vs/abs(dv)*0.5)

        #tic=time.time()
        # cube needs to be transposed to match the fits.data dimension 
        cube=KinMS(xs,ys,vs,
                   cellSize=cell,dv=abs(dv),
                   beamSize=beamsize,cleanOut=False,
                   inc=inc,gasSigma=gassigma,sbProf=sbprof,
                   sbRad=sbrad,velRad=velrad,velProf=velprof,
                   #nSamps=nsamps,
                   ra=xypos[0],dec=xypos[1],
                   restFreq=restfreq,vSys=vsys,phaseCen=phasecen,vOffset=voffset,
                   #fileName=outname+'_'+tag,
                   posAng=posang,
                   intFlux=intflux)
        #print('Took {0} seconds to execute KinMSpy'.format(float(time.time()-tic)/float(1)))
        
        if  dv<0:
            cube=np.flip(cube,axis=2)
        
        model=data.T*0.0
        #print('shape:',model.shape)
        #print('shape:',cube.shape)
        #print('-->',px_int,py_int,pz_int)
        #print('-->',[px_o,py_o,pz_o])
        model=gmake_insertmodel(model,cube,offset=[px_o,py_o,pz_o])
        #fits.writeto(tag+'.fits',model.T,overwrite=True)
        if  decomp==True:
            models[tag+'@'+obj['image']]=model.T
        
        if  'model@'+obj['image'] in models.keys():
            models['model@'+obj['image']]+=model.T
        else:
            models['model@'+obj['image']]=model.T.copy()
            models['header@'+obj['image']]=hd
            models['data@'+obj['image']]=data
            models['error@'+obj['image']]=error     
            models['mask@'+obj['image']]=mask
            models['sample@'+obj['image']]=sample
            
    return models

def gmake_kinmspy_lnlike(theta,fit_dct,inp_dct,dat_dct,
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
    models=gmake_kinmspy_api(mod_dct,dat_dct=dat_dct)
    #print('Took {0} second on one API run'.format(float(time.time()-tic0))) 
    #gmake_listpars(mod_dct)
     
    
    for key in models.keys(): 
        
        if  'data@' not in key:
            continue
        
        im=models[key]
        mo=models[key.replace('data@','model@')]
        em=models[key.replace('data@','error@')]
        mk=models[key.replace('data@','mask@')]
        sp=models[key.replace('data@','sample@')]
        hd=models[key.replace('data@','header@')]
        
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
        
        
        #"""
        imtmp=np.squeeze(em)
        nxyz=np.shape(imtmp)
        imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1]),np.arange(nxyz[2])),\
                                        imtmp,sp[:,::-1],method='linear')
        sigma2=imtmp**2.0
        imtmp=np.squeeze(im-mo)
        imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1]),np.arange(nxyz[2])),\
                                        imtmp,sp[:,::-1],method='linear')
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
        
        
        #"""

        #print('Took {0} second on calculating lnl/blobs'.format(float(time.time()-tic0)),key)
        
    lnl=blobs['lnprob']
    
    
    
    return lnl,blobs


def gmake_kinmspy_lnprior(theta,fit_dct):
    """
    pass through the likelihood prior function (limiting the parameter space)
    """
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    for index in range(len(theta)):
        if  theta[index]<p_lo[index] or theta[index]>p_up[index]:
            return -np.inf
    return 0.0

    
def gmake_kinmspy_lnprob(theta,fit_dct,inp_dct,dat_dct,
                         savemodel='',
                         verbose=False):
    """
    this is the evaluating function for emcee 
    """
    lp = gmake_kinmspy_lnprior(theta,fit_dct)
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        return -np.inf,blobs
    if  verbose==True:
        print("try ->",theta)
    lnl,blobs=gmake_kinmspy_lnlike(theta,fit_dct,inp_dct,dat_dct,savemodel=savemodel)
    return lp+lnl,blobs    
    
if  __name__=="__main__":

    pass