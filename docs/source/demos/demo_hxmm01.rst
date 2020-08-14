
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

    casatools ver: 2019.166
    casatasks ver: 2019.162


Import some convinient functions from ``rxutils``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    from rxutils.casa.proc import rmPointing  # help remove POINTING tables hidden under
    from rxutils.casa.proc import setLogfile  # help reset the casa 6 log file

2015.1.00723.S (Band 6, Cycle-3, Xue et al. 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spws Setup
^^^^^^^^^^

-  spw=0,4,8,12 228GHz H2O 211-202
-  spw=1,5,9,13 231GHz Continuum
-  spw=2,6,10,14 243GHz CI 2-1
-  spw=3,7,11,15 242GHz CO76/CI 7-6

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
    
    demo_dir='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/data/hxmm01/alma/2011.0.00539.S/'
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

    2019-10-11 18:42:05	INFO	mstransform::::casa	##########################################
    2019-10-11 18:42:05	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:42:05	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal', outputvis='bb1.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='0', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=112, start=8, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=False, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:42:05	INFO	mstransform::::casa	Combine spws 0 into new output spw
    2019-10-11 18:42:05	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-11 18:42:05	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal
    2019-10-11 18:42:05	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:42:05	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb1.ms
    2019-10-11 18:42:05	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:42:05	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:42:05	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-10-11 18:42:05	INFO	MSTransformManager::parseDataSelParams	spw selection is 0
    2019-10-11 18:42:05	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-11 18:42:05	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-11 18:42:05	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-11 18:42:05	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-11 18:42:05	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-11 18:42:05	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 112
    2019-10-11 18:42:05	INFO	MSTransformManager::parseFreqSpecParams	Start is 8
    2019-10-11 18:42:05	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-11 18:42:05	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-11 18:42:05	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:42:05	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-11 18:42:05	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-11 18:42:05	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 127, 1]
    2019-10-11 18:42:05	INFO	MSTransformManager::open	Select data
    2019-10-11 18:42:05	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:42:05	INFO	MSTransformDataHandler::makeSelection	21425 out of 85420 rows are going to be considered due to the selection criteria.
    2019-10-11 18:42:06	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-11 18:42:06	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 0
    2019-10-11 18:42:06	INFO	MSTransformManager::regridSpwAux	Input SPW:   128 channels, first channel = 3.369868125e+11 Hz, last channel = 3.350024375e+11 Hz, first width = -1.562500000e+07 Hz, last width = -1.562500000e+07 Hz
    2019-10-11 18:42:06	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-11 18:42:06	INFO	MSTransformRegridder::calcChanFreqs	 *** Encountered negative channel widths in input spectral window.
    2019-10-11 18:42:06	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-11 18:42:06	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.35981e+11 Hz
    2019-10-11 18:42:06	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-11 18:42:06	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56244e+07 Hz
    2019-10-11 18:42:06	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 112
    2019-10-11 18:42:06	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.74993e+09 Hz
    2019-10-11 18:42:06	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.35106e+11 Hz, upper edge = 3.36856e+11 Hz
    2019-10-11 18:42:06	INFO	MSTransformManager::regridSpwAux	Output SPW:   112 channels, first channel = 3.368478395e+11 Hz, last channel = 3.351135365e+11 Hz, first width = 1.562435188e+07 Hz, last width = 1.562435188e+07 Hz
    2019-10-11 18:42:06	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-11 18:42:09	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:42:09	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:42:04.728490 End time: 2019-10-11 13:42:08.736510
    2019-10-11 18:42:09	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:42:09	INFO	mstransform::::casa	##########################################


.. parsed-literal::

     44M	bb1.ms
     44M	bb1.ms


.. parsed-literal::

    2019-10-11 18:42:09	INFO	mstransform::::casa	##########################################
    2019-10-11 18:42:09	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:42:09	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal', outputvis='bb2.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='1', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=112, start=8, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=False, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:42:09	INFO	mstransform::::casa	Combine spws 1 into new output spw
    2019-10-11 18:42:09	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-11 18:42:09	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal
    2019-10-11 18:42:09	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:42:09	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb2.ms
    2019-10-11 18:42:09	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:42:09	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:42:09	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-10-11 18:42:09	INFO	MSTransformManager::parseDataSelParams	spw selection is 1
    2019-10-11 18:42:09	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-11 18:42:09	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-11 18:42:09	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-11 18:42:09	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-11 18:42:09	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-11 18:42:09	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 112
    2019-10-11 18:42:09	INFO	MSTransformManager::parseFreqSpecParams	Start is 8
    2019-10-11 18:42:09	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-11 18:42:09	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-11 18:42:09	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:42:09	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-11 18:42:09	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-11 18:42:09	INFO	MSTransformManager::initDataSelectionParams+	[1, 0, 127, 1]
    2019-10-11 18:42:09	INFO	MSTransformManager::open	Select data
    2019-10-11 18:42:09	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:42:09	INFO	MSTransformDataHandler::makeSelection	21145 out of 85420 rows are going to be considered due to the selection criteria.
    2019-10-11 18:42:10	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-11 18:42:10	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 1
    2019-10-11 18:42:10	INFO	MSTransformManager::regridSpwAux	Input SPW:   128 channels, first channel = 3.389243125e+11 Hz, last channel = 3.369399375e+11 Hz, first width = -1.562500000e+07 Hz, last width = -1.562500000e+07 Hz
    2019-10-11 18:42:10	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-11 18:42:10	INFO	MSTransformRegridder::calcChanFreqs	 *** Encountered negative channel widths in input spectral window.
    2019-10-11 18:42:10	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-11 18:42:10	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.37918e+11 Hz
    2019-10-11 18:42:10	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-11 18:42:10	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56244e+07 Hz
    2019-10-11 18:42:10	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 112
    2019-10-11 18:42:10	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.74993e+09 Hz
    2019-10-11 18:42:10	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.37043e+11 Hz, upper edge = 3.38793e+11 Hz
    2019-10-11 18:42:10	INFO	MSTransformManager::regridSpwAux	Output SPW:   112 channels, first channel = 3.387852592e+11 Hz, last channel = 3.370509561e+11 Hz, first width = 1.562435188e+07 Hz, last width = 1.562435188e+07 Hz
    2019-10-11 18:42:10	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-11 18:42:12	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:42:12	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:42:08.980516 End time: 2019-10-11 13:42:12.313884
    2019-10-11 18:42:12	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:42:12	INFO	mstransform::::casa	##########################################


.. parsed-literal::

     44M	bb2.ms
     44M	bb2.ms


.. parsed-literal::

    2019-10-11 18:42:13	INFO	mstransform::::casa	##########################################
    2019-10-11 18:42:13	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:42:13	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal', outputvis='bb3.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='2', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=112, start=8, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=False, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:42:13	INFO	mstransform::::casa	Combine spws 2 into new output spw
    2019-10-11 18:42:13	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-11 18:42:13	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal
    2019-10-11 18:42:13	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:42:13	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb3.ms
    2019-10-11 18:42:13	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:42:13	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:42:13	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-10-11 18:42:13	INFO	MSTransformManager::parseDataSelParams	spw selection is 2
    2019-10-11 18:42:13	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-11 18:42:13	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-11 18:42:13	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-11 18:42:13	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-11 18:42:13	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-11 18:42:13	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 112
    2019-10-11 18:42:13	INFO	MSTransformManager::parseFreqSpecParams	Start is 8
    2019-10-11 18:42:13	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-11 18:42:13	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-11 18:42:13	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:42:13	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-11 18:42:13	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-11 18:42:13	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 127, 1]
    2019-10-11 18:42:13	INFO	MSTransformManager::open	Select data
    2019-10-11 18:42:13	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:42:13	INFO	MSTransformDataHandler::makeSelection	21425 out of 85420 rows are going to be considered due to the selection criteria.
    2019-10-11 18:42:14	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-11 18:42:14	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 2
    2019-10-11 18:42:14	INFO	MSTransformManager::regridSpwAux	Input SPW:   128 channels, first channel = 3.470024375e+11 Hz, last channel = 3.489868125e+11 Hz, first width = 1.562500000e+07 Hz, last width = 1.562500000e+07 Hz
    2019-10-11 18:42:14	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-11 18:42:14	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-11 18:42:14	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.4798e+11 Hz
    2019-10-11 18:42:14	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56244e+07 Hz
    2019-10-11 18:42:14	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 112
    2019-10-11 18:42:14	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.74993e+09 Hz
    2019-10-11 18:42:14	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.47105e+11 Hz, upper edge = 3.48855e+11 Hz
    2019-10-11 18:42:14	INFO	MSTransformManager::regridSpwAux	Output SPW:   112 channels, first channel = 3.471130387e+11 Hz, last channel = 3.488473418e+11 Hz, first width = 1.562435188e+07 Hz, last width = 1.562435188e+07 Hz
    2019-10-11 18:42:14	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-11 18:42:16	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:42:16	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:42:12.601275 End time: 2019-10-11 13:42:16.161955
    2019-10-11 18:42:16	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:42:16	INFO	mstransform::::casa	##########################################


.. parsed-literal::

     44M	bb3.ms
     44M	bb3.ms


.. parsed-literal::

    2019-10-11 18:42:16	INFO	mstransform::::casa	##########################################
    2019-10-11 18:42:16	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:42:16	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal', outputvis='bb4.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='3', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=112, start=8, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=False, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:42:17	INFO	mstransform::::casa	Combine spws 3 into new output spw
    2019-10-11 18:42:17	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-11 18:42:17	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hxmm01/proc/2011.0.00539.S/calibrated/calibrated.ms.split.cal
    2019-10-11 18:42:17	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:42:17	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb4.ms
    2019-10-11 18:42:17	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:42:17	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:42:17	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-10-11 18:42:17	INFO	MSTransformManager::parseDataSelParams	spw selection is 3
    2019-10-11 18:42:17	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-11 18:42:17	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-11 18:42:17	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-11 18:42:17	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-11 18:42:17	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-11 18:42:17	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 112
    2019-10-11 18:42:17	INFO	MSTransformManager::parseFreqSpecParams	Start is 8
    2019-10-11 18:42:17	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-11 18:42:17	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-11 18:42:17	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:42:17	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-11 18:42:17	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-11 18:42:17	INFO	MSTransformManager::initDataSelectionParams+	[3, 0, 127, 1]
    2019-10-11 18:42:17	INFO	MSTransformManager::open	Select data
    2019-10-11 18:42:17	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:42:17	INFO	MSTransformDataHandler::makeSelection	21425 out of 85420 rows are going to be considered due to the selection criteria.
    2019-10-11 18:42:18	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-11 18:42:18	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 3
    2019-10-11 18:42:18	INFO	MSTransformManager::regridSpwAux	Input SPW:   128 channels, first channel = 3.490024375e+11 Hz, last channel = 3.509868125e+11 Hz, first width = 1.562500000e+07 Hz, last width = 1.562500000e+07 Hz
    2019-10-11 18:42:18	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-11 18:42:18	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-11 18:42:18	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 3.4998e+11 Hz
    2019-10-11 18:42:18	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 1.56244e+07 Hz
    2019-10-11 18:42:18	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 112
    2019-10-11 18:42:18	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.74993e+09 Hz
    2019-10-11 18:42:18	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 3.49105e+11 Hz, upper edge = 3.50855e+11 Hz
    2019-10-11 18:42:18	INFO	MSTransformManager::regridSpwAux	Output SPW:   112 channels, first channel = 3.491129558e+11 Hz, last channel = 3.508472588e+11 Hz, first width = 1.562435188e+07 Hz, last width = 1.562435188e+07 Hz
    2019-10-11 18:42:18	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-11 18:42:20	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:42:20	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:42:16.440852 End time: 2019-10-11 13:42:19.996538
    2019-10-11 18:42:20	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:42:20	INFO	mstransform::::casa	##########################################


.. parsed-literal::

     44M	bb4.ms
     44M	bb4.ms


.. parsed-literal::

    2019-10-11 18:42:20	INFO	mstransform::::casa	##########################################
    2019-10-11 18:42:20	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:42:20	INFO	mstransform::::casa	mstransform( vis='bb2.ms', outputvis='bb2.mfs.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=True, chanbin=112, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:42:20	INFO	ParallelDataHelper::::casa	Parse channel averaging parameters
    2019-10-11 18:42:20	INFO	MSTransformManager::parseMsSpecParams	Input file name is bb2.ms
    2019-10-11 18:42:20	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:42:20	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb2.mfs.ms
    2019-10-11 18:42:20	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:42:20	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:42:20	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-10-11 18:42:20	INFO	MSTransformManager::parseChanAvgParams	Channel average is activated
    2019-10-11 18:42:20	INFO	MSTransformManager::parseChanAvgParams	Channel bin is [112]
    2019-10-11 18:42:20	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:42:20	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-11 18:42:20	INFO	MSTransformManager::open	Select data
    2019-10-11 18:42:20	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:42:22	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-11 18:42:22	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:42:22	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:42:20.282151 End time: 2019-10-11 13:42:22.382679
    2019-10-11 18:42:22	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:42:22	INFO	mstransform::::casa	##########################################


.. parsed-literal::

    7.1M	bb2.mfs.ms
    7.1M	bb2.mfs.ms


.. parsed-literal::

    2019-10-11 18:42:23	INFO	mstransform::::casa	##########################################
    2019-10-11 18:42:23	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-11 18:42:23	INFO	mstransform::::casa	mstransform( vis='bb4.ms', outputvis='bb4.mfs.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='XMM01', spw='', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=True, chanbin=112, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-11 18:42:23	INFO	ParallelDataHelper::::casa	Parse channel averaging parameters
    2019-10-11 18:42:23	INFO	MSTransformManager::parseMsSpecParams	Input file name is bb4.ms
    2019-10-11 18:42:23	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-11 18:42:23	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb4.mfs.ms
    2019-10-11 18:42:23	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-11 18:42:23	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-11 18:42:23	INFO	MSTransformManager::parseDataSelParams	field selection is XMM01
    2019-10-11 18:42:23	INFO	MSTransformManager::parseChanAvgParams	Channel average is activated
    2019-10-11 18:42:23	INFO	MSTransformManager::parseChanAvgParams	Channel bin is [112]
    2019-10-11 18:42:23	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-11 18:42:23	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-11 18:42:23	INFO	MSTransformManager::open	Select data
    2019-10-11 18:42:23	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-11 18:42:24	INFO	ParallelDataHelper::::casa	Apply the transformations


.. parsed-literal::

    7.1M	bb4.mfs.ms
    7.1M	bb4.mfs.ms


.. parsed-literal::

    2019-10-11 18:42:25	INFO	mstransform::::casa	Result mstransform: True
    2019-10-11 18:42:25	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-11 13:42:22.694760 End time: 2019-10-11 13:42:25.022492
    2019-10-11 18:42:25	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-11 18:42:25	INFO	mstransform::::casa	##########################################

