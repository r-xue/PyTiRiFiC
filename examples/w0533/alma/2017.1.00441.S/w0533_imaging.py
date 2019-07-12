"""
os.system("rm -rf uid___A001_X1284_X190f_target.ms")
mstransform(outputvis='uid___A001_X1284_X190f_target.ms',
            vis='uid___A002_Xc81f73_X240f.ms', datacolumn='corrected',
            reindex=False, spw='21~28', field='W0533-3401',
            intent='OBSERVE_TARGET#ON_SOURCE')
"""

"""
# CO 3-2
msname='w0533_band3.bb1.cube4.ms'
os.system('rm -rf '+msname)
mstransform(vis='../calibrated/uid___A001_X1284_X190f_target.ms',outputvis=msname,datacolumn='data',field='W0533-3401',
            timeaverage=False,timebin='30s',
            chanaverage=True,chanbin=4,
            spw='25',outframe='LSRK',regridms=True,
            mode='channel',start=1,width=1,nchan=238,
            keepflags=False)
"""


"""

msname='w0533_band3.bb2.cube4.ms'
# os.system('rm -rf '+msname)
# mstransform(vis='../calibrated/uid___A001_X1284_X190f_target.ms',outputvis=msname,datacolumn='data',field='W0533-3401',
#             timeaverage=False,timebin='30s',
#             chanaverage=True,chanbin=4,
#             spw='27',outframe='LSRK',regridms=True,
#             mode='channel',start=1,width=1,nchan=238,
#             keepflags=False)
os.system('rm -rf '+msname.replace('cube4','mfs'))
mstransform(vis=msname,outputvis=msname.replace('cube4','mfs'),datacolumn='data',
            chanaverage=True,chanbin=1000,
            keepflags=False)


msname='w0533_band3.bb3.cube.ms'
# os.system('rm -rf '+msname)
# mstransform(vis='../calibrated/uid___A001_X1284_X190f_target.ms',outputvis=msname,datacolumn='data',field='W0533-3401',
#             timeaverage=False,timebin='30s',
#             spw='21',outframe='LSRK',regridms=True,
#             mode='channel',start=10,width=1,nchan=109,
#             keepflags=False)
os.system('rm -rf '+msname.replace('cube','mfs'))
mstransform(vis=msname,outputvis=msname.replace('cube','mfs'),datacolumn='data',
            chanaverage=True,chanbin=1000,
            keepflags=False)

msname='w0533_band3.bb4.cube.ms'
# os.system('rm -rf '+msname)
# mstransform(vis='../calibrated/uid___A001_X1284_X190f_target.ms',outputvis=msname,datacolumn='data',field='W0533-3401',
#             timeaverage=False,timebin='30s',
#             spw='23',outframe='LSRK',regridms=True,
#             mode='channel',start=10,width=1,nchan=109,
#             keepflags=False)
os.system('rm -rf '+msname.replace('cube','mfs'))
mstransform(vis=msname,outputvis=msname.replace('cube','mfs'),datacolumn='data',
            chanaverage=True,chanbin=1000,
            keepflags=False)
            
"""            


execfile('/Users/Rui/Dropbox/Worklib/projects/rx-recipe/nrao/alma_imager.py')


niter_list=[0]
imsize=[128]
threshold_list=list(np.array([0.])*0.0013)

imagename_list=['w0533.bb1.cube/w0533.iter'+str(x) for x in ['0']]
alma_imager(vis='w0533_band3.bb1.cube4.ms',imagename=imagename_list,
            spw='0',field='W0533-3401',datacolumn='data',
            imsize=imsize,cell='0.08arcsec',phasecenter='ICRS 05:33:58.44 -34.01.34.5',pblimit=-0.10,
            deconvolver='hogbom',specmode='cube',
            weighting='briggs',robust=0.5,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

imagename_list=['w0533.bb2.cube/w0533.iter'+str(x) for x in ['0']]
alma_imager(vis='w0533_band3.bb2.cube4.ms',imagename=imagename_list,
            spw='0',field='W0533-3401',datacolumn='data',
            imsize=imsize,cell='0.08arcsec',phasecenter='ICRS 05:33:58.44 -34.01.34.5',pblimit=-0.10,
            deconvolver='hogbom',specmode='cube',
            weighting='briggs',robust=0.5,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

imagename_list=['w0533.bb3.cube/w0533.iter'+str(x) for x in ['0']]
alma_imager(vis='w0533_band3.bb3.cube.ms',imagename=imagename_list,
            spw='0',field='W0533-3401',datacolumn='data',
            imsize=imsize,cell='0.08arcsec',phasecenter='ICRS 05:33:58.44 -34.01.34.5',pblimit=-0.10,
            deconvolver='hogbom',specmode='cube',
            weighting='briggs',robust=0.5,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

imagename_list=['w0533.bb4.cube/w0533.iter'+str(x) for x in ['0']]
alma_imager(vis='w0533_band3.bb4.cube.ms',imagename=imagename_list,
            spw='0',field='W0533-3401',datacolumn='data',
            imsize=imsize,cell='0.08arcsec',phasecenter='ICRS 05:33:58.44 -34.01.34.5',pblimit=-0.10,
            deconvolver='hogbom',specmode='cube',
            weighting='briggs',robust=0.5,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

"""
imagename_list=['w0533.bb1.mfs/w0533.iter'+str(x) for x in ['0']]
alma_imager(vis='w0533_band3.bb1.cube4.ms',imagename=imagename_list,
            spw='0',field='W0533-3401',datacolumn='data',
            imsize=imsize,cell='0.08arcsec',phasecenter='ICRS 05:33:58.44 -34.01.34.5',pblimit=-0.10,
            deconvolver='mtmfs',specmode='mfs',
            weighting='briggs',robust=0.5,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

imagename_list=['w0533.bb2.mfs/w0533.iter'+str(x) for x in ['0']]
alma_imager(vis='w0533_band3.bb2.cube4.ms',imagename=imagename_list,
            spw='0',field='W0533-3401',datacolumn='data',
            imsize=imsize,cell='0.08arcsec',phasecenter='ICRS 05:33:58.44 -34.01.34.5',pblimit=-0.10,
            deconvolver='mtmfs',specmode='mfs',
            weighting='briggs',robust=0.5,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

imagename_list=['w0533.bb3.mfs/w0533.iter'+str(x) for x in ['0']]
alma_imager(vis='w0533_band3.bb3.cube.ms',imagename=imagename_list,
            spw='0',field='W0533-3401',datacolumn='data',
            imsize=imsize,cell='0.08arcsec',phasecenter='ICRS 05:33:58.44 -34.01.34.5',pblimit=-0.10,
            deconvolver='mtmfs',specmode='mfs',
            weighting='briggs',robust=0.5,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)

imagename_list=['w0533.bb4.mfs/w0533.iter'+str(x) for x in ['0']]
alma_imager(vis='w0533_band3.bb4.cube.ms',imagename=imagename_list,
            spw='0',field='W0533-3401',datacolumn='data',
            imsize=imsize,cell='0.08arcsec',phasecenter='ICRS 05:33:58.44 -34.01.34.5',pblimit=-0.10,
            deconvolver='mtmfs',specmode='mfs',
            weighting='briggs',robust=0.5,
            threshold=threshold_list,usemask='user',pbmask=0.0,niter=niter_list,mask='',
            runexport=True)
"""
            
