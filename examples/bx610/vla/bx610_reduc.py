def config(xp):

    xp['spwrgd']       ='spw'
    xp['uvcs']          =False
    #xp['fitspw']        ='0:3~10;90~97'
    #xp['fitorder']      =1
    
    # IMAGING
    xp['cleanspec']         =True
    xp['cleancont']         =False
    
    xp['imsize']            =2**10
    xp['cell']              ='1.0arcsec'
    
    xp['cleanmode']         = 'velocity'    
    xp['cleanmode']         = 'channel'
    
    #xp['clean_start']       ='-1350km/s'
    #xp['clean_nchan']       =39
    #xp['clean_width']       ='75km/s'
    #xp['clean_start']       ='-1400km/s'
    #xp['clean_nchan']       =76
    #xp['clean_width']       ='40km/s'
    
    #xp['restfreq']          ='34.84619GHz'
    #xp['restfreq']          ='34.846191051995GHz'
    
    xp['phasecenter']       ='ICRS 23:46:09.4400 +012.49.19.300'
    #xp['clean_mask']        ='circle[[512pix,512pix],50pix]'
    
    #xp['minpb']             =0.05
    #xp['multiscale']        =[int(x*(2.25/1.0)) for x in [0.,1.,4.]]
    #xp['clean_gain']        =0.3
    #xp['cyclefactor']       =5.0
    #xp['negcomponent']      =0
    
    return xp

def c10a():
    
    xp=xu.init()
    
    xp['prefix']        ='../'+inspect.stack()[0][3]+'/'+inspect.stack()[0][3]
    xp['rawfiles']      ='/Volumes/Helium/Media/Scratch/10B-106_sb1993818_1.55481.19986877315.ms'
    xp['starttime']     =''
    xp['stoptime']      =''
    xp['importscan']    ='5~34'
    xp['importspw']     ='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['importscan']    ='5~77'
    xp['importspw']     ='0'    
    xp['importmode']    ='ms'
    
    
    # TRACK INFORMATION
    # DO NOT PICK FIELD NAME (DUPLICATED/CONFUSED ID)
    xp['source'] = '5'
    
    xp['fluxcal'] = '2'
    xp['fluxcal_uvrange']=''
    
    xp['phasecal'] = '4'
    xp['phasecal_uvrange']=''
    
    xp['spw_source'] = '0'
    xp['spw_fluxcal'] = '0'
    xp['spw_phasecal'] = '0'
    #xp['flagspw'] = '*:0~3;60~63'
    
    # CALIBRATION & OPTIONS
    #xp['flagselect']=["antenna='3'"] # rfi
    xp['syscal']=''
    
    xp=config(xp)
    xp['niter']        =0
    
    # RUN SCRIPTS
    #xp=xu.ximport(xp)

    au.timeOnSource(xp['prefix']+'.ms')
    #xp=xu.xcal(xp)
    
    #xp['spw_source']='3,4,5'
    xp=xu.xconsol(xp)
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='0')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='1')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='2')
    xp=xu.xclean(xp)
    

def d12jan():
    
    xp=xu.init()
    
    xp['prefix']        ='../'+inspect.stack()[0][3]+'/'+inspect.stack()[0][3]
    xp['rawfiles']      ='/media/rui/Lithium/raw/12A-201/11B-044.sb6590371.eb7328504.55932.04923909722.ms'
    xp['starttime']     =''
    xp['stoptime']      =''
    xp['importscan']    ='5~34'
    xp['importspw']     ='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['importmode']    ='ms'
    
    
    # TRACK INFORMATION
    # DO NOT PICK FIELD NAME (DUPLICATED/CONFUSED ID)
    xp['source'] = '5'
    
    xp['fluxcal'] = '2'
    xp['fluxcal_uvrange']=''
    
    xp['phasecal'] = '4'
    xp['phasecal_uvrange']=''
    
    xp['spw_source'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_fluxcal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_phasecal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    #xp['flagspw'] = '*:0~3;60~63'
    
    # CALIBRATION & OPTIONS
    xp['flagselect']=["antenna='3'"] # rfi
    xp['syscal']=''
    
    xp=config(xp)
    xp['niter']        =0
    
    # RUN SCRIPTS
    #xp=xu.ximport(xp)

    #au.timeOnSource(xp['prefix']+'.ms')
    #xp=xu.xcal(xp)
    
    xp['spw_source']='3,4,5'
    xp=xu.xconsol(xp)
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='0')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='1')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='2')
    #xp=xu.xclean(xp)

def c12mar():
    
    xp=xu.init()
    
    xp['prefix']        ='../'+inspect.stack()[0][3]+'/'+inspect.stack()[0][3]
    xp['rawfiles']      ='/Volumes/D1/projects/hxmm01/12A-201/raw/12A-201.sb9237873.eb9270010.55998.94909407407.ms'
    xp['starttime']     =''
    xp['stoptime']      =''
    xp['importscan']    ='5~34'
    xp['importspw']     ='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['importmode']    ='ms'
    
    
    # TRACK INFORMATION
    # DO NOT PICK FIELD NAME (DUPLICATED/CONFUSED ID)
    xp['source'] = '5'
    
    xp['fluxcal'] = '2'
    xp['fluxcal_uvrange']=''
    
    xp['phasecal'] = '4'
    xp['phasecal_uvrange']=''
    
    xp['spw_source'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_fluxcal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_phasecal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    #xp['flagspw'] = '*:0~3;60~63'
    
    # CALIBRATION & OPTIONS
    """
    xp['flagselect'] = ["mode='quack' quackinterval=8.0",
                    "timerange='03:42:30~03:43:00 ",
                    "timerange='06:51:10~06:51:20'",
                    "timerange='05:02:30~05:02:50'",
                    "timerange='07:11:14~07:11:16'",
                    "timerange='07:53:40~07:53:50'",
                    "timerange='08:02:10~08:02:20' "
                    ]
    """
    xp['syscal']=''
    
    xp=config(xp)
    xp['niter']        =0
    
    # RUN SCRIPTS
    #xp=xu.ximport(xp)

    #au.timeOnSource(xp['prefix']+'.ms')
    xp=xu.xcal(xp)
    
    xp['spw_source']='3,4,5'
    xp=xu.xconsol(xp)
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='0')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='1')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='2')
    #xp=xu.xclean(xp)

def b12jun():
    
    xp=xu.init()

    xp['prefix']        ='../'+inspect.stack()[0][3]+'/'+inspect.stack()[0][3]
    xp['rawfiles']      ='/Volumes/D1/projects/hxmm01/12A-201/raw/12A-201.sb9991067.eb10734424.56100.54596251158.ms'
    xp['starttime']     =''
    xp['stoptime']      =''
    xp['importscan']    ='5~34'
    xp['importspw']     ='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['importmode']    ='ms'
    
    
    # TRACK INFORMATION
    # DO NOT PICK FIELD NAME (DUPLICATED/CONFUSED ID)
    xp['source'] = '5'
    
    xp['fluxcal'] = '2'
    xp['fluxcal_uvrange']=''
    
    xp['phasecal'] = '4'
    xp['phasecal_uvrange']=''
    
    xp['spw_source'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_fluxcal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_phasecal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    #xp['flagspw'] = '*:0~3;60~63'
    
    # CALIBRATION & OPTIONS
    """
    xp['flagselect'] = ["mode='quack' quackinterval=8.0",
                    "timerange='03:42:30~03:43:00 ",
                    "timerange='06:51:10~06:51:20'",
                    "timerange='05:02:30~05:02:50'",
                    "timerange='07:11:14~07:11:16'",
                    "timerange='07:53:40~07:53:50'",
                    "timerange='08:02:10~08:02:20' "
                    ]
    """
    xp['syscal']=''
    
    xp=config(xp)
    xp['niter']        =0
    
    # RUN SCRIPTS
    #xp=xu.ximport(xp)

    #au.timeOnSource(xp['prefix']+'.ms')
    #xp=xu.xcal(xp)
    
    xp['spw_source']='3,4,5'
    xp=xu.xconsol(xp)
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='0')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='1')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='2')
    #xp=xu.xclean(xp)

def b12aug():
    
    xp=xu.init()
    
    xp['prefix']        ='../'+inspect.stack()[0][3]+'/'+inspect.stack()[0][3]
    xp['rawfiles']      ='/Volumes/D1/projects/hxmm01/12A-201/raw/12A-201.sb9991390.eb11312240.56146.441112025466.ms'
    xp['starttime']     =''
    xp['stoptime']      =''
    xp['importscan']    ='5~61'
    xp['importspw']     ='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['importmode']    ='ms'
    
    
    # TRACK INFORMATION
    # DO NOT PICK FIELD NAME (DUPLICATED/CONFUSED ID)
    xp['source'] = '5'
    
    xp['fluxcal'] = '2'
    xp['fluxcal_uvrange']=''
    
    xp['phasecal'] = '4'
    xp['phasecal_uvrange']=''
    
    xp['spw_source'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_fluxcal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_phasecal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    #xp['flagspw'] = '*:0~3;60~63'
    
    # CALIBRATION & OPTIONS
    """
    xp['flagselect'] = ["mode='quack' quackinterval=8.0",
                    "timerange='03:42:30~03:43:00 ",
                    "timerange='06:51:10~06:51:20'",
                    "timerange='05:02:30~05:02:50'",
                    "timerange='07:11:14~07:11:16'",
                    "timerange='07:53:40~07:53:50'",
                    "timerange='08:02:10~08:02:20' "
                    ]
    """
    xp['syscal']=''
    
    xp=config(xp)
    xp['niter']        =0
    
    # RUN SCRIPTS
    #xp=xu.ximport(xp)
    
    
#     flagmanager(vis=xp['prefix']+'.ms',mode='restore',versionname='Original')
#     flagdata(vis=xp['prefix']+'.ms',mode='unflag',scan='5')
#     flagcmd(vis=xp['prefix']+'.ms',inpmode='list',
#             inpfile=["timerange='10:46:70~10:47:30'"])
#     flagcmd(vis=xp['prefix']+'.ms',inpmode='list',
#             inpfile=["antenna='2'"])
#     #au.timeOnSource(xp['prefix']+'.ms')
#     flagmanager(vis=xp['prefix']+'.ms',
#                 mode='save',
#                 versionname='Original_Modified',
#                 comment='Original Flagging + Unflag Scan5',
#                 merge='replace')
# 
#     #flagmanager(vis=xp['prefix']+'.ms',mode='restore',versionname='Original_Modified')
#     xp['flagreset_version']='Original_Modified'
#     xp=xu.xcal(xp)
    
    xp['spw_source']='3,4,5'
    xp=xu.xconsol(xp)
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='0')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='1')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='2')
    #xp=xu.xclean(xp)

def b12sep():
    
    xp=xu.init()
    
    xp['prefix']        ='../'+inspect.stack()[0][3]+'/'+inspect.stack()[0][3]
    xp['rawfiles']      ='/Volumes/D1/projects/hxmm01/12A-201/raw/12A-201.sb9991390.eb11735360.56172.34942921296.ms'
    xp['starttime']     =''
    xp['stoptime']      =''
    xp['importscan']    ='5~61'
    xp['importspw']     ='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['importmode']    ='ms'
    
    
    # TRACK INFORMATION
    # DO NOT PICK FIELD NAME (DUPLICATED/CONFUSED ID)
    xp['source'] = '5'
    
    xp['fluxcal'] = '2'
    xp['fluxcal_uvrange']=''
    
    xp['phasecal'] = '4'
    xp['phasecal_uvrange']=''
    
    xp['spw_source'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_fluxcal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    xp['spw_phasecal'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    #xp['flagspw'] = '*:0~3;60~63'
    
    # CALIBRATION & OPTIONS
    """
    xp['flagselect'] = ["mode='quack' quackinterval=8.0",
                    "timerange='03:42:30~03:43:00 ",
                    "timerange='06:51:10~06:51:20'",
                    "timerange='05:02:30~05:02:50'",
                    "timerange='07:11:14~07:11:16'",
                    "timerange='07:53:40~07:53:50'",
                    "timerange='08:02:10~08:02:20' "
                    ]
    """
    xp['syscal']=''
    
    xp=config(xp)
    xp['niter']        =0
    
    # RUN SCRIPTS
    #xp=xu.ximport(xp)

    #au.timeOnSource(xp['prefix']+'.ms')
    #xp=xu.xcal(xp)
    
    xp['spw_source']='3,4,5'
    xp=xu.xconsol(xp)
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='0')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='1')
    #xu.checkvrange(vis=xp['prefix']+'.src.ms',outframe='BARY',restfreq=34846190000,verbose=True,spw='2')
    #xp=xu.xclean(xp)




def comb():

    xp=xu.init()

    # CONSOLIDATING
    xp['prefix']            ='../comb/HXMM01.CO10'
    xp['prefix_comb']       =['../d12jan/d12jan','../c12mar/c12mar',
                              '../b12jun/b12jun','../b12sep/b12sep']

    xp=config(xp)
    
    xp['cleanspec']         =True
    xp['cleancont']         =False

    xp['mosweight']         =False
    xp['scalewt']           =False

    xp['imsize']            =2**8*5
    xp['cell']              ='0.09arcsec'
    
   
    xp['minpb']             =0.2

    
    xp['phasecenter']       ="J2000 02h20m16.613000 -06d01m43.15000s"
    xp['clean_mask']        =['circle[ [02h20m16.613000,-06d01m43.15000s], 6.0arcsec]']

    xp['multiscale']        =[int(x*(0.5/0.09)) for x in [0.,1.,3.]]
    xp['clean_gain']        =0.3
    xp['cyclefactor']       =2.0
    xp['negcomponent']      =0
    xp['niter']             =1000
    xp['threshold_spec']    ='0.3mJy'
    
    xp['cleanmode']         = 'velocity'    
    xp['clean_start']       ='-1400km/s'
    xp['clean_nchan']       =74
    xp['clean_width']       ='40km/s'
    xp['restfreq']          ='34.846191051995GHz'

    
    # RUN SCRIPTS:
    xp=xu.xconsol(xp)
    
    #xp['ctag']              ='_ro'
    xp['cleanweight']       ='briggs'
    xp['ctag']              ='_na'
    xp['cleanweight']       ='natural'
    
    xp['velocity']          =False
    xp['history']           =True
    #xp=xu.xclean(xp)
    
    
def comb_imaging():
    
    list_spw    = ['0']
    list_name   = ['CO10']
    list_freq   = ['34.846191051995GHz']
    list_start  = ['-1400km/s']
    list_nchan  = [74]
    list_width  = ['40km/s']
    
    version='_ro_msc'
    robust=0.0
    multiscale  =[int(x*(0.24/0.03)) for x in [0.,1.,3.]]
    
    cell        = '0.15arcsec'
    imagesize   = [2**8*3,2**8*3]
    #   this leads to 1arcsecx1arcsec natural beam
    cell        = '0.09arcsec'
    imagesize   = [2**8*5,2**8*5]    
    #   this leads to 0.8arcx0.8arcsec natural beam
    cell        = '0.045arcsec'
    #   this leads to 0.62arcx0.61arcsec natural beam
    cell        = '0.030arcsec'
    #   this leads to 0.57arcx0.49arcsec natural beam
    cell        = '0.010arcsec'
    #   this leads to 0.54arcx0.41arcsec natural beam    
    cell        = '0.060arcsec'
    #   0.72x0.69" (natural)
    #   0.30x0.28" (ro0)
    cell        = '0.030arcsec'
    #   0.29x0.24" (ro0)
    imagesize   = [2**8*5,2**8*5]    
    #   this leads to 0.8arcx0.8arcsec natural beam
    #   so it;s better have 8*cell=1xbmaj    
    phasecen    = "J2000 02h20m16.613000 -06d01m43.15000s"
    masksou     = ['circle[ [02h20m16.613000,-06d01m43.15000s], 6.0arcsec]']
    
    for ind in range(len(list_spw)):
        
        souname     =   'HXMM01'+version
        myimagebase=souname+'.'+list_name[ind]
        visname         = '../calibrated/comb/HXMM01.CO10.src.ms'
        
        casalog.post('run snapshot spw '+str(list_spw[ind]),'INFO')
        os.system('rm -rf '+myimagebase+'.*')
        tclean(
            vis         = visname,
            spw         = list_spw[ind],
            imagename   = myimagebase,
            field       = '0',
            cell        = cell,
            imsize      = imagesize,
            niter       = 8000,
            interactive = False,
            threshold   ='0.3mJy',
            cyclefactor = 2.0,
            scales      = multiscale,
            pbcor       = False,
            weighting   = 'briggs',
            robust      = robust,
            specmode    = 'cube',
            start       = list_start[ind],
            nchan       = list_nchan[ind],
            width       = list_width[ind],
            restfreq    = list_freq[ind],
            outframe    = 'BARY',
            veltype     = 'radio',        
            phasecenter = phasecen,
            deconvolver = 'multiscale',
            interpolation='nearest', #linear
            parallel    = False,
            restoringbeam='common',
            calcpsf     = True,
            calcres     = True,
            pblimit     = 0.2,
            usemask     = 'user',
            mask        = masksou)
        
        velocity=False
        history=True
    
        os.system('rm -rf '+myimagebase+'.*.fits')
        
        impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb',
            outfile=myimagebase+'.image.pbcor',overwrite=True)
        fname_list=['.image.pbcor','.pb','.image','.residual','.psf','.model','.sumwt']
        for fname in fname_list:
            exportfits(imagename=myimagebase+fname,
                       fitsimage=myimagebase+fname+'.fits',
                       velocity=velocity,history=history,
                       optical=False,overwrite=True,dropstokes=False,stokeslast=True,dropdeg=False)    


def comb_imaging_75kms():
    
    list_spw    = ['0']
    list_name   = ['CO10']
    list_freq   = ['34.846191051995GHz']
    list_start  = ['-1350km/s']
    list_nchan  = [38]
    list_width  = ['75km/s']
    
    version='_ro_msc'
    robust=0.0
    multiscale  =[int(x*(0.35/0.06)) for x in [0.,1.,3.]]
    robust=0.5
    multiscale  =[int(x*(0.55/0.06)) for x in [0.,1.,3.]]
    
    cell        = '0.15arcsec'
    imagesize   = [2**8*3,2**8*3]
    #   this leads to 1arcsecx1arcsec natural beam
    cell        = '0.09arcsec'
    imagesize   = [2**8*5,2**8*5]    
    #   this leads to 0.8arcx0.8arcsec natural beam
    cell        = '0.045arcsec'
    #   this leads to 0.62arcx0.61arcsec natural beam
    cell        = '0.030arcsec'
    #   this leads to 0.57arcx0.49arcsec natural beam
    cell        = '0.010arcsec'
    #   this leads to 0.54arcx0.41arcsec natural beam    
    cell        = '0.060arcsec'
    #   0.72x0.69" (natural)
    #   0.30x0.28" (ro0)
    version='_ro_msc'
    cell        = '0.06arcsec'
    #   0.29x0.24" (ro0)
    imagesize   = [2**8*5,2**8*5]    
    #   this leads to 0.8arcx0.8arcsec natural beam
    #   so it;s better have 8*cell=1xbmaj    
    phasecen    = "J2000 02h20m16.613000 -06d01m43.15000s"
    masksou     = ['circle[ [02h20m16.613000,-06d01m43.15000s], 4.0arcsec]']
    
    for ind in range(len(list_spw)):
        
        souname     =   'HXMM01'+version
        myimagebase=souname+'.'+list_name[ind]
        visname         = '../calibrated/comb_75kms/HXMM01.CO10.src.ms'
        
        casalog.post('run snapshot spw '+str(list_spw[ind]),'INFO')
        os.system('rm -rf '+myimagebase+'.*')
        tclean(
            vis         = visname,
            spw         = list_spw[ind],
            imagename   = myimagebase,
            field       = '0',
            cell        = cell,
            imsize      = imagesize,
            niter       = 6000,
            interactive = False,
            threshold   ='0.3mJy',
            cyclefactor = 2.0,
            scales      = multiscale,
            pbcor       = False,
            weighting   = 'briggs',
            robust      = robust,
            specmode    = 'cube',
            start       = list_start[ind],
            nchan       = list_nchan[ind],
            width       = list_width[ind],
            restfreq    = list_freq[ind],
            outframe    = 'BARY',
            veltype     = 'radio',        
            phasecenter = phasecen,
            deconvolver = 'multiscale',
            interpolation='nearest', #linear
            parallel    = False,
            restoringbeam='common',
            calcpsf     = True,
            calcres     = True,
            pblimit     = 0.2,
            usemask     = 'user',
            mask        = masksou)
        
        velocity=False
        history=True
    
        os.system('rm -rf '+myimagebase+'.*.fits')
        
        impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb',
            outfile=myimagebase+'.image.pbcor',overwrite=True)
        fname_list=['.image.pbcor','.pb','.image','.residual','.psf','.model','.sumwt']
        for fname in fname_list:
            exportfits(imagename=myimagebase+fname,
                       fitsimage=myimagebase+fname+'.fits',
                       velocity=velocity,history=history,
                       optical=False,overwrite=True,dropstokes=False,stokeslast=True,dropdeg=False)

if  __name__=="__main__":
    
    #d12jan()
    #c12mar()
    #b12jun()
    #b12sep()
    
    #b12aug()   # heavily flagged
    
    c10a()
    #comb_imaging()
    #comb_imaging_75kms()
