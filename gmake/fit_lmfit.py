from .gmake_init import *
from .model_utils import * 

def lmfit_setup(inp_dct,dat_dct):
    
    
    opt_dct=inp_dct['optimize']
    
    fit_dct={'optimize':opt_dct.copy()}
    fit_dct['p_start']=[]
    fit_dct['p_lo']=[]
    fit_dct['p_up']=[]
    fit_dct['p_name']=[]
    fit_dct['p_scale']=[]
    fit_dct['p_rscale']=[]
    
    for p_name in opt_dct.keys():
        if  '@' not in p_name:
            continue
        fit_dct['p_name']=np.append(fit_dct['p_name'],[p_name])
        fit_dct['p_start']=np.append(fit_dct['p_start'],np.mean(read_par(inp_dct,p_name)))
        
        if  opt_dct[p_name][0]=='a' or opt_dct[p_name][0]=='r' or opt_dct[p_name][0]=='o': 
            si=1 ; mode=deepcopy(opt_dct[p_name][0])
        else:
            si=0 ; mode='a'
        fit_dct['p_lo']=np.append(fit_dct['p_lo'],
                                  gmake_read_range(center=fit_dct['p_start'][-1],
                                                   delta=opt_dct[p_name][si+0],
                                                   mode=mode))
        fit_dct['p_up']=np.append(fit_dct['p_up'],
                                  gmake_read_range(center=fit_dct['p_start'][-1],
                                                   delta=opt_dct[p_name][si+1],
                                                   mode=mode))                                  
        fit_dct['p_scale']=np.append(fit_dct['p_scale'],
                                  gmake_read_range(center=fit_dct['p_start'][-1],
                                                   delta=opt_dct[p_name][si+2],
                                                   mode=mode))        
        fit_dct['p_rscale']=np.append(fit_dct['p_rscale'],
                                  gmake_read_range(center=fit_dct['p_start'][-1],
                                                   delta=opt_dct[p_name][si+3],
                                                   mode=mode))           
        
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
        parinfo[i]['step']=fit_dct['p_scale'][i]
        parinfo[i]['relstep']=fit_dct['p_rscale'][i]
        parinfo[i]['limits']=[fit_dct['p_lo'][i],fit_dct['p_up'][i]]
        params.add('p_'+str(i+1),
                   value=fit_dct['p_start'][i],
                   vary=True,
                   min=fit_dct['p_lo'][i],
                   max=fit_dct['p_up'][i],
                   brute_step=fit_dct['p_rscale'][i])
                   
        

    gmake_pformat(fit_dct)    
    
    fit_dct['ndim']=len(fit_dct['p_start'])
    fit_dct['nthreads']=1
    fit_dct['outfolder']=opt_dct['outdir']
    fit_dct['p_mpfit_info']=parinfo
    fit_dct['p_lmfit_params']=params
    
    if  not os.path.exists(fit_dct['outfolder']):
        os.makedirs(fit_dct['outfolder'])

    
    fit_dct['ndim']=len(fit_dct['p_start'])
    #   turn off mutiple-processing since mkl_fft has been threaded.
    fit_dct['nthreads']=1   #multiprocessing.cpu_count()
    #fit_dct['nwalkers']=opt_dct['nwalkers']
    fit_dct['outfolder']=opt_dct['outdir']
    
    #print('nwalkers:',fit_dct['nwalkers'])
    print('nthreads:',fit_dct['nthreads'])
    print('ndim:    ',fit_dct['ndim'])
    print('outdir:  ',fit_dct['outfolder'])
    
    #np.save(fit_dct['outfolder']+'/dat_dct.npy',dat_dct)
    np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)   #   fitting metadata
    #np.save(fit_dct['outfolder']+'/inp_dct.npy',inp_dct)   #   input metadata    
    
    return fit_dct

def lmfit_iterate(fit_dct,inp_dct,dat_dct,nstep=500):
    """
    call iteration
    """

    """
    pprint.pprint(fit_dct['p_info'])
    p_mpfit=mpfit(gmake_model_wdev,fit_dct['p_start'],
                  parinfo=fit_dct['p_info'],
                  gtol=1e-10,xtol=1e-10,ftol=1e-10,damp=0.0,
                  functkw={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct},
                  maxiter=nstep)
    print(fit_dct['p_start'])
    print(p_mpfit)
    """

    
    ndim=len(fit_dct['p_name'])
    blobs={'pars':[],            # matching amoeba_sa.py (ndim+1+niter)
           'chi2':[]}
    
    lmfit_method=((fit_dct['method']).split("-"))[1]
    print(lmfit_method)
    
    if  lmfit_method=='nelder':
        result=minimize(gmake_model_lmfit_wdev,fit_dct['p_lmfit_params'],
                        kws={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct,'blobs':blobs},
                        calc_covar=True,
                        tol=1e-10,
                        method='nelder',
                        options={'maxiter':nstep,
                                'disp':True})
    if  lmfit_method=='brute':
        result=minimize(gmake_model_lmfit_wdev,fit_dct['p_lmfit_params'],
                        kws={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct,'blobs':blobs},
                        method='brute')
                
    fit_dct['p_lmfit_result']=result
    report_fit(fit_dct['p_lmfit_result'])

    blobs['chi2']=np.array(blobs['chi2'])       # (ndim)
    blobs['pars']=np.array(blobs['pars'])       # (ieval,ndim)
    fit_dct['p_lmfit_blobs']=blobs

    np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)

    return 

def lmfit_analyze_brute(outfolder):
    fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
    
    # min position
    # result.brute_x0
    
    # min value
    # result.brute_fval
    
    # fval grid
    # result.brute_Jout
    
    # p1_grid= np.unique(result.brute_grid[0].ravel())
    # p2_grid= np.unique(result.brute_grid[1].ravel())
    
    #grid_x, grid_y = [np.unique(par.ravel()) for par in result.brute_grid]
    #print(grid_x.shape)
    
    result=fit_dct['p_lmfit_result']

    ndim=result.brute_x0.size
    bt_grid=result.brute_grid
    if  ndim==1:
        bt_grid=result.brute_grid[np.newaxis]
        bt_x0=result.brute_x0[np.newaxis]
        
    else:
        bt_grid=result.brute_grid
        bt_x0=result.brute_x0
    
    
    figsize=(4.*2.0,ndim*2.5)
    pl.clf()
    ncol=2
    nrow=int(np.ceil(ndim*1.0/1))
    fig, axes = pl.subplots(nrow,ncol,figsize=figsize,squeeze=True)
    if  ndim==1:
        axes=axes[np.newaxis,:]
    print(result.brute_Jout.shape)
    print(result.brute_grid.shape)

    
    for i in range(ndim):

        pchain=(bt_grid[i,:]).ravel()
        axes[i,0].plot(np.arange(1,pchain.size+1),pchain, color="gray", alpha=0.4)
        axes[i,0].set_ylabel(fit_dct['p_name'][i])               
                       
        axes[i,1].plot(pchain,
                     result.brute_Jout.ravel(),
                     'o', color="gray", alpha=0.4)
        axes[i,1].axvline(bt_x0[i], ls='-', color='g',lw=3)
        axes[i,1].set_xlabel(fit_dct['p_name'][i]) 
        
        if  i==ndim-1:
            axes[i,0].set_xlabel('feval_grid_index') 
            
    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/brute-iteration.pdf"
    fig.savefig(figname)
    pl.close()     
            

    



    if  ndim!=2:
        
        return

    best_vals=True
    varlabels=None
    output=outfolder+"/brute-corner.pdf"
    
    npars = len(result.var_names)
    fig, axes = plt.subplots(npars, npars)

    if not varlabels:
        varlabels = result.var_names
    if best_vals and isinstance(best_vals, bool):
        best_vals = result.params

    for i, par1 in enumerate(result.var_names):
        for j, par2 in enumerate(result.var_names):

            # parameter vs chi2 in case of only one parameter
            if npars == 1:
                axes.plot(result.brute_grid, result.brute_Jout, 'o', ms=3)
                axes.set_ylabel(r'$\chi^{2}$')
                axes.set_xlabel(varlabels[i])
                if best_vals:
                    axes.axvline(best_vals[par1].value, ls='dashed', color='r')

            # parameter vs chi2 profile on top
            elif i == j and j < npars-1:
                if i == 0:
                    axes[0, 0].axis('off')
                ax = axes[i, j+1]
                red_axis = tuple([a for a in range(npars) if a != i])
                ax.plot(np.unique(result.brute_grid[i]),
                        np.minimum.reduce(result.brute_Jout, axis=red_axis),
                        'o', ms=3)
                ax.set_ylabel(r'$\chi^{2}$')
                ax.yaxis.set_label_position("right")
                ax.yaxis.set_ticks_position('right')
                ax.set_xticks([])
                if best_vals:
                    ax.axvline(best_vals[par1].value, ls='dashed', color='r')

            # parameter vs chi2 profile on the left
            elif j == 0 and i > 0:
                ax = axes[i, j]
                red_axis = tuple([a for a in range(npars) if a != i])
                ax.plot(np.minimum.reduce(result.brute_Jout, axis=red_axis),
                        np.unique(result.brute_grid[i]), 'o', ms=3)
                ax.invert_xaxis()
                ax.set_ylabel(varlabels[i])
                if i != npars-1:
                    ax.set_xticks([])
                elif i == npars-1:
                    ax.set_xlabel(r'$\chi^{2}$')
                if best_vals:
                    ax.axhline(best_vals[par1].value, ls='dashed', color='r')

            # contour plots for all combinations of two parameters
            elif j > i:
                ax = axes[j, i+1]
                red_axis = tuple([a for a in range(npars) if a != i and a != j])
                X, Y = np.meshgrid(np.unique(result.brute_grid[i]),
                                   np.unique(result.brute_grid[j]))
                lvls1 = np.linspace(result.brute_Jout.min(),
                                    np.median(result.brute_Jout)/2.0, 7, dtype='int')
                lvls2 = np.linspace(np.median(result.brute_Jout)/2.0,
                                    np.median(result.brute_Jout), 3, dtype='int')
                lvls = np.unique(np.concatenate((lvls1, lvls2)))
                ax.contourf(X.T, Y.T, np.minimum.reduce(result.brute_Jout, axis=red_axis),
                            lvls, norm=LogNorm())
                ax.set_yticks([])
                if best_vals:
                    ax.axvline(best_vals[par1].value, ls='dashed', color='r')
                    ax.axhline(best_vals[par2].value, ls='dashed', color='r')
                    ax.plot(best_vals[par1].value, best_vals[par2].value, 'rs', ms=3)
                if j != npars-1:
                    ax.set_xticks([])
                elif j == npars-1:
                    ax.set_xlabel(varlabels[i])
                if j - i >= 2:
                    axes[i, j].axis('off')
                    
    if output is not None:
        plt.savefig(output)    
    

    return

def lmfit_analyze_nelder(outfolder,
                        burnin=None):
    
    
    fit_dct=np.load(outfolder+'/fit_dct.npy',allow_pickle=True).item()
    p_name=fit_dct['p_name']
    p_lo=fit_dct['p_lo']
    p_up=fit_dct['p_up']
    p_start=fit_dct['p_start']
    p_format=fit_dct['p_format']
    p_format_prec=fit_dct['p_format_prec']
    
    chi2=fit_dct['p_lmfit_blobs']['chi2']
    pars=fit_dct['p_lmfit_blobs']['pars'].T
    p_best=np.array(list(fit_dct['p_lmfit_result'].params.valuesdict().values()))
    
    ndim=(pars.shape)[0]
    niter=(pars.shape)[1]
    if  burnin is None:
        burnin=int(niter*0.8)
    
    #   print out parameter shifting
    
    logging.debug("+"*80)
    maxlen=len(max(fit_dct['p_name'],key=len))
    for ind  in range(len(p_name)):
        textout=' {:{align}{width}} '.format(ind,align='<',width=2)
        textout+=' {:{align}{width}} '.format(p_name[ind],align='<',width=maxlen)
        textout+=' = {:{align}{width}{prec}} '.format(p_best[ind],align='^',width=13,prec=p_format_prec[ind])
        textout+=' <- {:{align}{width}{prec}} '.format(p_start[ind],align='^',width=13,prec=p_format_prec[ind])
        textout+=' ( {:{align}{width}{prec}}, '.format(p_lo[ind],align='^',width=13,prec=p_format_prec[ind])
        textout+=' {:{align}{width}{prec}} )'.format(p_up[ind],align='^',width=13,prec=p_format_prec[ind])
        logging.debug(textout)    
    logging.debug("-"*80)    
    
    
    #   PLOT PARAMETERS
    
    figsize=(8.*2.0,ndim*2.5)
    pl.clf()
    ncol=3
    nrow=int(np.ceil(ndim*1.0/1))
    fig, axes = pl.subplots(nrow+1,ncol,figsize=figsize,squeeze=True)
    
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

        ymin=np.nanmin(chi2[burnin:])
        ymax=np.nanmax(chi2[burnin:])
        axes[i,2].set_ylim(ymin, ymax)
        
        pick_ind=np.where(np.logical_and(chi2 < ymax,chi2 > ymin))
        axes[i,2].plot(pars[i,pick_ind].T,chi2[pick_ind],'o',color="gray", alpha=0.4,)


    axes[i+1,0].plot(np.arange(niter),chi2)
    axes[i+1,1].plot(np.arange(burnin,niter),chi2[burnin:])
    fig.delaxes(axes[i+1,2])
    axes[i+1,0].set_ylabel('Goodness Scale')
                
    fig.tight_layout(h_pad=0.0)
    figname=outfolder+"/iteration.pdf"
    fig.savefig(figname)
    pl.close()       
    
    #   PLOT CHISQ
    
#     figsize=(8.*1.0,1.0*2.5)
#     fig, axes = pl.subplots(1,2,sharex=False,figsize=figsize,squeeze=False)
#     
#     axes[0,0].plot(np.arange(niter),chi2)
#     axes[0,1].plot(np.arange(burnin,niter),chi2[burnin:])
#     
#     fig.tight_layout(h_pad=0.0)
#     figname=outfolder+"/lmfit-iteration-chisq.pdf"
#     fig.savefig(figname)
#     pl.close()    
    
    
