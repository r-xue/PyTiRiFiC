execfile('/Users/Rui/Dropbox/Worklib/projects/xlibpy/xlib/amoeba_sa.py')


def gmake_amoeba_setup(inp_dct,dat_dct):
    
    
    opt_dct=inp_dct['optimize']
    
    fit_dct={}
    fit_dct['p_start']=[]
    fit_dct['p_lo']=[]
    fit_dct['p_up']=[]
    fit_dct['p_name']=[]
    fit_dct['p_iscale']=[]
    
    
    for p_name in opt_dct.keys():
        if  '@' not in p_name:
            continue
        fit_dct['p_name']=np.append(fit_dct['p_name'],[p_name])
        fit_dct['p_start']=np.append(fit_dct['p_start'],np.mean(gmake_readpar(inp_dct,p_name)))
        fit_dct['p_lo']=np.append(fit_dct['p_lo'],opt_dct[p_name][0])
        fit_dct['p_up']=np.append(fit_dct['p_up'],opt_dct[p_name][1])
        fit_dct['p_iscale']=np.append(fit_dct['p_iscale'],opt_dct[p_name][2])

    gmake_pformat(fit_dct)    
    
    fit_dct['ndim']=len(fit_dct['p_start'])
    fit_dct['nthreads']=1
    fit_dct['outfolder']=opt_dct['outdir']
    
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

def gmake_amoeba_iterate(fit_dct,inp_dct,dat_dct,nstep=500):
    """
    calling amoeba
    """

    p_amoeba=amoeba_sa(gmake_model_chisq,fit_dct['p_start'],fit_dct['p_iscale'],
                       p_lo=fit_dct['p_lo'],p_up=fit_dct['p_up'],
                       funcargs={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct},
                       maxiter=nstep,temperature=0,verbose=True)

    fit_dct['p_amoeba']=p_amoeba
    
    np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)
    gmake_dct2fits(p_amoeba,outname=fit_dct['outfolder']+'/amoeba_chain')
