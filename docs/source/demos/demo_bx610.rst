
Example: BX610 (High-z SFG)
---------------------------

Prepare visibiity data from the calibrated MS restored by the local ALMA pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. code:: ipython3

    print('casatools ver:',ctools.version_string())
    print('casatasks ver:',ctasks.version_string())


.. parsed-literal::

    casatools ver: 2019.166
    casatasks ver: 2019.162


Import some convinient functions from ``rxutils``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    from rxutils.casa.proc import rmPointing        # help remove POINTING tables hidden under
    from rxutils.casa.proc import setLogfile        # help reset the casa 6 log file
    from rxutils.casa.proc import checkchflag       # help check channel-wise flagging stats
    from rxutils.casa.proc import getcommonfreqs    # obatin the frequency coverage of one SPW in a specified frame (e.g. TOPO-LSRK)

2013.1.00059.S (Band 4, Cycle-2, Aravena M.)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spws Setup
^^^^^^^^^^

-  spw=0 153GHz CI 1-0
-  spw=1 155GHz Continuum
-  spw=2 143GHz CO 4-3
-  spw=3 141GHz Continuum

Beam: 0.35“x0.30”

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

1 We can’t remove ms/POINTING table using ``rmtables()`` as its abence
will crash certain CASA tasks/tools (e.g. listable); instead, we set it
to have empty row, as it’s done in ``rmPointing()``.

.. code:: ipython3

    
    # Switch working directory
    
    demo_dir='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/data/bx610/alma/2013.1.00059.S/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_bx610.log')
    
    vis_name='/Volumes/D1/projects/hzdyn/2013.1.00059.S/science_goal.uid___A001_X12b_X239/group.uid___A001_X12b_X23a/member.uid___A001_X12b_X23b/calibrated/uid___A001_X12b_X23c_target.ms'
    #ctasks.listobs(vis_name)
    
    
    spw_list=['0','1','2','3']
    bb_list=['1','2','3','4']
    field='BX610'
    
    # For BB1 & BB2 & BB3 & BB4: TOPO->LSKR
    
    """
    for i in range(0,4):
        outvis='bb'+bb_list[i]+'.ms'
        os.system('rm -rf '+outvis)
        ctasks.mstransform(vis_name,outputvis=outvis,field='BX610',spw=spw_list[i],datacolumn='data',
                            regridms=True,outframe='lsrk',combinespws=True,mode='channel',start=1,nchan=478,width=1,
                            timeaverage=True,timebin='60s',maxuvwdistance=0.0,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)
    
    """
    
    # For BB2/BB4: Channel-averging
    
    for i in range(0,4):
        if  bb_list[i]=='1' or bb_list[i]=='3':
            continue
        outvis='bb'+bb_list[i]+'.mfs.ms'
        os.system('rm -rf '+outvis)
        ctasks.mstransform('bb'+bb_list[i]+'.ms',outputvis=outvis,field='BX610',datacolumn='data',
                            chanaverage=True,chanbin=478,
                            timeaverage=False,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)



.. parsed-literal::

    2019-10-14 16:37:38	INFO	mstransform::::casa	##########################################
    2019-10-14 16:37:38	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-14 16:37:38	INFO	mstransform::::casa	mstransform( vis='bb2.ms', outputvis='bb2.mfs.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=True, chanbin=478, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-14 16:37:38	INFO	ParallelDataHelper::::casa	Parse channel averaging parameters
    2019-10-14 16:37:38	INFO	MSTransformManager::parseMsSpecParams	Input file name is bb2.ms
    2019-10-14 16:37:38	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-14 16:37:38	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb2.mfs.ms
    2019-10-14 16:37:38	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-14 16:37:38	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-14 16:37:38	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-14 16:37:38	INFO	MSTransformManager::parseChanAvgParams	Channel average is activated
    2019-10-14 16:37:38	INFO	MSTransformManager::parseChanAvgParams	Channel bin is [478]
    2019-10-14 16:37:38	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-14 16:37:38	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-14 16:37:38	INFO	MSTransformManager::open	Select data
    2019-10-14 16:37:38	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-14 16:37:41	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-14 16:37:49	INFO	mstransform::::casa	Result mstransform: True
    2019-10-14 16:37:49	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-14 11:37:38.134344 End time: 2019-10-14 11:37:48.863458
    2019-10-14 16:37:49	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-14 16:37:49	INFO	mstransform::::casa	##########################################


.. parsed-literal::

     40M	bb2.mfs.ms


.. parsed-literal::

    2019-10-14 16:37:49	INFO	mstransform::::casa	##########################################
    2019-10-14 16:37:49	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-14 16:37:49	INFO	mstransform::::casa	mstransform( vis='bb4.ms', outputvis='bb4.mfs.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=True, chanbin=478, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-14 16:37:49	INFO	ParallelDataHelper::::casa	Parse channel averaging parameters
    2019-10-14 16:37:49	INFO	MSTransformManager::parseMsSpecParams	Input file name is bb4.ms
    2019-10-14 16:37:49	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-14 16:37:49	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb4.mfs.ms
    2019-10-14 16:37:49	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-14 16:37:49	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-14 16:37:49	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-14 16:37:49	INFO	MSTransformManager::parseChanAvgParams	Channel average is activated
    2019-10-14 16:37:49	INFO	MSTransformManager::parseChanAvgParams	Channel bin is [478]
    2019-10-14 16:37:49	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-14 16:37:49	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-14 16:37:49	INFO	MSTransformManager::open	Select data
    2019-10-14 16:37:49	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-14 16:37:52	INFO	ParallelDataHelper::::casa	Apply the transformations


.. parsed-literal::

     40M	bb4.mfs.ms


.. parsed-literal::

    2019-10-14 16:37:59	INFO	mstransform::::casa	Result mstransform: True
    2019-10-14 16:37:59	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-14 11:37:49.137738 End time: 2019-10-14 11:37:59.379531
    2019-10-14 16:37:59	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-14 16:37:59	INFO	mstransform::::casa	##########################################


2015.1.00250.S (Band 6, Cycle-3, Aravena M.)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spws Setup
^^^^^^^^^^

-  spw=0 BB1 250GHz Continuum
-  spw=1 BB2 252GHz CO 7-6 / CI 2-1
-  spw=2 BB3 234GHz H2O
-  spw=3 BB4 236GHz Continuum

Beam: 0.27“x0.24”

.. code:: ipython3

    # Switch working directory
    
    demo_dir='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_bx610.log')
    
    vis_name='/Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms'
    #ctasks.listobs(vis_name)
    
    
    spw_list=['0','1','2','3']
    bb_list=['1','2','3','4']
    field='BX610'
    
    # For BB1 & BB2 & BB3 & BB4: TOPO->LSKR
    
    
    for i in range(0,4):
        outvis='bb'+bb_list[i]+'.ms'
        os.system('rm -rf '+outvis)
        ctasks.mstransform(vis_name,outputvis=outvis,field='BX610',spw=spw_list[i],datacolumn='data',
                            regridms=True,outframe='lsrk',combinespws=True,mode='channel',start=1,nchan=238,width=1,
                            timeaverage=True,timebin='60s',maxuvwdistance=0.0,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)
        
    # For BB1/BB4: Channel-averging
    
    for i in range(0,4):
        if  bb_list[i]=='2' or bb_list[i]=='3':
            continue
        outvis='bb'+bb_list[i]+'.mfs.ms'
        os.system('rm -rf '+outvis)
        ctasks.mstransform('bb'+bb_list[i]+'.ms',outputvis=outvis,field='BX610',datacolumn='data',
                            chanaverage=True,chanbin=238,
                            timeaverage=False,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)    



.. parsed-literal::

    2019-10-14 16:44:11	INFO	mstransform::::casa	##########################################
    2019-10-14 16:44:11	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-14 16:44:11	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms', outputvis='bb1.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='0', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=238, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-14 16:44:11	INFO	mstransform::::casa	Combine spws 0 into new output spw
    2019-10-14 16:44:11	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-14 16:44:11	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-14 16:44:11	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms
    2019-10-14 16:44:11	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-14 16:44:11	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb1.ms
    2019-10-14 16:44:11	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-14 16:44:11	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-14 16:44:11	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-14 16:44:11	INFO	MSTransformManager::parseDataSelParams	spw selection is 0
    2019-10-14 16:44:11	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-14 16:44:11	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-14 16:44:11	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-14 16:44:11	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-14 16:44:11	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-14 16:44:11	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 238
    2019-10-14 16:44:11	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-10-14 16:44:11	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-14 16:44:11	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-14 16:44:11	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-14 16:44:11	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-14 16:44:11	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-14 16:44:11	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-14 16:44:11	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-14 16:44:11	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-10-14 16:44:11	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-14 16:44:11	INFO	MSTransformManager::initDataSelectionParams+	[0, 0, 239, 1]
    2019-10-14 16:44:11	INFO	MSTransformManager::open	Select data
    2019-10-14 16:44:11	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-14 16:44:13	INFO	MSTransformDataHandler::makeSelection	515942 out of 2353400 rows are going to be considered due to the selection criteria.
    2019-10-14 16:44:21	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-14 16:44:21	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 0
    2019-10-14 16:44:21	INFO	MSTransformManager::regridSpwAux	Input SPW:   240 channels, first channel = 2.491610813e+11 Hz, last channel = 2.510282688e+11 Hz, first width = 7.812500000e+06 Hz, last width = 7.812500000e+06 Hz
    2019-10-14 16:44:21	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-14 16:44:21	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-14 16:44:21	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.50073e+11 Hz
    2019-10-14 16:44:21	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 7.81183e+06 Hz
    2019-10-14 16:44:21	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 238
    2019-10-14 16:44:21	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.85922e+09 Hz
    2019-10-14 16:44:21	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.49144e+11 Hz, upper edge = 2.51003e+11 Hz
    2019-10-14 16:44:21	INFO	MSTransformManager::regridSpwAux	Output SPW:   238 channels, first channel = 2.491476712e+11 Hz, last channel = 2.509990760e+11 Hz, first width = 7.811834582e+06 Hz, last width = 7.811834582e+06 Hz
    2019-10-14 16:44:21	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-14 16:44:22	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-14 16:44:51	INFO	mstransform::::casa	Result mstransform: True
    2019-10-14 16:44:51	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-14 11:44:10.594830 End time: 2019-10-14 11:44:50.955703
    2019-10-14 16:44:51	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-14 16:44:51	INFO	mstransform::::casa	##########################################
    sh: -c: line 0: syntax error near unexpected token `('
    sh: -c: line 0: `After rmPointing()'


.. parsed-literal::

    245M	bb1.ms


.. parsed-literal::

    2019-10-14 16:45:24	INFO	mstransform::::casa	##########################################
    2019-10-14 16:45:24	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-14 16:45:24	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms', outputvis='bb2.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='1', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=238, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-14 16:45:24	INFO	mstransform::::casa	Combine spws 1 into new output spw
    2019-10-14 16:45:24	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-14 16:45:24	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-14 16:45:24	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms
    2019-10-14 16:45:24	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-14 16:45:24	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb2.ms
    2019-10-14 16:45:24	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-14 16:45:24	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-14 16:45:24	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-14 16:45:24	INFO	MSTransformManager::parseDataSelParams	spw selection is 1
    2019-10-14 16:45:24	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-14 16:45:24	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-14 16:45:24	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-14 16:45:24	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-14 16:45:24	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-14 16:45:24	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 238
    2019-10-14 16:45:24	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-10-14 16:45:24	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-14 16:45:24	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-14 16:45:24	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-14 16:45:24	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-14 16:45:24	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-14 16:45:24	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-14 16:45:24	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-14 16:45:24	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-10-14 16:45:24	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-14 16:45:24	INFO	MSTransformManager::initDataSelectionParams+	[1, 0, 239, 1]
    2019-10-14 16:45:24	INFO	MSTransformManager::open	Select data
    2019-10-14 16:45:24	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-14 16:45:26	INFO	MSTransformDataHandler::makeSelection	515942 out of 2353400 rows are going to be considered due to the selection criteria.
    2019-10-14 16:45:35	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-14 16:45:35	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 1
    2019-10-14 16:45:35	INFO	MSTransformManager::regridSpwAux	Input SPW:   240 channels, first channel = 2.507664063e+11 Hz, last channel = 2.526335938e+11 Hz, first width = 7.812500000e+06 Hz, last width = 7.812500000e+06 Hz
    2019-10-14 16:45:35	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-14 16:45:35	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-14 16:45:35	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.51679e+11 Hz
    2019-10-14 16:45:35	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 7.81183e+06 Hz
    2019-10-14 16:45:35	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 238
    2019-10-14 16:45:35	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.85922e+09 Hz
    2019-10-14 16:45:35	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.50749e+11 Hz, upper edge = 2.52608e+11 Hz
    2019-10-14 16:45:35	INFO	MSTransformManager::regridSpwAux	Output SPW:   238 channels, first channel = 2.507528594e+11 Hz, last channel = 2.526042642e+11 Hz, first width = 7.811834582e+06 Hz, last width = 7.811834582e+06 Hz
    2019-10-14 16:45:35	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-14 16:45:35	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-14 16:46:06	INFO	mstransform::::casa	Result mstransform: True
    2019-10-14 16:46:06	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-14 11:45:24.067595 End time: 2019-10-14 11:46:06.401140
    2019-10-14 16:46:06	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-14 16:46:06	INFO	mstransform::::casa	##########################################
    sh: -c: line 0: syntax error near unexpected token `('
    sh: -c: line 0: `After rmPointing()'


.. parsed-literal::

    245M	bb2.ms


.. parsed-literal::

    2019-10-14 16:46:37	INFO	mstransform::::casa	##########################################
    2019-10-14 16:46:37	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-14 16:46:37	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms', outputvis='bb3.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='2', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=238, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-14 16:46:38	INFO	mstransform::::casa	Combine spws 2 into new output spw
    2019-10-14 16:46:38	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-14 16:46:38	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-14 16:46:38	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms
    2019-10-14 16:46:38	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-14 16:46:38	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb3.ms
    2019-10-14 16:46:38	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-14 16:46:38	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-14 16:46:38	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-14 16:46:38	INFO	MSTransformManager::parseDataSelParams	spw selection is 2
    2019-10-14 16:46:38	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-14 16:46:38	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-14 16:46:38	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-14 16:46:38	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-14 16:46:38	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-14 16:46:38	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 238
    2019-10-14 16:46:38	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-10-14 16:46:38	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-14 16:46:38	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-14 16:46:38	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-14 16:46:38	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-14 16:46:38	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-14 16:46:38	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-14 16:46:38	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-14 16:46:38	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-10-14 16:46:38	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-14 16:46:38	INFO	MSTransformManager::initDataSelectionParams+	[2, 0, 239, 1]
    2019-10-14 16:46:38	INFO	MSTransformManager::open	Select data
    2019-10-14 16:46:38	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-14 16:46:40	INFO	MSTransformDataHandler::makeSelection	489423 out of 2353400 rows are going to be considered due to the selection criteria.
    2019-10-14 16:46:51	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-14 16:46:51	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 2
    2019-10-14 16:46:51	INFO	MSTransformManager::regridSpwAux	Input SPW:   240 channels, first channel = 2.351335937e+11 Hz, last channel = 2.332664062e+11 Hz, first width = -7.812500000e+06 Hz, last width = -7.812500000e+06 Hz
    2019-10-14 16:46:51	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-14 16:46:51	INFO	MSTransformRegridder::calcChanFreqs	 *** Encountered negative channel widths in input spectral window.
    2019-10-14 16:46:51	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-14 16:46:51	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.3418e+11 Hz
    2019-10-14 16:46:51	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-14 16:46:51	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 7.81183e+06 Hz
    2019-10-14 16:46:51	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 238
    2019-10-14 16:46:51	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.85922e+09 Hz
    2019-10-14 16:46:51	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.3325e+11 Hz, upper edge = 2.3511e+11 Hz
    2019-10-14 16:46:51	INFO	MSTransformManager::regridSpwAux	Output SPW:   238 channels, first channel = 2.351057548e+11 Hz, last channel = 2.332543500e+11 Hz, first width = 7.811834582e+06 Hz, last width = 7.811834582e+06 Hz
    2019-10-14 16:46:51	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-14 16:46:52	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-14 16:47:51	INFO	mstransform::::casa	Result mstransform: True
    2019-10-14 16:47:51	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-14 11:46:37.220774 End time: 2019-10-14 11:47:51.439951
    2019-10-14 16:47:51	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-14 16:47:51	INFO	mstransform::::casa	##########################################
    sh: -c: line 0: syntax error near unexpected token `('
    sh: -c: line 0: `After rmPointing()'


.. parsed-literal::

    244M	bb3.ms


.. parsed-literal::

    2019-10-14 16:48:26	INFO	mstransform::::casa	##########################################
    2019-10-14 16:48:26	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-14 16:48:26	INFO	mstransform::::casa	mstransform( vis='/Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms', outputvis='bb4.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='3', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='channel', nchan=238, start=1, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-14 16:48:26	INFO	mstransform::::casa	Combine spws 3 into new output spw
    2019-10-14 16:48:26	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-14 16:48:26	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-14 16:48:26	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/calibrated/uid___A001_X2fe_X20f_target.ms
    2019-10-14 16:48:26	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-14 16:48:26	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb4.ms
    2019-10-14 16:48:26	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-14 16:48:26	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-14 16:48:26	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-14 16:48:26	INFO	MSTransformManager::parseDataSelParams	spw selection is 3
    2019-10-14 16:48:26	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-14 16:48:26	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-14 16:48:26	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-14 16:48:26	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-14 16:48:26	INFO	MSTransformManager::parseFreqSpecParams	Mode is channel
    2019-10-14 16:48:26	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 238
    2019-10-14 16:48:26	INFO	MSTransformManager::parseFreqSpecParams	Start is 1
    2019-10-14 16:48:26	INFO	MSTransformManager::parseFreqSpecParams	Width is 1
    2019-10-14 16:48:26	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-14 16:48:26	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-14 16:48:26	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-14 16:48:26	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-14 16:48:26	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-14 16:48:26	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-14 16:48:26	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [4]
    2019-10-14 16:48:26	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-14 16:48:26	INFO	MSTransformManager::initDataSelectionParams+	[3, 0, 239, 1]
    2019-10-14 16:48:26	INFO	MSTransformManager::open	Select data
    2019-10-14 16:48:26	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-14 16:48:28	INFO	MSTransformDataHandler::makeSelection	515942 out of 2353400 rows are going to be considered due to the selection criteria.
    2019-10-14 16:48:36	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-14 16:48:36	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 3
    2019-10-14 16:48:36	INFO	MSTransformManager::regridSpwAux	Input SPW:   240 channels, first channel = 2.368335937e+11 Hz, last channel = 2.349664062e+11 Hz, first width = -7.812500000e+06 Hz, last width = -7.812500000e+06 Hz
    2019-10-14 16:48:36	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-14 16:48:36	INFO	MSTransformRegridder::calcChanFreqs	 *** Encountered negative channel widths in input spectral window.
    2019-10-14 16:48:36	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-14 16:48:36	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.3588e+11 Hz
    2019-10-14 16:48:36	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-14 16:48:36	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 7.81183e+06 Hz
    2019-10-14 16:48:36	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 238
    2019-10-14 16:48:36	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.85922e+09 Hz
    2019-10-14 16:48:36	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.3495e+11 Hz, upper edge = 2.3681e+11 Hz
    2019-10-14 16:48:36	INFO	MSTransformManager::regridSpwAux	Output SPW:   238 channels, first channel = 2.368056100e+11 Hz, last channel = 2.349542052e+11 Hz, first width = 7.811834582e+06 Hz, last width = 7.811834582e+06 Hz
    2019-10-14 16:48:36	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-14 16:48:37	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-14 16:49:10	INFO	mstransform::::casa	Result mstransform: True
    2019-10-14 16:49:10	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-14 11:48:25.875850 End time: 2019-10-14 11:49:09.989810
    2019-10-14 16:49:10	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-14 16:49:10	INFO	mstransform::::casa	##########################################
    sh: -c: line 0: syntax error near unexpected token `('
    sh: -c: line 0: `After rmPointing()'


.. parsed-literal::

    245M	bb4.ms


.. parsed-literal::

    2019-10-14 16:49:42	INFO	mstransform::::casa	##########################################
    2019-10-14 16:49:42	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-14 16:49:42	INFO	mstransform::::casa	mstransform( vis='bb1.ms', outputvis='bb1.mfs.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=True, chanbin=238, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-14 16:49:43	INFO	ParallelDataHelper::::casa	Parse channel averaging parameters
    2019-10-14 16:49:43	INFO	MSTransformManager::parseMsSpecParams	Input file name is bb1.ms
    2019-10-14 16:49:43	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-14 16:49:43	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb1.mfs.ms
    2019-10-14 16:49:43	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-14 16:49:43	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-14 16:49:43	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-14 16:49:43	INFO	MSTransformManager::parseChanAvgParams	Channel average is activated
    2019-10-14 16:49:43	INFO	MSTransformManager::parseChanAvgParams	Channel bin is [238]
    2019-10-14 16:49:43	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-14 16:49:43	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-14 16:49:43	INFO	MSTransformManager::open	Select data
    2019-10-14 16:49:43	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-14 16:49:46	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-14 16:49:49	INFO	mstransform::::casa	Result mstransform: True
    2019-10-14 16:49:49	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-14 11:49:42.476912 End time: 2019-10-14 11:49:49.491472
    2019-10-14 16:49:49	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-14 16:49:49	INFO	mstransform::::casa	##########################################
    sh: -c: line 0: syntax error near unexpected token `('
    sh: -c: line 0: `After rmPointing()'


.. parsed-literal::

     32M	bb1.mfs.ms


.. parsed-literal::

    2019-10-14 16:49:50	INFO	mstransform::::casa	##########################################
    2019-10-14 16:49:50	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-14 16:49:50	INFO	mstransform::::casa	mstransform( vis='bb4.ms', outputvis='bb4.mfs.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='', scan='', antenna='', correlation='', timerange='', intent='', array='', uvrange='', observation='', feed='', datacolumn='data', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=False, chanaverage=True, chanbin=238, hanning=False, regridms=False, mode='channel', nchan=-1, start=0, width=1, nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='', veltype='radio', preaverage=False, timeaverage=False, timebin='0s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-14 16:49:50	INFO	ParallelDataHelper::::casa	Parse channel averaging parameters
    2019-10-14 16:49:50	INFO	MSTransformManager::parseMsSpecParams	Input file name is bb4.ms
    2019-10-14 16:49:50	INFO	MSTransformManager::parseMsSpecParams	Data column is DATA
    2019-10-14 16:49:50	INFO	MSTransformManager::parseMsSpecParams	Output file name is bb4.mfs.ms
    2019-10-14 16:49:50	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-14 16:49:50	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-14 16:49:50	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-14 16:49:50	INFO	MSTransformManager::parseChanAvgParams	Channel average is activated
    2019-10-14 16:49:50	INFO	MSTransformManager::parseChanAvgParams	Channel bin is [238]
    2019-10-14 16:49:50	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input DATA column
    2019-10-14 16:49:50	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [0]
    2019-10-14 16:49:50	INFO	MSTransformManager::open	Select data
    2019-10-14 16:49:50	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-14 16:49:54	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-14 16:49:58	INFO	mstransform::::casa	Result mstransform: True
    2019-10-14 16:49:58	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-14 11:49:49.903919 End time: 2019-10-14 11:49:58.338018
    2019-10-14 16:49:58	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-14 16:49:58	INFO	mstransform::::casa	##########################################
    sh: -c: line 0: syntax error near unexpected token `('
    sh: -c: line 0: `After rmPointing()'


.. parsed-literal::

     32M	bb4.mfs.ms


2017.1.01045.S (Band 4, Cycle-5, Aravena M.)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spws Setup
^^^^^^^^^^

-  spw=29/2 BB=3 153GHz CI 1-0
-  spw=31/3 BB=4 155GHz Continuum
-  spw=25/0 BB=1 143GHz CO 4-3
-  spw=27/1 BB=2 141GHz Continuum

Beam: 0.35“x0.30”

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

1 We can’t remove ms/POINTING table using ``rmtables()`` as its abence
will crash certain CASA tasks/tools (e.g. listable); instead, we set it
to have empty row, as it’s done in ``rmPointing()``.

.. code:: ipython3

    
    demo_dir='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_bx610.log')
    
    repo='/Volumes/D3/alma/2017.1.01045.S/science_goal.uid___A001_X1288_X10c4/group.uid___A001_X1288_X10c5/member.uid___A001_X1288_X10c6/calibrated/working/'
    uid_list=['uid___A002_Xc69057_X91a','uid___A002_Xc69057_Xc5c','uid___A002_Xc69057_X1293','uid___A002_Xc6a3db_X430'] #uid___A002_Xc6a3db_X430.ms
    
    spw_list=['25','27','29','31']
    bb_list=['1','2','3','4']
    field='BX610'
    
    # For BB1 & BB2 & BB3 & BB4: TOPO->LSKR
    
    for i in range(0,1):
    
        freqs,chanwidth=getcommonfreqs([repo+'/'+uid+'.ms' for uid in uid_list],
                                       [spw_list[i]]*len(uid_list),
                                       chanbin=4,frame='LSRK',edge=1)
        print(min(freqs),max(freqs),chanwidth,len(freqs))
        
        vis_list=[]
        for uid in uid_list:
            vis_name=repo+uid+'.ms'
            outvis=uid+'_bb'+bb_list[i]+'.ms'
            os.system('rm -rf '+outvis)
            # use mode='freuqnecy' so if spw from different sessions are offseted, the concat result will still contain a single LSRK spw
            ctasks.mstransform(vis_name,outputvis=outvis,field='BX610',spw=spw_list[i],datacolumn='corrected',
                                regridms=True,outframe='lsrk',combinespws=True,mode='frequency',\
                                start=str(min(freqs))+'Hz',nchan=len(freqs),width=str(chanwidth)+'Hz',
                                timeaverage=True,timebin='60s',maxuvwdistance=0.0,
                                keepflags=False,usewtspectrum=False,intent='OBSERVE_TARGET#ON_SOURCE')                            
            rmPointing(outvis,verbose=True)
            vis_list+=[outvis]
    
        os.system('rm -rf '+'bb'+bb_list[i]+'.ms')
        ctasks.concat(vis=vis_list,concatvis='bb'+bb_list[i]+'.ms',copypointing=True)
        ctasks.listobs('bb'+bb_list[i]+'.ms')
     
    
    """
    # For BB2/BB4: Channel-averging
    
    for i in range(0,4):
        if  bb_list[i]=='1' or bb_list[i]=='3':
            continue
        outvis='bb'+bb_list[i]+'.mfs.ms'
        os.system('rm -rf '+outvis)
        ctasks.mstransform('bb'+bb_list[i]+'.ms',outputvis=outvis,field='BX610',datacolumn='data',
                            chanaverage=True,chanbin=478,
                            timeaverage=False,
                            keepflags=False,usewtspectrum=False)
        rmPointing(outvis)
    """    
    ##########
    



.. parsed-literal::

    2019-10-18 18:46:27	INFO	ms::cvelfreqs	Calculating grid ...
    2019-10-18 18:46:27	INFO	ms::cvelfreqs	Using observation time from earliest row of the MS given the SPW and FIELD selection:
    2019-10-18 18:46:27	INFO	ms::cvelfreqs	    2017/11/06/23:02:01 (UTC)
    2019-10-18 18:46:27	INFO	ms::cvelfreqs	Using tabulated observatory position for ALMA:
    2019-10-18 18:46:27	INFO	ms::cvelfreqs	   Position: [2.22514e+06, -5.44031e+06, -2.48103e+06] (ITRF)
    2019-10-18 18:46:27	INFO	SubMS::convertGridPars	 *** Encountered negative channel widths in input spectral window.
    2019-10-18 18:46:27	INFO	SubMS::convertGridPars	 Channels equidistant in freq
    2019-10-18 18:46:27	INFO	SubMS::convertGridPars+	 Central frequency (in output frame) = 1.43569e+11 Hz
    2019-10-18 18:46:27	INFO	SubMS::convertGridPars+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-18 18:46:27	INFO	SubMS::convertGridPars+	 Width of central channel (in output frame) = 976610 Hz
    2019-10-18 18:46:27	INFO	SubMS::convertGridPars+	 Number of channels = 1920
    2019-10-18 18:46:27	INFO	SubMS::convertGridPars+	 Total width of SPW (in output frame) = 1.87509e+09 Hz
    2019-10-18 18:46:27	INFO	SubMS::convertGridPars+	 Lower edge = 1.42631e+11 Hz, upper edge = 1.44506e+11 Hz
    2019-10-18 18:46:28	INFO	ms::cvelfreqs	Calculating grid ...
    2019-10-18 18:46:28	INFO	ms::cvelfreqs	Using observation time from earliest row of the MS given the SPW and FIELD selection:
    2019-10-18 18:46:28	INFO	ms::cvelfreqs	    2017/11/07/00:33:40 (UTC)
    2019-10-18 18:46:28	INFO	ms::cvelfreqs	Using tabulated observatory position for ALMA:
    2019-10-18 18:46:28	INFO	ms::cvelfreqs	   Position: [2.22514e+06, -5.44031e+06, -2.48103e+06] (ITRF)
    2019-10-18 18:46:28	INFO	SubMS::convertGridPars	 *** Encountered negative channel widths in input spectral window.
    2019-10-18 18:46:28	INFO	SubMS::convertGridPars	 Channels equidistant in freq
    2019-10-18 18:46:28	INFO	SubMS::convertGridPars+	 Central frequency (in output frame) = 1.43569e+11 Hz
    2019-10-18 18:46:28	INFO	SubMS::convertGridPars+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-18 18:46:28	INFO	SubMS::convertGridPars+	 Width of central channel (in output frame) = 976611 Hz
    2019-10-18 18:46:28	INFO	SubMS::convertGridPars+	 Number of channels = 1920
    2019-10-18 18:46:28	INFO	SubMS::convertGridPars+	 Total width of SPW (in output frame) = 1.87509e+09 Hz
    2019-10-18 18:46:28	INFO	SubMS::convertGridPars+	 Lower edge = 1.42631e+11 Hz, upper edge = 1.44506e+11 Hz
    2019-10-18 18:46:29	INFO	ms::cvelfreqs	Calculating grid ...
    2019-10-18 18:46:30	INFO	ms::cvelfreqs	Using observation time from earliest row of the MS given the SPW and FIELD selection:
    2019-10-18 18:46:30	INFO	ms::cvelfreqs	    2017/11/07/02:51:17 (UTC)
    2019-10-18 18:46:30	INFO	ms::cvelfreqs	Using tabulated observatory position for ALMA:
    2019-10-18 18:46:30	INFO	ms::cvelfreqs	   Position: [2.22514e+06, -5.44031e+06, -2.48103e+06] (ITRF)
    2019-10-18 18:46:30	INFO	SubMS::convertGridPars	 *** Encountered negative channel widths in input spectral window.
    2019-10-18 18:46:30	INFO	SubMS::convertGridPars	 Channels equidistant in freq
    2019-10-18 18:46:30	INFO	SubMS::convertGridPars+	 Central frequency (in output frame) = 1.43569e+11 Hz
    2019-10-18 18:46:30	INFO	SubMS::convertGridPars+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-18 18:46:30	INFO	SubMS::convertGridPars+	 Width of central channel (in output frame) = 976612 Hz
    2019-10-18 18:46:30	INFO	SubMS::convertGridPars+	 Number of channels = 1920
    2019-10-18 18:46:30	INFO	SubMS::convertGridPars+	 Total width of SPW (in output frame) = 1.87509e+09 Hz
    2019-10-18 18:46:30	INFO	SubMS::convertGridPars+	 Lower edge = 1.42631e+11 Hz, upper edge = 1.44506e+11 Hz
    2019-10-18 18:46:30	INFO	ms::cvelfreqs	Calculating grid ...
    2019-10-18 18:46:31	INFO	ms::cvelfreqs	Using observation time from earliest row of the MS given the SPW and FIELD selection:
    2019-10-18 18:46:31	INFO	ms::cvelfreqs	    2017/11/09/00:26:30 (UTC)
    2019-10-18 18:46:31	INFO	ms::cvelfreqs	Using tabulated observatory position for ALMA:
    2019-10-18 18:46:31	INFO	ms::cvelfreqs	   Position: [2.22514e+06, -5.44031e+06, -2.48103e+06] (ITRF)
    2019-10-18 18:46:31	INFO	SubMS::convertGridPars	 *** Encountered negative channel widths in input spectral window.
    2019-10-18 18:46:31	INFO	SubMS::convertGridPars	 Channels equidistant in freq
    2019-10-18 18:46:31	INFO	SubMS::convertGridPars+	 Central frequency (in output frame) = 1.43569e+11 Hz
    2019-10-18 18:46:31	INFO	SubMS::convertGridPars+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-18 18:46:31	INFO	SubMS::convertGridPars+	 Width of central channel (in output frame) = 976613 Hz
    2019-10-18 18:46:31	INFO	SubMS::convertGridPars+	 Number of channels = 1920
    2019-10-18 18:46:31	INFO	SubMS::convertGridPars+	 Total width of SPW (in output frame) = 1.8751e+09 Hz
    2019-10-18 18:46:31	INFO	SubMS::convertGridPars+	 Lower edge = 1.42631e+11 Hz, upper edge = 1.44506e+11 Hz
    2019-10-18 18:46:31	INFO	mstransform::::casa	##########################################
    2019-10-18 18:46:31	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-18 18:46:31	INFO	mstransform::::casa	mstransform( vis='/Volumes/D3/alma/2017.1.01045.S/science_goal.uid___A001_X1288_X10c4/group.uid___A001_X1288_X10c5/member.uid___A001_X1288_X10c6/calibrated/working/uid___A002_Xc69057_X91a.ms', outputvis='uid___A002_Xc69057_X91a_bb1.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='25', scan='', antenna='', correlation='', timerange='', intent='OBSERVE_TARGET#ON_SOURCE', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='frequency', nchan=479, start='142633992676.3963Hz', width='3906451.4650878906Hz', nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )


.. parsed-literal::

    142633992676.3963 144501276476.7083 3906451.4650878906 479


.. parsed-literal::

    2019-10-18 18:46:31	INFO	mstransform::::casa	Combine spws 25 into new output spw
    2019-10-18 18:46:31	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-18 18:46:31	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-18 18:46:31	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D3/alma/2017.1.01045.S/science_goal.uid___A001_X1288_X10c4/group.uid___A001_X1288_X10c5/member.uid___A001_X1288_X10c6/calibrated/working/uid___A002_Xc69057_X91a.ms
    2019-10-18 18:46:31	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-10-18 18:46:31	INFO	MSTransformManager::parseMsSpecParams	Output file name is uid___A002_Xc69057_X91a_bb1.ms
    2019-10-18 18:46:31	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-18 18:46:31	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-18 18:46:31	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-18 18:46:31	INFO	MSTransformManager::parseDataSelParams	spw selection is 25
    2019-10-18 18:46:31	INFO	MSTransformManager::parseDataSelParams	scan intent selection is OBSERVE_TARGET#ON_SOURCE
    2019-10-18 18:46:31	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-18 18:46:31	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-18 18:46:31	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-18 18:46:31	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-18 18:46:31	INFO	MSTransformManager::parseFreqSpecParams	Mode is frequency
    2019-10-18 18:46:31	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 479
    2019-10-18 18:46:31	INFO	MSTransformManager::parseFreqSpecParams	Start is 142633992676.3963Hz
    2019-10-18 18:46:31	INFO	MSTransformManager::parseFreqSpecParams	Width is 3906451.4650878906Hz
    2019-10-18 18:46:31	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-18 18:46:31	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-18 18:46:31	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-18 18:46:31	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-18 18:46:31	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-18 18:46:31	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-10-18 18:46:31	INFO	MSTransformManager::initDataSelectionParams	Selected Scans Intents Ids are [16]
    2019-10-18 18:46:31	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [3]
    2019-10-18 18:46:31	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-18 18:46:31	INFO	MSTransformManager::initDataSelectionParams+	[25, 0, 1919, 1]
    2019-10-18 18:46:31	INFO	MSTransformManager::open	Select data
    2019-10-18 18:46:31	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-18 18:46:44	INFO	MSTransformDataHandler::makeSelection	815745 out of 69496256 rows are going to be considered due to the selection criteria.
    2019-10-18 18:46:48	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-18 18:46:48	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 25
    2019-10-18 18:46:48	INFO	MSTransformManager::regridSpwAux	Input SPW:  1920 channels, first channel = 1.444985762e+11 Hz, last channel = 1.426245528e+11 Hz, first width = -9.765625000e+05 Hz, last width = -9.765625000e+05 Hz
    2019-10-18 18:46:48	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-18 18:46:48	INFO	MSTransformRegridder::calcChanFreqs	 *** Encountered negative channel widths in input spectral window.
    2019-10-18 18:46:48	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-18 18:46:48	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 1.43568e+11 Hz
    2019-10-18 18:46:48	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-18 18:46:48	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 3.90645e+06 Hz
    2019-10-18 18:46:48	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 479
    2019-10-18 18:46:48	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.87119e+09 Hz
    2019-10-18 18:46:48	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 1.42632e+11 Hz, upper edge = 1.44503e+11 Hz
    2019-10-18 18:46:48	INFO	MSTransformManager::checkAndPreaverageChannelsIfNeeded	Ratio between input and output width is >=2: 3.99999, but not doing pre-channel average (it is disabled by default since CASA release 5.0).
    2019-10-18 18:46:48	INFO	MSTransformManager::checkAndPreaverageChannelsIfNeeded	Regridding to intermediate grid (1920 channels) for interpolation as in tclean when the  ratio between the output and input widths is >2.
    2019-10-18 18:46:48	INFO	MSTransformManager::regridSpwAux	Output SPW:   479 channels, first channel = 1.445012765e+11 Hz, last channel = 1.426339927e+11 Hz, first width = 3.906451465e+06 Hz, last width = 3.906451465e+06 Hz
    2019-10-18 18:46:48	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-18 18:46:48	INFO	ParallelDataHelper::::casa	Apply the transformations
    2019-10-18 18:53:04	INFO	mstransform::::casa	Result mstransform: True
    2019-10-18 18:53:04	INFO	mstransform::::casa	Task mstransform complete. Start time: 2019-10-18 13:46:31.153249 End time: 2019-10-18 13:53:04.217099
    2019-10-18 18:53:04	INFO	mstransform::::casa	##### End Task: mstransform          #####
    2019-10-18 18:53:04	INFO	mstransform::::casa	##########################################


.. parsed-literal::

    Before rmPointing()
    1.1G	uid___A002_Xc69057_X91a_bb1.ms
    After rmPointing()
    418M	uid___A002_Xc69057_X91a_bb1.ms


.. parsed-literal::

    2019-10-18 18:53:30	INFO	mstransform::::casa	##########################################
    2019-10-18 18:53:30	INFO	mstransform::::casa	##### Begin Task: mstransform        #####
    2019-10-18 18:53:30	INFO	mstransform::::casa	mstransform( vis='/Volumes/D3/alma/2017.1.01045.S/science_goal.uid___A001_X1288_X10c4/group.uid___A001_X1288_X10c5/member.uid___A001_X1288_X10c6/calibrated/working/uid___A002_Xc69057_Xc5c.ms', outputvis='uid___A002_Xc69057_Xc5c_bb1.ms', createmms=False, separationaxis='auto', numsubms='auto', tileshape=[0], field='BX610', spw='25', scan='', antenna='', correlation='', timerange='', intent='OBSERVE_TARGET#ON_SOURCE', array='', uvrange='', observation='', feed='', datacolumn='corrected', realmodelcol=False, keepflags=False, usewtspectrum=False, combinespws=True, chanaverage=False, chanbin=1, hanning=False, regridms=True, mode='frequency', nchan=479, start='142633992676.3963Hz', width='3906451.4650878906Hz', nspw=1, interpolation='linear', phasecenter='', restfreq='', outframe='lsrk', veltype='radio', preaverage=False, timeaverage=True, timebin='60s', timespan='', maxuvwdistance=0.0, docallib=False, callib='', douvcontsub=False, fitspw='', fitorder=0, want_cont=False, denoising_lib=True, nthreads=1, niter=1, disableparallel=False, ddistart=-1, taql='', monolithic_processing=False, reindex=True )
    2019-10-18 18:53:30	INFO	mstransform::::casa	Combine spws 25 into new output spw
    2019-10-18 18:53:30	INFO	mstransform::::casa	Parse regridding parameters
    2019-10-18 18:53:30	INFO	ParallelDataHelper::::casa	Parse time averaging parameters
    2019-10-18 18:53:30	INFO	MSTransformManager::parseMsSpecParams	Input file name is /Volumes/D3/alma/2017.1.01045.S/science_goal.uid___A001_X1288_X10c4/group.uid___A001_X1288_X10c5/member.uid___A001_X1288_X10c6/calibrated/working/uid___A002_Xc69057_Xc5c.ms
    2019-10-18 18:53:30	INFO	MSTransformManager::parseMsSpecParams	Data column is CORRECTED
    2019-10-18 18:53:30	INFO	MSTransformManager::parseMsSpecParams	Output file name is uid___A002_Xc69057_Xc5c_bb1.ms
    2019-10-18 18:53:30	INFO	MSTransformManager::parseMsSpecParams	Re-index is enabled 
    2019-10-18 18:53:30	INFO	MSTransformManager::parseMsSpecParams	Tile shape is [0]
    2019-10-18 18:53:30	INFO	MSTransformManager::parseDataSelParams	field selection is BX610
    2019-10-18 18:53:30	INFO	MSTransformManager::parseDataSelParams	spw selection is 25
    2019-10-18 18:53:30	INFO	MSTransformManager::parseDataSelParams	scan intent selection is OBSERVE_TARGET#ON_SOURCE
    2019-10-18 18:53:30	INFO	MSTransformManager::parseFreqTransParams	Combine Spectral Windows is activated
    2019-10-18 18:53:30	INFO	MSTransformManager::parseRefFrameTransParams	Regrid MS is activated
    2019-10-18 18:53:30	INFO	MSTransformManager::parseRefFrameTransParams	Output reference frame is lsrk
    2019-10-18 18:53:30	INFO	MSTransformManager::parseRefFrameTransParams	Interpolation method is linear
    2019-10-18 18:53:30	INFO	MSTransformManager::parseFreqSpecParams	Mode is frequency
    2019-10-18 18:53:30	INFO	MSTransformManager::parseFreqSpecParams	Number of output channels is 479
    2019-10-18 18:53:30	INFO	MSTransformManager::parseFreqSpecParams	Start is 142633992676.3963Hz
    2019-10-18 18:53:30	INFO	MSTransformManager::parseFreqSpecParams	Width is 3906451.4650878906Hz
    2019-10-18 18:53:30	INFO	MSTransformManager::parseRefFrameTransParams	Enabling channel pre-averaging
    2019-10-18 18:53:30	INFO	MSTransformManager::parseTimeAvgParams	Time average is activated
    2019-10-18 18:53:30	INFO	MSTransformManager::parseTimeAvgParams	Time bin is 60 seconds
    2019-10-18 18:53:30	WARN	MSTransformManager::parseTimeAvgParams	Operating with ALMA data, automatically adding state to timespan 
    2019-10-18 18:53:30	WARN	MSTransformManager::parseTimeAvgParams+	In order to remove sub-scan boundaries which limit time average to 30s 
    2019-10-18 18:53:30	INFO	MSTransformManager::colCheckInfo	Adding DATA column to output MS from input CORRECTED_DATA column
    2019-10-18 18:53:30	INFO	MSTransformManager::initDataSelectionParams	Selected Scans Intents Ids are [16]
    2019-10-18 18:53:30	INFO	MSTransformManager::initDataSelectionParams	Selected Fields Ids are [3]
    2019-10-18 18:53:30	INFO	MSTransformManager::initDataSelectionParams	Selected SPWs Ids are Axis Lengths: [1, 4]  (NB: Matrix in Row/Column order)
    2019-10-18 18:53:30	INFO	MSTransformManager::initDataSelectionParams+	[25, 0, 1919, 1]
    2019-10-18 18:53:30	INFO	MSTransformManager::open	Select data
    2019-10-18 18:53:30	INFO	MSTransformManager::createOutputMSStructure	Create output MS structure
    2019-10-18 18:53:47	INFO	MSTransformDataHandler::makeSelection	831728 out of 69208973 rows are going to be considered due to the selection criteria.
    2019-10-18 18:53:55	WARN	MSTransformManager::setup	There is only one selected SPW, no need to combine 
    2019-10-18 18:53:55	INFO	MSTransformManager::regridSpwSubTable	Regridding SPW with Id 25
    2019-10-18 18:53:55	INFO	MSTransformManager::regridSpwAux	Input SPW:  1920 channels, first channel = 1.444984883e+11 Hz, last channel = 1.426244648e+11 Hz, first width = -9.765625000e+05 Hz, last width = -9.765625000e+05 Hz
    2019-10-18 18:53:55	INFO	MSTransformManager::regridSpwAux	Calculate frequencies in output reference frame 
    2019-10-18 18:53:55	INFO	MSTransformRegridder::calcChanFreqs	 *** Encountered negative channel widths in input spectral window.
    2019-10-18 18:53:55	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-10-18 18:53:55	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 1.43568e+11 Hz
    2019-10-18 18:53:55	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-10-18 18:53:55	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 3.90645e+06 Hz
    2019-10-18 18:53:55	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 479
    2019-10-18 18:53:55	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.87119e+09 Hz
    2019-10-18 18:53:55	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 1.42632e+11 Hz, upper edge = 1.44503e+11 Hz
    2019-10-18 18:53:55	INFO	MSTransformManager::checkAndPreaverageChannelsIfNeeded	Ratio between input and output width is >=2: 3.99999, but not doing pre-channel average (it is disabled by default since CASA release 5.0).
    2019-10-18 18:53:55	INFO	MSTransformManager::checkAndPreaverageChannelsIfNeeded	Regridding to intermediate grid (1920 channels) for interpolation as in tclean when the  ratio between the output and input widths is >2.
    2019-10-18 18:53:55	INFO	MSTransformManager::regridSpwAux	Output SPW:   479 channels, first channel = 1.445012765e+11 Hz, last channel = 1.426339927e+11 Hz, first width = 3.906451465e+06 Hz, last width = 3.906451465e+06 Hz
    2019-10-18 18:53:55	INFO	MSTransformManager::setIterationApproach	Combining data through state for time average
    2019-10-18 18:53:55	INFO	ParallelDataHelper::::casa	Apply the transformations


.. code:: ipython3

    142633016064.75403 144500299865.06604 3906451.4650878906 479
