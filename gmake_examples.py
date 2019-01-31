    execfile('gmake_utils.py')
    objs=gmake_readpars('examples/bx610/bx610xy.inp',verbose=False)
    gmake_listpars(objs)
    
    inc_list=np.arange(20.,80.,10.)
    for inc in inc_list:
        objs['co76']['inc']=inc
        objs=gmake_fillpars(objs)
        models=gmake_kinmspy_api(objs,outname='testexample',verbose=False)
        ext='_'+str(int(inc))
        fits.writeto('model'+ext+'.fits',
                 models['model@examples/bx610/bx610_spw27.fits'],
                 models['header@examples/bx610/bx610_spw27.fits'],
                 overwrite=True)
        fits.writeto('co76'+ext+'_model.fits',
                 models['co76@examples/bx610/bx610_spw27.fits'],
                 models['header@examples/bx610/bx610_spw27.fits'],
                 overwrite=True)
        fits.writeto('ci21'+ext+'_model.fits',
                 models['ci21@examples/bx610/bx610_spw27.fits'],
                 models['header@examples/bx610/bx610_spw27.fits'],
                 overwrite=True)
        fits.writeto('data.fits',
                 models['data@examples/bx610/bx610_spw27.fits'],
                 models['header@examples/bx610/bx610_spw27.fits'],
                 overwrite=True) 
    
    #print(">"*80)
    #gmake_listpars(objs)
    #print("<"*80)
    
    tic=time.time()
    
    
    
    
            
    print(models.keys())
    print('Took {0} seconds to execute KinMSpy'.format(float(time.time()-tic)/float(1)))
          