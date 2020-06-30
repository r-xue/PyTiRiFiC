import os

import numpy as np
import re
import subprocess
import shutil as su

#   identify the instance context

try:
    casa_version=cu.version_string()
except:
    casa_version='casa6beta'
    
#   import tasks/toolkits into the same namespace identical to the CASA standalone package.

if  casa_version=='casa6beta':
    #import casatasks as ctasks
    #import casatools as ctools
    from casatasks import tclean
    from casatasks import exportfits
    from casatools import table as tb
    
def ext_list():
    """
    tclean output file extenstion list
    """
    ext_list=['pb','pb.tt0',
          'psf','psf.tt0','psf.tt1','psf.tt2',
          'sumwt','sumwt.tt0','sumwt.tt1','sumwt.tt2',
          'residual','residual.tt0','residual.tt1',
          'image','image.tt0','image.tt1',
          'model','model.tt0','model.tt1',
          'mask','alpha','alpha.error']
    
    return ext_list    

def invert(vis='',imagename='',
           datacolumn='data',antenna='',
           weighting='briggs',robust=1.0,npixels=0,
           cell=0.04,imsize=[128,128],phasecenter='',
           specmode='cube',start=0,width=1,nchan=-1,perchanweightdensity=True,
           restoringbeam='',onlydm=True,pbmask=0,pblimit=0):
    """
    Generate a compact dirty image from a MS dataset as a quick imaging snapshot;
    
    Note about the default setting:
    
    +   restoringbeam='' to preserve the original dirty beam shape:
        if "common" then additional undesired convolution will happen
    +   Another faster way to do this would be using the toolkits:
        imager.open('3C273XC1.MS')  
        imager.defineimage(nx=256, ny=256, cellx='0.7arcsec', celly='0.7arcsec')  
        imager.image(type='corrected', image='3C273XC1.dirty')  
        imager.close()
        But it may be difficult to write a function to cover all setting already in casatasks.tclean() 
 
    """
    for ext in ext_list():
        os.system('rm -rf '+imagename+'.'+ext)


    tclean(vis=vis,imagename=imagename,
           datacolumn=datacolumn,antenna=antenna,
           niter=0,
           weighting=weighting, robust=robust,npixels=npixels,
           specmode=specmode,start=start,width=width,nchan=nchan,perchanweightdensity=perchanweightdensity,
           interpolation='nearest',restoringbeam=restoringbeam,deconvolver='hogbom',
           imsize=imsize, cell=cell, phasecenter=phasecenter,pbmask=pbmask,pblimit=pblimit)

    if  onlydm==True:
        exportfits(imagename=imagename+'.image',
               fitsimage=imagename+'.fits',
               bitpix=-32, maxpix=-1,minpix=0,
               overwrite=True, velocity=False, optical=False,
               stokeslast=True,dropstokes=False)
        for ext in ext_list():
            os.system('rm -rf '+imagename+'.'+ext)        
    else:
        exportimages(imagename,droptable=True)
        
    return

def copyimages(imagename='',
               outname=''):
    """
    copy a imaging product set
    if imagename==outname, it will do nothing
    """
    for ext in ext_list():
        if  imagename==outname:
            continue
        os.system("rm -rf "+outname+'.'+ext)
        if  os.path.exists(imagename+'.'+ext):
            print('copy: '+imagename+'.'+ext+' >> '+outname+'.'+ext)
            su.copytree(src=imagename+'.'+ext,dst=outname+'.'+ext)

def exportimages(imagenames,
                 velocity=False,optical=False,
                 overwrite=True,
                 stokeslast=True,dropstokes=False,
                 dropmask=False,droptable=False,
                 compress=False):
    """
    a wrap function to export tclean products into FITS
    """
    
    image_list = [imagenames] if  isinstance(imagenames,str) else imagenames
    
    fits_list=[]
    for ext in ext_list():
        for fname in image_list:
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
    
    # not implemented yet
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

def xclean(vis='',imagename='',
           spw='',field='',datacolumn='data',
           imsize=[128,128],cell='0.04arcsec',
           phasecenter='',pblimit=-0.10,
           stokes='I',outframe='LSRK',
           start='',width='',nchan=-1,interpolation='linear',perchanweightdensity=True,
           deconvolver='mtmfs',specmode='mfs',scales=[],
           weighting='briggs',robust=1.0,
           threshold='0.0Jy',niter=10000,nsigma=0.0,restoringbeam='',
           usemask='pb',pbmask=0.2,mask='',
           uselast=False,runexport=True):
                
                
    """
    A imaging/clean workflow function which wrap around tclean/exports,
    helping you make customized better imaging products
    
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
    uselast_list=[uselast] if not isinstance(uselast,(list,np.ndarray)) else list(uselast)
    
    nclean=len(imagename_list)
    if  nclean>1 and len(niter_list)==1:
        niter_list=niter_list*nclean
    if  nclean>1 and len(nsigma_list)==1:
        nsigma_list=nsigma_list*nclean
    if  nclean>1 and len(threshold_list)==1:
        threshold_list=threshold_list*nclean
    if  nclean>1 and len(uselast_list)==1:
        uselast_list=uselast_list*nclean                     

    for i in range(len(imagename_list)):
        
        if  uselast[i]==True:
            #   use the last imagename space in the list;
            #   or just use the current one (assume it exists) 
            if  i>=1:    
                copyimages(imagename_list[i-1],imagename_list[i])
            os.system('rm -rf '+imagename_list[i]+'.mask')
            calcrp=False
        else:
            #   clean up the current imagename space
            #   ready for a start-from-scratch clean
            for ext in ext_list():
                os.system('rm -rf '+imagename_list[i]+'.'+ext)            
            calcrp=True
            
        tclean(vis=vis,
               field=field,spw=spw,datacolumn=datacolumn,
               imagename=imagename_list[i],
               imsize=imsize, cell=cell, phasecenter=phasecenter, stokes=stokes,
               specmode=specmode, nchan=nchan, outframe=outframe,
               start=start,width=width,interpolation=interpolation,perchanweightdensity=perchanweightdensity,
               gridder='standard', chanchunks=-1, usepointing=False, mosweight=False,
               deconvolver=deconvolver, scales=scales,
               pblimit=pblimit, restoration=True,
               restoringbeam=restoringbeam, pbcor=False, weighting=weighting, robust=robust,
               niter=niter_list[i], threshold=threshold_list[i], nsigma=float(nsigma_list[i]),
               cycleniter=-1, cyclefactor=1.0,
               interactive=0,
               usemask=usemask,pbmask=pbmask,mask=mask,
               sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5,
               negativethreshold=0.0, minbeamfrac=0.3, growiterations=75,
               dogrowprune=True, minpercentchange=1.0, savemodel='none',
               restart=True, calcres=calcrp, calcpsf=calcrp, parallel=False)
        
        os.system('cp -rf tclean.last '+imagename_list[i]+'.tclean.last')
        
        if  niter_list[i]!=0:
            os.system('cp -rf summaryplot_1.png '+imagename_list[i]+'.summaryplot.png')
        if  runexport==True:
            exportimages(imagename_list[i],droptable=True)
            
    return
    
if  __name__=="__main__":
    
    pass