

def gmake_lmfit_setup(inp_dct,dat_dct):
    
    
    opt_dct=inp_dct['optimize']
    
    fit_dct={}
    fit_dct['p_start']=[]
    fit_dct['p_lo']=[]
    fit_dct['p_up']=[]
    fit_dct['p_name']=[]
    fit_dct['p_iscale']=[]
    fit_dct['p_rscale']=[]
    
    for p_name in opt_dct.keys():
        if  '@' not in p_name:
            continue
        fit_dct['p_name']=np.append(fit_dct['p_name'],[p_name])
        fit_dct['p_start']=np.append(fit_dct['p_start'],np.mean(gmake_readpar(inp_dct,p_name)))
        fit_dct['p_lo']=np.append(fit_dct['p_lo'],opt_dct[p_name][0])
        fit_dct['p_up']=np.append(fit_dct['p_up'],opt_dct[p_name][1])
        fit_dct['p_iscale']=np.append(fit_dct['p_iscale'],opt_dct[p_name][2])
        fit_dct['p_rscale']=np.append(fit_dct['p_rscale'],opt_dct[p_name][3])
        
    parinfo = [{'value':0.,
                'fixed':0,
                'limited':[0,0],
                'limits':[0.,0.],
                'parname':'',
                'step':0,
                'relstep':0,
                'mpside':0,
                'mpmaxstep':0,
                'mpminstep':0,
                } for i in range(len(fit_dct['p_name']))]
    
    params=Parameters()
    for i in range(len(fit_dct['p_name'])):
        parinfo[i]['parname']=fit_dct['p_name'][i]
        parinfo[i]['limited']=[1,1]
        parinfo[i]['value']=fit_dct['p_start'][i]
        parinfo[i]['step']=fit_dct['p_iscale'][i]
        parinfo[i]['relstep']=fit_dct['p_rscale'][i]
        parinfo[i]['limits']=[fit_dct['p_lo'][i],fit_dct['p_up'][i]]
        params.add(fit_dct['p_name'][i].replace('@','_at_'),
                   value=fit_dct['p_start'][i],
                   vary=True,
                   min=fit_dct['p_lo'][i],
                   max=fit_dct['p_up'][i])
        

    gmake_pformat(fit_dct)    
    
    fit_dct['ndim']=len(fit_dct['p_start'])
    fit_dct['nthreads']=1
    fit_dct['outfolder']=opt_dct['outdir']
    fit_dct['p_info']=parinfo
    fit_dct['p_lmfit_params']=params
    
    if  not os.path.exists(fit_dct['outfolder']):
        os.makedirs(fit_dct['outfolder'])

    
    fit_dct['ndim']=len(fit_dct['p_start'])
    #   turn off mutiple-processing since mkl_fft has been threaded.
    fit_dct['nthreads']=1   #multiprocessing.cpu_count()
    fit_dct['nwalkers']=opt_dct['nwalkers']
    fit_dct['outfolder']=opt_dct['outdir']
    
    print('nwalkers:',fit_dct['nwalkers'])
    print('nthreads:',fit_dct['nthreads'])
    print('ndim:    ',fit_dct['ndim'])    
    
    np.save(fit_dct['outfolder']+'/dat_dct.npy',dat_dct)
    np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)   #   fitting metadata
    np.save(fit_dct['outfolder']+'/inp_dct.npy',inp_dct)   #   input metadata    
    
    return fit_dct

def gmake_lmfit_iterate(fit_dct,inp_dct,dat_dct,nstep=500):
    """
    calling amoeba
    """

#     pprint.pprint(fit_dct['p_info'])
#     p_mpfit=mpfit(gmake_model_wdev,fit_dct['p_start'],
#                   parinfo=fit_dct['p_info'],
#                   gtol=1e-10,xtol=1e-10,ftol=1e-10,damp=0.0,
#                   functkw={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct},
#                   maxiter=nstep)
#     print(fit_dct['p_start'])
#     print(p_mpfit)

    #"""
    out = minimize(gmake_model_lmfit_wdev,fit_dct['p_lmfit_params'],
                   kws={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct},calc_covar=True,
                   #method='leastsq'
                   method='nelder',options={'maxiter':10,'disp':True})
    pprint.pprint(out)
    #fit_dct['p_m']=p_mpfit
    
    #np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)
    #gmake_dct2fits(p_amoeba,outname=fit_dct['outfolder']+'/mpfit_chain')
    #"""
