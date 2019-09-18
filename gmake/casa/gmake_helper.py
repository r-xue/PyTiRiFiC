"""
A set of CASA functions intended to help modeling analysis
"""

def ext_list():
    
    ext_list=['pb','pb.tt0',
          'psf','psf.tt0','psf.tt1','psf.tt2',
          'sumwt','sumwt.tt0','sumwt.tt1','sumwt.tt2',
          'residual','residual.tt0','residual.tt1',
          'image','image.tt0','image.tt1',
          'model','model.tt0','model.tt1',
          'mask','alpha','alpha.error']
    
    return ext_list    

def ms2im(vis='',
          imagename='',
          datacolumn='data',
          niter=0,
          specmode='cube',
          cell=1.0,
          imsize=[128,128]):
    """
    generate imaging snapshots of model/data MS.
    """
    
    for ext in ext_list():
        os.system('rm -rf '+imagename+'.'+ext)

    tclean(vis=vis,
           datacolumn=datacolumn,
           imagename=imagename,niter=niter,specmode=specmode,
           interpolation='nearest',
           imsize=imsize, cell=cell)
    
    exportfits(imagename=imagename+'.image',
               fitsimage=imagename+'.fits',
               bitpix=-32, maxpix=-1,minpix=0,
               overwrite=True, velocity=False, optical=False,
               stokeslast=True,dropstokes=False)
    if  'data_' in imagename:
        exportfits(imagename=imagename+'.psf',
               fitsimage=imagename.replace('data_','kernel_')+'.fits',
               bitpix=-32, maxpix=-1,minpix=0,
               overwrite=True, velocity=False, optical=False,
               stokeslast=True,dropstokes=False)    
    
    for ext in ext_list():
        os.system('rm -rf '+imagename+'.'+ext)
        
    return
