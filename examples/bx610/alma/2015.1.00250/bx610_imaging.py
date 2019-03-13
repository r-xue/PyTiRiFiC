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




execfile('/Users/Rui/Dropbox/Workspace/projects/alma_g09/scripts/alma_imager.py')

#plotuv_freqtime_amp(vis='uid___A001_X2fe_X20f_target.ms',spw=['0','1','2','3'])


niter_list=[0,10000]
imsize=[1280,1280]

"""
threshold_list=list(np.array([0.,2.])*2.94183e-05)
imagename_list=['bx610.bb1_msc_ro1_pm.mfs/bx610.iter'+str(x) for x in ['0','n']]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='0:249.188425~251.0087375GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='pb',pbmask=0.2,niter=niter_list,
            runexport=True)
# 
threshold_list=list(np.array([0.,2.])*3.27551e-05)
imagename_list=['bx610.bb2_msc_ro1_pm.mfs/bx610.iter'+str(x) for x in ['0','n']]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='1:250.79375~251.0828125GHz;251.3953125~251.8875GHz;252.16875~252.6140625GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='pb',pbmask=0.2,niter=niter_list,
            runexport=True)
 
threshold_list=list(np.array([0.,2.])*2.64528e-05)
imagename_list=['bx610.bb3_msc_ro1_pm.mfs/bx610.iter'+str(x) for x in ['0','n']]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='2:233.2859375~233.722GHz;234.538~235.10625GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='pb',pbmask=0.2,niter=niter_list,
            runexport=True)
 
threshold_list=list(np.array([0.,2.])*2.47293e-05)
imagename_list=['bx610.bb4_msc_ro1_pm.mfs/bx610.iter'+str(x) for x in ['0','n']]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='3:234.9859375~236.80625GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='pb',pbmask=0.2,niter=niter_list,
            runexport=True)
"""

"""
threshold_list=list(np.array([0.,2.])*2.94183e-05)
imagename_list=['bx610.bb1_msc_ro1_nm.mfs/bx610.iter'+str(x) for x in ['0','n']]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='0:249.188425~251.0087375GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

threshold_list=list(np.array([0.,2.])*3.27551e-05)
imagename_list=['bx610.bb2_msc_ro1_nm.mfs/bx610.iter'+str(x) for x in ['0','n']]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='1:250.79375~251.0828125GHz;251.3953125~251.8875GHz;252.16875~252.6140625GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

threshold_list=list(np.array([0.,2.])*2.64528e-05)
imagename_list=['bx610.bb3_msc_ro1_nm.mfs/bx610.iter'+str(x) for x in ['0','n']]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='2:233.2859375~233.722GHz;234.538~235.10625GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

threshold_list=list(np.array([0.,2.])*2.47293e-05)
imagename_list=['bx610.bb4_msc_ro1_nm.mfs/bx610.iter'+str(x) for x in ['0','n']]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='3:234.9859375~236.80625GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)
"""


niter_list=[0,10000]
imsize=[1280,1280]

#threshold_list=list(np.array([0.,2.])*0.0009)
#imagename_list=['bx610.bb1_msc_ro1_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
threshold_list=list(np.array([0.,2.])*0.0013)
imagename_list=['bx610.bb1_msc_ro0_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='0',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='249.147701942GHz',width='7.81215119823MHz',nchan=238,
            deconvolver='multiscale',specmode='cube',scales=[0,5],
            #weighting='briggs',robust=1.0,
            weighting='briggs',robust=0.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

#threshold_list=list(np.array([0.,2.])*0.0009)
#imagename_list=['bx610.bb2_msc_ro1_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
threshold_list=list(np.array([0.,2.])*0.0013)
imagename_list=['bx610.bb2_msc_ro0_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='1',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='250.752890409GHz',width='7.81215322296MHz',nchan=238,
            deconvolver='multiscale',specmode='cube',scales=[0,5],
            #weighting='briggs',robust=1.0,
            weighting='briggs',robust=0.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

#threshold_list=list(np.array([0.,2.])*0.0008)
#imagename_list=['bx610.bb3_msc_ro1_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
threshold_list=list(np.array([0.,2.])*0.0011)
imagename_list=['bx610.bb3_msc_ro0_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='2',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='233.254378783GHz',width='7.81213115096MHz',nchan=238,
            deconvolver='multiscale',specmode='cube',scales=[0,5],
            #weighting='briggs',robust=1.0,
            weighting='briggs',robust=0.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

#threshold_list=list(np.array([0.,2.])*0.0008)
#imagename_list=['bx610.bb4_msc_ro1_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
threshold_list=list(np.array([0.,2.])*0.0011)
imagename_list=['bx610.bb4_msc_ro0_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='uid___A001_X2fe_X20f_target.ms',imagename=imagename_list,
            spw='3',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='234.954234198GHz',width='7.8121332951MHz',nchan=238,
            deconvolver='multiscale',specmode='cube',scales=[0,5],
            #weighting='briggs',robust=1.0,
            weighting='briggs',robust=0.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)
