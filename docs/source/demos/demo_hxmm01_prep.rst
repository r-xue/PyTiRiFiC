Example: HXMM01 (High-z Merger)
-------------------------------

Prepare visibiity data from the calibrated MS restored by the local ALMA pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load some essential Python modules + CASA 6 tasks/tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    
    import sys,os,glob,io,socket
    import logging
    from pprint import pprint
    
    import casatasks as ctasks
    import casatools as ctools
    
    # Import wurlitzer for display real-time console logs
    #   https://github.com/minrk/wurlitzer
    %reload_ext wurlitzer
    
    # for inline plots
    %matplotlib inline
    %config InlineBackend.figure_format = "retina"


Using the beta-version of CASA 6

.. code:: ipython3

    print('casatools ver:',ctools.version_string())
    print('casatasks ver:',ctasks.version_string())


.. parsed-literal::

    casatools ver: 2019.172
    casatasks ver: 2019.166


Import some convinient functions from ``rxutils``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    from rxutils.casa.proc import rmPointing  # help remove POINTING tables hidden under
    from rxutils.casa.proc import setLogfile  # help reset the casa 6 log file

11B-044 / 12A-201
~~~~~~~~~~~~~~~~~

Reduce Raw Data SIze
^^^^^^^^^^^^^^^^^^^^

::

   pick only RR / LL
   remove completed-flagged rows
   save the initial ("exported") flagging version as "Original" following the importvla() tradition

.. code:: ipython3

    import glob
    import os
    from casatasks import mstransform
    from casatasks import flagmanager
    demo_dir='/Volumes/S1/raw/12A201/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_hxmm01_prep.log')    
        
    mslist=glob.glob('*.ms')
    
    for ms in mslist:
        outms='/Volumes/S1/proc/12A201/'+ms.replace('.ms','.ms')
        os.system('rm -rf '+outms)
        mstransform(vis=ms,outputvis=outms,correlation='RR,LL',keepflags=False,datacolumn='data')
        flagmanager(vis=outms,mode='save',versionname='Original',merge='replace',\
                    comment='Original Flagging from the archive with online/shadown/zero flagging applied nad completed flagged rows are removed')


::


    ---------------------------------------------------------------------------

    FileNotFoundError                         Traceback (most recent call last)

    <ipython-input-4-03a141d40760> in <module>
          5 demo_dir='/Volumes/S1/raw/12A201/'
          6 if  'hypersion' or 'mini' in socket.gethostname() :
    ----> 7     os.chdir(demo_dir)
          8 setLogfile(demo_dir+'/'+'demo_hxmm01_prep.log')
          9 


    FileNotFoundError: [Errno 2] No such file or directory: '/Volumes/S1/raw/12A201/'


Data Calibration with the modified VLA scripted pipeline (rxpipeline)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   see ~/Documents/Library/CASA/rxpipeline for more details

Frame-Transfer (TOPO->LSRK) & SPW-combine & Time-Averging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    from casatasks import mstransform
    # Switch working directory
    
    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/hxmm01/vla/12A201/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_hxmm01.log')
    
    
    mslist=[]
    mslist.extend(glob.glob('/Volumes/S1/proc/12A201*/12A*ms'))
    mslist.extend(glob.glob('/Volumes/S1/proc/11B044*/11B*ms'))
    mslist.remove('/Volumes/S1/proc/12A201.120807/12A-201.sb9991390.eb11312240.56146.441112025466.ms')
    
    for ms in mslist:
    
        outvis=ms.split('/')[-2]
        outvis=outvis+'.ms'    
        os.system('rm -rf '+outvis)
        
        mstransform(ms,outputvis=outvis,field='5',spw='0~7',datacolumn='corrected',
                    regridms=True,outframe='lsrk',combinespws=True,mode='channel',start=0,nchan=-1,width=1,
                    timeaverage=True,timebin='60s',maxuvwdistance=0.0,interpolation='linear', 
                    keepflags=False,usewtspectrum=False)
        #rmPointing(outvis)
        


.. parsed-literal::

    2019-12-06 17:05:27	INFO	mstransform::::casa	##########################################
    2019-12-06 17:05:27	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-06 17:05:27	INFO	mstransform::::casa	mstransform( vis='/Volumes/S1/proc/12A201.120312/12A-201.sb9237873.eb9270010.55998.94909407407.ms', outputvis='12A201.120312.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='5', spw='0~7', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-06 17:05:27	INFO	mstransform::::casa	Combine spws 0~7 into new output spw
    2019-12-06 17:05:27	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-06 17:05:27	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-06 17:05:27	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/S1/proc/12A201.120312/12A-201.sb9237873.eb9270010.55998.94909407407.ms
    2019-12-06 17:05:27	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-06 17:05:27	INFO	MSTransformManager::parseMsSpecParams	Output file name is 12A201.120312.ms
    2019-12-06 17:05:27	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-06 17:05:27	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-06 17:05:27	INFO	MSTransformManager::parseDataSelParams	field selection is 5
    2019-12-06 17:05:27	INFO	MSTransformManager::parseDataSelParams	spw selection is 0~7
    2019-12-06 17:05:27	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-06 17:05:27	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-06 17:05:27	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-06 17:05:27	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-06 17:05:27	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-06 17:05:27	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is -1
    2019-12-06 17:05:27	INFO	MSTransformManager::parseFreqSpecParams	Start is 0
    2019-12-06 17:05:27	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-06 17:05:27	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-06 17:05:27	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-06 17:05:27	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-12-06 17:05:27	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [5]
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [8, 4]  (NB: Matrix in Row/Column order)
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 63, 1
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams+	 1, 0, 63, 1
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams+	 2, 0, 63, 1
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams+	 3, 0, 63, 1
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams+	 4, 0, 63, 1
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams+	 5, 0, 63, 1
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams+	 6, 0, 63, 1
    2019-12-06 17:05:27	INFO	MSTransformManager::initDataSelectionParams+	 7, 0, 63, 1]
    2019-12-06 17:05:27	INFO	MSTransformManager::open	Select data
    2019-12-06 17:05:27	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-06 17:05:32	INFO	MSTransformDataHandler::makeSelection	2854680 out of 7301327 rows are going to be considered due to the selection criteria.
    2019-12-06 17:07:08	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    64 channels, first channel = 3.428073000e+10 Hz, last channel = 3.440673000e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    64 channels, first channel = 3.440873000e+10 Hz, last channel = 3.453473000e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   2:    64 channels, first channel = 3.453673000e+10 Hz, last channel = 3.466273000e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   3:    64 channels, first channel = 3.466473000e+10 Hz, last channel = 3.479073000e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   4:    64 channels, first channel = 3.479273000e+10 Hz, last channel = 3.491873000e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   5:    64 channels, first channel = 3.492073000e+10 Hz, last channel = 3.504673000e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   6:    64 channels, first channel = 3.504873000e+10 Hz, last channel = 3.517473000e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::combineSpwsCore	   SPW   7:    64 channels, first channel = 3.517673000e+10 Hz, last channel = 3.530273000e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformManager::regridSpwAux	Combined SPW:   512 channels, first channel = 3.428073000e+10 Hz, last channel = 3.530273000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-06 17:07:08	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-06 17:07:08	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-06 17:07:08	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.47951e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 2.00019e+06 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 512
    2019-12-06 17:07:08	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.0241e+09 Hz
    2019-12-06 17:07:08	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.4283e+10 Hz, upper edge = 3.53071e+10 Hz
    2019-12-06 17:07:08	INFO	MSTransformManager::regridSpwAux	Output SPW:   512 channels, first channel = 3.428400413e+10 Hz, last channel = 3.530610174e+10 Hz, first width = 2.000191018e+06 Hz, last width = 2.000191018e+06 Hz
    2019-12-06 17:07:08	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-06 17:07:08	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-06 17:07:08	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-06 17:07:08	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-06 17:07:08	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-06 17:07:08	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-06 17:07:12	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-06 17:07:13	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-06 17:08:13	INFO	mstransform::::casa	Result mstransform: True
    2019-12-06 17:08:13	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-06 11:05:27.079098 End time: 2019-12-06 11:08:13.309785
    2019-12-06 17:08:13	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-06 17:08:13	INFO	mstransform::::casa	##########################################
    2019-12-06 17:08:13	INFO	mstransform::::casa	##########################################
    2019-12-06 17:08:13	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-06 17:08:13	INFO	mstransform::::casa	mstransform( vis='/Volumes/S1/proc/12A201.120807/12A-201.sb9991390.eb11312240.56146.441112025466_scaled.ms', outputvis='12A201.120807.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='5', spw='0~7', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-06 17:08:13	INFO	mstransform::::casa	Combine spws 0~7 into new output spw
    2019-12-06 17:08:13	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-06 17:08:13	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-06 17:08:13	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/S1/proc/12A201.120807/12A-201.sb9991390.eb11312240.56146.441112025466_scaled.ms
    2019-12-06 17:08:13	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-06 17:08:13	INFO	MSTransformManager::parseMsSpecParams	Output file name is 12A201.120807.ms
    2019-12-06 17:08:13	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-06 17:08:13	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-06 17:08:13	INFO	MSTransformManager::parseDataSelParams	field selection is 5
    2019-12-06 17:08:13	INFO	MSTransformManager::parseDataSelParams	spw selection is 0~7
    2019-12-06 17:08:13	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-06 17:08:13	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-06 17:08:13	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-06 17:08:13	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-06 17:08:13	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-06 17:08:13	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is -1
    2019-12-06 17:08:13	INFO	MSTransformManager::parseFreqSpecParams	Start is 0
    2019-12-06 17:08:13	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-06 17:08:13	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-06 17:08:13	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-06 17:08:13	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-12-06 17:08:13	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [5]
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [8, 4]  (NB: Matrix in Row/Column order)
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 63, 1
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams+	 1, 0, 63, 1
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams+	 2, 0, 63, 1
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams+	 3, 0, 63, 1
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams+	 4, 0, 63, 1
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams+	 5, 0, 63, 1
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams+	 6, 0, 63, 1
    2019-12-06 17:08:13	INFO	MSTransformManager::initDataSelectionParams+	 7, 0, 63, 1]
    2019-12-06 17:08:13	INFO	MSTransformManager::open	Select data
    2019-12-06 17:08:13	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-06 17:08:19	INFO	MSTransformDataHandler::makeSelection	3259349 out of 7554412 rows are going to be considered due to the selection criteria.
    2019-12-06 17:12:51	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    64 channels, first channel = 3.428073000e+10 Hz, last channel = 3.440673000e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    64 channels, first channel = 3.440873000e+10 Hz, last channel = 3.453473000e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   2:    64 channels, first channel = 3.453673000e+10 Hz, last channel = 3.466273000e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   3:    64 channels, first channel = 3.466473000e+10 Hz, last channel = 3.479073000e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   4:    64 channels, first channel = 3.479273000e+10 Hz, last channel = 3.491873000e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   5:    64 channels, first channel = 3.492073000e+10 Hz, last channel = 3.504673000e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   6:    64 channels, first channel = 3.504873000e+10 Hz, last channel = 3.517473000e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   7:    64 channels, first channel = 3.517673000e+10 Hz, last channel = 3.530273000e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformManager::regridSpwAux	Combined SPW:   512 channels, first channel = 3.428073000e+10 Hz, last channel = 3.530273000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-06 17:12:51	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-06 17:12:51	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-06 17:12:51	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.47898e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99989e+06 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 512
    2019-12-06 17:12:51	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.02394e+09 Hz
    2019-12-06 17:12:51	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.42779e+10 Hz, upper edge = 3.53018e+10 Hz
    2019-12-06 17:12:51	INFO	MSTransformManager::regridSpwAux	Output SPW:   512 channels, first channel = 3.427886887e+10 Hz, last channel = 3.530081339e+10 Hz, first width = 1.999891419e+06 Hz, last width = 1.999891419e+06 Hz
    2019-12-06 17:12:51	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-06 17:12:51	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-06 17:12:51	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-06 17:12:51	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-06 17:12:51	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-06 17:12:51	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-06 17:13:13	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-06 17:13:15	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-06 17:14:22	INFO	mstransform::::casa	Result mstransform: True
    2019-12-06 17:14:22	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-06 11:08:13.368605 End time: 2019-12-06 11:14:22.021566
    2019-12-06 17:14:22	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-06 17:14:22	INFO	mstransform::::casa	##########################################
    2019-12-06 17:14:22	INFO	mstransform::::casa	##########################################
    2019-12-06 17:14:22	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-06 17:14:22	INFO	mstransform::::casa	mstransform( vis='/Volumes/S1/proc/12A201.120902/12A-201.sb9991390.eb11735360.56172.34942921296.ms', outputvis='12A201.120902.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='5', spw='0~7', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-06 17:14:22	INFO	mstransform::::casa	Combine spws 0~7 into new output spw
    2019-12-06 17:14:22	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-06 17:14:22	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-06 17:14:22	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/S1/proc/12A201.120902/12A-201.sb9991390.eb11735360.56172.34942921296.ms
    2019-12-06 17:14:22	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-06 17:14:22	INFO	MSTransformManager::parseMsSpecParams	Output file name is 12A201.120902.ms
    2019-12-06 17:14:22	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-06 17:14:22	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-06 17:14:22	INFO	MSTransformManager::parseDataSelParams	field selection is 5
    2019-12-06 17:14:22	INFO	MSTransformManager::parseDataSelParams	spw selection is 0~7
    2019-12-06 17:14:22	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-06 17:14:22	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-06 17:14:22	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-06 17:14:22	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-06 17:14:22	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-06 17:14:22	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is -1
    2019-12-06 17:14:22	INFO	MSTransformManager::parseFreqSpecParams	Start is 0
    2019-12-06 17:14:22	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-06 17:14:22	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-06 17:14:22	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-06 17:14:22	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-12-06 17:14:22	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [5]
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [8, 4]  (NB: Matrix in Row/Column order)
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 63, 1
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams+	 1, 0, 63, 1
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams+	 2, 0, 63, 1
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams+	 3, 0, 63, 1
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams+	 4, 0, 63, 1
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams+	 5, 0, 63, 1
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams+	 6, 0, 63, 1
    2019-12-06 17:14:22	INFO	MSTransformManager::initDataSelectionParams+	 7, 0, 63, 1]
    2019-12-06 17:14:22	INFO	MSTransformManager::open	Select data
    2019-12-06 17:14:22	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-06 17:14:28	INFO	MSTransformDataHandler::makeSelection	3081712 out of 9865532 rows are going to be considered due to the selection criteria.
    2019-12-06 17:18:51	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    64 channels, first channel = 3.428073000e+10 Hz, last channel = 3.440673000e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    64 channels, first channel = 3.440873000e+10 Hz, last channel = 3.453473000e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   2:    64 channels, first channel = 3.453673000e+10 Hz, last channel = 3.466273000e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   3:    64 channels, first channel = 3.466473000e+10 Hz, last channel = 3.479073000e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   4:    64 channels, first channel = 3.479273000e+10 Hz, last channel = 3.491873000e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   5:    64 channels, first channel = 3.492073000e+10 Hz, last channel = 3.504673000e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   6:    64 channels, first channel = 3.504873000e+10 Hz, last channel = 3.517473000e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::combineSpwsCore	   SPW   7:    64 channels, first channel = 3.517673000e+10 Hz, last channel = 3.530273000e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformManager::regridSpwAux	Combined SPW:   512 channels, first channel = 3.428073000e+10 Hz, last channel = 3.530273000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-06 17:18:51	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-06 17:18:51	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-06 17:18:51	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.47905e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99993e+06 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 512
    2019-12-06 17:18:51	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.02396e+09 Hz
    2019-12-06 17:18:51	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.42785e+10 Hz, upper edge = 3.53025e+10 Hz
    2019-12-06 17:18:51	INFO	MSTransformManager::regridSpwAux	Output SPW:   512 channels, first channel = 3.427949564e+10 Hz, last channel = 3.530145884e+10 Hz, first width = 1.999927985e+06 Hz, last width = 1.999927985e+06 Hz
    2019-12-06 17:18:51	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-06 17:18:51	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-06 17:18:51	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-06 17:18:51	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-06 17:18:51	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-06 17:18:51	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-06 17:19:13	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-06 17:19:14	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-06 17:20:20	INFO	mstransform::::casa	Result mstransform: True
    2019-12-06 17:20:20	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-06 11:14:22.092509 End time: 2019-12-06 11:20:19.798193
    2019-12-06 17:20:20	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-06 17:20:20	INFO	mstransform::::casa	##########################################
    2019-12-06 17:20:20	INFO	mstransform::::casa	##########################################
    2019-12-06 17:20:20	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-06 17:20:20	INFO	mstransform::::casa	mstransform( vis='/Volumes/S1/proc/12A201.120622/12A-201.sb9991067.eb10734424.56100.54596251158.ms', outputvis='12A201.120622.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='5', spw='0~7', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-06 17:20:20	INFO	mstransform::::casa	Combine spws 0~7 into new output spw
    2019-12-06 17:20:20	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-06 17:20:20	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-06 17:20:20	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/S1/proc/12A201.120622/12A-201.sb9991067.eb10734424.56100.54596251158.ms
    2019-12-06 17:20:20	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-06 17:20:20	INFO	MSTransformManager::parseMsSpecParams	Output file name is 12A201.120622.ms
    2019-12-06 17:20:20	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-06 17:20:20	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-06 17:20:20	INFO	MSTransformManager::parseDataSelParams	field selection is 5
    2019-12-06 17:20:20	INFO	MSTransformManager::parseDataSelParams	spw selection is 0~7
    2019-12-06 17:20:20	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-06 17:20:20	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-06 17:20:20	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-06 17:20:20	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-06 17:20:20	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-06 17:20:20	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is -1
    2019-12-06 17:20:20	INFO	MSTransformManager::parseFreqSpecParams	Start is 0
    2019-12-06 17:20:20	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-06 17:20:20	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-06 17:20:20	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-06 17:20:20	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-12-06 17:20:20	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [5]
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [8, 4]  (NB: Matrix in Row/Column order)
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 63, 1
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams+	 1, 0, 63, 1
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams+	 2, 0, 63, 1
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams+	 3, 0, 63, 1
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams+	 4, 0, 63, 1
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams+	 5, 0, 63, 1
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams+	 6, 0, 63, 1
    2019-12-06 17:20:20	INFO	MSTransformManager::initDataSelectionParams+	 7, 0, 63, 1]
    2019-12-06 17:20:20	INFO	MSTransformManager::open	Select data
    2019-12-06 17:20:20	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-06 17:20:24	INFO	MSTransformDataHandler::makeSelection	2315434 out of 7170320 rows are going to be considered due to the selection criteria.
    2019-12-06 17:23:59	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    64 channels, first channel = 3.428073000e+10 Hz, last channel = 3.440673000e+10 Hz
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    64 channels, first channel = 3.440873000e+10 Hz, last channel = 3.453473000e+10 Hz
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	   SPW   2:    64 channels, first channel = 3.453673000e+10 Hz, last channel = 3.466273000e+10 Hz
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	   SPW   3:    64 channels, first channel = 3.466473000e+10 Hz, last channel = 3.479073000e+10 Hz
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	   SPW   4:    64 channels, first channel = 3.479273000e+10 Hz, last channel = 3.491873000e+10 Hz
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	   SPW   5:    64 channels, first channel = 3.492073000e+10 Hz, last channel = 3.504673000e+10 Hz
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	   SPW   6:    64 channels, first channel = 3.504873000e+10 Hz, last channel = 3.517473000e+10 Hz
    2019-12-06 17:23:59	INFO	MSTransformRegridder::combineSpwsCore	   SPW   7:    64 channels, first channel = 3.517673000e+10 Hz, last channel = 3.530273000e+10 Hz
    2019-12-06 17:23:59	INFO	MSTransformManager::regridSpwAux	Combined SPW:   512 channels, first channel = 3.428073000e+10 Hz, last channel = 3.530273000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-06 17:23:59	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-06 17:24:00	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-06 17:24:00	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.47901e+10 Hz
    2019-12-06 17:24:00	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.99991e+06 Hz
    2019-12-06 17:24:00	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 512
    2019-12-06 17:24:00	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.02395e+09 Hz
    2019-12-06 17:24:00	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.42782e+10 Hz, upper edge = 3.53021e+10 Hz
    2019-12-06 17:24:00	INFO	MSTransformManager::regridSpwAux	Output SPW:   512 channels, first channel = 3.427917192e+10 Hz, last channel = 3.530112547e+10 Hz, first width = 1.999909099e+06 Hz, last width = 1.999909099e+06 Hz
    2019-12-06 17:24:00	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-06 17:24:00	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-06 17:24:00	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-06 17:24:00	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-06 17:24:00	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-06 17:24:00	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-06 17:24:12	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-06 17:24:13	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-06 17:25:05	INFO	mstransform::::casa	Result mstransform: True
    2019-12-06 17:25:05	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-06 11:20:19.887213 End time: 2019-12-06 11:25:05.308821
    2019-12-06 17:25:05	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-06 17:25:05	INFO	mstransform::::casa	##########################################
    2019-12-06 17:25:05	INFO	mstransform::::casa	##########################################
    2019-12-06 17:25:05	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-06 17:25:05	INFO	mstransform::::casa	mstransform( vis='/Volumes/S1/proc/11B044.120106/11B-044.sb6590371.eb7328504.55932.04923909722.ms', outputvis='11B044.120106.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='5', spw='0~7', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-06 17:25:05	INFO	mstransform::::casa	Combine spws 0~7 into new output spw
    2019-12-06 17:25:05	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-06 17:25:05	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-12-06 17:25:05	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/S1/proc/11B044.120106/11B-044.sb6590371.eb7328504.55932.04923909722.ms
    2019-12-06 17:25:05	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-12-06 17:25:05	INFO	MSTransformManager::parseMsSpecParams	Output file name is 11B044.120106.ms
    2019-12-06 17:25:05	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-06 17:25:05	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-06 17:25:05	INFO	MSTransformManager::parseDataSelParams	field selection is 5
    2019-12-06 17:25:05	INFO	MSTransformManager::parseDataSelParams	spw selection is 0~7
    2019-12-06 17:25:05	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-06 17:25:05	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-06 17:25:05	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-06 17:25:05	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-06 17:25:05	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-06 17:25:05	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is -1
    2019-12-06 17:25:05	INFO	MSTransformManager::parseFreqSpecParams	Start is 0
    2019-12-06 17:25:05	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-06 17:25:05	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-06 17:25:05	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-12-06 17:25:05	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-12-06 17:25:05	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [5]
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [8, 4]  (NB: Matrix in Row/Column order)
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 63, 1
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams+	 1, 0, 63, 1
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams+	 2, 0, 63, 1
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams+	 3, 0, 63, 1
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams+	 4, 0, 63, 1
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams+	 5, 0, 63, 1
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams+	 6, 0, 63, 1
    2019-12-06 17:25:06	INFO	MSTransformManager::initDataSelectionParams+	 7, 0, 63, 1]
    2019-12-06 17:25:06	INFO	MSTransformManager::open	Select data
    2019-12-06 17:25:06	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-06 17:25:11	INFO	MSTransformDataHandler::makeSelection	2746622 out of 7071680 rows are going to be considered due to the selection criteria.
    2019-12-06 17:28:37	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:    64 channels, first channel = 3.428073000e+10 Hz, last channel = 3.440673000e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:    64 channels, first channel = 3.440873000e+10 Hz, last channel = 3.453473000e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	   SPW   2:    64 channels, first channel = 3.453673000e+10 Hz, last channel = 3.466273000e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	   SPW   3:    64 channels, first channel = 3.466473000e+10 Hz, last channel = 3.479073000e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	   SPW   4:    64 channels, first channel = 3.479273000e+10 Hz, last channel = 3.491873000e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	   SPW   5:    64 channels, first channel = 3.492073000e+10 Hz, last channel = 3.504673000e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	   SPW   6:    64 channels, first channel = 3.504873000e+10 Hz, last channel = 3.517473000e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::combineSpwsCore	   SPW   7:    64 channels, first channel = 3.517673000e+10 Hz, last channel = 3.530273000e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformManager::regridSpwAux	Combined SPW:   512 channels, first channel = 3.428073000e+10 Hz, last channel = 3.530273000e+10 Hz, first width = 2.000000000e+06 Hz, last width = 2.000000000e+06 Hz
    2019-12-06 17:28:37	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-06 17:28:37	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-06 17:28:37	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.47962e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 2.00025e+06 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 512
    2019-12-06 17:28:37	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.02413e+09 Hz
    2019-12-06 17:28:37	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.42841e+10 Hz, upper edge = 3.53082e+10 Hz
    2019-12-06 17:28:37	INFO	MSTransformManager::regridSpwAux	Output SPW:   512 channels, first channel = 3.428509663e+10 Hz, last channel = 3.530722681e+10 Hz, first width = 2.000254757e+06 Hz, last width = 2.000254757e+06 Hz
    2019-12-06 17:28:37	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-12-06 17:28:37	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-12-06 17:28:37	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-12-06 17:28:37	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-12-06 17:28:37	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of CALDEVICE sub-table and removing duplicates 
    2019-12-06 17:28:37	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSPOWER sub-table and removing duplicates 
    2019-12-06 17:28:49	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-12-06 17:28:51	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-06 17:29:53	INFO	mstransform::::casa	Result mstransform: True
    2019-12-06 17:29:53	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-06 11:25:05.424731 End time: 2019-12-06 11:29:52.643717
    2019-12-06 17:29:53	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-06 17:29:53	INFO	mstransform::::casa	##########################################


--------------

2015.1.00723.S (Band 6, Cycle-3, Xue et al. 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spws Setup
^^^^^^^^^^

-  spw=0,4,8,12 BB1 228GHz H2O 211-202
-  spw=1,5,9,13 BB2 231GHz Continuum
-  spw=2,6,10,14 BB3 243GHz CI 2-1
-  spw=3,7,11,15 BB4 242GHz CO76/CI 7-6

Export one MS per baseband
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Combine the SPWs from each baseband into a single SPW
-  Transform the frame from TOPO to LSRK
-  Exclude the edge channels

Note: GMaKE requires the input MS contains only one SPW and one FIELD.

MS manupilation
^^^^^^^^^^^^^^^

-  The integration time is rebined to 60s (limited by the time-averging
   smearing)
-  The continuum SPW is averged into 1 representive channel (limited by
   the bandwidth smearing)
-  The point tables were removed\ `1 <#fn1>`__: they are only used for
   mosaic imaging, not in this specific case; for ALMA data, the table
   can be quite large even for channle-/time-averaged data)

1 We can’t remove ms/POINTING table directly using ``rmtables()`` as its
abence will crash certain CASA tasks/tools (e.g. listable); instead, we
set it to have empty row, as it’s done by
``rxutils.casa.proc.rmPointing()``.

.. code:: ipython3

    
    # Switch working directory
    
    demo_dir='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/data/hxmm01/alma/2015.1.00723.S/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_hxmm01.log')
    
    vis_name='/Volumes/D1/projects/hxmm01/proc/2015.1.00723.S/calibrated/calibrated.ms.split.cal'
    #ctasks.listobs(vis_name)
    
    spw_list=['0,4,8,12','1,5,9,13','2,6,10,14','3,7,11,15']
    bb_list=['1','2','3','4']
    field='HXMM01'
    
    # For BB1 & BB2: TOPO->LSKR
    
    for i in range(0,2):
        outvis='bb'+bb_list[i]+'.ms'
        os.system('rm -rf '+outvis)
        ctasks.mstransform(vis_name,outputvis=outvis,field='HXMM01',spw=spw_list[i],datacolumn='data',
                            regridms=True,outframe='lsrk',combinespws=True,mode='channel',start=9,nchan=110,width=1,
                            timeaverage=True,timebin='60s',maxuvwdistance=0.0,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)
    
    
    # For BB3+BB4: TOPO->LSKR
    
    outvis='bb34.ms'
    os.system('rm -rf '+outvis)
    ctasks.mstransform(vis_name,outputvis=outvis,field='HXMM01',spw='3,2,7,6,11,10,15,14',datacolumn='data',scan='',
                         regridms=True,outframe='lsrk',combinespws=True,mode='channel',start=10,nchan=161,width=1,
                         timeaverage=True,timebin='60s',maxuvwdistance=0.0,
                         keepflags=False,usewtspectrum=False)         
    rmPointing(outvis)
    
    # For BB2: Channel-averging
    
    for i in range(1,2):
        outvis='bb'+bb_list[i]+'.mfs.ms'
        os.system('rm -rf '+'bb'+bb_list[i]+'.mfs.ms')
        ctasks.mstransform('bb'+bb_list[i]+'.ms',outputvis=outvis,field='HXMM01',datacolumn='data',
                            chanaverage=True,chanbin=110,
                            timeaverage=False,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)
       


.. parsed-literal::

    2019-10-11 18:29:37	INFO	mstransform::::casa	##########################################
    2019-10-11 18:29:37	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:29:37	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2015.1.00723.S/calibrated/calibrated.ms.split.cal', outputvis='bb1.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='HXMM01', spw='0,4,8,12', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=110, start=9, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:29:37	INFO	mstransform::::casa	Combine spws 0,4,8,12 into new output spw
    2019-10-11 18:29:37	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-11 18:29:37	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-11 18:29:37	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2015.1.00723.S/calibrated/calibrated.ms.split.cal
    2019-10-11 18:29:37	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:29:37	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb1.ms
    2019-10-11 18:29:37	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:29:37	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:29:37	INFO	MSTransformManager::parseDataSelParams	field selection is HXMM01
    2019-10-11 18:29:37	INFO	MSTransformManager::parseDataSelParams	spw selection is 0,4,8,12
    2019-10-11 18:29:37	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-11 18:29:37	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-11 18:29:37	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-11 18:29:37	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-11 18:29:37	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-11 18:29:37	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 110
    2019-10-11 18:29:37	INFO	MSTransformManager::parseFreqSpecParams	Start is 9
    2019-10-11 18:29:37	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-11 18:29:37	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-11 18:29:37	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-11 18:29:37	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-11 18:29:37	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-11 18:29:37	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-11 18:29:37	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:29:37	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [5]
    2019-10-11 18:29:37	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [4, 4]  (NB: Matrix in Row/Column order)
    2019-10-11 18:29:37	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 127, 1
    2019-10-11 18:29:37	INFO	MSTransformManager::initDataSelectionParams+	 4, 0, 127, 1
    2019-10-11 18:29:37	INFO	MSTransformManager::initDataSelectionParams+	 8, 0, 127, 1
    2019-10-11 18:29:37	INFO	MSTransformManager::initDataSelectionParams+	 12, 0, 127, 1]
    2019-10-11 18:29:37	INFO	MSTransformManager::open	Select data
    2019-10-11 18:29:37	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:29:46	INFO	MSTransformDataHandler::makeSelection	3268823 out of 23010816 rows are going to be considered due to the selection criteria.
    2019-10-11 18:30:00	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-10-11 18:30:00	INFO	MSTransformRegridder::combineSpwsCore	 *** Encountered negative channel widths in SPECTRAL_WINDOW table.
    2019-10-11 18:30:00	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-10-11 18:30:00	INFO	MSTransformRegridder::combineSpwsCore	   SPW   3:   128 channels, first channel = 2.262190809e+11 Hz, last channel = 2.282034559e+11 Hz
    2019-10-11 18:30:00	INFO	MSTransformRegridder::combineSpwsCore	   SPW   2:   128 channels, first channel = 2.262193145e+11 Hz, last channel = 2.282036895e+11 Hz
    2019-10-11 18:30:00	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:   128 channels, first channel = 2.262194854e+11 Hz, last channel = 2.282038604e+11 Hz
    2019-10-11 18:30:00	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:   128 channels, first channel = 2.262206599e+11 Hz, last channel = 2.282050349e+11 Hz
    2019-10-11 18:30:00	INFO	MSTransformManager::regridSpwAux	Combined SPW:   128 channels, first channel = 2.262190809e+11 Hz, last channel = 2.282042454e+11 Hz, first width = 1.720400463e+07 Hz, last width = 1.720400463e+07 Hz
    2019-10-11 18:30:00	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-11 18:30:00	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-11 18:30:00	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.27198e+11 Hz
    2019-10-11 18:30:00	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56241e+07 Hz
    2019-10-11 18:30:00	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 110
    2019-10-11 18:30:00	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.71865e+09 Hz
    2019-10-11 18:30:00	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.26339e+11 Hz, upper edge = 2.28058e+11 Hz
    2019-10-11 18:30:00	INFO	MSTransformManager::regridSpwAux	Output SPW:   110 channels, first channel = 2.263469318e+11 Hz, last channel = 2.280499606e+11 Hz, first width = 1.562411823e+07 Hz, last width = 1.562411823e+07 Hz
    2019-10-11 18:30:00	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-10-11 18:30:00	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-10-11 18:30:00	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-10-11 18:30:00	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-10-11 18:30:00	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSCAL sub-table and removing duplicates 
    2019-10-11 18:30:00	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-11 18:30:00	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-10-11 18:30:01	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-11 18:31:33	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:31:33	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:29:36.654245 End time: 2019-10-11 13:31:33.203307
    2019-10-11 18:31:33	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:31:33	INFO	mstransform::::casa	##########################################


.. parsed-literal::

    2.4G	bb1.ms
    250M	bb1.ms


.. parsed-literal::

    2019-10-11 18:33:00	INFO	mstransform::::casa	##########################################
    2019-10-11 18:33:00	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:33:00	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2015.1.00723.S/calibrated/calibrated.ms.split.cal', outputvis='bb2.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='HXMM01', spw='1,5,9,13', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=110, start=9, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:33:00	INFO	mstransform::::casa	Combine spws 1,5,9,13 into new output spw
    2019-10-11 18:33:00	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-11 18:33:00	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-11 18:33:00	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2015.1.00723.S/calibrated/calibrated.ms.split.cal
    2019-10-11 18:33:00	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:33:00	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb2.ms
    2019-10-11 18:33:00	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:33:00	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:33:00	INFO	MSTransformManager::parseDataSelParams	field selection is HXMM01
    2019-10-11 18:33:00	INFO	MSTransformManager::parseDataSelParams	spw selection is 1,5,9,13
    2019-10-11 18:33:00	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-11 18:33:00	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-11 18:33:00	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-11 18:33:00	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-11 18:33:00	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-11 18:33:00	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 110
    2019-10-11 18:33:00	INFO	MSTransformManager::parseFreqSpecParams	Start is 9
    2019-10-11 18:33:00	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-11 18:33:00	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-11 18:33:00	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-11 18:33:00	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-11 18:33:00	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-11 18:33:00	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-11 18:33:00	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:33:00	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [5]
    2019-10-11 18:33:00	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [4, 4]  (NB: Matrix in Row/Column order)
    2019-10-11 18:33:00	INFO	MSTransformManager::initDataSelectionParams+	[1, 0, 127, 1
    2019-10-11 18:33:00	INFO	MSTransformManager::initDataSelectionParams+	 5, 0, 127, 1
    2019-10-11 18:33:00	INFO	MSTransformManager::initDataSelectionParams+	 9, 0, 127, 1
    2019-10-11 18:33:00	INFO	MSTransformManager::initDataSelectionParams+	 13, 0, 127, 1]
    2019-10-11 18:33:00	INFO	MSTransformManager::open	Select data
    2019-10-11 18:33:00	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:33:09	INFO	MSTransformDataHandler::makeSelection	3102721 out of 23010816 rows are going to be considered due to the selection criteria.
    2019-10-11 18:33:23	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-10-11 18:33:23	INFO	MSTransformRegridder::combineSpwsCore	 *** Encountered negative channel widths in SPECTRAL_WINDOW table.
    2019-10-11 18:33:23	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-10-11 18:33:23	INFO	MSTransformRegridder::combineSpwsCore	   SPW   3:   128 channels, first channel = 2.290192198e+11 Hz, last channel = 2.310035948e+11 Hz
    2019-10-11 18:33:23	INFO	MSTransformRegridder::combineSpwsCore	   SPW   2:   128 channels, first channel = 2.290194563e+11 Hz, last channel = 2.310038313e+11 Hz
    2019-10-11 18:33:23	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:   128 channels, first channel = 2.290196293e+11 Hz, last channel = 2.310040043e+11 Hz
    2019-10-11 18:33:23	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:   128 channels, first channel = 2.290208183e+11 Hz, last channel = 2.310051933e+11 Hz
    2019-10-11 18:33:23	INFO	MSTransformManager::regridSpwAux	Combined SPW:   128 channels, first channel = 2.290192198e+11 Hz, last channel = 2.310043940e+11 Hz, first width = 1.722346420e+07 Hz, last width = 1.722346420e+07 Hz
    2019-10-11 18:33:23	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-11 18:33:23	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-11 18:33:23	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.29998e+11 Hz
    2019-10-11 18:33:23	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56241e+07 Hz
    2019-10-11 18:33:23	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 110
    2019-10-11 18:33:23	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.71865e+09 Hz
    2019-10-11 18:33:23	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.29139e+11 Hz, upper edge = 2.30858e+11 Hz
    2019-10-11 18:33:23	INFO	MSTransformManager::regridSpwAux	Output SPW:   110 channels, first channel = 2.291469126e+11 Hz, last channel = 2.308499415e+11 Hz, first width = 1.562411823e+07 Hz, last width = 1.562411823e+07 Hz
    2019-10-11 18:33:23	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-10-11 18:33:23	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-10-11 18:33:23	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-10-11 18:33:23	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-10-11 18:33:23	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSCAL sub-table and removing duplicates 
    2019-10-11 18:33:23	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-11 18:33:23	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-10-11 18:33:24	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-11 18:34:52	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:34:52	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:32:59.860686 End time: 2019-10-11 13:34:51.585876
    2019-10-11 18:34:52	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:34:52	INFO	mstransform::::casa	##########################################


.. parsed-literal::

    2.4G	bb2.ms
    234M	bb2.ms


.. parsed-literal::

    2019-10-11 18:36:29	INFO	mstransform::::casa	##########################################
    2019-10-11 18:36:29	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:36:29	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2015.1.00723.S/calibrated/calibrated.ms.split.cal', outputvis='bb34.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='HXMM01', spw='3,2,7,6,11,10,15,14', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=161, start=10, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:36:29	INFO	mstransform::::casa	Combine spws 3,2,7,6,11,10,15,14 into new output spw
    2019-10-11 18:36:29	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-11 18:36:29	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-11 18:36:29	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2015.1.00723.S/calibrated/calibrated.ms.split.cal
    2019-10-11 18:36:29	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:36:29	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb34.ms
    2019-10-11 18:36:29	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:36:29	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:36:29	INFO	MSTransformManager::parseDataSelParams	field selection is HXMM01
    2019-10-11 18:36:29	INFO	MSTransformManager::parseDataSelParams	spw selection is 3,2,7,6,11,10,15,14
    2019-10-11 18:36:29	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-11 18:36:29	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-11 18:36:29	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-11 18:36:29	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-11 18:36:29	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-11 18:36:29	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 161
    2019-10-11 18:36:29	INFO	MSTransformManager::parseFreqSpecParams	Start is 10
    2019-10-11 18:36:29	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-11 18:36:29	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-11 18:36:29	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-11 18:36:29	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-11 18:36:29	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-11 18:36:29	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-11 18:36:29	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [5]
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [8, 4]  (NB: Matrix in Row/Column order)
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams+	[3, 0, 127, 1
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams+	 2, 0, 127, 1
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams+	 7, 0, 127, 1
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams+	 6, 0, 127, 1
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams+	 11, 0, 127, 1
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams+	 10, 0, 127, 1
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams+	 15, 0, 127, 1
    2019-10-11 18:36:29	INFO	MSTransformManager::initDataSelectionParams+	 14, 0, 127, 1]
    2019-10-11 18:36:29	INFO	MSTransformManager::open	Select data
    2019-10-11 18:36:29	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:36:43	INFO	MSTransformDataHandler::makeSelection	6499787 out of 23010816 rows are going to be considered due to the selection criteria.
    2019-10-11 18:36:58	INFO	MSTransformManager::regridAndCombineSpwSubtable	Calculate combined SPW frequencies
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	Input SPWs sorted by first (lowest) channel frequency:
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   6:   128 channels, first channel = 2.427198993e+11 Hz, last channel = 2.447042743e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   4:   128 channels, first channel = 2.427201499e+11 Hz, last channel = 2.447045249e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   2:   128 channels, first channel = 2.427203331e+11 Hz, last channel = 2.447047081e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   0:   128 channels, first channel = 2.427215930e+11 Hz, last channel = 2.447059680e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   7:   128 channels, first channel = 2.435299395e+11 Hz, last channel = 2.455143145e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   5:   128 channels, first channel = 2.435301909e+11 Hz, last channel = 2.455145659e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   3:   128 channels, first channel = 2.435303747e+11 Hz, last channel = 2.455147497e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::combineSpwsCore	   SPW   1:   128 channels, first channel = 2.435316388e+11 Hz, last channel = 2.455160138e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformManager::regridSpwAux	Combined SPW:   179 channels, first channel = 2.427198993e+11 Hz, last channel = 2.455151641e+11 Hz, first width = 1.732430644e+07 Hz, last width = 1.732430644e+07 Hz
    2019-10-11 18:36:58	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-11 18:36:58	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-11 18:36:58	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.44112e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56241e+07 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 161
    2019-10-11 18:36:58	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 2.51548e+09 Hz
    2019-10-11 18:36:58	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.42855e+11 Hz, upper edge = 2.4537e+11 Hz
    2019-10-11 18:36:58	INFO	MSTransformManager::regridSpwAux	Output SPW:   161 channels, first channel = 2.428624430e+11 Hz, last channel = 2.453623019e+11 Hz, first width = 1.562411823e+07 Hz, last width = 1.562411823e+07 Hz
    2019-10-11 18:36:58	INFO	MSTransformManager::regridAndCombineSpwSubtable	Write output SPW subtable 
    2019-10-11 18:36:58	INFO	MSTransformManager::reindexDDISubTable	Re-indexing DDI sub-table
    2019-10-11 18:36:58	INFO	MSTransformManager::reindexSourceSubTable	Re-indexing SOURCE sub-table
    2019-10-11 18:36:58	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of FEED sub-table and removing duplicates 
    2019-10-11 18:36:58	INFO	MSTransformManager::reindexGenericTimeDependentSubTable	Re-indexing SPW column of SYSCAL sub-table and removing duplicates 
    2019-10-11 18:36:58	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-11 18:36:58	INFO	MSTransformManager::setIterationApproach	Combining data from selected spectral windows
    2019-10-11 18:37:00	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-11 18:40:33	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:40:33	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:36:28.740727 End time: 2019-10-11 13:40:33.337073
    2019-10-11 18:40:33	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:40:33	INFO	mstransform::::casa	##########################################


.. parsed-literal::

    2.5G	bb34.ms
    350M	bb34.ms


.. parsed-literal::

    2019-10-11 18:41:59	INFO	mstransform::::casa	##########################################
    2019-10-11 18:41:59	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:41:59	INFO	mstransform::::casa	mstransform( vis='bb2.ms', outputvis='bb2.mfs.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='HXMM01', spw='', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=True, chanbin=110, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:41:59	INFO	ParallelDataHelper::::casa	Parse channel averaging parameters
    2019-10-11 18:41:59	INFO	MSTransformManager::parseMsSpecParams	Input file name is bb2.ms
    2019-10-11 18:41:59	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:41:59	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb2.mfs.ms
    2019-10-11 18:41:59	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:41:59	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:41:59	INFO	MSTransformManager::parseDataSelParams	field selection is HXMM01
    2019-10-11 18:41:59	INFO	MSTransformManager::parseChanAvgParams	Channel average is activated
    2019-10-11 18:41:59	INFO	MSTransformManager::parseChanAvgParams	Channel bin is [110]
    2019-10-11 18:41:59	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:41:59	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-11 18:41:59	INFO	MSTransformManager::open	Select data
    2019-10-11 18:41:59	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:42:01	INFO	ParallelDataHelper::::casa	Apply the transformations


.. parsed-literal::

     39M	bb2.mfs.ms
     39M	bb2.mfs.ms


.. parsed-literal::

    2019-10-11 18:42:04	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:42:04	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:41:59.079658 End time: 2019-10-11 13:42:04.359815
    2019-10-11 18:42:04	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:42:04	INFO	mstransform::::casa	##########################################


2011.0.00539.S (Band 7, Cycle-0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spws Setup
^^^^^^^^^^

-  spw=0 336GHz H2O 111-000
-  spw=1 338GHz Continuum
-  spw=2 348GHz CO10-9 / H2O312-221
-  spw=3 350GHz Continuum

.. code:: ipython3

    # Switch working directory
    
    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/hxmm01/alma/2011.0.00539.S/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_hxmm01.log')
    
    vis_name='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal'
    #ctasks.listobs(vis_name)
    
    spw_list=['0','1','2','3']
    bb_list=['1','2','3','4']
    field='XMM01'
    
    # For BB1 & BB2 & BB3 & BB4: TOPO->LSKR
    
    for i in range(0,4):
        outvis='bb'+bb_list[i]+'.ms'
        os.system('rm -rf '+outvis)
        ctasks.mstransform(vis_name,outputvis=outvis,field='XMM01',spw=spw_list[i],datacolumn='data',
                            regridms=True,outframe='lsrk',combinespws=True,mode='channel',start=8,nchan=112,width=1,
                            timeaverage=False,timebin='60s',maxuvwdistance=0.0,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)
    
    # For BB2/BB4: Channel-averging
    
    for i in range(0,4):
        if  bb_list[i]=='1' or bb_list[i]=='3':
            continue
        outvis='bb'+bb_list[i]+'.mfs.ms'
        os.system('rm -rf '+outvis)
        ctasks.mstransform('bb'+bb_list[i]+'.ms',outputvis=outvis,field='XMM01',datacolumn='data',
                            chanaverage=True,chanbin=112,
                            timeaverage=False,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)



.. parsed-literal::

    2019-12-03 16:15:54	INFO	mstransform::::casa	##########################################
    2019-12-03 16:15:54	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-03 16:15:54	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal', outputvis='bb1.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='0', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=112, start=8, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=False, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-03 16:15:54	INFO	mstransform::::casa	Combine spws 0 into new output spw
    2019-12-03 16:15:54	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-03 16:15:54	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal
    2019-12-03 16:15:54	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-12-03 16:15:54	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb1.ms
    2019-12-03 16:15:54	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-03 16:15:54	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-03 16:15:54	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-12-03 16:15:54	INFO	MSTransformManager::parseDataSelParams	spw selection is 0
    2019-12-03 16:15:54	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-03 16:15:54	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-03 16:15:54	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-03 16:15:54	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-03 16:15:54	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-03 16:15:54	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 112
    2019-12-03 16:15:54	INFO	MSTransformManager::parseFreqSpecParams	Start is 8
    2019-12-03 16:15:54	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-03 16:15:54	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-03 16:15:54	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-12-03 16:15:54	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-12-03 16:15:54	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-12-03 16:15:54	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 127, 1]
    2019-12-03 16:15:54	INFO	MSTransformManager::open	Select data
    2019-12-03 16:15:54	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-03 16:15:54	INFO	MSTransformDataHandler::makeSelection	21425 out of 85420 rows are going to be considered due to the selection criteria.
    2019-12-03 16:15:55	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-12-03 16:15:55	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 0
    2019-12-03 16:15:55	INFO	MSTransformManager::regridSpwAux	Input SPW:   128 channels, first channel = 3.369868125e+11 Hz, last channel = 3.350024375e+11 Hz, first width = -1.562500000e+07 Hz, last width = -1.562500000e+07 Hz
    2019-12-03 16:15:55	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-03 16:15:55	INFO	MSTransformRegridder::calcChanFreqs	 *** Encountered negative channel widths in input spectral window.
    2019-12-03 16:15:55	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-03 16:15:55	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.35981e+11 Hz
    2019-12-03 16:15:55	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-12-03 16:15:55	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56244e+07 Hz
    2019-12-03 16:15:55	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 112
    2019-12-03 16:15:55	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.74993e+09 Hz
    2019-12-03 16:15:55	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.35106e+11 Hz, upper edge = 3.36856e+11 Hz
    2019-12-03 16:15:55	INFO	MSTransformManager::regridSpwAux	Output SPW:   112 channels, first channel = 3.368478395e+11 Hz, last channel = 3.351135365e+11 Hz, first width = 1.562435188e+07 Hz, last width = 1.562435188e+07 Hz
    2019-12-03 16:15:55	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-03 16:15:57	INFO	mstransform::::casa	Result mstransform: True
    2019-12-03 16:15:57	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-03 10:15:53.849305 End time: 2019-12-03 10:15:57.346496
    2019-12-03 16:15:57	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-03 16:15:57	INFO	mstransform::::casa	##########################################
    2019-12-03 16:15:57	INFO	mstransform::::casa	##########################################
    2019-12-03 16:15:57	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-03 16:15:57	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal', outputvis='bb2.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='1', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=112, start=8, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=False, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-03 16:15:57	INFO	mstransform::::casa	Combine spws 1 into new output spw
    2019-12-03 16:15:57	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-03 16:15:57	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal
    2019-12-03 16:15:57	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-12-03 16:15:57	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb2.ms
    2019-12-03 16:15:57	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-03 16:15:57	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-03 16:15:57	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-12-03 16:15:57	INFO	MSTransformManager::parseDataSelParams	spw selection is 1
    2019-12-03 16:15:57	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-03 16:15:57	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-03 16:15:57	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-03 16:15:57	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-03 16:15:57	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-03 16:15:57	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 112
    2019-12-03 16:15:57	INFO	MSTransformManager::parseFreqSpecParams	Start is 8
    2019-12-03 16:15:57	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-03 16:15:57	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-03 16:15:57	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-12-03 16:15:57	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-12-03 16:15:57	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-12-03 16:15:57	INFO	MSTransformManager::initDataSelectionParams+	[1, 0, 127, 1]
    2019-12-03 16:15:57	INFO	MSTransformManager::open	Select data
    2019-12-03 16:15:57	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-03 16:15:58	INFO	MSTransformDataHandler::makeSelection	21145 out of 85420 rows are going to be considered due to the selection criteria.
    2019-12-03 16:15:58	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-12-03 16:15:58	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 1
    2019-12-03 16:15:58	INFO	MSTransformManager::regridSpwAux	Input SPW:   128 channels, first channel = 3.389243125e+11 Hz, last channel = 3.369399375e+11 Hz, first width = -1.562500000e+07 Hz, last width = -1.562500000e+07 Hz
    2019-12-03 16:15:58	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-03 16:15:58	INFO	MSTransformRegridder::calcChanFreqs	 *** Encountered negative channel widths in input spectral window.
    2019-12-03 16:15:58	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-03 16:15:58	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.37918e+11 Hz
    2019-12-03 16:15:58	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-12-03 16:15:58	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56244e+07 Hz
    2019-12-03 16:15:58	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 112
    2019-12-03 16:15:58	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.74993e+09 Hz
    2019-12-03 16:15:58	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.37043e+11 Hz, upper edge = 3.38793e+11 Hz
    2019-12-03 16:15:58	INFO	MSTransformManager::regridSpwAux	Output SPW:   112 channels, first channel = 3.387852592e+11 Hz, last channel = 3.370509561e+11 Hz, first width = 1.562435188e+07 Hz, last width = 1.562435188e+07 Hz
    2019-12-03 16:15:58	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-03 16:16:00	INFO	mstransform::::casa	Result mstransform: True
    2019-12-03 16:16:00	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-03 10:15:57.425616 End time: 2019-12-03 10:16:00.401649
    2019-12-03 16:16:00	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-03 16:16:00	INFO	mstransform::::casa	##########################################
    2019-12-03 16:16:00	INFO	mstransform::::casa	##########################################
    2019-12-03 16:16:00	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-03 16:16:00	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal', outputvis='bb3.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='2', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=112, start=8, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=False, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-03 16:16:00	INFO	mstransform::::casa	Combine spws 2 into new output spw
    2019-12-03 16:16:00	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-03 16:16:00	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal
    2019-12-03 16:16:00	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-12-03 16:16:00	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb3.ms
    2019-12-03 16:16:00	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-03 16:16:00	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-03 16:16:00	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-12-03 16:16:00	INFO	MSTransformManager::parseDataSelParams	spw selection is 2
    2019-12-03 16:16:00	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-03 16:16:00	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-03 16:16:00	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-03 16:16:00	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-03 16:16:00	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-03 16:16:00	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 112
    2019-12-03 16:16:00	INFO	MSTransformManager::parseFreqSpecParams	Start is 8
    2019-12-03 16:16:00	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-03 16:16:00	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-03 16:16:01	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-12-03 16:16:01	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-12-03 16:16:01	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-12-03 16:16:01	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 127, 1]
    2019-12-03 16:16:01	INFO	MSTransformManager::open	Select data
    2019-12-03 16:16:01	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-03 16:16:01	INFO	MSTransformDataHandler::makeSelection	21425 out of 85420 rows are going to be considered due to the selection criteria.
    2019-12-03 16:16:01	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-12-03 16:16:01	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 2
    2019-12-03 16:16:01	INFO	MSTransformManager::regridSpwAux	Input SPW:   128 channels, first channel = 3.470024375e+11 Hz, last channel = 3.489868125e+11 Hz, first width = 1.562500000e+07 Hz, last width = 1.562500000e+07 Hz
    2019-12-03 16:16:01	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-03 16:16:01	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-03 16:16:01	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.4798e+11 Hz
    2019-12-03 16:16:01	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56244e+07 Hz
    2019-12-03 16:16:01	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 112
    2019-12-03 16:16:01	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.74993e+09 Hz
    2019-12-03 16:16:01	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.47105e+11 Hz, upper edge = 3.48855e+11 Hz
    2019-12-03 16:16:01	INFO	MSTransformManager::regridSpwAux	Output SPW:   112 channels, first channel = 3.471130387e+11 Hz, last channel = 3.488473418e+11 Hz, first width = 1.562435188e+07 Hz, last width = 1.562435188e+07 Hz
    2019-12-03 16:16:01	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-12-03 16:16:03	INFO	mstransform::::casa	Result mstransform: True
    2019-12-03 16:16:03	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-12-03 10:16:00.470994 End time: 2019-12-03 10:16:03.175861
    2019-12-03 16:16:03	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-12-03 16:16:03	INFO	mstransform::::casa	##########################################
    2019-12-03 16:16:03	INFO	mstransform::::casa	##########################################
    2019-12-03 16:16:03	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-12-03 16:16:03	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal', outputvis='bb4.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='3', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=112, start=8, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=False, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-12-03 16:16:03	INFO	mstransform::::casa	Combine spws 3 into new output spw
    2019-12-03 16:16:03	INFO	mstransform::::casa	Parse regridding parameters
    2019-12-03 16:16:03	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal
    2019-12-03 16:16:03	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-12-03 16:16:03	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb4.ms
    2019-12-03 16:16:03	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-12-03 16:16:03	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-12-03 16:16:03	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-12-03 16:16:03	INFO	MSTransformManager::parseDataSelParams	spw selection is 3
    2019-12-03 16:16:03	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-12-03 16:16:03	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-12-03 16:16:03	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-12-03 16:16:03	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-12-03 16:16:03	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-12-03 16:16:03	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 112
    2019-12-03 16:16:03	INFO	MSTransformManager::parseFreqSpecParams	Start is 8
    2019-12-03 16:16:03	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-12-03 16:16:03	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-12-03 16:16:03	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-12-03 16:16:03	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-12-03 16:16:03	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-12-03 16:16:03	INFO	MSTransformManager::initDataSelectionParams+	[3, 0, 127, 1]
    2019-12-03 16:16:03	INFO	MSTransformManager::open	Select data
    2019-12-03 16:16:03	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-12-03 16:16:03	INFO	MSTransformDataHandler::makeSelection	21425 out of 85420 rows are going to be considered due to the selection criteria.
    2019-12-03 16:16:04	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-12-03 16:16:04	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 3
    2019-12-03 16:16:04	INFO	MSTransformManager::regridSpwAux	Input SPW:   128 channels, first channel = 3.490024375e+11 Hz, last channel = 3.509868125e+11 Hz, first width = 1.562500000e+07 Hz, last width = 1.562500000e+07 Hz
    2019-12-03 16:16:04	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-12-03 16:16:04	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-12-03 16:16:04	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.4998e+11 Hz
    2019-12-03 16:16:04	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56244e+07 Hz
    2019-12-03 16:16:04	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 112
    2019-12-03 16:16:04	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.74993e+09 Hz
    2019-12-03 16:16:04	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.49105e+11 Hz, upper edge = 3.50855e+11 Hz
    2019-12-03 16:16:04	INFO	MSTransformManager::regridSpwAux	Output SPW:   112 channels, first channel = 3.491129558e+11 Hz, last channel = 3.508472588e+11 Hz, first width = 1.562435188e+07 Hz, last width = 1.562435188e+07 Hz


::


    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-6-9091c1a9e9a7> in <module>
         21                         regridms=True,outframe='lsrk',combinespws=True,mode='channel',start=8,nchan=112,width=1,
         22                         timeaverage=False,timebin='60s',maxuvwdistance=0.0,
    ---> 23                         keepflags=False,usewtspectrum=False)
         24     rmPointing(outvis)
         25 


    ~/Library/Python/3.7/lib/python/site-packages/casatasks/mstransform.py in __call__(self, vis, outputvis, createmms, separationaxis, numsubms, tileshape, field, spw, scan, antenna, correlation, timerange, intent, array, uvrange, observation, feed, datacolumn, realmodelcol, keepflags, usewtspectrum, combinespws, chanaverage, chanbin, hanning, regridms, mode, nchan, start, width, nspw, interpolation, phasecenter, restfreq, outframe, veltype, preaverage, timeaverage, timebin, timespan, maxuvwdistance, docallib, callib, douvcontsub, fitspw, fitorder, want_cont, denoising_lib, nthreads, niter, disableparallel, ddistart, taql, monolithic_processing, reindex)
        612         assert _pc.validate(doc,schema), str(_pc.errors)
        613         _logging_state_ = _start_log( 'mstransform', [ 'vis=' + repr(_pc.document['vis']), 'outputvis=' + repr(_pc.document['outputvis']), 'createmms=' + repr(_pc.document['createmms']), 'separationaxis=' + repr(_pc.document['separationaxis']), 'numsubms=' + repr(_pc.document['numsubms']), 'tileshape=' + repr(_pc.document['tileshape']), 'field=' + repr(_pc.document['field']), 'spw=' + repr(_pc.document['spw']), 'scan=' + repr(_pc.document['scan']), 'antenna=' + repr(_pc.document['antenna']), 'correlation=' + repr(_pc.document['correlation']), 'timerange=' + repr(_pc.document['timerange']), 'intent=' + repr(_pc.document['intent']), 'array=' + repr(_pc.document['array']), 'uvrange=' + repr(_pc.document['uvrange']), 'observation=' + repr(_pc.document['observation']), 'feed=' + repr(_pc.document['feed']), 'datacolumn=' + repr(_pc.document['datacolumn']), 'realmodelcol=' + repr(_pc.document['realmodelcol']), 'keepflags=' + repr(_pc.document['keepflags']), 'usewtspectrum=' + repr(_pc.document['usewtspectrum']), 'combinespws=' + repr(_pc.document['combinespws']), 'chanaverage=' + repr(_pc.document['chanaverage']), 'chanbin=' + repr(_pc.document['chanbin']), 'hanning=' + repr(_pc.document['hanning']), 'regridms=' + repr(_pc.document['regridms']), 'mode=' + repr(_pc.document['mode']), 'nchan=' + repr(_pc.document['nchan']), 'start=' + repr(_pc.document['start']), 'width=' + repr(_pc.document['width']), 'nspw=' + repr(_pc.document['nspw']), 'interpolation=' + repr(_pc.document['interpolation']), 'phasecenter=' + repr(_pc.document['phasecenter']), 'restfreq=' + repr(_pc.document['restfreq']), 'outframe=' + repr(_pc.document['outframe']), 'veltype=' + repr(_pc.document['veltype']), 'preaverage=' + repr(_pc.document['preaverage']), 'timeaverage=' + repr(_pc.document['timeaverage']), 'timebin=' + repr(_pc.document['timebin']), 'timespan=' + repr(_pc.document['timespan']), 'maxuvwdistance=' + repr(_pc.document['maxuvwdistance']), 'docallib=' + repr(_pc.document['docallib']), 'callib=' + repr(_pc.document['callib']), 'douvcontsub=' + repr(_pc.document['douvcontsub']), 'fitspw=' + repr(_pc.document['fitspw']), 'fitorder=' + repr(_pc.document['fitorder']), 'want_cont=' + repr(_pc.document['want_cont']), 'denoising_lib=' + repr(_pc.document['denoising_lib']), 'nthreads=' + repr(_pc.document['nthreads']), 'niter=' + repr(_pc.document['niter']), 'disableparallel=' + repr(_pc.document['disableparallel']), 'ddistart=' + repr(_pc.document['ddistart']), 'taql=' + repr(_pc.document['taql']), 'monolithic_processing=' + repr(_pc.document['monolithic_processing']), 'reindex=' + repr(_pc.document['reindex']) ] )
    --> 614         return _end_log( _logging_state_, 'mstransform', _mstransform_t( _pc.document['vis'], _pc.document['outputvis'], _pc.document['createmms'], _pc.document['separationaxis'], _pc.document['numsubms'], _pc.document['tileshape'], _pc.document['field'], _pc.document['spw'], _pc.document['scan'], _pc.document['antenna'], _pc.document['correlation'], _pc.document['timerange'], _pc.document['intent'], _pc.document['array'], _pc.document['uvrange'], _pc.document['observation'], _pc.document['feed'], _pc.document['datacolumn'], _pc.document['realmodelcol'], _pc.document['keepflags'], _pc.document['usewtspectrum'], _pc.document['combinespws'], _pc.document['chanaverage'], _pc.document['chanbin'], _pc.document['hanning'], _pc.document['regridms'], _pc.document['mode'], _pc.document['nchan'], _pc.document['start'], _pc.document['width'], _pc.document['nspw'], _pc.document['interpolation'], _pc.document['phasecenter'], _pc.document['restfreq'], _pc.document['outframe'], _pc.document['veltype'], _pc.document['preaverage'], _pc.document['timeaverage'], _pc.document['timebin'], _pc.document['timespan'], _pc.document['maxuvwdistance'], _pc.document['docallib'], _pc.document['callib'], _pc.document['douvcontsub'], _pc.document['fitspw'], _pc.document['fitorder'], _pc.document['want_cont'], _pc.document['denoising_lib'], _pc.document['nthreads'], _pc.document['niter'], _pc.document['disableparallel'], _pc.document['ddistart'], _pc.document['taql'], _pc.document['monolithic_processing'], _pc.document['reindex'] ) )
        615 
        616 mstransform = _mstransform( )


    ~/Library/Python/3.7/lib/python/site-packages/casatasks/private/task_mstransform.py in mstransform(vis, outputvis, createmms, separationaxis, numsubms, tileshape, field, spw, scan, antenna, correlation, timerange, intent, array, uvrange, observation, feed, datacolumn, realmodelcol, keepflags, usewtspectrum, combinespws, chanaverage, chanbin, hanning, regridms, mode, nchan, start, width, nspw, interpolation, phasecenter, restfreq, outframe, veltype, preaverage, timeaverage, timebin, timespan, maxuvwdistance, docallib, callib, douvcontsub, fitspw, fitorder, want_cont, denoising_lib, nthreads, niter, disableparallel, ddistart, taql, monolithic_processing, reindex)
        314 
        315         # Open the MS, select the data and configure the output
    --> 316         mtlocal.open()
        317 
        318         # Run the tool


    ~/Library/Python/3.7/lib/python/site-packages/casatools/mstransformer.py in open(self)
         44         """It assumes that mt.config() was run before.
         45         """
    ---> 46         _open_result = self._swigobj.open()
         47         return _open_result
         48 


    ~/Library/Python/3.7/lib/python/site-packages/casatools/__casac__/mstransformer.py in open(self)
        174 
        175         """
    --> 176         return _mstransformer.mstransformer_open(self)
        177 
        178 


    KeyboardInterrupt: 


