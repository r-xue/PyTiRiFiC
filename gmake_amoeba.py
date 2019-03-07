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
    #fit_dct['nwalkers']=opt_dct['nwalkers']
    fit_dct['outfolder']=opt_dct['outdir']
    
    #print('nwalkers:',fit_dct['nwalkers'])
    #print('nthreads:',fit_dct['nthreads'])
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
                       ftol=1e-10,temperature=0,
                       maxiter=nstep,verbose=True)

    fit_dct['p_amoeba']=p_amoeba
    
    np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)
    gmake_dct2fits(p_amoeba,outname=fit_dct['outfolder']+'/amoeba_chain')

def gmake_amoeba_analyze(outfolder,
                         burnin=50):
    
    t=Table.read(outfolder+'/'+'amoeba_chain.fits')
    
    """
    dict['p_best']=pars[:,np.argmin(chi2)]
    dict['p0']=p0
    dict['niter']=niter
    dict['maxiter']=maxiter
    dict['ftol']=ftol
    dict['chi2']=chi2       # (ndim+1+niter)        chi2 at each simplex vertex
    dict['pars']=pars       # (ndim,ndim+1+niter)   positions of each simplex vertex
    dict['temperature']=temperature
    dict['p_up']=p_up
    dict['p_up']=p_lo
    """
    fit_dct=np.load(outfolder+'/fit_dct.npy').item()
    p_name=fit_dct['p_name']
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    p_start=fit_dct['p_start']
    p_format=fit_dct['p_format']
    
    chi2=t['chi2'].data[0]
    pars=t['pars'].data[0]
    p_best=t['p_best'].data[0]
    
    ndim=(pars.shape)[0]
    niter=(pars.shape)[1]
    
    
    #####################
    
    
    for index  in range(len(p_name)):
        
        print((p_name[index]+" = {0:"+p_format[index]+"}").\
              format( p_best[index]))        
    
    
    
    #   PLOT PARAMETERS
    
    figsize=(8.*2.0,ndim*2.5)
    pl.clf()
    ncol=2
    nrow=int(np.ceil(ndim*1.0/1))
    fig, axes = pl.subplots(nrow,ncol,figsize=figsize,squeeze=True)
    
    for i in range(ndim):
        
        axes[i,0].plot(np.arange(niter),(pars[i,:]).T, color="gray", alpha=0.4)
        ymin, ymax = axes[i,0].get_ylim()
        axes[i,0].set_ylim(ymin, ymax)
        axes[i,0].set_xlim(0, niter)
        axes[i,0].axhline(p_lo[i], color="r", lw=0.8,ls='-')
        axes[i,0].axhline(p_up[i], color="r", lw=0.8,ls='-')
        axes[i,0].axhline(p_start[i],color="b", lw=2,ls='-')
        axes[i,0].set_ylabel(p_name[i])
        axes[i,0].axhline(p_best[i],color="g", lw=3,ls='-')
        
        if  i==ndim-1:
            axes[i,0].set_xlabel("step number")

        #"""
        axes[i,1].plot(np.arange(burnin,niter),pars[i,burnin:].T, color="gray", alpha=0.4)
        ymin, ymax = axes[i,1].get_ylim()
        axes[i,1].set_ylim(ymin, ymax)
        axes[i,1].set_xlim(burnin, niter)
        axes[i,1].axhline(p_lo[i], color="r", lw=0.8,ls='-')
        axes[i,1].axhline(p_up[i], color="r", lw=0.8,ls='-')
        axes[i,1].axhline(p_start[i],color="b", lw=2,ls='-')
        axes[i,1].axhline(p_best[i],color="g", lw=3,ls='-')
        #"""
        
        if  i==ndim-1:
            axes[i,1].set_xlabel("step number")
                
    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/amoeba-iteration.pdf"
    fig.savefig(figname)
    pl.close()       
    
    #   PLOT CHISQ
    
    figsize=(8.*1.0,1.0*2.5)
    fig, axes = pl.subplots(1,2,sharex=False,figsize=figsize,squeeze=False)
    
    axes[0,0].plot(np.arange(niter),chi2)
    axes[0,1].plot(np.arange(burnin,niter),chi2[burnin:])
    
    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/amoeba-iteration-chisq.pdf"
    fig.savefig(figname)
    pl.close()    
    