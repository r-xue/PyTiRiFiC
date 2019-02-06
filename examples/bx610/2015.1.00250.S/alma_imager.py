import shutil as su

def exportimages(imagenames,
                 velocity=False,optical=False,
                 overwrite=True,
                 stokeslast=True,dropstokes=False,
                 dropmask=True,
                 compress=False):
    """
    export tclean products into FITS
    """
    
    ext_list=['pb','pb.tt0',
          'psf','psf.tt0','psf.tt1','psf.tt2',
          'sumwt','sumwt.tt0','sumwt.tt1','sumwt.tt2',
          'residual','residual.tt0','residual.tt1',
          'image','image.tt0','image.tt1',
          'model','model.tt0','model.tt1',
          'mask','alpha','alpha.error']
    
    image_list = [imagenames] if  isinstance(imagenames,str) else imagenames
    
    fits_list=[]
    for ext in ext_list:
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
                start='',width='',nchan=-1,
                deconvolver='mtmfs',specmode='mfs',scales=[0.,5.],
                weighting='briggs',robust=1.0,
                threshold='0.0Jy',usemask='pb',pbmask=0.2,niter=10000,
                runclean=False,runexport=True):
                
                
    """
    A workflow script which helps you make "slightly" better imaging products
    
    note:
        + doesn't require a pipeline CASA version since no calibration is involved

        + def. of tt0/tt1:
            https://casa.nrao.edu/Release3.3.0/docs/UserMan/UserMansu232.html    
    
        + clean vs. tclean: 
            https://casaguides.nrao.edu/index.php/TCLEAN_and_ALMA
    """

    #   only different between im0 and imn
    
    im0=imagename+'.iter0'
    imn=imagename+'.itern'
    imagename_list=[im0,imn]
    niter_list=[0,10000]
    calcrp_list=[True,False]
    
    if  runclean==False:
        npass=1
    else:
        npass=2
    
    ext_list=['pb','pb.tt0',
          'psf','psf.tt0','psf.tt1','psf.tt2',
          'sumwt','sumwt.tt0','sumwt.tt1','sumwt.tt2',
          'residual','residual.tt0','residual.tt1',
          'image','image.tt0','image.tt1',
          'model','model.tt0','model.tt1',
          'mask','alpha','alpha.error']    

    for i in range(npass):
        
        if  imagename_list[i]==im0:
            os.system('rm -rf '+imagename_list[i]+'*')
        
        tclean(vis=vis,
               field=field,
               spw=spw,
               imagename=imagename_list[i],
               imsize=imsize, cell=cell, phasecenter=phasecenter, stokes=stokes,
               specmode=specmode, nchan=nchan, outframe=outframe,
               start=start,width=width,
               gridder='standard', chanchunks=-1, usepointing=False, mosweight=False,
               deconvolver=deconvolver, scales=scales,
               pblimit=pblimit, restoration=True,
               restoringbeam='common', pbcor=False, weighting=weighting, robust=robust,
               niter=niter_list[i], threshold=threshold, interactive=0,
               usemask=usemask,pbmask=pbmask,
               sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5,
               negativethreshold=0.0, minbeamfrac=0.3, growiterations=75,
               dogrowprune=True, minpercentchange=1.0, savemodel='none',
               restart=True, calcres=calcrp_list[i], calcpsf=calcrp_list[i], parallel=False)
        
        
        if  imagename_list[i]==im0:
            for ext in ext_list:
                os.system("rm -rf "+imn+'.'+ext)
                if  os.path.exists(im0+'.'+ext):
                    su.copytree(src=im0+'.'+ext,dst=imn+'.'+ext)

        if  imagename_list[i]==imn:
            os.system('cp -rf summaryplot_1.png '+imn+'.summaryplot.png')
    
    
    if  runexport==True:
        for i in range(npass):
            exportimages(imagename_list[i])
            
    return
    

if  __name__=="__main__":
    
    alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename='bx610.bb1_msc_ro1.mfs',
                spw='0:249.188425~251.0087375GHz',field='BX610',datacolumn='data',
                imsize=[960,960],cell='0.043arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
                start='',width='',nchan=-1,
                deconvolver='mtmfs',specmode='mfs',scales=[0,5],
                weighting='briggs',robust=1.0,
                threshold='6.1230152e-05Jy',usemask='pb',pbmask=0.2,niter=10000,
                runclean=True,runexport=True)
    
    alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename='bx610.bb2_msc_ro1.mfs',
                spw='1:250.79375~251.0828125GHz;251.3953125~251.8875GHz;252.16875~252.6140625GHz',field='BX610',datacolumn='data',
                imsize=[960,960],cell='0.043arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
                start='',width='',nchan=-1,
                deconvolver='mtmfs',specmode='mfs',scales=[0,5],
                weighting='briggs',robust=1.0,
                threshold='6.7647961e-05Jy',usemask='pb',pbmask=0.2,niter=10000,
                runclean=True,runexport=True)
    
    alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename='bx610.bb3_msc_ro1.mfs',
                spw='2:233.2859375~235.10625GHz',field='BX610',datacolumn='data',
                imsize=[960,960],cell='0.043arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
                start='',width='',nchan=-1,
                deconvolver='mtmfs',specmode='mfs',scales=[0,5],
                weighting='briggs',robust=1.0,
                threshold='5.6094865e-05Jy',usemask='pb',pbmask=0.2,niter=10000,
                runclean=True,runexport=True)
    
    alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename='bx610.bb4_msc_ro1.mfs',
                spw='3:234.9859375~236.80625GHz',field='BX610',datacolumn='data',
                imsize=[960,960],cell='0.043arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
                start='',width='',nchan=-1,
                deconvolver='mtmfs',specmode='mfs',scales=[0,5],
                weighting='briggs',robust=1.0,
                threshold='5.1352235e-05Jy',usemask='pb',pbmask=0.2,niter=10000,
                runclean=True,runexport=True)            
