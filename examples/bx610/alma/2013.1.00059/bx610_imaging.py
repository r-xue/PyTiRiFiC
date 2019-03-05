"""
os.system("rm -rf id___A002_Xa48b1f_X3ca7_target.ms")
mstransform(outputvis='uid___A002_Xa48b1f_X3ca7_target.ms',
            vis='uid___A002_Xa48b1f_X3ca7.ms.split.cal', datacolumn='data',keepflags=False,
            reindex=False, spw='', field='BX610',
            intent='OBSERVE_TARGET#ON_SOURCE')

os.system("rm -rf uid___A002_Xa4ce71_X1356_target.ms")
mstransform(outputvis='uid___A002_Xa4ce71_X1356_target.ms',
            vis='uid___A002_Xa4ce71_X1356.ms.split.cal', datacolumn='data',keepflags=False,
            reindex=False, spw='', field='BX610',
            intent='OBSERVE_TARGET#ON_SOURCE')
"""
#os.system('rm -rf uid___A001_X12b_X23c_target.ms')
#concat(vis=['uid___A002_Xa48b1f_X3ca7_target.ms','uid___A002_Xa4ce71_X1356_target.ms'],concatvis='uid___A001_X12b_X23c_target.ms')



##### Reduction Version

#+ 2013.1.00059.S v4.3.1
#+ 2015.1.00250.S v4.7.0 v4.7.2


"""
spw_list=['0','1','2','3']
spwtag_list=['spw25','spw27','spw29','spw31']

for ind in range(4):

    os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms')
    os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
    mstransform(vis='uid___A001_X12b_X23c_target.ms',outputvis='uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',timeaverage=True,timebin='30s',spw=spw_list[ind],datacolumn='data',chanaverage=True,chanbin=10,
            keepflags=True)
    initweights('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',wtmode='weight',dowtsp=True)
    exportuvfits('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms','uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
#
"""

execfile('/Users/Rui/Dropbox/Worklib/projects/rx-recipe/nrao/alma_imager.py')

#plotuv_freqtime_amp(vis='uid___A001_X12b_X23c_target.ms',spw=['0','1','2','3'])
#plotuv_freqtime_amp(vis='uid___A001_X12b_X23c_target.ms',spw=['0','1','2','3'],xaxis='time')

#"""
niter_list=[0,10000]
imsize=[1280,1280]


threshold_list=list(np.array([0.,2.])*2.4e-05)
imagename_list=['bx610_band4.bb1_msc_ro1_nm.mfs/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='../calibrated/uid___A001_X12b_X23c_target.ms',imagename=imagename_list,
            spw='0:152.373278~153.069GHz;153.522~154.373278GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

threshold_list=list(np.array([0.,2.])*2.2e-05)
imagename_list=['bx610_band4.bb2_msc_ro1_nm.mfs/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='../calibrated/uid___A001_X12b_X23c_target.ms',imagename=imagename_list,
            spw='1',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

threshold_list=list(np.array([0.,2.])*2.3e-05)
imagename_list=['bx610_band4.bb3_msc_ro1_nm.mfs/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='../calibrated/uid___A001_X12b_X23c_target.ms',imagename=imagename_list,
            spw='2:142.202~143.359GHz;143.835~144.202GHz',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

threshold_list=list(np.array([0.,2.])*2.0e-05)
imagename_list=['bx610_band4.bb4_msc_ro1_nm.mfs/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='../calibrated/uid___A001_X12b_X23c_target.ms',imagename=imagename_list,
            spw='3',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='',width='',nchan=-1,
            deconvolver='mtmfs',specmode='mfs',scales=[0,5],
            weighting='briggs',robust=1.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)
#"""


"""
niter_list=[0,10000]
imsize=[1280,1280]

## CI

threshold_list=list(np.array([0.,2.])*0.00068124209)
imagename_list=['bx610_band4.bb1_msc_ro1_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#threshold_list=list(np.array([0.,2.])*0.0009)
#imagename_list=['bx610_band4.bb1_msc_ro0_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='../calibrated/uid___A001_X12b_X23c_target.ms',imagename=imagename_list,
            spw='0',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='152.373278GHz',width='7.812500MHz',nchan=238,
            deconvolver='multiscale',specmode='cube',scales=[0,5],
            weighting='briggs',robust=1.0,
            #weighting='briggs',robust=0.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

threshold_list=list(np.array([0.,2.])*0.00070085691)
imagename_list=['bx610_band4.bb2_msc_ro1_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#threshold_list=list(np.array([0.,2.])*0.0009)
#imagename_list=['bx610_band4.bb2_msc_ro0_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='../calibrated/uid___A001_X12b_X23c_target.ms',imagename=imagename_list,
            spw='1',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='154.248278GHz',width='7.8125006MHz',nchan=238,
            deconvolver='multiscale',specmode='cube',scales=[0,5],
            weighting='briggs',robust=1.0,
            #weighting='briggs',robust=0.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

## CO43

threshold_list=list(np.array([0.,2.])*0.00065050490)
imagename_list=['bx610_band4.bb3_msc_ro1_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#threshold_list=list(np.array([0.,2.])*0.0008)
#imagename_list=['bx610_band4.bb3_msc_ro0_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='../calibrated/uid___A001_X12b_X23c_target.ms',imagename=imagename_list,
            spw='2',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='142.3275GHz',width='7.8125006MHz',nchan=238,
            deconvolver='multiscale',specmode='cube',scales=[0,5],
            weighting='briggs',robust=1.0,
            #weighting='briggs',robust=0.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)

threshold_list=list(np.array([0.,2.])*0.00066460425)
imagename_list=['bx610_band4.bb4_msc_ro1_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#threshold_list=list(np.array([0.,2.])*0.0008)
#imagename_list=['bx610_band4.bb4_msc_ro0_nm.cube/bx610.iter'+str(x) for x in ['0','n']]
#imagename_list=imagename_list[0]
alma_imager(vis='../calibrated/uid___A001_X12b_X23c_target.ms',imagename=imagename_list,
            spw='3',field='BX610',datacolumn='data',
            imsize=imsize,cell='0.04arcsec',phasecenter='ICRS 23:46:09.4400 +012.49.19.300',pblimit=-0.10,
            start='140.4945GHz',width='7.812500MHz',nchan=238,
            deconvolver='multiscale',specmode='cube',scales=[0,5],
            weighting='briggs',robust=1.0,
            #weighting='briggs',robust=0.0,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            reuse=[True,False],
            runexport=True)
"""            
