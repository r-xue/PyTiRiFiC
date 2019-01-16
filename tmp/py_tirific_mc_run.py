
if  __name__=="__main__":
    """
        RUN simulations
    """
    #####
    mcpars['nstep']=1000
    #####
    
    tic=time.time()
    dt=0.0
    
    print("")
    print("Running MCMC...")
    print(">>"+mcpars['chainfile'])
    print(">>"+mcpars['outfolder']+"/chain_mef.fits")
    print("")
    
    if  mcpars['mode']=='test_emcee':
        mcpars['nstep']=2
    
    for i,(pos_i,lnprob_i,rstat_i,blobs_i) in enumerate(sampler.sample(mcpars['pos_last'],iterations=mcpars['nstep'])):
        # http://emcee.readthedocs.io/en/stable/api.html#emcee.EnsembleSampler.sample
        # pos    (nwalkers,ndim)
        # lnprob (nwalkers,)
        # blobs  (nwalkers,)
        mcpars['step_last']+=1
        
        #   WRITE ASCII TABLE
        tic0=time.time() 
        f = open(mcpars['chainfile'], "a")
        for k in range(pos_i.shape[0]):
            output='{0:<5}'.format(mcpars['step_last'])
            output+=' {0:<5}'.format(k)
            output+=' '.join(('{0:'+mcpars['p_format'][x]+'}').format(pos_i[k][x]) for x in range(len(pos_i[k])))
            output+=' {0:<6.0f} {1:<6.0f} {2:<6.0f} {3:<5.0f}'.format(lnprob_i[k],blobs_i[k]['chisq'],blobs_i[k]['ndata'],blobs_i[k]['npar'])
            output+='\n'
            f.write(output)
        f.close()
        dt+=float(time.time()-tic0)
         
        if  mcpars['mode']!='test_emcee':
            
            if  (i+1) % int(mcpars['nstep']/10.0) == 0 :
                
                print("{0:5.1%}".format(float(i+1)/mcpars['nstep']))
                print("IO {0:8.1f}s".format(dt))
                print("CPU{0:8.1f}m").format(float(time.time()-tic)/float(60.))
                
            #   WRITE FITS TABLE
            
                tic0=time.time()
                #astable=ascii.read(mcpars['chainfile'])
                #astable.write(mcpars['fitstable'],format='fits',overwrite=True)
                #dt+=float(time.time()-tic0)            
                
                #   WRITE MEF FILE (chaintable/metadata)
                
                #   CHAIN CUBE
                tic0=time.time()
                hdr=fits.Header()
                hdr['CTYPE1']='PARAM'
                hdr['CTYPE2']='STEP'
                hdr['CTYPE3']='WALKER'
                hdu1=fits.PrimaryHDU(sampler.chain[:,0:mcpars['step_last'],:],hdr)
                
                #   PARAMETER TABLE
                col1=fits.Column(name='p_keys',array=mcpars['p_keys'],format='A')
                col2=fits.Column(name='p_start',array=mcpars['p_start'],format='D')
                col3=fits.Column(name='p_lo',array=mcpars['p_lo'],format='D')
                col4=fits.Column(name='p_up',array=mcpars['p_up'],format='D')
                col5=fits.Column(name='p_scale',array=mcpars['p_scale'],format='D')
                col6=fits.Column(name='p_format',array=mcpars['p_format'],format='A')
                cols = fits.ColDefs([col1,col2,col3,col4,col5,col6])
                hdu2 = fits.BinTableHDU.from_columns(cols)
                
                #   ACCEPTFRAC
                col1=fits.Column(name='acceptfraction',array=sampler.acceptance_fraction,format='D')
                cols = fits.ColDefs([col1])
                hdu3 = fits.BinTableHDU.from_columns(cols)
                
                #   DUMP OUT
                hdus=fits.HDUList([hdu1,hdu2,hdu3])
                hdus.writeto(mcpars['outfolder']+"/chain_mef.fits",overwrite=True)
                np.save(mcpars['outfolder']+'/mcpars.npy',mcpars)
                
                p_median,p_error1,p_error2=py_tirific_analyze(mcpars['outfolder'],plotsub=None,burnin=int((i+1)/2.0),plotcorner=False)
                
                
                dt+=float(time.time()-tic0)
        
        mcpars['pos_last']=pos_i

    print("Done.")
    print 'Took {0} minutes'.format(float(time.time()-tic)/float(60.))
    

