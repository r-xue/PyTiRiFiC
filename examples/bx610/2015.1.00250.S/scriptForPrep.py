"""
os.system("rm -rf uid___A002_Xb638bc_X2aa8_target.ms")
mstransform(outputvis='uid___A002_Xb638bc_X2aa8_target.ms',
            vis='uid___A002_Xb638bc_X2aa8.ms.split.cal', datacolumn='data',
            reindex=False, spw='', field='BX610',
            intent='OBSERVE_TARGET#ON_SOURCE')

os.system("rm -rf uid___A002_Xb64387_X1f95_target.ms")
mstransform(outputvis='uid___A002_Xb64387_X1f95_target.ms',
            vis='uid___A002_Xb64387_X1f95.ms.split.cal', datacolumn='data',
            reindex=False, spw='', field='BX610',
            intent='OBSERVE_TARGET#ON_SOURCE')
"""

#os.system('rm -rf uid___A001_X2fe_X20f_target.ms')
#concat(vis=['uid___A002_Xb638bc_X2aa8_target.ms','uid___A002_Xb64387_X1f95_target.ms'],concatvis='uid___A001_X2fe_X20f_target.ms')

"""
listobs('uid___A001_X2fe_X20f_target.ms')
os.system('rm -rf uid___A001_X2fe_X20f_target.spw27.cube.I.iter0.*')
tclean(phasecenter='ICRS 23:46:09.4400 +012.49.19.300',
       vis='uid___A001_X2fe_X20f_target.ms',
       imagename='uid___A001_X2fe_X20f_target.spw27.cube.I.iter0',
       threshold='0.0mJy', imsize=[960, 960], start='250.752890409GHz',
       npixels=0, cell=['0.043arcsec'], width='7.81215322296MHz',
       outframe='LSRK', gridder='standard', niter=0, datacolumn='data',
       savemodel='none', restoration=False, intent='OBSERVE_TARGET#ON_SOURCE',
       robust=0.5, usemask='user', parallel=False, stokes='I', nchan=238,
       deconvolver='hogbom', weighting='briggs', pbcor=False, pblimit=0.2,
       restoringbeam='common', specmode='cube', chanchunks=-1, interactive=0)
exportfits(dropstokes=False, minpix=0,
           fitsimage='uid___A001_X2fe_X20f_target.spw27.cube.I.iter0.residual.fits',
           imagename='uid___A001_X2fe_X20f_target.spw27.cube.I.iter0.residual',
           overwrite=True, bitpix=-32, maxpix=-1, velocity=False, optical=False,
           stokeslast=True)
"""

"""
tclean(phasecenter='ICRS 23:46:09.4400 +012.49.19.300',
       vis='uid___A001_X2fe_X20f_target.ms',
       imagename='uid___A001_X2fe_X20f_target.spw25.cube.I.iter0',
       threshold='0.0mJy', imsize=[960, 960], start='249.147701942GHz',
       npixels=0, cell=['0.043arcsec'], width='7.81215119823MHz',
       outframe='LSRK', gridder='standard', niter=0, datacolumn='data',
       savemodel='none', restoration=False, intent='OBSERVE_TARGET#ON_SOURCE',
       robust=0.5, usemask='user', parallel=False, stokes='I', nchan=238,
       deconvolver='hogbom', weighting='briggs', pbcor=False, pblimit=0.2,
       restoringbeam='common', specmode='cube', chanchunks=-1, interactive=0)
exportfits(dropstokes=False, minpix=0,
           fitsimage='uid___A001_X2fe_X20f_target.spw25.cube.I.iter0.residual.fits',
           imagename='uid___A001_X2fe_X20f_target.spw25.cube.I.iter0.residual',
           overwrite=True, bitpix=-32, maxpix=-1, velocity=False, optical=False,
           stokeslast=True)
tclean(phasecenter='ICRS 23:46:09.4400 +012.49.19.300',
       vis='uid___A001_X2fe_X20f_target.ms',
       imagename='uid___A001_X2fe_X20f_target.spw29.cube.I.iter0',
       threshold='0.0mJy', imsize=[960, 960], start='233.254378783GHz',
       npixels=0, cell=['0.043arcsec'], width='7.81213115096MHz',
       outframe='LSRK', gridder='standard', niter=0, datacolumn='data',
       savemodel='none', restoration=False, intent='OBSERVE_TARGET#ON_SOURCE',
       robust=0.5, usemask='user', parallel=False, stokes='I', nchan=238,
       deconvolver='hogbom', weighting='briggs', pbcor=False, pblimit=0.2,
       restoringbeam='common', specmode='cube', chanchunks=-1, interactive=0)
exportfits(dropstokes=False, minpix=0,
           fitsimage='uid___A001_X2fe_X20f_target.spw29.cube.I.iter0.residual.fits',
           imagename='uid___A001_X2fe_X20f_target.spw29.cube.I.iter0.residual',
           overwrite=True, bitpix=-32, maxpix=-1, velocity=False, optical=False,
           stokeslast=True)
tclean(phasecenter='ICRS 23:46:09.4400 +012.49.19.300',
       vis='uid___A001_X2fe_X20f_target.ms',
       imagename='uid___A001_X2fe_X20f_target.spw31.cube.I.iter0',
       threshold='0.0mJy', imsize=[960, 960], start='234.954234198GHz',
       npixels=0, cell=['0.043arcsec'], width='7.8121332951MHz',
       outframe='LSRK', gridder='standard', niter=0, datacolumn='data',
       savemodel='none', restoration=False, intent='OBSERVE_TARGET#ON_SOURCE',
       robust=0.5, usemask='user', parallel=False, stokes='I', nchan=238,
       deconvolver='hogbom', weighting='briggs', pbcor=False, pblimit=0.2,
       restoringbeam='common', specmode='cube', chanchunks=-1, interactive=0)
exportfits(dropstokes=False, minpix=0,
           fitsimage='uid___A001_X2fe_X20f_target.spw31.cube.I.iter0.residual.fits',
           imagename='uid___A001_X2fe_X20f_target.spw31.cube.I.iter0.residual',
           overwrite=True, bitpix=-32, maxpix=-1, velocity=False, optical=False,
           stokeslast=True)       
"""

spw_list=['0','1','2','3']
spwtag_list=['spw25','spw27','spw29','spw31']

for ind in range(4):

    os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms')
    os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
    mstransform(vis='uid___A001_X2fe_X20f_target.ms',outputvis='uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',timeaverage=True,timebin='30s',spw=spw_list[ind],datacolumn='data',chanaverage=True,chanbin=10,
            keepflags=True)
    initweights('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',wtmode='weight',dowtsp=True)
    exportuvfits('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms','uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
#

