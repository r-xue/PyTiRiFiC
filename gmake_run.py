
execfile('gmake_model_func.py')
execfile('gmake_model.py')
execfile('gmake_utils.py')
execfile('gmake_emcee.py')
execfile('gmake_amoeba.py')
execfile('gmake_mpfit.py')
execfile('gmake_lmfit.py')
execfile('/Users/Rui/Library/Python/2.7/lib/python/site-packages/mgefit/cap_mpfit.py')

if  __name__=="__main__":
    
    ####################################
    #   EMCEE
    ####################################
    
    """
    #   build a dict holding input config
    #   build a dict holding data
    #   build the sampler and a dict holding sampler metadata
    #inp_dct=gmake_readinp('examples/bx610/bx610xy_dm64_all.inp',verbose=False)
    #inp_dct=gmake_readinp('examples/bx610/bx610xy_cm64_all.inp',verbose=False)
    #inp_dct=gmake_readinp('examples/bx610/bx610xy_band4_cm64_all.inp',verbose=False)
    inp_dct=gmake_readinp('examples/bx610/bx610xy_nas_cm64_all.inp',verbose=False)
    #inp_dct=gmake_readinp('examples/bx610/bx610xy_cm_cont.inp',verbose=False)
    #inp_dct=gmake_readinp('examples/bx610/bx610xy_dm_cont.inp',verbose=False)
    dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
    fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
    gmake_emcee_iterate(sampler,fit_dct,nstep=1000)

    outfolder='bx610xy_nas_cm64_all_emcee'
    fit_tab=gmake_emcee_analyze(outfolder,plotsub=None,burnin=600,plotcorner=True,
                    verbose=True)
    fit_dct=np.load(outfolder+'/fit_dct.npy').item()
    inp_dct=np.load(outfolder+'/inp_dct.npy').item()
    dat_dct=np.load(outfolder+'/dat_dct.npy').item()
    fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
    theta=fit_tab['p_start'].data[0]
    lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_start')
    print('pstart:    ',lnl,blobs)     
    theta=fit_tab['p_median'].data[0]
    lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_median')
    print('p_median: ',lnl,blobs)
    """

    ####################################
    #   AMOEBA
    ####################################
    
    #version='bx610xy_nas_nc_dm128_bb14_amoeba'
    #version='bx610xy_nas_nc_cm128_bb14_amoeba'
    version='bx610xy_nas_nc_cm128mfs_bb14_amoeba'
    
    #version='bx610xy_nas_dm128_bb14_amoeba'
    #version='bx610xy_nas_cm128_bb14_amoeba'
    #version='bx610xy_nas_cm128mfs_bb14_amoeba'
    
    version='bx610xy_nas_dm128_b1234_amoeba'
    version='bx610xy_band4_dm64_b1234_amoeba'
    version='bx610xy_band4_dm128_b1234_amoeba'
        
    #"""
    inp_dct=gmake_readinp('examples/bx610/'+version+'.inp',verbose=False)
    dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
    fit_dct=gmake_amoeba_setup(inp_dct,dat_dct)
    gmake_amoeba_iterate(fit_dct,inp_dct,dat_dct,nstep=500)
    #"""
    outfolder=version
    gmake_amoeba_analyze(outfolder,burnin=350)
    fit_dct=np.load(outfolder+'/fit_dct.npy').item()
    inp_dct=np.load(outfolder+'/inp_dct.npy').item()
    dat_dct=np.load(outfolder+'/dat_dct.npy').item()
    #fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
    theta=fit_dct['p_amoeba']['p0']
    lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_start')
    print('pstart:    ',lnl,blobs)     
    theta=fit_dct['p_amoeba']['p_best']
    lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_best')
    print('p_best: ',lnl,blobs)    
    #"""    

    ####################################
    #   LMFIT
    ####################################
    
    #inp_dct=gmake_readinp('examples/bx610/bx610xy_nas_cm64_all_mpfit.inp',verbose=False)
    #dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
    #fit_dct=gmake_lmfit_setup(inp_dct,dat_dct)
    #gmake_lmfit_iterate(fit_dct,inp_dct,dat_dct,nstep=100)    
    
    