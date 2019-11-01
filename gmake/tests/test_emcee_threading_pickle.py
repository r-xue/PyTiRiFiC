    tic1=time.time()
    sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                model_lnprob,backend=backend,blobs_dtype=dtype,
                                args=(fit_dct,builtins.inp_dct,builtins.dat_dct),
                                runtime_sortingfn=sort_on_runtime)
    sampler.run_mcmc(fit_dct['pos_last'],fit_dct['nstep'],progress=True)        
    logger.debug('nth=0,Took {0} minutes'.format(float(time.time()-tic1)/float(60.)))    

    tic1=time.time()
    with Pool(processes=1) as pool:
        #   use model_lnprob_globe without the keyword dat_dct to avoid redundant data pickling  
        sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                    model_lnprob_globe,backend=backend,blobs_dtype=dtype,
                                    args=(fit_dct,builtins.inp_dct),
                                    runtime_sortingfn=sort_on_runtime,pool=pool)    
        #sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
        #                            model_lnprob,backend=backend,blobs_dtype=dtype,
        #                            args=(fit_dct,builtins.inp_dct,builtins.dat_dct),
        #                            runtime_sortingfn=sort_on_runtime,pool=pool)
        sampler.run_mcmc(fit_dct['pos_last'],fit_dct['nstep'],progress=True)
    logger.debug('nth=1,Took {0} minutes'.format(float(time.time()-tic1)/float(60.)))    
    
    
    tic1=time.time()
    with Pool(processes=8) as pool:
        #   use model_lnprob_globe without the keyword dat_dct to avoid redundant data pickling  
        sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
                                    model_lnprob_globe,backend=backend,blobs_dtype=dtype,
                                    args=(fit_dct,builtins.inp_dct),
                                    runtime_sortingfn=sort_on_runtime,pool=pool)    
        #sampler = emcee.EnsembleSampler(fit_dct['nwalkers'],fit_dct['ndim'],
        #                            model_lnprob,backend=backend,blobs_dtype=dtype,
        #                            args=(fit_dct,builtins.inp_dct,builtins.dat_dct),
        #                            runtime_sortingfn=sort_on_runtime,pool=pool)
        sampler.run_mcmc(fit_dct['pos_last'],fit_dct['nstep'],progress=True)
    logger.debug('nth=1,Took {0} minutes'.format(float(time.time()-tic1)/float(60.)))   
    
    

    **********exe read_inp()**************
hostname: hyperion; 8 CPU cores
emcee threading: 8
OpenMP threading: 1
100%10/10 [00:03<00:00,  2.53it/s]
nth=0,Took 0.0753490169843038 minutes
100%10/10 [00:04<00:00,  2.58it/s]
nth=1,Took 0.08026969830195109 minutes
100%10/10 [00:01<00:00,  9.15it/s]
nth=1,Took 0.020972315470377603 minutes
Done.
Took 0.17820310195287067 minutes