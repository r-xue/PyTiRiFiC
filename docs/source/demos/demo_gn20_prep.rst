Example: GN20 (z~4 SMF) : Data Prep
-----------------------------------

Archive Query:
~~~~~~~~~~~~~~

We make the follow choices:

::

   To reduce the data size and local I/O(SDM->MS), we selected MS as the download format with importevla flagging turned on.

   In addition, we turned off relevant (e.g. shadow) in the local pipeline to save pipeline running time.

   We didn't chose any spectral/time averaging to preserve original raw data characertics for better calibrations.

Load some essential Python modules + CASA 6 tasks/tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    
    import sys,os,glob,io,socket
    import logging
    from pprint import pprint
    import numpy as np
    
    import casatasks as ctasks
    import casatools as ctools
    
    # Import wurlitzer for display real-time console logs
    #   https://github.com/minrk/wurlitzer
    %reload_ext wurlitzer
    
    # for inline plots
    %matplotlib inline
    %config InlineBackend.figure_format = "retina"


Using the beta-version of CASA 6
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    print('casatools ver:',ctools.version_string())
    print('casatasks ver:',ctasks.version_string())


.. parsed-literal::

    casatools ver: 2019.172
    casatasks ver: 2019.166


Import some convinient functions from ``rxutils``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    from rxutils.casa.proc import rmPointing        # help remove POINTING tables hidden under
    from rxutils.casa.proc import setLogfile        # help reset the casa 6 log file
    from rxutils.casa.proc import checkchflag       # help check channel-wise flagging stats
    from rxutils.casa.proc import getcommonfreqs    # obatin the frequency coverage of one SPW in a specified frame (e.g. TOPO-LSRK)
    from rxutils.casa.proc import rmColumns         # remove columns from MS

Reduce Raw Data Size
~~~~~~~~~~~~~~~~~~~~

The main purpose of this step is getting rid of RL/LR and flagged rows
to speed up calibrations and reduce local I/O load.

.. code:: ipython3

    import glob
    import os
    from casatasks import mstransform
    
    demo_dir='/Volumes/D2/raw/AC974/' # where the original archival dataset stored
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile('/Volumes/D1/raw/AC974/demo_gn20_prep.log')
        
    mslist=glob.glob('*.ms')
    
    for ms in mslist:
        outms='/Volumes/D1/raw/AC974/'+ms.replace('.ms','.ms') # a slim verson of archival data
        if  os.path.isdir(outms):
            continue
        mstransform(vis=ms,outputvis=outms,correlation='RR,LL',keepflags=False,datacolumn='data')
        flagmanager(vis=outms,mode='save',versionname='Original',merge='replace',\
                    comment='Original Flagging from the archive with online/shadown/zero flagging applied nad completed flagged rows are removed')    


.. parsed-literal::

    2019-11-26 22:02:43	INFO	mstransform::::casa	##########################################
    2019-11-26 22:02:43	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-11-26 22:02:43	INFO	mstransform::::casa	mstransform( vis='AC974.sb3282289.eb3372715.55618.305010428245.ms', outputvis='/Volumes/D1/raw/AC974/AC974.sb3282289.eb3372715.55618.305010428245.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='', spw='', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=False, chanbin=1, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-11-26 22:02:43	INFO	MSTransformManager::parseMsSpecParams	Input file name is AC974.sb3282289.eb3372715.55618.305010428245.ms
    2019-11-26 22:02:43	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-11-26 22:02:43	INFO	MSTransformManager::parseMsSpecParams	Output file name is /Volumes/D1/raw/AC974/AC974.sb3282289.eb3372715.55618.305010428245.ms
    2019-11-26 22:02:43	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-11-26 22:02:43	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-11-26 22:02:43	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-11-26 22:02:43	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-11-26 22:02:43	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [3] to [3] with stride [1], length [1]]]
    2019-11-26 22:02:43	INFO	MSTransformManager::open	Select data
    2019-11-26 22:02:43	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-11-26 22:03:19	INFO	MSTransformDataHandler::makeSelection	14075263 out of 16259750 rows are going to be considered due to the selection criteria.
    2019-11-26 22:03:27	INFO	mstransform::::casa	Apply the transformations
    2019-11-26 22:09:03	INFO	mstransform::::casa	Result mstransform: True
    2019-11-26 22:09:03	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-11-26 16:02:42.687432 End time: 2019-11-26 16:09:02.886568
    2019-11-26 22:09:03	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-11-26 22:09:03	INFO	mstransform::::casa	##########################################
    2019-11-26 22:09:03	INFO	mstransform::::casa	##########################################
    2019-11-26 22:09:03	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-11-26 22:09:03	INFO	mstransform::::casa	mstransform( vis='AC974.sb3282289.eb3372716_000.55619.25416130787.ms', outputvis='/Volumes/D1/raw/AC974/AC974.sb3282289.eb3372716_000.55619.25416130787.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='', spw='', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=False, chanbin=1, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-11-26 22:09:03	INFO	MSTransformManager::parseMsSpecParams	Input file name is AC974.sb3282289.eb3372716_000.55619.25416130787.ms
    2019-11-26 22:09:03	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-11-26 22:09:03	INFO	MSTransformManager::parseMsSpecParams	Output file name is /Volumes/D1/raw/AC974/AC974.sb3282289.eb3372716_000.55619.25416130787.ms
    2019-11-26 22:09:03	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-11-26 22:09:03	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-11-26 22:09:03	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-11-26 22:09:03	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-11-26 22:09:03	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [3] to [3] with stride [1], length [1]]]
    2019-11-26 22:09:03	INFO	MSTransformManager::open	Select data
    2019-11-26 22:09:03	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-11-26 22:09:31	INFO	MSTransformDataHandler::makeSelection	13513309 out of 16335150 rows are going to be considered due to the selection criteria.
    2019-11-26 22:09:40	INFO	mstransform::::casa	Apply the transformations


Data Calibration
~~~~~~~~~~~~~~~~

Prepare visibiity data from the calibrated MS from the modified VLA scripted pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The VLA CASA-integrated pipleline began to operate from Jan 2013. The
“scripted” older pipeline from NRAO seems to work with the dataset after
some modification in the pipeline and minor data metadata corrections.

https://science.nrao.edu/facilities/vla/data-processing/pipeline/scripted-pipeline

Hodge+2012:

   We observed the CO(2–1) transition toward the GN20 field as part of
   VLA key project AC974. The project was awarded 96 hr in
   B-configuration (baselines up to 10 km) and 28 hr in D-configuration
   (baselines up to 1 km), for a total of 124 hr. The observations were
   dynamically scheduled and took place in 2010 March–April
   (D-configuration) and 2011 February–April (B-configuration). The
   CO(2–1) line (rest frequency ν = 230.5424 GHz) is redshifted to ν =
   45.655 GHz at z = 4.05, requiring the Q band. The primary beam is ∼1′
   (FWHM) at this frequency, and the pointing center was chosen to be
   10′′ west of GN20 so that GN20, the nearby SMGs (and fellow
   protocluster members) GN20.2a and GN20.2b, and the z = 1.5 galaxy
   BzK–21,000 would all fall within the 70% sensitivity radius of the
   primary beam (data presented in J. A. Hodge et al. 2012, submitted).
   All images have been corrected for the response of the VLA primary
   beam. We centered the two 128 MHz intermediate frequencies (IFs) at
   45.592 GHz and 45.720 GHz, for a total bandwidth of 246 MHz or 1600
   km s−1 (taking into account the overlap). Each of the two IFs had 64
   channels, resulting in an instrumental velocity resolution of 13 km s
   polarization mode.

..

   | AC974_sb1178393_1.55284.176880300925 public AC974 x 10-Mar-29
     04:14:43 10-Mar-29 11:13:28 32.19GB VLA:D:0 C Q SDMset raw OK Scans
     Logs
   | AC974_sb1178393_1.55290.15952814815 public AC974 x 10-Apr-04
     03:51:01 10-Apr-04 10:49:52 32.20GB VLA:D:0 C Q SDMset raw OK Scans
     Logs
   | AC974_sb1178393_1_000.55294.19113723379 public AC974 x 10-Apr-08
     04:35:15 10-Apr-08 11:33:59 34.81GB VLA:D:0 C Q SDMset raw OK Scans
     Logs
   | AC974_sb1178393_1.55295.14680190972 public AC974 x 10-Apr-09
     03:31:24 10-Apr-09 10:30:13 34.82GB VLA:D:0 C Q SDMset raw OK Scans
     Logs
   | AC974.sb3282289.eb3372706.55603.30302575231 public AC974 x
     11-Feb-11 07:16:26 11-Feb-11 14:15:17 35.38GB VLA:C=>CNB:0 C Q
     SDMset raw OK Scans Logs
   | AC974.sb3282289.eb3372707.55604.21726888889 public AC974 x
     11-Feb-12 05:12:53 11-Feb-12 12:11:40 38.12GB VLA:C=>CNB:0 C Q
     SDMset raw OK Scans Logs
   | AC974.sb3282289.eb3372708.55606.21154611111 public AC974 x
     11-Feb-14 05:04:58 11-Feb-14 12:03:49 38.13GB VLA:C=>CNB:0 C Q
     SDMset raw OK Scans Logs
   | AC974.sb3282289.eb3372709.55608.19656930555 public AC974 x
     11-Feb-16 04:57:06 11-Feb-16 11:55:57 38.13GB VLA:C=>CNB:0 C Q
     SDMset raw info Scans Logs
   | AC974.sb3282289.eb3372710.55609.20419065972 public AC974 x
     11-Feb-17 04:54:03 11-Feb-17 11:52:01 35.30GB VLA:C=>CNB:0 C Q
     SDMset raw OK Scans Logs
   | AC974.sb3282289.eb3372711.55610.18910030092 public AC974 x
     11-Feb-18 04:49:14 11-Feb-18 11:48:05 35.38GB VLA:C=>CNB:0 C Q
     SDMset raw OK Scans Logs
   | AC974.sb3282289.eb3372712.55611.200792627315 public AC974 x
     11-Feb-19 04:50:17 11-Feb-19 11:49:08 38.13GB VLA:C=>CNB:0 C Q
     SDMset raw OK Scans Logs
   | AC974.sb3282289.eb3372713.55613.19257357639 public AC974 x
     11-Feb-21 04:37:26 11-Feb-21 11:36:17 38.12GB VLA:C=>CNB:0 C Q
     SDMset raw OK Scans Logs
   | AC974.sb3282289.eb3372714.55616.27802989583 public AC974 x
     11-Feb-24 06:40:24 11-Feb-24 13:39:08 35.38GB VLA:B:0 C Q SDMset
     raw OK Scans Logs
   | AC974.sb3282289.eb3372715.55618.305010428245 public AC974 x
     11-Feb-26 07:19:14 11-Feb-26 14:16:09 35.22GB VLA:B:0 C Q SDMset
     raw OK Scans Logs
   | AC974.sb3282289.eb3372716_000.55619.25416130787 public AC974 x
     11-Feb-27 06:08:32 11-Feb-27 13:07:23 35.39GB VLA:B:0 C Q SDMset
     raw OK Scans Logs
   | AC974.sb3282289.eb3372717.55626.21851298611 public AC974 x
     11-Mar-06 05:16:06 11-Mar-06 12:14:57 37.68GB VLA:B:0 C Q SDMset
     raw OK Scans Logs
   | AC974.sb3282289.eb3372718.55632.18241631945 public AC974 x
     11-Mar-12 04:22:43 11-Mar-12 11:21:26 37.67GB VLA:B:0 C Q SDMset
     raw OK Scans Logs
   | AC974.sb3848174.eb3850825.55679.073782673615 public AC974 x
     11-Apr-28 01:47:41 11-Apr-28 06:46:52 26.92GB VLA:B:0 C Q SDMset
     raw OK Scans Logs


Prep Calibrated Data:
~~~~~~~~~~~~~~~~~~~~~

Steps to proceed:

::

   Split Calibrated Visibility Window by Window

   Perform Channel/Time averging

   Averging over continuum channel / spectral window partition

   Averging to 30s
   Combine two SPWs covering CO 2-1

   rename file: projectid.yymmdd

   inspect WEIGHT column at the end

.. code:: ipython3

    # Switch working directory
    
    import glob 
    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/gn20/vla/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_GN20.log')
    
    mslist=[]
    mslist.extend(glob.glob('/Volumes/D1/proc/AC*/AC*ms')) # calibrated vis are in S1/proc and D1/proc 
                                                          # du -hs /Volumes/*/proc/AC*/AC*ms | wc -l
    mslist=sorted(mslist)
    print(mslist)
    print(len(mslist))
    for ms in mslist:
    
        #ctasks.flagdata(vis_name,autocorr=True,flagbackup=True)
        outms=ms.split('/')[-2]
        outms=outms+'.ms'    
        #if  not ('100408' in ms or '100409' in ms):
        #    continue
        #if os.path.isdir(outms):
        #   continue    
        os.system('rm -rf '+outms)
        os.system('rm -rf '+outms+'.flagversions')
        antenna=''
        ctasks.mstransform(ms,outputvis=outms,field='GN20cluster',spw='2:0~62,3:1~63',datacolumn='corrected',correlation='RR,LL',antenna=antenna,
                            regridms=True,outframe='lsrk',combinespws=True,mode='channel',start=1,nchan=128,width=1,
                            timeaverage=True,timebin='30s',maxuvwdistance=0.0,
                            keepflags=False,usewtspectrum=False)
        #ctasks.cvel2(ms,outputvis=outms,field='GN20cluster',spw='2,3',passall=False,
        #             start=1,nchan=128,width=1,
        #rmPointing(outvis) # pointing tables are generally small for EVLA data
        


.. parsed-literal::

    ['/Volumes/D1/proc/AC974.100329/AC974_sb1178393_1.55284.176880300925.ms', '/Volumes/D1/proc/AC974.100404/AC974_sb1178393_1.55290.15952814815.ms', '/Volumes/D1/proc/AC974.100408/AC974_sb1178393_1_000.55294.19113723379.ms', '/Volumes/D1/proc/AC974.100409/AC974_sb1178393_1.55295.14680190972.ms', '/Volumes/D1/proc/AC974.110211/AC974.sb3282289.eb3372706.55603.30302575231.ms', '/Volumes/D1/proc/AC974.110212/AC974.sb3282289.eb3372707.55604.21726888889.ms', '/Volumes/D1/proc/AC974.110214/AC974.sb3282289.eb3372708.55606.21154611111.ms', '/Volumes/D1/proc/AC974.110216/AC974.sb3282289.eb3372709.55608.19656930555.ms', '/Volumes/D1/proc/AC974.110217/AC974.sb3282289.eb3372710.55609.20419065972.ms', '/Volumes/D1/proc/AC974.110218/AC974.sb3282289.eb3372711.55610.18910030092.ms', '/Volumes/D1/proc/AC974.110219/AC974.sb3282289.eb3372712.55611.200792627315.ms', '/Volumes/D1/proc/AC974.110221/AC974.sb3282289.eb3372713.55613.19257357639.ms', '/Volumes/D1/proc/AC974.110224/AC974.sb3282289.eb3372714.55616.27802989583.ms', '/Volumes/D1/proc/AC974.110226/AC974.sb3282289.eb3372715.55618.305010428245.ms', '/Volumes/D1/proc/AC974.110227/AC974.sb3282289.eb3372716_000.55619.25416130787.ms', '/Volumes/D1/proc/AC974.110306/AC974.sb3282289.eb3372717.55626.21851298611.ms', '/Volumes/D1/proc/AC974.110312/AC974.sb3282289.eb3372718.55632.18241631945.ms', '/Volumes/D1/proc/AC974.110428/AC974.sb3848174.eb3850825.55679.073782673615.ms']
    18


.. parsed-literal::

    2019-12-12 21:13:39	INFO	mstransform::::casa	##########################################
    2019-12-12 21:13:39	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 21:13:39	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.100329/AC974_sb1178393_1.55284.176880300925.ms', outputvis='AC974.100329.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 21:13:40	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 21:13:40	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 21:13:40	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 21:13:40	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.100329/AC974_sb1178393_1.55284.176880300925.ms
    2019-12-12 21:13:40	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 21:13:40	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.100329.ms
    2019-12-12 21:13:40	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 21:13:40	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 21:13:40	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 21:13:40	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 21:13:40	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 21:13:40	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 21:13:40	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 21:13:40	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 21:13:40	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 21:13:40	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 21:13:40	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 21:13:40	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 21:13:40	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 21:13:40	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 21:13:40	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 21:13:40	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 21:13:40	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 21:13:40	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 21:13:40	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 21:13:40	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 21:13:40	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 21:13:40	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 21:13:40	INFO	MSTransformManager::open	Select data
    2019-12-12 21:13:40	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 21:13:55	INFO	MSTransformDataHandler::makeSelection	7303515 out of 12808048 rows are going to be considered due to the selection criteria.
    2019-12-12 21:13:56	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 21:13:56	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 21:13:56	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 21:13:56	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 21:13:56	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 21:13:56	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 21:13:56	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 21:13:56	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.5662e+10 Hz
    2019-12-12 21:13:56	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 2e+06 Hz
    2019-12-12 21:13:56	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 21:13:56	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.56e+08 Hz
    2019-12-12 21:13:56	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.5534e+10 Hz, upper edge = 4.579e+10 Hz
    2019-12-12 21:13:56	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553499637e+10 Hz, last channel = 4.578899635e+10 Hz, first width = 1.999999840e+06 Hz, last width = 1.999999840e+06 Hz
    2019-12-12 21:13:56	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 21:13:56	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 21:13:56	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 21:13:56	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 21:13:56	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 21:13:59	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 21:14:26	WARN	MSTransformManager::combineCubeOfData	Detected combination of SPWs with different EXPOSURE 
    2019-12-12 21:14:26	WARN	MSTransformManager::combineCubeOfData+	Will use WEIGHT to combine them (WEIGHT_SPECTRUM not available)
    2019-12-12 21:20:45	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 21:20:45	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 15:13:39.477294 End time: 2019-12-12 15:20:44.918468
    2019-12-12 21:20:45	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 21:20:45	INFO	mstransform::::casa	##########################################
    2019-12-12 21:20:45	INFO	mstransform::::casa	##########################################
    2019-12-12 21:20:45	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 21:20:45	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.100404/AC974_sb1178393_1.55290.15952814815.ms', outputvis='AC974.100404.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 21:20:46	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 21:20:46	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 21:20:46	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 21:20:46	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.100404/AC974_sb1178393_1.55290.15952814815.ms
    2019-12-12 21:20:46	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 21:20:46	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.100404.ms
    2019-12-12 21:20:46	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 21:20:46	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 21:20:46	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 21:20:46	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 21:20:46	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 21:20:46	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 21:20:46	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 21:20:46	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 21:20:46	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 21:20:46	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 21:20:46	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 21:20:46	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 21:20:46	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 21:20:46	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 21:20:46	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 21:20:46	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 21:20:46	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 21:20:46	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 21:20:46	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 21:20:46	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 21:20:46	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 21:20:46	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 21:20:46	INFO	MSTransformManager::open	Select data
    2019-12-12 21:20:46	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 21:21:06	INFO	MSTransformDataHandler::makeSelection	8367937 out of 12685329 rows are going to be considered due to the selection criteria.
    2019-12-12 21:21:08	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 21:21:08	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 21:21:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 21:21:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 21:21:08	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 21:21:08	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 21:21:08	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 21:21:08	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56622e+10 Hz
    2019-12-12 21:21:08	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 2.00001e+06 Hz
    2019-12-12 21:21:08	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 21:21:08	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.56001e+08 Hz
    2019-12-12 21:21:08	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55342e+10 Hz, upper edge = 4.57902e+10 Hz
    2019-12-12 21:21:08	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553517972e+10 Hz, last channel = 4.578918072e+10 Hz, first width = 2.000007894e+06 Hz, last width = 2.000007894e+06 Hz
    2019-12-12 21:21:08	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 21:21:08	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 21:21:08	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 21:21:08	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 21:21:08	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 21:21:12	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 21:26:34	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 21:26:34	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 15:20:45.179512 End time: 2019-12-12 15:26:33.512044
    2019-12-12 21:26:34	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 21:26:34	INFO	mstransform::::casa	##########################################
    2019-12-12 21:26:34	INFO	mstransform::::casa	##########################################
    2019-12-12 21:26:34	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 21:26:34	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.100408/AC974_sb1178393_1_000.55294.19113723379.ms', outputvis='AC974.100408.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 21:26:34	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 21:26:34	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 21:26:34	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 21:26:34	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.100408/AC974_sb1178393_1_000.55294.19113723379.ms
    2019-12-12 21:26:34	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 21:26:34	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.100408.ms
    2019-12-12 21:26:34	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 21:26:34	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 21:26:34	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 21:26:34	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 21:26:34	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 21:26:34	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 21:26:34	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 21:26:34	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 21:26:34	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 21:26:34	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 21:26:34	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 21:26:34	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 21:26:34	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 21:26:34	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 21:26:34	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 21:26:34	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 21:26:34	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 21:26:34	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 21:26:34	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 21:26:34	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 21:26:34	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 21:26:34	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 21:26:34	INFO	MSTransformManager::open	Select data
    2019-12-12 21:26:34	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 21:26:51	INFO	MSTransformDataHandler::makeSelection	7851759 out of 13403168 rows are going to be considered due to the selection criteria.
    2019-12-12 21:26:52	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 21:26:52	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 21:26:52	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 21:26:52	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 21:26:52	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 21:26:52	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 21:26:52	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 21:26:52	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56623e+10 Hz
    2019-12-12 21:26:52	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 2.00001e+06 Hz
    2019-12-12 21:26:52	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 21:26:52	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.56002e+08 Hz
    2019-12-12 21:26:52	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55343e+10 Hz, upper edge = 4.57903e+10 Hz
    2019-12-12 21:26:52	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553529912e+10 Hz, last channel = 4.578930078e+10 Hz, first width = 2.000013138e+06 Hz, last width = 2.000013138e+06 Hz
    2019-12-12 21:26:52	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 21:26:52	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 21:26:52	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 21:26:52	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 21:26:52	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 21:26:56	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 21:31:03	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 21:31:03	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 15:26:33.714940 End time: 2019-12-12 15:31:02.900550
    2019-12-12 21:31:03	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 21:31:03	INFO	mstransform::::casa	##########################################
    2019-12-12 21:31:03	INFO	mstransform::::casa	##########################################
    2019-12-12 21:31:03	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 21:31:03	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.100409/AC974_sb1178393_1.55295.14680190972.ms', outputvis='AC974.100409.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 21:31:03	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 21:31:03	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 21:31:03	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 21:31:03	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.100409/AC974_sb1178393_1.55295.14680190972.ms
    2019-12-12 21:31:03	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 21:31:03	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.100409.ms
    2019-12-12 21:31:03	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 21:31:03	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 21:31:03	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 21:31:03	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 21:31:03	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 21:31:03	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 21:31:03	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 21:31:03	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 21:31:03	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 21:31:03	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 21:31:03	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 21:31:03	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 21:31:03	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 21:31:03	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 21:31:03	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 21:31:03	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 21:31:03	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 21:31:03	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [2]
    2019-12-12 21:31:03	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 21:31:03	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 21:31:03	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 21:31:03	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 21:31:03	INFO	MSTransformManager::open	Select data
    2019-12-12 21:31:03	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 21:31:18	INFO	MSTransformDataHandler::makeSelection	8835468 out of 13020370 rows are going to be considered due to the selection criteria.
    2019-12-12 21:31:19	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 21:31:19	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 21:31:19	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 21:31:19	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 21:31:19	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 21:31:19	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 21:31:19	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 21:31:19	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56623e+10 Hz
    2019-12-12 21:31:19	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 2.00001e+06 Hz
    2019-12-12 21:31:19	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 21:31:19	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.56002e+08 Hz
    2019-12-12 21:31:19	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55343e+10 Hz, upper edge = 4.57903e+10 Hz
    2019-12-12 21:31:19	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553531901e+10 Hz, last channel = 4.578932079e+10 Hz, first width = 2.000014012e+06 Hz, last width = 2.000014012e+06 Hz
    2019-12-12 21:31:19	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 21:31:19	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 21:31:19	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 21:31:19	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 21:31:19	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 21:31:23	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 21:34:25	WARN	MSTransformManager::combineCubeOfData	Detected combination of SPWs with different EXPOSURE 
    2019-12-12 21:34:25	WARN	MSTransformManager::combineCubeOfData+	Will use WEIGHT to combine them (WEIGHT_SPECTRUM not available)
    2019-12-12 21:35:42	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 21:35:42	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 15:31:03.091836 End time: 2019-12-12 15:35:41.847386
    2019-12-12 21:35:42	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 21:35:42	INFO	mstransform::::casa	##########################################
    2019-12-12 21:35:42	INFO	mstransform::::casa	##########################################
    2019-12-12 21:35:42	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 21:35:42	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110211/AC974.sb3282289.eb3372706.55603.30302575231.ms', outputvis='AC974.110211.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 21:35:42	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 21:35:42	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 21:35:42	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 21:35:42	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110211/AC974.sb3282289.eb3372706.55603.30302575231.ms
    2019-12-12 21:35:42	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 21:35:42	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110211.ms
    2019-12-12 21:35:42	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 21:35:42	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 21:35:42	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 21:35:42	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 21:35:42	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 21:35:42	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 21:35:42	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 21:35:42	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 21:35:42	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 21:35:42	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 21:35:42	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 21:35:42	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 21:35:42	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 21:35:42	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 21:35:42	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 21:35:42	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 21:35:42	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 21:35:42	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 21:35:42	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 21:35:42	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 21:35:42	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 21:35:42	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 21:35:42	INFO	MSTransformManager::open	Select data
    2019-12-12 21:35:42	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 21:35:59	INFO	MSTransformDataHandler::makeSelection	8282856 out of 12829641 rows are going to be considered due to the selection criteria.
    2019-12-12 21:41:15	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 21:41:15	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 21:41:15	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 21:41:15	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 21:41:15	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 21:41:15	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 21:41:15	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 21:41:15	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56602e+10 Hz
    2019-12-12 21:41:15	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99992e+06 Hz
    2019-12-12 21:41:15	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 21:41:15	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.5599e+08 Hz
    2019-12-12 21:41:15	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55322e+10 Hz, upper edge = 4.57882e+10 Hz
    2019-12-12 21:41:15	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553317044e+10 Hz, last channel = 4.578716023e+10 Hz, first width = 1.999919641e+06 Hz, last width = 1.999919641e+06 Hz
    2019-12-12 21:41:15	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 21:41:15	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 21:41:15	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 21:41:15	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 21:41:15	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 21:41:15	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 21:41:29	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 21:41:34	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 21:42:30	WARN	MSTransformManager::combineCubeOfData	Detected combination of SPWs with different EXPOSURE 
    2019-12-12 21:42:30	WARN	MSTransformManager::combineCubeOfData+	Will use WEIGHT to combine them (WEIGHT_SPECTRUM not available)
    2019-12-12 21:45:21	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 21:45:21	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 15:35:42.060891 End time: 2019-12-12 15:45:21.065694
    2019-12-12 21:45:21	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 21:45:21	INFO	mstransform::::casa	##########################################
    2019-12-12 21:45:21	INFO	mstransform::::casa	##########################################
    2019-12-12 21:45:21	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 21:45:21	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110212/AC974.sb3282289.eb3372707.55604.21726888889.ms', outputvis='AC974.110212.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 21:45:22	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 21:45:22	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 21:45:22	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 21:45:22	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110212/AC974.sb3282289.eb3372707.55604.21726888889.ms
    2019-12-12 21:45:22	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 21:45:22	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110212.ms
    2019-12-12 21:45:22	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 21:45:22	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 21:45:22	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 21:45:22	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 21:45:22	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 21:45:22	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 21:45:22	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 21:45:22	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 21:45:22	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 21:45:22	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 21:45:22	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 21:45:22	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 21:45:22	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 21:45:22	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 21:45:22	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 21:45:22	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 21:45:22	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 21:45:22	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 21:45:22	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 21:45:22	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 21:45:22	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 21:45:22	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 21:45:22	INFO	MSTransformManager::open	Select data
    2019-12-12 21:45:22	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 21:45:39	INFO	MSTransformDataHandler::makeSelection	9979501 out of 14122679 rows are going to be considered due to the selection criteria.
    2019-12-12 21:51:02	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 21:51:02	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 21:51:02	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 21:51:02	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 21:51:02	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 21:51:02	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 21:51:02	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 21:51:02	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56602e+10 Hz
    2019-12-12 21:51:02	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99992e+06 Hz
    2019-12-12 21:51:02	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 21:51:02	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.5599e+08 Hz
    2019-12-12 21:51:02	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55322e+10 Hz, upper edge = 4.57882e+10 Hz
    2019-12-12 21:51:02	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553320218e+10 Hz, last channel = 4.578719216e+10 Hz, first width = 1.999921036e+06 Hz, last width = 1.999921036e+06 Hz
    2019-12-12 21:51:02	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 21:51:02	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 21:51:02	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 21:51:02	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 21:51:02	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 21:51:02	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 21:51:16	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 21:51:21	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 21:56:05	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 21:56:05	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 15:45:21.262288 End time: 2019-12-12 15:56:04.771898
    2019-12-12 21:56:05	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 21:56:05	INFO	mstransform::::casa	##########################################
    2019-12-12 21:56:05	INFO	mstransform::::casa	##########################################
    2019-12-12 21:56:05	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 21:56:05	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110214/AC974.sb3282289.eb3372708.55606.21154611111.ms', outputvis='AC974.110214.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 21:56:05	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 21:56:05	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 21:56:05	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 21:56:05	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110214/AC974.sb3282289.eb3372708.55606.21154611111.ms
    2019-12-12 21:56:05	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 21:56:05	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110214.ms
    2019-12-12 21:56:05	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 21:56:05	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 21:56:05	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 21:56:05	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 21:56:05	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 21:56:05	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 21:56:05	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 21:56:05	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 21:56:05	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 21:56:05	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 21:56:05	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 21:56:05	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 21:56:05	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 21:56:05	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 21:56:05	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 21:56:05	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 21:56:05	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 21:56:05	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 21:56:05	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 21:56:05	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 21:56:05	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 21:56:05	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 21:56:05	INFO	MSTransformManager::open	Select data
    2019-12-12 21:56:05	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 21:56:27	INFO	MSTransformDataHandler::makeSelection	10876837 out of 14181298 rows are going to be considered due to the selection criteria.
    2019-12-12 22:01:31	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 22:01:31	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 22:01:31	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 22:01:31	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 22:01:31	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 22:01:31	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 22:01:31	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 22:01:31	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56603e+10 Hz
    2019-12-12 22:01:31	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99992e+06 Hz
    2019-12-12 22:01:31	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 22:01:31	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.5599e+08 Hz
    2019-12-12 22:01:31	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55323e+10 Hz, upper edge = 4.57883e+10 Hz
    2019-12-12 22:01:31	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553328753e+10 Hz, last channel = 4.578727798e+10 Hz, first width = 1.999924785e+06 Hz, last width = 1.999924785e+06 Hz
    2019-12-12 22:01:31	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 22:01:31	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 22:01:31	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 22:01:31	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 22:01:31	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 22:01:31	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 22:01:44	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 22:01:50	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 22:06:30	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 22:06:30	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 15:56:04.954313 End time: 2019-12-12 16:06:30.391054
    2019-12-12 22:06:30	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 22:06:30	INFO	mstransform::::casa	##########################################
    2019-12-12 22:06:31	INFO	mstransform::::casa	##########################################
    2019-12-12 22:06:31	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 22:06:31	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110216/AC974.sb3282289.eb3372709.55608.19656930555.ms', outputvis='AC974.110216.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 22:06:31	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 22:06:31	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 22:06:31	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 22:06:31	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110216/AC974.sb3282289.eb3372709.55608.19656930555.ms
    2019-12-12 22:06:31	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 22:06:31	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110216.ms
    2019-12-12 22:06:31	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 22:06:31	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 22:06:31	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 22:06:31	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 22:06:31	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 22:06:31	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 22:06:31	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 22:06:31	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 22:06:31	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 22:06:31	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 22:06:31	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 22:06:31	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 22:06:31	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 22:06:31	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 22:06:31	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 22:06:31	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 22:06:31	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 22:06:31	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 22:06:31	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 22:06:31	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 22:06:31	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 22:06:31	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 22:06:31	INFO	MSTransformManager::open	Select data
    2019-12-12 22:06:31	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 22:06:45	INFO	MSTransformDataHandler::makeSelection	8712774 out of 14325602 rows are going to be considered due to the selection criteria.
    2019-12-12 22:11:24	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 22:11:24	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 22:11:24	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 22:11:24	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 22:11:24	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 22:11:24	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 22:11:24	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 22:11:24	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56604e+10 Hz
    2019-12-12 22:11:24	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99993e+06 Hz
    2019-12-12 22:11:24	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 22:11:24	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55991e+08 Hz
    2019-12-12 22:11:24	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55324e+10 Hz, upper edge = 4.57884e+10 Hz
    2019-12-12 22:11:24	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553337281e+10 Hz, last channel = 4.578736374e+10 Hz, first width = 1.999928530e+06 Hz, last width = 1.999928530e+06 Hz
    2019-12-12 22:11:24	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 22:11:24	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 22:11:24	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 22:11:24	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 22:11:24	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 22:11:24	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 22:11:37	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 22:11:40	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 22:15:16	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 22:15:16	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 16:06:30.715326 End time: 2019-12-12 16:15:16.312736
    2019-12-12 22:15:16	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 22:15:16	INFO	mstransform::::casa	##########################################
    2019-12-12 22:15:16	INFO	mstransform::::casa	##########################################
    2019-12-12 22:15:16	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 22:15:16	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110217/AC974.sb3282289.eb3372710.55609.20419065972.ms', outputvis='AC974.110217.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 22:15:17	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 22:15:17	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 22:15:17	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 22:15:17	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110217/AC974.sb3282289.eb3372710.55609.20419065972.ms
    2019-12-12 22:15:17	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 22:15:17	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110217.ms
    2019-12-12 22:15:17	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 22:15:17	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 22:15:17	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 22:15:17	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 22:15:17	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 22:15:17	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 22:15:17	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 22:15:17	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 22:15:17	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 22:15:17	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 22:15:17	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 22:15:17	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 22:15:17	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 22:15:17	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 22:15:17	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 22:15:17	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 22:15:17	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 22:15:17	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 22:15:17	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 22:15:17	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 22:15:17	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 22:15:17	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 22:15:17	INFO	MSTransformManager::open	Select data
    2019-12-12 22:15:17	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 22:15:32	INFO	MSTransformDataHandler::makeSelection	9185008 out of 13123452 rows are going to be considered due to the selection criteria.
    2019-12-12 22:19:58	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 22:19:58	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 22:19:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 22:19:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 22:19:58	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 22:19:58	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 22:19:58	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 22:19:58	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56604e+10 Hz
    2019-12-12 22:19:58	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99993e+06 Hz
    2019-12-12 22:19:58	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 22:19:58	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55991e+08 Hz
    2019-12-12 22:19:58	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55324e+10 Hz, upper edge = 4.57884e+10 Hz
    2019-12-12 22:19:58	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553341541e+10 Hz, last channel = 4.578740657e+10 Hz, first width = 1.999930401e+06 Hz, last width = 1.999930401e+06 Hz
    2019-12-12 22:19:58	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 22:19:58	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 22:19:58	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 22:19:58	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 22:19:58	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 22:19:58	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 22:20:10	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 22:20:14	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 22:23:38	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 22:23:38	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 16:15:16.478489 End time: 2019-12-12 16:23:38.222787
    2019-12-12 22:23:38	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 22:23:38	INFO	mstransform::::casa	##########################################
    2019-12-12 22:23:38	INFO	mstransform::::casa	##########################################
    2019-12-12 22:23:38	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 22:23:38	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110218/AC974.sb3282289.eb3372711.55610.18910030092.ms', outputvis='AC974.110218.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 22:23:39	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 22:23:39	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 22:23:39	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 22:23:39	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110218/AC974.sb3282289.eb3372711.55610.18910030092.ms
    2019-12-12 22:23:39	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 22:23:39	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110218.ms
    2019-12-12 22:23:39	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 22:23:39	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 22:23:39	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 22:23:39	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 22:23:39	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 22:23:39	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 22:23:39	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 22:23:39	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 22:23:39	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 22:23:39	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 22:23:39	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 22:23:39	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 22:23:39	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 22:23:39	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 22:23:39	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 22:23:39	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 22:23:39	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 22:23:39	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 22:23:39	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 22:23:39	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 22:23:39	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 22:23:39	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 22:23:39	INFO	MSTransformManager::open	Select data
    2019-12-12 22:23:39	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 22:23:55	INFO	MSTransformDataHandler::makeSelection	10186152 out of 13163710 rows are going to be considered due to the selection criteria.
    2019-12-12 22:28:24	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 22:28:24	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 22:28:24	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 22:28:24	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 22:28:24	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 22:28:24	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 22:28:24	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 22:28:24	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56605e+10 Hz
    2019-12-12 22:28:24	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99993e+06 Hz
    2019-12-12 22:28:24	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 22:28:24	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55991e+08 Hz
    2019-12-12 22:28:24	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55325e+10 Hz, upper edge = 4.57884e+10 Hz
    2019-12-12 22:28:24	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553345797e+10 Hz, last channel = 4.578744937e+10 Hz, first width = 1.999932271e+06 Hz, last width = 1.999932271e+06 Hz
    2019-12-12 22:28:24	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 22:28:24	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 22:28:24	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 22:28:24	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 22:28:24	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 22:28:24	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 22:28:36	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 22:28:40	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 22:32:28	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 22:32:28	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 16:23:38.403276 End time: 2019-12-12 16:32:28.395304
    2019-12-12 22:32:28	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 22:32:28	INFO	mstransform::::casa	##########################################
    2019-12-12 22:32:29	INFO	mstransform::::casa	##########################################
    2019-12-12 22:32:29	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 22:32:29	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110219/AC974.sb3282289.eb3372712.55611.200792627315.ms', outputvis='AC974.110219.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 22:32:29	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 22:32:29	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 22:32:29	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 22:32:29	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110219/AC974.sb3282289.eb3372712.55611.200792627315.ms
    2019-12-12 22:32:29	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 22:32:29	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110219.ms
    2019-12-12 22:32:29	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 22:32:29	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 22:32:29	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 22:32:29	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 22:32:29	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 22:32:29	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 22:32:29	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 22:32:29	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 22:32:29	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 22:32:29	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 22:32:29	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 22:32:29	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 22:32:29	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 22:32:29	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 22:32:29	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 22:32:29	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 22:32:29	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 22:32:29	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 22:32:29	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 22:32:29	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 22:32:29	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 22:32:29	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 22:32:29	INFO	MSTransformManager::open	Select data
    2019-12-12 22:32:29	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 22:32:45	INFO	MSTransformDataHandler::makeSelection	10466882 out of 14224133 rows are going to be considered due to the selection criteria.
    2019-12-12 22:37:07	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 22:37:07	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 22:37:07	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 22:37:07	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 22:37:07	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 22:37:07	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 22:37:07	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 22:37:07	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56605e+10 Hz
    2019-12-12 22:37:07	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99993e+06 Hz
    2019-12-12 22:37:07	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 22:37:07	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55992e+08 Hz
    2019-12-12 22:37:07	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55325e+10 Hz, upper edge = 4.57885e+10 Hz
    2019-12-12 22:37:07	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553350083e+10 Hz, last channel = 4.578749247e+10 Hz, first width = 1.999934153e+06 Hz, last width = 1.999934153e+06 Hz
    2019-12-12 22:37:07	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 22:37:07	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 22:37:07	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 22:37:07	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 22:37:07	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 22:37:07	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 22:37:19	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 22:37:23	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 22:41:06	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 22:41:06	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 16:32:28.588900 End time: 2019-12-12 16:41:05.744280
    2019-12-12 22:41:06	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 22:41:06	INFO	mstransform::::casa	##########################################
    2019-12-12 22:41:06	INFO	mstransform::::casa	##########################################
    2019-12-12 22:41:06	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 22:41:06	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110221/AC974.sb3282289.eb3372713.55613.19257357639.ms', outputvis='AC974.110221.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 22:41:06	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 22:41:06	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 22:41:06	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 22:41:06	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110221/AC974.sb3282289.eb3372713.55613.19257357639.ms
    2019-12-12 22:41:06	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 22:41:06	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110221.ms
    2019-12-12 22:41:06	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 22:41:06	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 22:41:06	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 22:41:06	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 22:41:06	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 22:41:06	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 22:41:06	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 22:41:06	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 22:41:06	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 22:41:06	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 22:41:06	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 22:41:06	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 22:41:06	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 22:41:06	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 22:41:06	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 22:41:06	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 22:41:06	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 22:41:06	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 22:41:06	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 22:41:06	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 22:41:06	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 22:41:06	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 22:41:06	INFO	MSTransformManager::open	Select data
    2019-12-12 22:41:06	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 22:41:23	INFO	MSTransformDataHandler::makeSelection	10980929 out of 13692028 rows are going to be considered due to the selection criteria.
    2019-12-12 22:45:54	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 22:45:54	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 22:45:54	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 22:45:54	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 22:45:54	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 22:45:54	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 22:45:54	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 22:45:54	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56606e+10 Hz
    2019-12-12 22:45:54	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99994e+06 Hz
    2019-12-12 22:45:54	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 22:45:54	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55992e+08 Hz
    2019-12-12 22:45:54	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55326e+10 Hz, upper edge = 4.57886e+10 Hz
    2019-12-12 22:45:54	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553358552e+10 Hz, last channel = 4.578757763e+10 Hz, first width = 1.999937873e+06 Hz, last width = 1.999937873e+06 Hz
    2019-12-12 22:45:54	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 22:45:54	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 22:45:54	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 22:45:54	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 22:45:54	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 22:45:54	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 22:46:06	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 22:46:10	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 22:51:14	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 22:51:14	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 16:41:06.096449 End time: 2019-12-12 16:51:13.812185
    2019-12-12 22:51:14	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 22:51:14	INFO	mstransform::::casa	##########################################
    2019-12-12 22:51:14	INFO	mstransform::::casa	##########################################
    2019-12-12 22:51:14	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 22:51:14	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110224/AC974.sb3282289.eb3372714.55616.27802989583.ms', outputvis='AC974.110224.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 22:51:14	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 22:51:14	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 22:51:14	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 22:51:14	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110224/AC974.sb3282289.eb3372714.55616.27802989583.ms
    2019-12-12 22:51:14	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 22:51:14	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110224.ms
    2019-12-12 22:51:14	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 22:51:14	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 22:51:14	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 22:51:14	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 22:51:14	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 22:51:14	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 22:51:14	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 22:51:14	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 22:51:14	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 22:51:14	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 22:51:14	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 22:51:14	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 22:51:14	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 22:51:14	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 22:51:14	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 22:51:14	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 22:51:14	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 22:51:14	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 22:51:14	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 22:51:14	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 22:51:14	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 22:51:14	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 22:51:14	INFO	MSTransformManager::open	Select data
    2019-12-12 22:51:14	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 22:51:31	INFO	MSTransformDataHandler::makeSelection	10105141 out of 13095912 rows are going to be considered due to the selection criteria.
    2019-12-12 22:55:44	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 22:55:44	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 22:55:44	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 22:55:44	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 22:55:44	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 22:55:44	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 22:55:44	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 22:55:44	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56607e+10 Hz
    2019-12-12 22:55:44	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99994e+06 Hz
    2019-12-12 22:55:44	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 22:55:44	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55993e+08 Hz
    2019-12-12 22:55:44	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55327e+10 Hz, upper edge = 4.57887e+10 Hz
    2019-12-12 22:55:44	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553372552e+10 Hz, last channel = 4.578771841e+10 Hz, first width = 1.999944022e+06 Hz, last width = 1.999944022e+06 Hz
    2019-12-12 22:55:44	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 22:55:44	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 22:55:44	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 22:55:44	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 22:55:44	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 22:55:44	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 22:55:56	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 22:56:00	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 23:00:28	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 23:00:28	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 16:51:14.087578 End time: 2019-12-12 17:00:27.696466
    2019-12-12 23:00:28	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 23:00:28	INFO	mstransform::::casa	##########################################
    2019-12-12 23:00:28	INFO	mstransform::::casa	##########################################
    2019-12-12 23:00:28	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 23:00:28	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110226/AC974.sb3282289.eb3372715.55618.305010428245.ms', outputvis='AC974.110226.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 23:00:28	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 23:00:28	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 23:00:28	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 23:00:28	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110226/AC974.sb3282289.eb3372715.55618.305010428245.ms
    2019-12-12 23:00:28	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 23:00:28	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110226.ms
    2019-12-12 23:00:28	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 23:00:28	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 23:00:28	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 23:00:28	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 23:00:28	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 23:00:28	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 23:00:28	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 23:00:28	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 23:00:28	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 23:00:28	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 23:00:28	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 23:00:28	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 23:00:28	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 23:00:28	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 23:00:28	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 23:00:28	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 23:00:28	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 23:00:28	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 23:00:28	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 23:00:28	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 23:00:28	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 23:00:28	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 23:00:28	INFO	MSTransformManager::open	Select data
    2019-12-12 23:00:28	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 23:00:45	INFO	MSTransformDataHandler::makeSelection	11326247 out of 13228256 rows are going to be considered due to the selection criteria.
    2019-12-12 23:04:52	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 23:04:52	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 23:04:52	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 23:04:52	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 23:04:52	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 23:04:52	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 23:04:52	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 23:04:52	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56608e+10 Hz
    2019-12-12 23:04:52	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99995e+06 Hz
    2019-12-12 23:04:52	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 23:04:52	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55993e+08 Hz
    2019-12-12 23:04:52	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55328e+10 Hz, upper edge = 4.57888e+10 Hz
    2019-12-12 23:04:52	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553381587e+10 Hz, last channel = 4.578780926e+10 Hz, first width = 1.999947990e+06 Hz, last width = 1.999947990e+06 Hz
    2019-12-12 23:04:52	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 23:04:52	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 23:04:52	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 23:04:52	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 23:04:52	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 23:04:52	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 23:05:03	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 23:05:07	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 23:09:06	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 23:09:06	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 17:00:28.044549 End time: 2019-12-12 17:09:06.072133
    2019-12-12 23:09:06	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 23:09:06	INFO	mstransform::::casa	##########################################
    2019-12-12 23:09:06	INFO	mstransform::::casa	##########################################
    2019-12-12 23:09:06	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 23:09:06	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110227/AC974.sb3282289.eb3372716_000.55619.25416130787.ms', outputvis='AC974.110227.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 23:09:06	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 23:09:06	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 23:09:06	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 23:09:06	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110227/AC974.sb3282289.eb3372716_000.55619.25416130787.ms
    2019-12-12 23:09:06	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 23:09:06	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110227.ms
    2019-12-12 23:09:06	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 23:09:06	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 23:09:06	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 23:09:06	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 23:09:06	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 23:09:06	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 23:09:06	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 23:09:06	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 23:09:06	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 23:09:06	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 23:09:06	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 23:09:06	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 23:09:06	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 23:09:06	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 23:09:06	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 23:09:06	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 23:09:06	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 23:09:06	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 23:09:06	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 23:09:06	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 23:09:06	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 23:09:06	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 23:09:06	INFO	MSTransformManager::open	Select data
    2019-12-12 23:09:06	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 23:09:21	INFO	MSTransformDataHandler::makeSelection	9732796 out of 12508216 rows are going to be considered due to the selection criteria.
    2019-12-12 23:13:23	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 23:13:23	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 23:13:23	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 23:13:23	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 23:13:23	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 23:13:23	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 23:13:23	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 23:13:23	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56608e+10 Hz
    2019-12-12 23:13:23	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99995e+06 Hz
    2019-12-12 23:13:23	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 23:13:23	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55994e+08 Hz
    2019-12-12 23:13:23	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55328e+10 Hz, upper edge = 4.57888e+10 Hz
    2019-12-12 23:13:23	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553384994e+10 Hz, last channel = 4.578784353e+10 Hz, first width = 1.999949487e+06 Hz, last width = 1.999949487e+06 Hz
    2019-12-12 23:13:23	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 23:13:23	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 23:13:23	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 23:13:23	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 23:13:23	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 23:13:23	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 23:13:34	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 23:13:38	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 23:17:16	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 23:17:16	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 17:09:06.234953 End time: 2019-12-12 17:17:15.692100
    2019-12-12 23:17:16	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 23:17:16	INFO	mstransform::::casa	##########################################
    2019-12-12 23:17:16	INFO	mstransform::::casa	##########################################
    2019-12-12 23:17:16	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 23:17:16	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110306/AC974.sb3282289.eb3372717.55626.21851298611.ms', outputvis='AC974.110306.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 23:17:16	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 23:17:16	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 23:17:16	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 23:17:16	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110306/AC974.sb3282289.eb3372717.55626.21851298611.ms
    2019-12-12 23:17:16	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 23:17:16	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110306.ms
    2019-12-12 23:17:16	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 23:17:16	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 23:17:16	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 23:17:16	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 23:17:16	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 23:17:16	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 23:17:16	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 23:17:16	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 23:17:16	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 23:17:16	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 23:17:16	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 23:17:16	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 23:17:16	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 23:17:16	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 23:17:16	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 23:17:16	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 23:17:16	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 23:17:16	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 23:17:16	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 23:17:16	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 23:17:16	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 23:17:16	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 23:17:16	INFO	MSTransformManager::open	Select data
    2019-12-12 23:17:16	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 23:17:33	INFO	MSTransformDataHandler::makeSelection	11200851 out of 14200294 rows are going to be considered due to the selection criteria.
    2019-12-12 23:21:41	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 23:21:41	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 23:21:41	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 23:21:41	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 23:21:41	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 23:21:41	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 23:21:42	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 23:21:42	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56611e+10 Hz
    2019-12-12 23:21:42	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99996e+06 Hz
    2019-12-12 23:21:42	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 23:21:42	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55995e+08 Hz
    2019-12-12 23:21:42	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55331e+10 Hz, upper edge = 4.57891e+10 Hz
    2019-12-12 23:21:42	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553413789e+10 Hz, last channel = 4.578813308e+10 Hz, first width = 1.999962134e+06 Hz, last width = 1.999962134e+06 Hz
    2019-12-12 23:21:42	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 23:21:42	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 23:21:42	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 23:21:42	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 23:21:42	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 23:21:42	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 23:21:53	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 23:21:58	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 23:25:43	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 23:25:43	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 17:17:16.056184 End time: 2019-12-12 17:25:43.437518
    2019-12-12 23:25:43	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 23:25:43	INFO	mstransform::::casa	##########################################
    2019-12-12 23:25:44	INFO	mstransform::::casa	##########################################
    2019-12-12 23:25:44	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 23:25:44	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110312/AC974.sb3282289.eb3372718.55632.18241631945.ms', outputvis='AC974.110312.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 23:25:44	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 23:25:44	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 23:25:44	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 23:25:44	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110312/AC974.sb3282289.eb3372718.55632.18241631945.ms
    2019-12-12 23:25:44	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 23:25:44	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110312.ms
    2019-12-12 23:25:44	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 23:25:44	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 23:25:44	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 23:25:44	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 23:25:44	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 23:25:44	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 23:25:44	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 23:25:44	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 23:25:44	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 23:25:44	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 23:25:44	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 23:25:44	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 23:25:44	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 23:25:44	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 23:25:44	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 23:25:44	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 23:25:44	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 23:25:44	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 23:25:44	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 23:25:44	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 23:25:44	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 23:25:44	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 23:25:44	INFO	MSTransformManager::open	Select data
    2019-12-12 23:25:44	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 23:26:03	INFO	MSTransformDataHandler::makeSelection	12141576 out of 14114042 rows are going to be considered due to the selection criteria.
    2019-12-12 23:30:12	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 23:30:12	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 23:30:12	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 23:30:12	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 23:30:12	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 23:30:12	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 23:30:13	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 23:30:13	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56614e+10 Hz
    2019-12-12 23:30:13	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99997e+06 Hz
    2019-12-12 23:30:13	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 23:30:13	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.55996e+08 Hz
    2019-12-12 23:30:13	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55334e+10 Hz, upper edge = 4.57894e+10 Hz
    2019-12-12 23:30:13	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553437441e+10 Hz, last channel = 4.578837092e+10 Hz, first width = 1.999972523e+06 Hz, last width = 1.999972523e+06 Hz
    2019-12-12 23:30:13	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 23:30:13	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 23:30:13	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 23:30:13	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 23:30:13	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 23:30:13	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 23:30:24	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 23:30:29	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 23:34:52	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 23:34:52	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 17:25:43.614334 End time: 2019-12-12 17:34:52.479483
    2019-12-12 23:34:52	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 23:34:52	INFO	mstransform::::casa	##########################################
    2019-12-12 23:34:53	INFO	mstransform::::casa	##########################################
    2019-12-12 23:34:53	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-12 23:34:53	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/proc/AC974.110428/AC974.sb3848174.eb3850825.55679.073782673615.ms', outputvis='AC974.110428.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='GN20cluster', spw='2:0~62,3:1~63', scan='', antenna='', correlation='RR,LL', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=128, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='30s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-12 23:34:53	INFO	mstransform::::casa	Combine spws 2:0~62,3:1~63 into new output spw
    2019-12-12 23:34:53	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-12 23:34:53	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-12 23:34:53	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/proc/AC974.110428/AC974.sb3848174.eb3850825.55679.073782673615.ms
    2019-12-12 23:34:53	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-12 23:34:53	INFO	MSTransformManager::parseMsSpecParams	Output file name is AC974.110428.ms
    2019-12-12 23:34:53	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-12 23:34:53	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-12 23:34:53	INFO	MSTransformManager::parseDataSelParams	field selection is GN20cluster
    2019-12-12 23:34:53	INFO	MSTransformManager::parseDataSelParams	spw selection is 2:0~62,3:1~63
    2019-12-12 23:34:53	INFO	MSTransformManager::parseDataSelParams	correlation selection is RR,LL
    2019-12-12 23:34:53	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-12 23:34:53	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-12 23:34:53	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-12 23:34:53	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-12 23:34:53	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-12 23:34:53	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 128
    2019-12-12 23:34:53	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-12-12 23:34:53	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-12 23:34:53	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-12 23:34:53	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-12 23:34:53	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 30 seconds
    2019-12-12 23:34:53	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-12 23:34:53	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-12-12 23:34:53	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [2, 4]  (NB: Matrix in Row/Column order)
    2019-12-12 23:34:53	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 62, 1
    2019-12-12 23:34:53	INFO	MSTransformManager::initDataSelectionParams+	 3, 1, 63, 1]
    2019-12-12 23:34:53	INFO	MSTransformManager::initDataSelectionParams	Selected correlations are [[[0] to [0] with stride [1], length [1], [1] to [1] with stride [1], length [1]]]
    2019-12-12 23:34:53	INFO	MSTransformManager::open	Select data
    2019-12-12 23:34:53	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-12 23:35:07	INFO	MSTransformDataHandler::makeSelection	7664456 out of 9865381 rows are going to be considered due to the selection criteria.
    2019-12-12 23:38:01	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-12 23:38:01	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-12 23:38:01	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    63 channels, first channel = 4.553300000e+10 Hz, last channel = 4.565700000e+10 Hz
    2019-12-12 23:38:01	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    63 channels, first channel = 4.565300000e+10 Hz, last channel = 4.577700000e+10 Hz
    2019-12-12 23:38:01	INFO	MSTransformManager::regridSpwAux	Combined SPW:   123 channels, first channel = 4.553300000e+10 Hz, last channel = 4.577700000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-12 23:38:01	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-12 23:38:01	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-12 23:38:01	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 4.56627e+10 Hz
    2019-12-12 23:38:01	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 2.00003e+06 Hz
    2019-12-12 23:38:01	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 128
    2019-12-12 23:38:01	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.56004e+08 Hz
    2019-12-12 23:38:01	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 4.55347e+10 Hz, upper edge = 4.57907e+10 Hz
    2019-12-12 23:38:01	INFO	MSTransformManager::regridSpwAux	Output SPW:   128 channels, first channel = 4.553570412e+10 Hz, last channel = 4.578970805e+10 Hz, first width = 2.000030927e+06 Hz, last width = 2.000030927e+06 Hz
    2019-12-12 23:38:01	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-12 23:38:01	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-12 23:38:01	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-12 23:38:01	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-12 23:38:01	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-12 23:38:01	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-12 23:38:07	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-12 23:38:10	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-12 23:41:20	INFO	mstransform::::casa	Result mstransform: True
    2019-12-12 23:41:20	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-12 17:34:52.632422 End time: 2019-12-12 17:41:20.103130
    2019-12-12 23:41:20	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-12 23:41:20	INFO	mstransform::::casa	##########################################


