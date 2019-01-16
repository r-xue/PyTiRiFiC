
if  __name__=="__main__":

    mcpars={}


    #mode: test_int, test_runtime, test_emcee
    
    ###########################################################################################
    """
    mcpars['mode']='test'
    mcpars['mode']='amoeba'                 # run amoeba
    mcpars['iter']=False
    mcpars['p_scale_temperature']=1.0
    #mcpars['mode']='emcee'                  # run emcee
    mcpars['version']='HXMM01N.all'
    mcpars['outfolder']=mcpars['version']+'.'+mcpars['mode']
    mcpars['imlist']=['CICO76','water']     #   imset name
    mcpars['objects']=['N1,N2','N1,N2']     #   included objects
    mcpars['lines']=['CO76,CI','water']     #   included lines
    mcpars['pline']='CO76'          #   primary line for setting up the shared disk parameter
                                    #   typically the bright and extended line
    """                                                    
    ###########################################################################################


    """
    mcpars['mode']='emcee'                  # run emcee
    mcpars['iter']=False
    mcpars['nwalkers']=120
    mcpars['version']='HXMM01N.vsbr'
    mcpars['imlist']=['CICO76','water']     #   imset name
    mcpars['objects']=['N1','N1']     #   included objects
    mcpars['lines']=['CO76,CI','water']     #   included lines
    mcpars['pline']='CO76'          #   primary line for setting up the shared disk parameter
                                    #   typically the bright and extended line                    
    """
    
    """
    mcpars['mode']='emcee'                  # run emcee
    mcpars['iter']=False
    mcpars['nwalkers']=100
    mcpars['version']='HXMM01N.carbon09exp'
    mcpars['imlist']=['CICO76']     #   imset name
    mcpars['objects']=['N1']        #   included objects
    mcpars['lines']=['CO76,CI']     #   included lines
    mcpars['pline']='CO76'          #   primary line for setting up the shared disk parameter
                                    #   typically the bright and extended line                    
    """



    #"""
    mcpars['mode']='emcee'                  # run emcee
    mcpars['iter']=False
    mcpars['nwalkers']=106
    mcpars['version']='Core.test'
    mcpars['imlist']=['CII']     #   imset name
    mcpars['objects']=['Core']     #   included objects
    mcpars['lines']=['CII']     #   included lines
    mcpars['pline']='CII'          #   primary line for setting up the shared disk parameter
                                    #   typically the bright and extended line    
    #"""
    
    """
    mcpars['mode']='emcee'
    mcpars['iter']=False
    mcpars['nwalkers']=60
    mcpars['version']='HXMM01.co09exp'
    mcpars['imlist']=['CO10']     #   imset name
    mcpars['objects']=['N1,S2,S3']     #   included objects
    mcpars['lines']=['CO10']     #   included lines
    mcpars['pline']='CO10'          #   primary line for setting up the shared disk parameter
                                    #   typically the bright and extended line                        
    """

    #mcpars['mode']='test_runtime'       # test single-thread speed; more related to I/O speed overhead
    #mcpars['mode']='test_emcee'         # test emcee speed; more about the CPU raw power (freq x core)
    
    """
    mcpars['mode']='emcee'                  # run emcee
    mcpars['iter']=False
    mcpars['version']='HXMM01N.water'
    mcpars['imlist']=['water']     #   imset name
    mcpars['objects']=['N1']     #   included objects
    mcpars['lines']=['water']     #   included lines
    mcpars['pline']='water'          #   primary line for setting up the shared disk parameter
                                    #   typically the bright and extended line                
    """
    
    ########################################################################################################
    
    
    mcpars['nthreads']=multiprocessing.cpu_count()
    mcpars['outfolder']=mcpars['version']+'.'+mcpars['mode']
    
    disks=py_tirific_mc_setup_hxmm01_disks(mcpars['lines'],mcpars['objects'])
    imsets,data=py_tirific_mc_setup_hxmm01_imsets(mcpars['imlist'],mcpars['lines'],mcpars['objects'])
    
    #    LOAD VARYING PARAMETERS
    
    mcpars['p_start']=[]
    mcpars['p_lo']=[]
    mcpars['p_up']=[]
    mcpars['p_keys']=[]
    mcpars['p_iscale']=[]       #   initial dispersion for MCMC, at least larger than pixel length
    mcpars['p_scale']=[]        #   NM fit scaling parameter, for the searching range 
    
    # DEFINE PARA:  OBJECT BY OBJECT
    
    for object in sorted(set((','.join(mcpars['objects'])).split(','))):
        
        # USE PRIMARY LINE METADATA FOR THE OBJECT INFO



        
        if  mcpars['pline']!='CO10':
        
            tmp=(getdisk(disks,object,mcpars['pline']))['xypos']
            
            """
            
            mcpars['p_keys']=np.append(mcpars['p_keys'],['x'+object])
            mcpars['p_start']=np.append(mcpars['p_start'],tmp[0])
            mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[0]-1./3600)
            mcpars['p_up']=np.append(mcpars['p_up'],tmp[0]+1./3600)
            mcpars['p_iscale']=np.append(mcpars['p_iscale'],0.002/3600)
            mcpars['p_scale']=np.append(mcpars['p_scale'],0.5/3600)
            mcpars['p_keys']=np.append(mcpars['p_keys'],['y'+object])
            mcpars['p_start']=np.append(mcpars['p_start'],tmp[1])
            mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[1]-1./3600)
            mcpars['p_up']=np.append(mcpars['p_up'],tmp[1]+1./3600)
            mcpars['p_iscale']=np.append(mcpars['p_iscale'],0.002/3600)
            mcpars['p_scale']=np.append(mcpars['p_scale'],0.5/3600)
                 
            """
            
            tmp=(getdisk(disks,object,mcpars['pline']))['inc']    
            mcpars['p_keys']=np.append(mcpars['p_keys'],['in'+object])
            mcpars['p_start']=np.append(mcpars['p_start'],tmp)
            mcpars['p_lo']=np.append(mcpars['p_lo'],0.0)
            mcpars['p_up']=np.append(mcpars['p_up'],90.0)
            mcpars['p_iscale']=np.append(mcpars['p_iscale'],2.)
            mcpars['p_scale']=np.append(mcpars['p_scale'],45.)
            
            tmp=(getdisk(disks,object,mcpars['pline']))['pa'] 
            mcpars['p_keys']=np.append(mcpars['p_keys'],['pa'+object])
            mcpars['p_start']=np.append(mcpars['p_start'],tmp)
            mcpars['p_lo']=np.append(mcpars['p_lo'],tmp-90.0)
            mcpars['p_up']=np.append(mcpars['p_up'],tmp+90.0)
            mcpars['p_iscale']=np.append(mcpars['p_iscale'],2.)
            mcpars['p_scale']=np.append(mcpars['p_scale'],45.)
            
            tmp=(getdisk(disks,object,mcpars['pline']))['vsys'] 
            mcpars['p_keys']=np.append(mcpars['p_keys'],['vs'+object])
            mcpars['p_start']=np.append(mcpars['p_start'],tmp)
            mcpars['p_lo']=np.append(mcpars['p_lo'],-1000)
            mcpars['p_up']=np.append(mcpars['p_up'],1000)
            mcpars['p_iscale']=np.append(mcpars['p_iscale'],20.0)
            mcpars['p_scale']=np.append(mcpars['p_scale'],200.0)
            
            tmp=np.array((getdisk(disks,object,mcpars['pline']))['vrot'])
            nr=len(tmp)
            mcpars['p_keys']=np.append(mcpars['p_keys'],['vr'+str(x+1)+object for x in range(1,nr)])
            mcpars['p_start']=np.append(mcpars['p_start'],tmp[1:])
            mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[1:]*0.0-20000.)
            mcpars['p_up']=np.append(mcpars['p_up'],tmp[1:]*0.0+20000.)
            mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp[1:]*0.0+20.0)
            mcpars['p_scale']=np.append(mcpars['p_scale'],tmp[1:]*0.0+500.0)
            
            #"""
        
        """
        tmp=np.array((getdisk(disks,object,mcpars['pline']))['lc0'])
        nr=len(tmp)
        mcpars['p_keys']=np.append(mcpars['p_keys'],['lc'+str(x+1)+object for x in range(1,nr)])
        mcpars['p_start']=np.append(mcpars['p_start'],tmp[1:])
        mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[1:]*0.0-1.0)
        mcpars['p_up']=np.append(mcpars['p_up'],tmp[1:]*0.0+1.0)
        mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp[1:]*0.0+0.01)
        mcpars['p_scale']=np.append(mcpars['p_scale'],tmp[1:]*0.0+0.3)
        tmp=np.array((getdisk(disks,object,mcpars['pline']))['ls0'])
        nr=len(tmp)
        mcpars['p_keys']=np.append(mcpars['p_keys'],['ls'+str(x+1)+object for x in range(1,nr)])
        mcpars['p_start']=np.append(mcpars['p_start'],tmp[1:])
        mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[1:]*0.0-1.0)
        mcpars['p_up']=np.append(mcpars['p_up'],tmp[1:]*0.0+1.0)
        mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp[1:]*0.0+0.01)
        mcpars['p_scale']=np.append(mcpars['p_scale'],tmp[1:]*0.0+0.3)     
        """
        
        #"""
        tmp=np.mean((getdisk(disks,object,mcpars['pline']))['vdisp'])
        mcpars['p_keys']=np.append(mcpars['p_keys'],'vd'+object)
        mcpars['p_start']=np.append(mcpars['p_start'],tmp)
        mcpars['p_lo']=np.append(mcpars['p_lo'],tmp*0.0)
        mcpars['p_up']=np.append(mcpars['p_up'],tmp*0.0+1000.)
        mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp*0.0+15.)
        mcpars['p_scale']=np.append(mcpars['p_scale'],tmp*0.0+200.0)
        #"""
        
        """
        tmp=np.array((getdisk(disks,object,mcpars['pline']))['ldisp'])
        mcpars['p_keys']=np.append(mcpars['p_keys'],['ld'+str(x)+object for x in [0,1]])
        mcpars['p_start']=np.append(mcpars['p_start'],tmp)
        mcpars['p_lo']=np.append(mcpars['p_lo'],[10.,10.])
        mcpars['p_up']=np.append(mcpars['p_up'],[400.0,400.0])
        mcpars['p_iscale']=np.append(mcpars['p_iscale'],[15.,15.])
        mcpars['p_scale']=np.append(mcpars['p_scale'],[150.,150.])
        """
        
        """
        tmp=np.array((getdisk(disks,object,mcpars['pline']))['edisp'])
        mcpars['p_keys']=np.append(mcpars['p_keys'],['ed'+str(x)+object for x in [0,1]])
        mcpars['p_start']=np.append(mcpars['p_start'],tmp)
        mcpars['p_lo']=np.append(mcpars['p_lo'],[10.,-6.0])
        mcpars['p_up']=np.append(mcpars['p_up'],[400.0,6.0])
        mcpars['p_iscale']=np.append(mcpars['p_iscale'],[15.,0.2])
        mcpars['p_scale']=np.append(mcpars['p_scale'],[140.,3])
        """        
        
        for line in sorted(set((','.join(mcpars['lines'])).split(','))):
            
            if  mcpars['pline']!='CO10':
                
                # constrain CO 10 vdist is impossible (wild results)
                
                #tmp=np.array((getdisk(disks,object,line))['vdisp'])
                #mcpars['p_keys']=np.append(mcpars['p_keys'],['vd'+str(x+1)+line+object for x in range(nr)])
                """
                tmp=np.mean((getdisk(disks,object,line))['vdisp'])
                mcpars['p_keys']=np.append(mcpars['p_keys'],['vd'+line+object])
                mcpars['p_start']=np.append(mcpars['p_start'],tmp)
                mcpars['p_lo']=np.append(mcpars['p_lo'],tmp*0.0)
                mcpars['p_up']=np.append(mcpars['p_up'],tmp*0.0+1000.)
                mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp*0.0+15.0)
                mcpars['p_scale']=np.append(mcpars['p_scale'],tmp*0.0+200.0)
                """

                """
                tmp=np.array((getdisk(disks,object,line))['sm1a'])
                nr=len(tmp)
                mcpars['p_keys']=np.append(mcpars['p_keys'],['sm1a'+str(x+1)+line+object for x in range(1,nr)])
                mcpars['p_start']=np.append(mcpars['p_start'],tmp[1:])
                mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[1:]*0.0-1.0)
                mcpars['p_up']=np.append(mcpars['p_up'],tmp[1:]*0.0+1.0)
                mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp[1:]*0.0+0.05)
                mcpars['p_scale']=np.append(mcpars['p_scale'],tmp[1:]*0.0+1.0)
                
                #tmp=np.mean((getdisk(disks,object,line))['sm1p'])
                #mcpars['p_keys']=np.append(mcpars['p_keys'],'sm1p'+line+object)
                
                tmp=np.array((getdisk(disks,object,line))['sm1p'])
                nr=len(tmp)
                mcpars['p_keys']=np.append(mcpars['p_keys'],['sm1p'+str(x+1)+line+object for x in range(1,nr)])                
                mcpars['p_start']=np.append(mcpars['p_start'],tmp[1:])
                mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[1:]-90.0)
                mcpars['p_up']=np.append(mcpars['p_up'],tmp[1:]+90.0)
                mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp[1:]*0.0+10.0)
                mcpars['p_scale']=np.append(mcpars['p_scale'],tmp[1:]*0.0+180.0)
                """
                
                """
                tmp=np.array((getdisk(disks,object,line))['sbr'])
                nr=len(tmp)
                mcpars['p_keys']=np.append(mcpars['p_keys'],['sb'+str(x+1)+line+object for x in range(0,nr)])
                mcpars['p_start']=np.append(mcpars['p_start'],tmp[:])
                mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[:]*0.0-500.)
                mcpars['p_up']=np.append(mcpars['p_up'],tmp[:]*0.0+500.)
                mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp[:]*0.0+0.02)
                mcpars['p_scale']=np.append(mcpars['p_scale'],tmp[:]*0.0+5.0)
                """
                tmp=np.array((getdisk(disks,object,line))['esbr'])
                mcpars['p_keys']=np.append(mcpars['p_keys'],['es'+str(x)+line+object for x in [0,1]])
                mcpars['p_start']=np.append(mcpars['p_start'],tmp)
                mcpars['p_lo']=np.append(mcpars['p_lo'],[0,0.001])
                mcpars['p_up']=np.append(mcpars['p_up'],[100.0,5.0])
                mcpars['p_iscale']=np.append(mcpars['p_iscale'],[0.02,0.01])
                mcpars['p_scale']=np.append(mcpars['p_scale'],[5.,4.])
                
                
            else:

                tmp=np.array((getdisk(disks,object,line))['esbr'])
                mcpars['p_keys']=np.append(mcpars['p_keys'],['es'+str(x)+line+object for x in [0,1]])
                mcpars['p_start']=np.append(mcpars['p_start'],tmp)
                mcpars['p_lo']=np.append(mcpars['p_lo'],[0,0.001])
                mcpars['p_up']=np.append(mcpars['p_up'],[100.0,5.0])
                mcpars['p_iscale']=np.append(mcpars['p_iscale'],[0.02,0.002])
                mcpars['p_scale']=np.append(mcpars['p_scale'],[5.,4.])
                
                #tmp=np.array((getdisk(disks,object,line))['sm1a'])
                #tmp=tmp[0:7]
                #nr=len(tmp)
                #mcpars['p_keys']=np.append(mcpars['p_keys'],['sm1a'+str(x+1)+line+object for x in range(1,nr)])
                #mcpars['p_start']=np.append(mcpars['p_start'],tmp[1:])
                #mcpars['p_lo']=np.append(mcpars['p_lo'],tmp[1:]*0.0-1.0)
                #mcpars['p_up']=np.append(mcpars['p_up'],tmp[1:]*0.0+1.0)
                #mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp[1:]*0.0+0.05)
                #mcpars['p_scale']=np.append(mcpars['p_scale'],tmp[1:]*0.0+1.0)
                
                        

            """
            for ind in range(len(mcpars['lines'])):
                if  line in (mcpars['lines'])[ind]:
                    imlist0=(mcpars['imlist'])[ind]
                    tmp=data[imlist0]['is']
                    mcpars['p_keys']=np.append(mcpars['p_keys'],['is'+str(x)+line+object for x in range(len(tmp))])
                    mcpars['p_start']=np.append(mcpars['p_start'],tmp)
                    mcpars['p_lo']=np.append(mcpars['p_lo'],tmp*0.0)
                    mcpars['p_up']=np.append(mcpars['p_up'],tmp*0.0+2000.0)
                    mcpars['p_iscale']=np.append(mcpars['p_iscale'],tmp*0.0+0.02)
                    mcpars['p_scale']=np.append(mcpars['p_scale'],tmp*0.0+5.0)
            """
            
    # DEFINE NOISE SCALING:  IM BY IM ONLY FOR MCMC
    
    if  mcpars['mode']=='emcee' or mcpars['mode']=='test_emcee':
        
        if  mcpars['iter']==True:
            mcpars_amoeba=np.load(mcpars['version']+'.'+'amoeba'+'/mcpars.npy').item()
            mcpars['p_start']=mcpars_amoeba['p_amoeba']['p_best']
                        
        """
        for imlist0 in mcpars['imlist']:
            # note: lnf=p.log(np.sqrt(chisq/dof))
            mcpars['p_keys']=np.append(mcpars['p_keys'],['lnf'+imlist0])
            if  imlist0=='water':
                if  fnmatch.fnmatch(mcpars['version'],'HXMM01S*'): 
                    mcpars['p_start']=np.append(mcpars['p_start'],0.05)
                if  fnmatch.fnmatch(mcpars['version'],'HXMM01N*'): 
                    mcpars['p_start']=np.append(mcpars['p_start'],0.11)                
            if  imlist0=='CICO76':
                if  fnmatch.fnmatch(mcpars['version'],'HXMM01S*'):
                    mcpars['p_start']=np.append(mcpars['p_start'],0.0)
                if  fnmatch.fnmatch(mcpars['version'],'HXMM01N*'):
                    mcpars['p_start']=np.append(mcpars['p_start'],0.0)
            if  imlist0=='CO10':
                mcpars['p_start']=np.append(mcpars['p_start'],-0.14)            
            mcpars['p_lo']=np.append(mcpars['p_lo'],-2.0)
            mcpars['p_up']=np.append(mcpars['p_up'],2.0)
            mcpars['p_iscale']=np.append(mcpars['p_iscale'],0.005)
            mcpars['p_scale']=np.append(mcpars['p_scale'],1.)
        """

    
    # DEFINE PARAMETER FORMAT
    
    mcpars=py_tirific_mc_pformat(mcpars)
    
    if  mcpars['mode']=='emcee' or mcpars['mode']=='test_emcee':
        
        #   SETUP MCMC
        
        print "+"*90
        mcpars['ndim']=len(mcpars['p_start'])
        
        print 'nwalkers:',mcpars['nwalkers']
        print 'nthreads:',mcpars['nthreads']
        print 'ndim:    ',mcpars['ndim']
        
        np.random.seed(0)
        mcpars['pos_start'] = \
        [ np.maximum(np.minimum(mcpars['p_start']+mcpars['p_iscale']*np.random.randn(mcpars['ndim']),mcpars['p_up']),mcpars['p_lo']) for i in range(mcpars['nwalkers']) ]
        
        sampler = emcee.EnsembleSampler(mcpars['nwalkers'],mcpars['ndim'],tirific_lnprob,
                                        args=(data,imsets,disks,mcpars),threads=mcpars['nthreads'],runtime_sortingfn=sort_on_runtime)
                                        #args=(data,imsets,disks,mcpars),threads=mcpars['nthreads'])
        if  not os.path.exists(mcpars['outfolder']):
            os.makedirs(mcpars['outfolder'])
        mcpars['chainfile']=mcpars['outfolder']+'/chain.dat'
        mcpars['fitstable']=mcpars['outfolder']+'/chain.fits'
        f=open(mcpars['chainfile'], "w")
        output='{0:<5}'.format('#is')
        output+=' {0:<5}'.format('iw')
        output+=' '.join(('{0:'+mcpars['p_format_keys'][x]+'}').format(mcpars['p_keys'][x]) for x in range(len(mcpars['p_keys'])))
        output+=' {0:<6} {1:<6} {2:<6} {3:<5}'.format('lnprob','chisq','ndata','npar')
        output+='\n'
        f.write(output)
        f.close()
        
        #    BOOK KEEPING
        
        mcpars['pos_last']=deepcopy(mcpars['pos_start'])
        mcpars['step_last']=0
        
        np.save(mcpars['outfolder']+'/mcpars.npy',mcpars)   #   Mmcmc metadata
        np.save(mcpars['outfolder']+'/imsets.npy',imsets)   #   images metadata
        np.save(mcpars['outfolder']+'/disks.npy',disks)     #   disk metadata
        np.save(mcpars['outfolder']+'/data.npy',data)       #   data holder
        
        #print "+"*90
        #py_tirific_pprint(mcpars['p_keys'],mcpars_amoeba['p_amoeba']['p_best'],mcpars['p_start'],mcpars['p_lo'],mcpars['p_up'],mcpars['p_format'])
        #print "+"*90
        tic0=time.time()
        tmp=copy.deepcopy(mcpars)
        tmp['outfolder']=mcpars['outfolder']+'/p_start'
        lnl,blobs=tirific_lnlike(mcpars['p_start'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=False,decomp=False,moms=False,inty=1,usesp=True)
        print 'ndata->',blobs['ndata']
        print 'chisq->',blobs['chisq']
        print 'Took {0} second for one trial'.format(float(time.time()-tic0))
        lnl,blobs=tirific_lnlike(mcpars['p_start'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=1,usesp=True)
        
        #tmp['outfolder']=mcpars['outfolder']+'/p_start_na'
        #lnl,blobs=tirific_lnlike(mcpars['p_start'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=1,usesp=True,beam=False)
        #tmp['outfolder']=mcpars['outfolder']+'/p_start_fo_na'
        #lnl,blobs=tirific_lnlike(mcpars['p_start'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=1,usesp=True,beam=False,faceon=True)
        
    if  mcpars['mode']=='test_emcee':
        
        execfile(code_path+'/py_tirific_mc_run.py')
        
              
    if  mcpars['mode']=='amoeba':

        tic0=time.time()
        
        if  mcpars['iter']==True:
            mcpars_amoeba=np.load(mcpars['version']+'.'+'amoeba'+'/mcpars.npy').item()
            mcpars['p_start']=deepcopy(mcpars_amoeba['p_amoeba']['p_best'])
            if 'p_scale_temperature' in mcpars.keys():
                mcpars['p_scale']=mcpars['p_scale']*mcpars['p_scale_temperature']
        
        tmp=copy.deepcopy(mcpars)
        tmp['outfolder']=mcpars['outfolder']+'/p_start'
        lnl,blobs=tirific_lnlike(mcpars['p_start'],data,imsets,disks,tmp)
        print 'Took {0} second for one trial'.format(float(time.time()-tic0))
                
        tmp=copy.deepcopy(mcpars)
        tmp['outfolder']=mcpars['outfolder']+'/p_start'
        lnl,blobs=tirific_lnlike(mcpars['p_start'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=False,moms=True,inty=1,usesp=False)
        print 'chisq<<<',blobs['chisq']
        print 'ndata<<<',blobs['ndata']
        tmp1=blobs['chisq']
        
        mcpars['p_amoeba']=amoeba_sa(tirific_chisq,
                     mcpars['p_start'],
                     mcpars['p_scale'],
                     p_lo=mcpars['p_lo'],
                     p_up=mcpars['p_up'],
                     funcargs={'data':data,'imsets':imsets,'disks':disks,'mcpars':mcpars,'verbose':False},
                     verbose=True,ftol=1e-7,
                     maxiter=1000)
        np.save(mcpars['outfolder']+'/mcpars.npy',mcpars)
        
        tmp=copy.deepcopy(mcpars)
        tmp['outfolder']=mcpars['outfolder']+'/p_best'
        lnl,blobs=tirific_lnlike(mcpars['p_amoeba']['p_best'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=False,moms=True,inty=1,usesp=False)
        lnl,blobs=tirific_lnlike(mcpars['p_amoeba']['p_best'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=1,usesp=False)
        print 'chisq<<<<',tmp1
        print 'chisq>>>>',blobs['chisq']
        print 'ndata>>>>',blobs['ndata']
        
        tmp=copy.deepcopy(mcpars)   # intrinsic
        tmp['outfolder']=mcpars['outfolder']+'/p_best_na'
        lnl,blobs=tirific_lnlike(mcpars['p_amoeba']['p_best'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=False,moms=True,inty=1,usesp=False,beam=False)
        lnl,blobs=tirific_lnlike(mcpars['p_amoeba']['p_best'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=1,usesp=False,beam=False)
        print 'chisq->',blobs['chisq']
        
        tmp=copy.deepcopy(mcpars)   # face-on
        tmp['outfolder']=mcpars['outfolder']+'/p_best_fo'
        p_keys=deepcopy(tmp['p_keys'])
        p_test=tmp['p_amoeba']['p_best']
        for t in range(len(p_keys)):
            if  fnmatch.fnmatch(p_keys[t],'in*'):
                p_test[t]=0.0
        lnl,blobs=tirific_lnlike(p_test,data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=False,moms=True,inty=1,usesp=False,beam=False)        
        lnl,blobs=tirific_lnlike(p_test,data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=1,usesp=False,beam=False)
        print 'chisq->',blobs['chisq']                
        
        print "+"*90
        py_tirific_pprint(mcpars['p_keys'],mcpars['p_amoeba']['p_best'],mcpars['p_start'],mcpars['p_lo'],mcpars['p_up'],mcpars['p_format'])
        print "+"*90
        print 'Took {0} second for this AMOEBA run'.format(float(time.time()-tic0))
        
        
    if  mcpars['mode']=='test_runtime':
        # test singlethread running time with 10 trails 
        tmp=copy.deepcopy(mcpars)
        tmp['outfolder']=mcpars['outfolder']+'/p_start'
        py_tirific_pprint(mcpars['p_keys'],mcpars['p_start'],mcpars['p_start'],mcpars['p_lo'],mcpars['p_up'],mcpars['p_format'])
        print "+"*90
        tic0=time.time()
        for i in range(5):
            #lnl,blobs=tirific_lnlike(mcpars['p_start'],data,imsets,disks,tmp,verbose=False,uuid=True,keepfile=False,beam=True,decomp=False)
            lnl,blobs=tirific_lnlike(mcpars['p_start'],data,imsets,disks,tmp,verbose=False,uuid=False,keepfile=True,beam=True,decomp=False)
        print blobs['ndata']
        print 'Took {0} second for 5 trials on single-thread evaluation'.format(float(time.time()-tic0))    
        print np.shape(data['CICO76']['im'])
        print lnl
        
        
    if  mcpars['mode']=='test_init':

        tmp=copy.deepcopy(mcpars)
        
        #for imlist0 in imsets.keys():
        #    (imsets[imlist0])['cflux_scale']=1e-7
        
        py_tirific_pprint(mcpars['p_keys'],mcpars['p_start'],mcpars['p_start'],mcpars['p_lo'],mcpars['p_up'],mcpars['p_format'])
        print "+"*90
        tic0=time.time()
        
        tmp['outfolder']=mcpars['outfolder']+'/p_start'
        lnl,blobs=tirific_lnlike(tmp['p_start'],data,imsets,disks,tmp,verbose=False,uuid=False,keepfile=True,beam=True,decomp=True,moms=True,ppp=True)
        tmp['outfolder']=mcpars['outfolder']+'/p_start_na'
        lnl,blobs=tirific_lnlike(tmp['p_start'],data,imsets,disks,tmp,verbose=False,uuid=False,keepfile=True,beam=False,decomp=True,moms=True,ppp=True)
        
        p_keys=deepcopy(tmp['p_keys'])
        p_start=deepcopy(tmp['p_start'])
        for t in range(len(p_keys)):
            if  fnmatch.fnmatch(p_keys[t],'in*'):
                p_start[t]=1.0    
        tmp['outfolder']=mcpars['outfolder']+'/p_start_fo'
        lnl,blobs=tirific_lnlike(p_start,data,imsets,disks,tmp,verbose=False,uuid=False,keepfile=True,beam=True,decomp=True,moms=True,ppp=True)
        tmp['outfolder']=mcpars['outfolder']+'/p_start_fo_na'
        lnl,blobs=tirific_lnlike(p_start,data,imsets,disks,tmp,verbose=False,uuid=False,keepfile=True,beam=False,decomp=True,moms=True,ppp=True)
        
        print 'Took {0} second for the test_init run'.format(float(time.time()-tic0))    
        #print np.shape(data[['im'])        

    
    #tmp=copy.deepcopy(mcpars)       
    #tmp['outfolder']='HXMM01S.all.afit/p_bestfit'  
    #lnl,blobs=tirific_lnlike(p_afit['p_best'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True) 
    #tmp['outfolder']='HXMM01S.all.afit/p_bestfit_na'       
    #py_tirific_pprint(mcpars['p_keys'],p_afit['p_best'],mcpars['p_start'],mcpars['p_format'])
    
    
    #p0=mcpars['p_start']
    #ps=mcpars['p_iscale']*1e3
    #initial_simplex=np.outer(np.ones(len(p0)+1),p0)
    #for i in range(len(p0)):
    #    initial_simplex[i+1, i]=p0[i]+ps[i]
    
    #pr=optimize.minimize(tirific_chisq_d,p0,args=(data,imsets,disks,mcpars),method='Nelder-Mead',tol=1e-10,options={'disp':True,'maxiter':200,'maxiter':200,'initial_simplex':initial_simplex}) 
    #print pr.x
    #print pr.fun
    
    #pr=optimize.minimize(tirific_chisq_d,p0,args=(data,imsets,disks,mcpars),method='BFGS',tol=1,options={'disp':True,'maxiter':200})
    #print pr.x
    #print pr.fun
    
    
    
    
    
    
    
    #    SAVE START MODEL
    
    #tic=time.time()
    #tmp=deepcopy(mcpars)
    #tmp['outfolder']=tmp['outfolder']+'/p_start'
    
    
    #print("Done.")
    #print 'Took {0} minutes'.format(float(time.time()-tic)/float(60.))    
    
    
    #lnl,blobs=tirific_lnlike([],data,imsets,disks,mcpars,uuid=False,verbose=True,keepfile=True,ppp=True)
    
        
    #tirific_diskmod(imsets['CICO76'],disks,verbose=True,decomp=False)


