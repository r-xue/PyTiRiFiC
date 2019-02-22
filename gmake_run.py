
execfile('gmake_model_func.py')
execfile('gmake_model.py')
execfile('gmake_utils.py')
execfile('gmake_emcee.py')

if  __name__=="__main__":
    
    #pass
    
    """
    #   build a dict holding input config
    #   build a dict holding data
    #   build the sampler and a dict holding sampler metadata
    inp_dct=gmake_readinp('examples/bx610/bx610xy_dm64_all.inp',verbose=False)
    inp_dct=gmake_readinp('examples/bx610/bx610xy_cm64_all.inp',verbose=False)
    #inp_dct=gmake_readinp('examples/bx610/bx610xy_cm_cont.inp',verbose=False)
    #inp_dct=gmake_readinp('examples/bx610/bx610xy_dm_cont.inp',verbose=False)
    dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
    fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
    gmake_emcee_iterate(sampler,fit_dct,nstep=600)
    """
    
    #"""
    outfolder='bx610xy_cm64_all_emcee'
    
    fit_tab=gmake_emcee_analyze(outfolder,plotsub=None,burnin=400,plotcorner=True,
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
    #"""

