
try:
    casa_version=cu.version_string()
except:
    casa_version=None

if  casa_version is not None:

    def ext_list():
        
        ext_list=['pb','pb.tt0',
              'psf','psf.tt0','psf.tt1','psf.tt2',
              'sumwt','sumwt.tt0','sumwt.tt1','sumwt.tt2',
              'residual','residual.tt0','residual.tt1',
              'image','image.tt0','image.tt1',
              'model','model.tt0','model.tt1',
              'mask','alpha','alpha.error']
        
        return ext_list    

    def ms2im(vis,imagename,datacolumn='data',
              cell=0.04,imsize=[128,128]):
        
        
        for ext in ext_list():
            os.system('rm -rf '+imagename+'.'+ext)

        tclean(vis=vis,
               datacolumn=datacolumn,
               imagename=imagename,niter=0,specmode='cube',
               interpolation='nearest',
               imsize=imsize, cell=cell)
        
        exportfits(imagename=imagename+'.image',
                   fitsimage=imagename+'.fits',
                   bitpix=-32, maxpix=-1,minpix=0,
                   overwrite=True, velocity=False, optical=False,
                   stokeslast=True,dropstokes=False)
        
        exportfits(imagename=imagename+'.psf',
                   fitsimage=imagename.replace('data_','kernel_')+'.fits',
                   bitpix=-32, maxpix=-1,minpix=0,
                   overwrite=True, velocity=False, optical=False,
                   stokeslast=True,dropstokes=False)    
        
        for ext in ext_list():
            os.system('rm -rf '+imagename+'.'+ext)
            
        return
    
     
    if  __name__=="__main__":
        
        ms2im(vis,imagename,datacolumn=datacolumn)

    
    #vis='examples/bx610/models/uvb6_ab/p_fits/data_b6_bb2.ms'
    #execfile('/Users/Rui/Dropbox/Worklib/projects/rx-recipe/nrao/alma_imager.py')
    #imagename=vis.replace('.ms','').replace('/data_','/cmodel_')
    #ms2im(vis,imagename,datacolumn='corrected')
    #    
    #imagename=vis.replace('.ms','').replace('/data_','/data_')
    #ms2im(vis,imagename,datacolumn='data')
    
