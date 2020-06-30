import shutil as su
from __builtin__ import True


def plotuv_freqtime_amp(vis='',spw=[''],xaxis='freq'):
    """
        vis='calibrated_target.ms',spw
    """
    if  'freq' in xaxis:
        for spw0 in spw:
            plotms(vis,xaxis='freq',yaxis='amp',spw=spw0,
                   plotfile=vis+'.spw'+spw0+'_freq_amp.png',overwrite=True,showgui=False,
                   showatm=True,showtsky=False)
    if  'time' in xaxis:
        for spw0 in spw:
            plotms(vis,xaxis='time',yaxis='amp',spw=spw0,
                   plotfile=vis+'.spw'+spw0+'_time_amp.png',overwrite=True,showgui=False,
                   showatm=False,showtsky=False)

def ext_list():
    
    ext_list=['pb','pb.tt0',
          'psf','psf.tt0','psf.tt1','psf.tt2',
          'sumwt','sumwt.tt0','sumwt.tt1','sumwt.tt2',
          'residual','residual.tt0','residual.tt1',
          'image','image.tt0','image.tt1',
          'model','model.tt0','model.tt1',
          'mask','alpha','alpha.error']
    
    return ext_list    
    

def copyimages(imagename='',
               outname=''):
    
    for ext in ext_list():
        os.system("rm -rf "+outname+'.'+ext)
        if  os.path.exists(imagename+'.'+ext):
            print('copy: '+imagename+'.'+ext+' >> '+outname+'.'+ext)
            su.copytree(src=imagename+'.'+ext,dst=outname+'.'+ext)

def exportimages(imagenames,
                 velocity=False,optical=False,
                 overwrite=True,
                 stokeslast=True,dropstokes=False,
                 dropmask=True,droptable=False,
                 compress=False):
    """
    export tclean products into FITS
    """
    
    image_list = [imagenames] if  isinstance(imagenames,str) else imagenames
    
    fits_list=[]
    for ext in ext_list():
        for fname in [imagenames]:
            if  os.path.exists(fname+'.'+ext):
                if  dropmask==True:
                    if  ('.image' in fname+'.'+ext or '.residual' in fname+'.'+ext) \
                        and os.path.exists(fname+'.'+ext+'/mask0'):
                        makemask(mode='delete',inpimage=fname+'.'+ext,
                                 inpmask=fname+'.'+ext+':mask0')
                exportfits(fitsimage=fname+'.'+ext+'.fits',
                   imagename=fname+'.'+ext,
                   bitpix=-32, maxpix=-1,minpix=0,
                   overwrite=overwrite, velocity=velocity, optical=optical,
                   stokeslast=stokeslast,dropstokes=dropstokes)
                if  droptable==True:
                    os.system("rm -rf "+fname+'.'+ext)
                fits_list+=[fname+'.'+ext+'.fits']
    
    fitsnames=' '.join(fits_list)
    
    if  compress==True:
        
        bin_path=['/opt/local/bin']
        lib_path=['/usr/local/miriad-carma/opt/casa/lib']
        extenv={"PATH":os.pathsep.join(list(set(bin_path))),
                "DYLD_LIBRARY_PATH":os.pathsep.join(list(set(lib_path))),
                "HOME":"~/"}
        cmd='pigz '+fitsnames
        p=subprocess.Popen(cmd,shell=True,env=extenv,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.read()
        print(output)
        
    return 

def alma_imager(vis='',imagename='',
                spw='',field='',datacolumn='data',
                imsize=[540,540],cell='0.2arcsec',phasecenter='',pblimit=-0.10,
                stokes='I',outframe='LSRK',
                start='',width='',nchan=-1,interpolation='linear',
                deconvolver='mtmfs',specmode='mfs',scales=[],
                weighting='briggs',robust=1.0,
                threshold='0.0Jy',niter=10000,nsigma=0.0,
                usemask='pb',pbmask=0.2,mask='',
                reuse=False,
                runexport=True):
                
                
    """
    A workflow script which helps you make "slightly" better imaging products
    
    note:
        + doesn't require a pipeline CASA version since no calibration is involved

        + def. of tt0/tt1:
            https://casa.nrao.edu/Release3.3.0/docs/UserMan/UserMansu232.html    
    
        + clean vs. tclean: 
            https://casaguides.nrao.edu/index.php/TCLEAN_and_ALMA
            
        + reuse:    reuse existing imaging set
    """

    #   only different between im0 and imn

    imagename_list = [imagename] if  not isinstance(imagename,(list,np.ndarray)) else list(imagename)
    niter_list = [niter] if  not isinstance(niter,(list,np.ndarray)) else list(niter)
    nsigma_list = [nsigma] if  not isinstance(nsigma,(list,np.ndarray)) else list(nsigma)
    threshold_list = [threshold] if  not isinstance(threshold,(list,np.ndarray)) else list(threshold)
    reuse_list=[reuse] if not isinstance(reuse,(list,np.ndarray)) else list(reuse)

    if  len(imagename_list)>1 and len(niter_list)==1:
        niter_list=niter_list*len(imagename_list)
    if  len(imagename_list)>1 and len(nsigma_list)==1:
        nsigma_list=nsigma_list*len(imagename_list)        
    if  len(imagename_list)>1 and len(threshold_list)==1:
        threshold_list=threshold_list*len(imagename_list)     
    if  len(imagename_list)>1 and len(reuse_list)==1:
        reuse_list=reuse_list*len(imagename_list)    

    calcrp_list=[False]*len(imagename_list)
    calcrp_list[0]=True

    for i in range(len(imagename_list)):
        
        if  reuse_list[i]==True:
            continue
        
        os.system('rm -rf '+imagename_list[i]+'.*')
        if  calcrp_list[i]==False and i>=1:    
            copyimages(imagename_list[i-1],imagename_list[i])
            os.system('rm -rf '+imagename_list[i]+'.mask')
        
        tclean(vis=vis,
               field=field,spw=spw,datacolumn=datacolumn,
               imagename=imagename_list[i],
               imsize=imsize, cell=cell, phasecenter=phasecenter, stokes=stokes,
               specmode=specmode, nchan=nchan, outframe=outframe,
               start=start,width=width,interpolation=interpolation,
               gridder='standard', chanchunks=-1, usepointing=False, mosweight=False,
               deconvolver=deconvolver, scales=scales,
               pblimit=pblimit, restoration=True,
               restoringbeam='common', pbcor=False, weighting=weighting, robust=robust,
               niter=niter_list[i], threshold=threshold_list[i], nsigma=float(nsigma_list[i]),
               cycleniter=-1, cyclefactor=1.0,
               interactive=0,
               usemask=usemask,pbmask=pbmask,mask=mask,
               sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5,
               negativethreshold=0.0, minbeamfrac=0.3, growiterations=75,
               dogrowprune=True, minpercentchange=1.0, savemodel='none',
               restart=True, calcres=calcrp_list[i], calcpsf=calcrp_list[i], parallel=False)
        os.system('cp -rf tclean.last '+imagename_list[i]+'.tclean.last')
        if  niter_list[i]!=0:
            os.system('cp -rf summaryplot_1.png '+imagename_list[i]+'.summaryplot.png')
        if  runexport==True:
            exportimages(imagename_list[i])
            
    return
    
if  __name__=="__main__":
    
    pass
    
                
