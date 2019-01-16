
if  __name__=="__main__":
    """
    We can call this otf using the scratch *mef.fits
    #execfile(home+'/Dropbox/Worklib/projects/highz/hxmm01/py_tirific_analyze_run.py')
    """
        
        
    execfile(home+'/Dropbox/Worklib/projects/highz/hzdyn/py_tirific_fun.py')
    execfile(home+'/Dropbox/Worklib/projects/highz/hzdyn/py_tirific_analyze.py')
    
    #   STEP1   check mef.fits

    #"""
    burnin=500
    nrmax=2
    inp_folder='Core.test.emcee'              # use the input data from this folder
    par_folder='Core.test.emcee'     # use the mcmc analysis results (i.e. p_median) from this folder for building models 
    out_folder='Core.test.model'              # dump model here
    p_median,p_error1,p_error2=py_tirific_analyze(inp_folder,plotsub=None,burnin=burnin,plotcorner=True,verbose=True)
    mcpars=np.load(inp_folder+'/mcpars.npy').item()
    for index in range(len(mcpars['p_median'])):
        restore=deepcopy((mcpars['p_median'])[index])
        delta=0.0
        """
        if  index==7:
            delta=50.0
        if  index==11:
            delta=320.0
        if  index==9:
            delta=-20.0
        if  index==10:
            delta=-20.0
        if  index==11:
            delta=+480.0
        """                                            
        (mcpars['p_median'])[index]=(mcpars['p_median'])[index]+delta
        print index,(mcpars['p_keys'])[index],restore,(mcpars['p_median'])[index]
    np.save(out_folder+'/mcpars.npy',mcpars)
    #"""
    
    """
    burnin=3000
    nrmax=6 
    inp_folder='HXMM01S.carbon09exp.emcee'              # use the input data from this folder
    par_folder='../rois/HXMM01S.carbon09exp.emcee'     # use the mcmc analysis results (i.e. p_median) from this folder for building models 
    out_folder='HXMM01S.carbon09exp.model'              # dump model here
    #p_median,p_error1,p_error2=py_tirific_analyze(inp_folder,plotsub=None,burnin=burnin,plotcorner=False,verbose=True)
    
    mcpars=np.load(inp_folder+'/mcpars.npy').item()
    for index in range(len(mcpars['p_median'])):
        restore=deepcopy((mcpars['p_median'])[index])
        delta=0.0        
        if  index==6:
            delta=40.0
        if  index==7:
            delta=20.0
        if  index==8:
            delta=120.0
        if  index==9:
            delta=-20.0                                    
        if  index==10:
            delta=+40.0            
        if  index==36:
            delta=-80.0
        if  index==38:
            delta=80.0
        if  index==40:
            delta=-40.0
        if  index==20:
            delta=+0.02
        if  index==49:
            delta=-0.02            
        if  index==58:
            delta=-0.03            
        (mcpars['p_median'])[index]=(mcpars['p_median'])[index]+delta
        print index,(mcpars['p_keys'])[index],restore,(mcpars['p_median'])[index]
    np.save(out_folder+'/mcpars.npy',mcpars)
    """
    

    
    """
    burnin=750
    nrmax=5 
    inp_folder='HXMM01.co09exp.emcee'              # use the input data from this folder
    par_folder='../roi/HXMM01.co09exp.emcee'     # use the mcmc analysis results (i.e. p_median) from this folder for building models 
    out_folder='HXMM01.co09exp.model'              # dump model here
    p_median,p_error1,p_error2=py_tirific_analyze(inp_folder,plotsub=None,burnin=burnin,plotcorner=False,verbose=True)
    mcpars=np.load(inp_folder+'/mcpars.npy').item()
    np.save(out_folder+'/mcpars.npy',mcpars)
    """
    

    
    """
    nrmax=5 
    inp_folder='HXMM01N.vsbr.emcee'              # use the input data from this folder
    out_folder='HXMM01N.base.model'              # dump model here
    par_folder='../broin/HXMM01N.vsbr.emcee'     # use the mcmc analysis results (i.e. p_median) from this folder for building models    
    """
    
    #"""
    
    #inp_folder='HXMM01N.CICO76. emcee'
    #out_folder='HXMM01N.CICO76.emcee'
    #par_folder='HXMM01N.CICO76.emcee'

    #inp_folder='HXMM01N.all.emcee.v1'
    #out_folder='HXMM01N.all.emcee.v1'
    #par_folder='HXMM01N.all.emcee.v1'
    
    #inp_folder='HXMM01N.all.emcee'
    #out_folder='HXMM01N.all.emcee'
    #par_folder='HXMM01N.all.emcee'    
    
    #inp_folder='HXMM01S.all.mcmc.v1'
    #out_folder='HXMM01S.all.mcmc.v1'
    #par_folder='HXMM01S.all.mcmc.v1'    
     
    #inp_folder='HXMM01S.all.emcee'              # use the input data from this folder
    #out_folder='HXMM01S.all.model'              # dump model here
    #par_folder='../brois/HXMM01S.all.amoeba'     # use the mcmc analysis results (i.e. p_median) from this folder for building models 

     
    
    ##################################

    inty=0
    
    # if a parameter doesn't move much from the starting point, maybe it doesn't affect the X^2 in any way.
    
    tmp=np.load(inp_folder+'/mcpars.npy').item()
    data=np.load(inp_folder+'/data.npy').item()
    imsets=np.load(inp_folder+'/imsets.npy').item()
    disks=np.load(inp_folder+'/disks.npy')
    pick=np.load(par_folder+'/mcpars.npy').item()
    
    tmp=np.load(out_folder+'/mcpars.npy').item()
    data=np.load(inp_folder+'/data.npy').item()
    imsets=np.load(inp_folder+'/imsets.npy').item()
    disks=np.load(inp_folder+'/disks.npy')
    pick=np.load(out_folder+'/mcpars.npy').item()    

    for imlist0 in imsets.keys():
        (imsets[imlist0])['cflux_scale']=1e-7
        
    tmp['outfolder']=out_folder+'/p_start'
    lnl,blobs=tirific_lnlike(pick['p_start'],data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=inty)
    print 'ndata->',blobs['ndata']
    print 'chisq->',blobs['chisq']
    
    tmp['outfolder']=out_folder+'/p_median'
    p_median=deepcopy(pick['p_amoeba']['p_best']) if  fnmatch.fnmatch(par_folder,'*amoeba*') else deepcopy(pick['p_median'])

    lnl,blobs=tirific_lnlike(p_median,data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=inty)
    print 'chisq->',blobs['chisq']

    """
    for i in range(nrmax):
        tmp['outfolder']=out_folder+'/p_median_r'+str(i+2)
        p_median=deepcopy(pick['p_amoeba']['p_best']) if  fnmatch.fnmatch(par_folder,'*amoeba*') else deepcopy(pick['p_median'])
        lnl,blobs=tirific_lnlike(p_median,data,imsets,disks,tmp,uuid=False,verbose=True,keepfile=True,ppp=True,decomp=False,moms=True,maxnur=i+2,inty=inty)
    """
    
    tmp['outfolder']=out_folder+'/p_median_fo'
    p_median=deepcopy(pick['p_amoeba']['p_best']) if  fnmatch.fnmatch(par_folder,'*amoeba*') else deepcopy(pick['p_median'])
    """
    p_keys=deepcopy(tmp['p_keys'])
    for t in range(len(p_keys)):
        if  fnmatch.fnmatch(p_keys[t],'in*'):
            p_median[t]=0.0
    """            
    lnl,blobs=tirific_lnlike(p_median,data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,moms=True,inty=inty,faceon=True)
    tmp['outfolder']=out_folder+'/p_median_fo_na'   
    lnl,blobs=tirific_lnlike(p_median,data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,beam=False,moms=True,inty=inty,faceon=True)
        
    tmp['outfolder']=out_folder+'/p_median_na'
    p_median=deepcopy(pick['p_amoeba']['p_best']) if  fnmatch.fnmatch(par_folder,'*amoeba*') else deepcopy(pick['p_median'])
    lnl,blobs=tirific_lnlike(p_median,data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=True,beam=False,moms=True,inty=inty)
    
    """
    for i in range(nrmax):
        tmp['outfolder']=out_folder+'/p_median_na_r'+str(i+2)
        p_median=deepcopy(pick['p_amoeba']['p_best']) if  fnmatch.fnmatch(par_folder,'*amoeba*') else deepcopy(pick['p_median'])
        lnl,blobs=tirific_lnlike(p_median,data,imsets,disks,tmp,uuid=False,verbose=False,keepfile=True,ppp=True,decomp=False,moms=True,maxnur=i+2,inty=inty)
    """
    
    print ""
    print "take a look:"
    cmd='kvis '
    cmd+=' '+out_folder+'/p_median/*'+'_im.fits'
    cmd+=' '+out_folder+'/p_median/*'+'_sp.fits'
    cmd+=' '+out_folder+'/p_start/*'+'_ppv.fits'
    cmd+=' '+out_folder+'/p_median/*'+'_ppv.fits'
    print cmd

    cmd='gvall '
    cmd+=' '+out_folder+'/p_median/*'+'.ps'
    cmd+=' '+out_folder+'/p_start/*'+'.ps'
    print cmd

