
def gmake_model_api(mod_dct,dat_dct,
                    nsamps=100000,
                    decomp=False,
                    verbose=False):
    """
    call for the model construction:
    
    notes on evaluating efficiency:
    
        While building the intrinsic data-model from a physical model can be expensive,
        the simulated observation (2D/3D convolution) is usually the bottle-neck.
        
        some tips to improve the effeciency:
            + exclude empty (masked/flux=0) region for the convolution
            + joint all objects in the intrinsic model before the convolution, e.g.
                overlapping objects, lines
            + use to low-dimension convolution when possible (e.g. for the narrow-band continumm) 
            
        before splitting line & cont models:
            --- apicall   : 2.10178  seconds ---
        after splitting line & cont models:
            --- apicall   : 0.84662  seconds ---
    """
    models={'mod_dct':mod_dct.copy()}
    
    if  verbose==True:
        start_time = time.time()
    
    #   FIRST PASS: add models OBJECT by OBJECT
                
    for tag in list(mod_dct.keys()):

        #   skip if no "method" or the item is not a physical model
        
        obj=mod_dct[tag]
      
        if  'method' not in obj.keys():
            continue    
        if  tag=='optimize':
            continue        
        
        if  verbose==True:
            print("+"*40); print('@',tag); print('method:',obj['method']) ; print("-"*40)

        if  'vis' in mod_dct[tag].keys():
            
            vis_list=mod_dct[tag]['vis'].split(",")
            
            for vis in vis_list:
                
                if  'data@'+vis not in models.keys():
                    
                    #test_time = time.time()
                    models['data@'+vis]=dat_dct['data@'+vis]
                    models['type@'+vis]=dat_dct['type@'+vis]
                    models['weight@'+vis]=dat_dct['weight@'+vis]   
                    models['uvw@'+vis]=dat_dct['uvw@'+vis]
                    models['chanfreq@'+vis]=dat_dct['chanfreq@'+vis]
                    models['chanwidth@'+vis]=dat_dct['chanwidth@'+vis]
                    models['phasecenter@'+vis]=dat_dct['phasecenter@'+vis]
    
                    
                    wv=np.mean(const.c/models['chanfreq@'+vis])
                    nxy, dxy = get_image_size(models['uvw@'+vis][:,0]/wv, models['uvw@'+vis][:,1]/wv, verbose=False)
                    nxy=128
                    
                    header=fits.Header.fromfile('gmake_image.header',endcard=False,sep='\n',padding=False)
                    header['NAXIS1']=nxy
                    header['NAXIS2']=nxy
                    header['NAXIS3']=np.size(models['chanfreq@'+vis])
                    header['CRVAL1']=models['phasecenter@'+vis][0]
                    header['CRVAL2']=models['phasecenter@'+vis][1]
    
                    header['CRVAL3']=models['chanfreq@'+vis][0]
                    header['CDELT1']=-np.rad2deg(dxy)
                    header['CDELT2']=np.rad2deg(dxy)
                    header['CDELT3']=np.mean(dat_dct['chanwidth@'+vis])   
                    header['CRPIX1']=np.floor(nxy/2)+1
                    header['CRPIX2']=np.floor(nxy/2)+1
                    
                    models['header@'+vis]=header.copy()
                    
                    naxis=(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])
                    #   uvmodel: np.complex64
                    #   imodel:  np.float32
                    models['imodel@'+vis]=np.zeros(naxis,dtype=np.float32)
                    models['imod2d@'+vis]=np.zeros(naxis,dtype=np.float32)
                    models['imod3d@'+vis]=np.zeros(naxis,dtype=np.float32)
                    models['uvmodel@'+vis]=np.zeros((models['data@'+vis].shape)[0:2],
                                                    dtype=models['data@'+vis].dtype,
                                                    order='F')
                    
                    
                if  'disk2d' in obj['method'].lower():
                    test_time = time.time()
                    pintflux=0.0
                    if  'pintflux' in obj:
                        pintflux=obj['pintflux']
                    imodel=gmake_model_disk2d(models['header@'+vis],obj['xypos'][0],obj['xypos'][1],
                                             r_eff=obj['sbser'][0],n=obj['sbser'][1],posang=obj['pa'],
                                             ellip=1.-np.cos(np.deg2rad(obj['inc'])),
                                             pintflux=pintflux,
                                             intflux=obj['intflux'],restfreq=obj['restfreq'],alpha=obj['alpha'])
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('test:'+vis,time.time() - test_time))
                    #print(imodel.shape)
                    models['imod2d@'+vis]+=imodel
                    models['imodel@'+vis]+=imodel
                    
    
                if  'kinmspy' in obj['method'].lower():
                    
                    test_time = time.time()              
                    imodel,imodel_prof=gmake_model_kinmspy(models['header@'+vis],obj,nsamps=nsamps,fixseed=False)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('test:'+vis,time.time() - test_time))
                    #print(imodel.shape)
                    models['imod3d@'+vis]+=imodel
                    models['imod3d_prof@'+tag+'@'+vis]=imodel_prof.copy()
                    models['imodel@'+vis]+=imodel     
                    
        if  'image' in mod_dct[tag].keys():
            
            image_list=mod_dct[tag]['image'].split(",")
            
            for image in image_list:
                
                if  'data@'+image not in models.keys():
                    
                    #test_time = time.time()
                    models['header@'+image]=dat_dct['header@'+image]
                    models['data@'+image]=dat_dct['data@'+image]
                    models['error@'+image]=dat_dct['error@'+image]   
                    models['mask@'+image]=dat_dct['mask@'+image]
                    models['type@'+image]=dat_dct['type@'+image]
                    
                    if  'sample@'+image in dat_dct.keys():
                        models['sample@'+image]=dat_dct['sample@'+image]
                    else:
                        models['sample@'+image]=None
                        
                    if  'pmodel@'+image in dat_dct.keys():
                        models['pmodel@'+image]=dat_dct['pmodel@'+image]
                    else:
                        models['pmodel@'+image]=None                                            
                    
                    if  'psf@'+image in dat_dct.keys():
                        models['psf@'+image]=dat_dct['psf@'+image]
                    else:
                        models['psf@'+image]=None
                    naxis=models['data@'+image].shape
                    if  len(naxis)==3:
                        naxis=(1,)+naxis
                    models['imodel@'+image]=np.zeros(naxis)
                    models['cmodel@'+image]=np.zeros(naxis)
                    #   save 2d objects (even it has been broadcasted to 3D for spectral cube)
                    #   save 3D objects (like spectral line emission from kinmspy/tirific)
                    models['imod2d@'+image]=np.zeros(naxis)
                    models['imod3d@'+image]=np.zeros(naxis)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('import:'+image,time.time() - test_time))
      
                
                if  'disk2d' in obj['method'].lower():
                    #test_time = time.time()
                    pintflux=0.0
                    if  'pintflux' in obj:
                        pintflux=obj['pintflux']
                    imodel=gmake_model_disk2d(models['header@'+image],obj['xypos'][0],obj['xypos'][1],
                                             r_eff=obj['sbser'][0],n=obj['sbser'][1],posang=obj['pa'],
                                             ellip=1.-np.cos(np.deg2rad(obj['inc'])),
                                             pintflux=pintflux,
                                             intflux=obj['intflux'],restfreq=obj['restfreq'],alpha=obj['alpha'])
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('test:'+image,time.time() - test_time))
                    #print(imodel.shape)
                    models['imod2d@'+image]+=imodel
                    models['imodel@'+image]+=imodel
                    
    
                if  'kinmspy' in obj['method'].lower():
                    #test_time = time.time()              
                    
                    
                    imodel,imodel_prof=gmake_model_kinmspy(models['header@'+image],obj,nsamps=nsamps,fixseed=False)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('test:'+image,time.time() - test_time))
                    #print(imodel.shape)
                    models['imod3d@'+image]+=imodel
                    models['imod3d_prof@'+tag+'@'+image]=imodel_prof.copy()
                    models['imodel@'+image]+=imodel              

    if  verbose==True:            
        print("---{0:^10} : {1:<8.5f} seconds ---\n".format('imodel-total',time.time() - start_time))
    
    #   SECOND PASS (OPTIONAL): simulate observations VIS BY VIS


    if  verbose==True:
        start_time = time.time()
                                
    for tag in list(models.keys()):
        
        
        """
        if  'imodel@' in tag:
            print(tag)
            uvmodel=gmake_model_uvsample(models[tag],models[tag.replace('imodel@','header@')],
                                        models[tag.replace('imodel@','data@')],
                                        models[tag.replace('imodel@','uvw@')],
                                        models[tag.replace('imodel@','phasecenter@')],
                                        uvmodel_in=models[tag.replace('imodel@','uvmodel@')],
                                        average=False,
                                        verbose=False)
            #models[tag.replace('imodel@','uvmodel@')]+=uvmodel 
        if  'imodel@' in tag:
            print(tag)
            cmodel,kernel=gmake_model_simobs(models[tag],
                                             models[tag.replace('imodel@','header@')],
                                             psf=models[tag.replace('imodel@','psf@')],
                                             returnkernel=True,
                                             verbose=True)
            models[tag.replace('imodel@','cmodel@')]=cmodel.copy()
            models[tag.replace('imodel@','kernel@')]=kernel.copy()                  
        """
         
        #"""   
        if  'imod2d@' in tag:

            if  models[tag.replace('imod2d@','type@')]=='vis':
                #print('>>> '+tag)
                uvmodel=gmake_model_uvsample(models[tag],models[tag.replace('imod2d@','header@')],
                                            models[tag.replace('imod2d@','data@')],
                                            models[tag.replace('imod2d@','uvw@')],
                                            models[tag.replace('imod2d@','phasecenter@')],
                                            uvmodel_in=models[tag.replace('imod2d@','uvmodel@')],
                                            average=True,
                                            verbose=False)
                #models[tag.replace('imod2d@','uvmodel@')]+=uvmodel 
            if  models[tag.replace('imod2d@','type@')]=='image':
                #print('-->',tag)
                fits.writeto('test1.fits',models[tag],header=models[tag.replace('imod2d@','header@')],overwrite=True)
                fits.writeto('test3.fits',models[tag.replace('imod2d@','psf@')],header=models[tag.replace('imod2d@','header@')],overwrite=True)
                cmodel,kernel=gmake_model_convol(models[tag],
                                     models[tag.replace('imod2d@','header@')],
                                     psf=models[tag.replace('imod2d@','psf@')],
                                     returnkernel=True,
                                     average=True,
                                     verbose=False)
                fits.writeto('test2.fits',cmodel,header=models[tag.replace('imod2d@','header@')],overwrite=True)
                                                                    
                models[tag.replace('imod2d@','cmod2d@')]=cmodel.copy()
                models[tag.replace('imod2d@','cmodel@')]+=cmodel.copy()
                models[tag.replace('imod2d@','kernel@')]=kernel.copy()                      
            
        if  'imod3d@' in tag:

            if  models[tag.replace('imod3d@','type@')]=='vis':
            
                #print('>>> '+tag)
                uvmodel=gmake_model_uvsample(models[tag],models[tag.replace('imod3d@','header@')],
                                            models[tag.replace('imod3d@','data@')],
                                            models[tag.replace('imod3d@','uvw@')],
                                            models[tag.replace('imod3d@','phasecenter@')],
                                            uvmodel_in=models[tag.replace('imod3d@','uvmodel@')],
                                            average=False,
                                            verbose=False)
                 #models[tag.replace('imod3d@','uvmodel@')]+=uvmodel
             
            if  models[tag.replace('imod3d@','type@')]=='image':
                              #print('-->',tag)
                cmodel,kernel=gmake_model_convol(models[tag],
                                     models[tag.replace('imod3d@','header@')],
                                     psf=models[tag.replace('imod3d@','psf@')],
                                     returnkernel=True,
                                     average=False,
                                     verbose=False)
                models[tag.replace('imod3d@','cmod3d@')]=cmodel.copy()
                models[tag.replace('imod3d@','cmodel@')]+=cmodel.copy()
                models[tag.replace('imod3d@','kernel@')]=kernel.copy()
             
        #"""
        
        #print(uvmodel.flags)
        #print("--")
        #print(models[tag.replace('imod2d@','uvmodel@')].flags)                                      
        #print(uvmodel is models[tag.replace('imod2d@','uvmodel@')])                               
        
    if  verbose==True:            
        print("---{0:^10} : {1:<8.5f} seconds ---".format('simobs-total',time.time() - start_time))            
                
    return models                

def gmake_model_lnlike(theta,fit_dct,inp_dct,dat_dct,
                         savemodel='',returnwdev=False,
                         verbose=False):
    """
    the likelihood function
    
        step:    + fill the varying parameter into inp_dct
                 + convert inp_dct to mod_dct
                 + use mod_dct to regenerate RC
    """
    
    blobs={'lnprob':0.0,
           'chisq':0.0,
           'ndata':0.0,
           'wdev':np.array([]),
           'npar':len(theta)}
     
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
    gmake_gravity_galpy(mod_dct,plotrc=False)
    #print('Took {0} second on inp2mod'.format(float(time.time()-tic0))) 
    
    #tic0=time.time()
    #models=gmake_kinmspy_api(mod_dct,dat_dct=dat_dct)
    nsamps=100000
    if  savemodel!='':
        nsamps=nsamps*10
    models=gmake_model_api(mod_dct,dat_dct=dat_dct,
                           decomp=False,verbose=False,nsamps=nsamps)
    #print('Took {0} second on one API run'.format(float(time.time()-tic0))) 
    #gmake_listpars(mod_dct)
    
    #tic0=time.time()
    
    for key in models.keys(): 
        
        if  'data@' not in key:
            continue


        if  models[key.replace('data@','type@')]=='vis':
            
            uvmodel=models[key.replace('data@','uvmodel@')]
            uvdata=models[key]
            
            #
            # averaging different correllation assumed to be RR/LL or XX/YY
            # don't use weight_spectrum here
            #        
            #uvdata=np.mean(models[key],axis=-1)                            # nrecord x nchan
            #weight=np.sum(models[key.replace('data@','weight@')],axis=-1)   # nrecord
            #weight=models[key.replace('data@','weight@')]
            #weight+spectrum=np.broadcast_to(weight[:,np.newaxis],uvmodel.shape)      # nrecord x nchan (just view for memory saving)
    
            nchan=(uvmodel.shape)[-1]
    
            weight_sqrt=ne.evaluate("sqrt(a)",
                               local_dict={"a":models[key.replace('data@','weight@')]})
            weight_sqrt=np.sqrt(models[key.replace('data@','weight@')])        
            wdev=ne.evaluate("abs(a-b).real*c",
                             local_dict={'a':models[key],
                                         'b':models[key.replace('data@','uvmodel@')],
                                         'c':np.broadcast_to(weight_sqrt[:,np.newaxis],uvmodel.shape)})
            """
            wdev=ne.evaluate("abs(a-b).real*sqrt(c)",
                             local_dict={'a':models[key],
                                         'b':models[key.replace('data@','uvmodel@')],
                                         'c':np.broadcast_to((models[key.replace('data@','weight@')])[:,np.newaxis],uvmodel.shape)})
            """
            lnl1=ne.evaluate("sum(wdev**2)")    # speed up for long vectors:  lnl1=np.sum( wdev**2 )
            lnl2=ne.evaluate("sum(-log(a))",
                             local_dict={'a':models[key.replace('data@','weight@')]})*nchan + \
                 np.log(2.0*np.pi)*uvdata.size
            
            lnl=-0.5*(lnl1+lnl2)        
            blobs['lnprob']+=lnl
            blobs['chisq']+=lnl1
            blobs['ndata']+=wdev.size
            #print(key,lnl1,wdev.size)
            
            if  returnwdev==True:
                blobs['wdev']=np.append(blobs['wdev'],wdev)
            
        #print("---{0:^30} : {1:<8.5f} seconds ---\n".format('chisq',time.time() - tic0))

        if  models[key.replace('data@','type@')]=='image':
            
            im=models[key]
            hd=models[key.replace('data@','header@')]        
            mo=models[key.replace('data@','cmodel@')]
            em=models[key.replace('data@','error@')]
            mk=models[key.replace('data@','mask@')]
            sp=models[key.replace('data@','sample@')]
            
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
    
            if  sp is not None:
                imtmp=np.squeeze(em)
                nxyz=np.shape(imtmp)
                if  len(nxyz)==3:
                    imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1]),np.arange(nxyz[2])),\
                                                imtmp,sp[:,::-1],method='linear')
                else:
                    imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1])),\
                                                imtmp,sp[:,1::-1],method='linear')
                sigma2=imtmp**2.
                imtmp=np.squeeze(im-mo)
                
                if  len(nxyz)==3:
                    imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1]),np.arange(nxyz[2])),\
                                                imtmp,sp[:,::-1],method='linear')
                else:
                    imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1])),\
                                                imtmp,sp[:,1::-1],method='linear')
            else:
                
                sigma2=np.ravel(np.squeeze(em)**2.)
                imtmp=np.ravel(np.squeeze(im-mo))
                mk=np.ravel(mk)
                sigma2=sigma2[np.where(mk==0)]
                imtmp=imtmp[np.where(mk==0)]
            
            #print(sp[:,1::-1])
    
            lnl1=np.nansum( (imtmp)**2/sigma2 )
            lnl2=np.nansum( np.log(sigma2*2.0*np.pi) )
            lnl=-0.5*(lnl1+lnl2)
            wdev=imtmp/np.sqrt(sigma2)
      
            
            blobs['lnprob']+=lnl
            blobs['chisq']+=lnl1
            blobs['ndata']+=wdev.size

            if  returnwdev==True:
                blobs['wdev']=np.append(blobs['wdev'],wdev)         


    if  savemodel!='':
        #   remove certain words from long file names 

        outname_exclude=None
        if  'shortname' in inp_dct['optimize'].keys():
            outname_exclude=inp_dct['optimize']['shortname']
        if  'outname_exclude' in inp_dct['optimize'].keys():
            outname_exclude=inp_dct['optimize']['outname_exclude']
            
        outname_replace=None
        if  'outname_replace' in inp_dct['optimize'].keys():
            outname_replace=inp_dct['optimize']['outname_replace']
                                
        print('+'*80)
        print('export set: {0:^50}'.format(savemodel))
        start_time = time.time()
        print('+'*80)
        gmake_model_export(models,outdir=savemodel,
                           outname_exclude=outname_exclude,
                           outname_replace=outname_replace)
        print('-'*80)
        print("--- took {0:<8.5f} seconds ---".format(time.time()-start_time))        

    lnl=blobs['lnprob']
    
    return lnl,blobs

#@profile
def gmake_model_export(models,outdir='./',outname_exclude=None,outname_replace=None):
    """
        export model into FITS
        shortname:    a string list to get rid of from the original data image name
        
    """
    for key in list(models.keys()): 
        
        if  'data@' not in key:
            continue

        
        if  models[key.replace('data@','type@')]=='vis':
        
            basename=key.replace('data@','')
            #   name string replacement
            if  outname_replace is not None:
                for ostring, rstring in outname_replace:
                    basename=basename.replace(ostring,rstring)
            #   name string exclusion
            if  outname_exclude is not None:
                for ostring in outname_exclude:
                    basename=basename.replace(ostring,'')            
            basename=os.path.basename(basename)
            print('-->','data_'+basename)
            
            if  not os.path.exists(outdir):
                os.makedirs(outdir)
                
                
            versions=['data','imodel','cmodel','error','mask','kernel','psf','residual',
                      'imod2d','imod3d','cmod2d','cmod3d']
            versions=['imodel','imod2d','imod3d']        
            hd=models[key.replace('data@','header@')]
            for version in versions:             
                if  key.replace('data@',version+'@') in models.keys():
                    if  models[key.replace('data@',version+'@')] is not None:
                        print(key.replace('data@',version+'@'))
                        tmp=(models[key.replace('data@',version+'@')]).copy()
                        if  tmp.ndim==2:
                            tmp=tmp[np.newaxis,np.newaxis,:,:]
                        fits.writeto(outdir+'/'+version+'_'+basename,
                                     tmp,
                                     models[key.replace('data@','header@')],
                                     overwrite=True)
            
            for prof in list(models.keys()):
                
                if  'imod3d_prof@' in prof  and key.replace('data@','') in prof:
                    outname=prof.replace(key.replace('data@',''),'')
                    outname=outname.replace('imod3d_prof@','imodrp_').replace('@','_')
                    gmake_dct2fits(models[prof],outname=outdir+'/'+outname+basename.replace('.fits',''))
                    
    
            oldms=key.replace('data@','')
            newms=outdir+'/data_'+basename.replace('.fits','.ms')
            
            print("copy "+oldms+'  to  '+newms)
            os.system("rm -rf "+newms)
            os.system('cp -rf '+oldms+' '+newms)
            
            add_uvmodel(newms,models[key.replace('data@','uvmodel@')]) 
        
        
        if  models[key.replace('data@','type@')]=='image':
            
            basename=key.replace('data@','')
            #   name string replacement
            if  outname_replace is not None:
                for ostring, rstring in outname_replace:
                    basename=basename.replace(ostring,rstring)
            #   name string exclusion
            if  outname_exclude is not None:
                for ostring in outname_exclude:
                    basename=basename.replace(ostring,'')            
            basename=os.path.basename(basename)
            
            print('-->','data_'+basename)
            
            if  not os.path.exists(outdir):
                os.makedirs(outdir)
            versions=['data','imodel','cmodel','error','mask','kernel','psf','residual',
                      'imod2d','imod3d','cmod2d','cmod3d']
            hd=models[key.replace('data@','header@')]
            for version in versions:
                if  version=='residual' and key.replace('data@','cmodel@') in models.keys():
                    if  models[key.replace('data@','cmodel@')] is not None:
                        fits.writeto(outdir+'/'+version+'_'+basename,
                                     models[key]-models[key.replace('data@','cmodel@')],
                                     models[key.replace('data@','header@')],
                                     overwrite=True)                
                if  key.replace('data@',version+'@') in models.keys():
                    if  models[key.replace('data@',version+'@')] is not None:
                        tmp=(models[key.replace('data@',version+'@')]).copy()
                        if  tmp.ndim==2:
                            tmp=tmp[np.newaxis,np.newaxis,:,:]
                        fits.writeto(outdir+'/'+version+'_'+basename,
                                     tmp,
                                     models[key.replace('data@','header@')],
                                     overwrite=True)
            
            for prof in list(models.keys()):
                
                if  'imod3d_prof@' in prof  and key.replace('data@','') in prof:
    
                    outname=prof.replace(key.replace('data@',''),'')
                    outname=outname.replace('imod3d_prof@','imodel_').replace('@','_')
                    gmake_dct2fits(models[prof],outname=outdir+'/'+outname+basename.replace('.fits','.rp'))            
        

    np.save(outdir+'/'+'mod_dct.npy',models['mod_dct'])

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

    if  verbose==True:
        start_time = time.time()
        
    lp = gmake_model_lnprior(theta,fit_dct)
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        return -np.inf,blobs
    lnl,blobs=gmake_model_lnlike(theta,fit_dct,inp_dct,dat_dct,savemodel=savemodel)
    
    if  verbose==True:
        print("try ->",theta)
        print("---{0:^10} : {1:<8.5f} seconds ---".format('lnprob',time.time()-start_time))    
    
    return lp+lnl,blobs        


def gmake_model_chisq(theta,
                      fit_dct=None,inp_dct=None,dat_dct=None,
                      savemodel='',
                      verbose=False):
    """
    this is the evaluating function for amoeba 
    """

    if  verbose==True:
        start_time = time.time()
        
    lp = gmake_model_lnprior(theta,fit_dct)
    if  lp!=0:
        lp=+np.inf
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        #return +np.inf,blobs
        return +np.inf
    
    lnl,blobs=gmake_model_lnlike(theta,fit_dct,inp_dct,dat_dct,savemodel=savemodel)
    
    if  verbose==True:
        print("try ->",theta)
        print("---{0:^10} : {1:<8.5f} seconds ---".format('lnprob',time.time()-start_time))    

    return lp+blobs['chisq']       


def gmake_model_lmfit_wdev(params,
                     #fjac=None, x=None, y=None, err=None,
                     fit_dct=None,inp_dct=None,dat_dct=None,
                     blobs=None,      # save the metadata along / list
                     savemodel='',
                     verbose=True):
    """
    this is the evaluating function for mpfit
    return weighted deviations:
        http://cars9.uchicago.edu/software/python/mpfit.html
        or
        from mgefit
    """
    theta=[]
    for key in params:
        theta.append(params[key].value)
    theta=np.array(theta)
    
    status=0
    if  verbose==True:
        start_time = time.time()
        
    lp = gmake_model_lnprior(theta,fit_dct)
    if  lp!=0:
        lp=+np.inf
#     if  not np.isfinite(lp):
#         blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
#         #return +np.inf,blobs
#         return +np.inf
    
    lnl,blob=gmake_model_lnlike(theta,fit_dct,inp_dct,dat_dct,savemodel=savemodel)
 
    wdev=blob['wdev'].flatten().copy()
    
    if  blobs is not None:
        blobs['pars'].append(theta)
        blobs['chi2'].append(blob['chisq'])

    if  verbose==True:
        print("")
        print('ifeva: ',len(blobs['chi2']))
        print('try:   ',theta)
        print('chisq: ','{0:>16.2f} {1:>16.2f}'.format(np.sum(wdev**2.0),wdev.size))
        print("---{0:^10} : {1:<8.5f} seconds ---".format('lnprob',time.time()-start_time))

    return wdev       





if  __name__=="__main__":
    
    pass




