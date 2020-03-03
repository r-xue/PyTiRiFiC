

# if casa run casa lines
# if python run python lines

dir='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/bx610/models/uvb6_ab/p_fits/'
os.system('rm -rf chmap/bx610.model.*')
tclean(vis=dir+'data_b6_bb2.ms',imagename='chmap/bx610.model',specmode='cube',niter=0,
       datacolumn='corrected',
       imsize=128,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300')

os.system('rm -rf chmap/bx610.data.*')
tclean(vis=dir+'data_b6_bb2.ms',imagename='chmap/bx610.data',specmode='cube',niter=0,
       datacolumn='data',
       imsize=128,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300')


exportfits(fitsimage='bx610.model.fits',
           imagename='chmap/bx610.model.image',
           bitpix=-32, maxpix=-1,minpix=0,
           overwrite=True, velocity=False, optical=False,
           stokeslast=True,dropstokes=False)

exportfits(fitsimage='bx610.data.fits',
           imagename='chmap/bx610.data.image',
           bitpix=-32, maxpix=-1,minpix=0,
           overwrite=True, velocity=False, optical=False,
           stokeslast=True,dropstokes=False)