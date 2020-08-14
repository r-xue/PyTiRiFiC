Test the performance of the Image-to-MS-related modules
-------------------------------------------------------

.. code:: ipython3

    import sys
    import glob
    import os
    import io
    import logging
    import emcee
    from pprint import pprint
    
    import socket 
    print(os.getcwd())
    print(socket.gethostname())
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir('/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output/')
    
    import gmake
    print(gmake.__version__)
    print(gmake.__email__)
    print(gmake.__demo__)
    gmake.check_setup()
    
    inpfile=gmake.__demo__+'/../examples/inpfile/bx610_band6_uv_mc.inp'
    logfile=''
    
    print('>'*40)
    #gmake.logger_config()
    #gmake.logger_status()
    #import pprint
    #pprint.pprint(logging.Logger.manager.loggerDict) 
    gmake.logger_config()
    inp_dct=gmake.read_inp(inpfile)
    outdir=inp_dct['optimize']['outdir']
    gmake.logger_config(logfile=outdir+'/gmake.log',loglevel='DEBUG',logfilelevel='DEBUG')
    gmake.logger_status()


.. parsed-literal::

    /Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/notebook
    hyperion


.. parsed-literal::

    Python version:   3.7.4 (default, Sep  7 2019, 19:52:29) 
    [Clang 10.0.1 (clang-1001.0.46.4)]
    Host Name:        hyperion
    Num of Core:      8
    Total Memory:     32.0 GB
    Available Memory: 11.33 GB
    ################################################################################
    astropy            >=3.2.2      4.0.dev25797
    emcee              >=3.0.0      3.0.0       
    corner             >=2.0        2.0.1       
    tqdm               unspecified  4.31.1      
    lmfit              unspecified  0.9.12      
    asteval            >=0.9.14     0.9.14      
    numexpr            >=2.7.0      2.7.0       
    hickle             unspecified  3.4.5       
    alpy               unspecified  0.22.0      
    regions            unspecified  0.3         
    scipy              unspecified  1.2.1       
    reproject          unspecified  0.6.dev644  
    python-casacore    >=3.1.1      3.1.1       
    scikit-image       unspecified  0.14.2      
    galpy              unspecified  1.5.dev0    
    mkl-fft            unspecified  1.0.14      
    pvextractor        >=0.2.dev327 0.2.dev327  
    spectral-cube      >=0.4.5.dev  0.4.5.dev2235
    radio-beam         >=0.3        0.3.3.dev397
    reproject          >=0.6.dev    0.6.dev644  
    casa-proc          unspecified  0.1.dev3    


.. parsed-literal::

    0.2.dev1
    rx.astro@gmail.com
    /Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


::


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <ipython-input-1-fecfb0ed8cdd> in <module>
         29 gmake.logger_config()
         30 inp_dct=gmake.read_inp(inpfile)
    ---> 31 outdir=inp_dct['optimize']['outdir']
         32 gmake.logger_config(logfile=outdir+'/gmake.log',loglevel='DEBUG',logfilelevel='DEBUG')
         33 gmake.logger_status()


    KeyError: 'outdir'


.. code:: ipython3

    dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True)


.. parsed-literal::

    read data (may take some time..)


::


    ---------------------------------------------------------------------------

    RuntimeError                              Traceback (most recent call last)

    <ipython-input-2-7b83568be513> in <module>
    ----> 1 dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True)
    

    ~/Dropbox/Worklib/projects/GMaKE/gmake/io_utils.py in read_data(inp_dct, fill_mask, fill_error, memorytable, polaverage, dataflag, saveflag)
         50 
         51 
    ---> 52                     t=ctb.table(vis_list[ind],ack=False,memorytable=memorytable)
         53                     # set order='F' for the quick access of u/v/w
         54                     dat_dct['uvw@'+vis_list[ind]]=(t.getcol('UVW')).astype(np.float32,order='F')


    ~/Library/Python/3.7/lib/python/site-packages/casacore/tables/table.py in __init__(self, tablename, tabledesc, nrow, readonly, lockoptions, ack, dminfo, endian, memorytable, concatsubtables, _columnnames, _datatypes, _oper, _delete)
        370                         opt = 6
        371                 if isinstance(tabname, string_types):
    --> 372                     Table.__init__(self, tabname, lockopt, opt)
        373                     if ack:
        374                         six.print_('Successful', typstr, 'open of',


    RuntimeError: Table ../data/bx610/alma/band6/bx610_band6.bb2.cube3.ms does not exist


.. code:: ipython3

    from pprint import pprint
    #pprint(dat_dct)

.. code:: ipython3

    fit_dct,sampler=gmake.fit_setup(inp_dct,dat_dct)


.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    optimizer: emcee
    optimizing parameters: index / name / start / lo_limit / up_limit / scale
     0   vsys@co76          117.49      (    -120.00   ,     280.00     )     40.00     
     1   vrot[1:5]@co76     197.04      (     0.00     ,     800.00     )     40.00     
     2   vdis[0:5]@co76      50.82      (     0.00     ,     800.00     )     10.00     
     3   pa@co76            -52.41      (    -132.41   ,      27.59     )     5.00      
     4   inc@co76            44.06      (     5.00     ,      85.00     )     5.00      
     5   xypos[0]@co76    356.5393259   (  356.5390481 ,   356.5396037  )   0.0000389   
     6   xypos[1]@co76    12.8220182    (  12.8217404  ,   12.8222960   )   0.0000389   
     7   intflux@co76        1.30       (     0.10     ,     200.00     )     0.05      
     8   sbser[0]@co76       0.22       (     0.01     ,      1.00      )     0.01      
     9   intflux@ci21        0.65       (     0.10     ,     200.00     )     0.01      
     10  sbser[0]@ci21       0.19       (     0.01     ,      1.00      )     0.01      
     11  intflux@h2o         0.38       (     0.10     ,     200.00     )     0.01      
     12  sbser[0]@h2o        0.17       (     0.01     ,      1.00      )     0.01      
     13  intflux@cont        0.00       (     0.00     ,      0.01      )     0.01      
     14  sbser[0]@cont       0.12       (     0.01     ,      0.30      )     0.01      
     15  alpha@cont          3.72       (     3.00     ,      4.50      )     0.10      
     16  pa@cont             12.06      (    -47.94    ,      72.06     )     5.00      
     17  inc@cont            27.53      (     0.00     ,      45.00     )     5.00      
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    nwalkers:40
    nthreads:1
    ndim:    18
    outdir:  bx610_band6_uv_mc
    one trial                                          : 2.12374  seconds
    ndata->80455719.0
    chisq->627572167.2467092


.. code:: ipython3

    #import gmake,time
    #import memory_profiler
    #%load_ext line_profiler
    #%load_ext memory_profiler
    #gmake.galario_threads(12)
    from galario.single import threads as galario_threads
    import multiprocessing
    galario_threads(multiprocessing.cpu_count())
    %time lnl,blobs=gmake.model_lnlike(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,savemodel=None,verbose=True)
    print(lnl,blobs)


.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++
    @ co76
    method: disk3d
    ----------------------------------------
    ++++++++++++++++++++++++++++++++++++++++
    @ ci21
    method: disk3d
    ----------------------------------------
    ++++++++++++++++++++++++++++++++++++++++
    @ h2o
    method: disk3d
    ----------------------------------------
    ++++++++++++++++++++++++++++++++++++++++
    @ cont
    method: disk2d
    ----------------------------------------
    >>>>>initialize-total : 0.09252  seconds ---
    
    ++++++++++++++++++++++++++++++++++++++++
    @ co76
    method: disk3d
    ----------------------------------------
    ++++++++++++++++++++++++++++++++++++++++
    @ ci21
    method: disk3d
    ----------------------------------------
    ++++++++++++++++++++++++++++++++++++++++
    @ h2o
    method: disk3d
    ----------------------------------------
    ++++++++++++++++++++++++++++++++++++++++
    @ cont
    method: disk2d
    ----------------------------------------
    >>>>>fill-total : 0.24356  seconds ---
    
    nchan,nrecord: 79 515942
    uvsampling plane counts:  43
    --- uvsample  : 0.54576  seconds ---
    out=in+model: True
    nchan,nrecord: 79 489423
    uvsampling plane counts:  21
    --- uvsample  : 0.29338  seconds ---
    out=in+model: True
    nchan,nrecord: 1 515942
    uvsampling plane counts:  1
    --- uvsample  : 0.01252  seconds ---
    out=in+model: True
    nchan,nrecord: 1 515942
    uvsampling plane counts:  1
    --- uvsample  : 0.01337  seconds ---
    out=in+model: True
    >>>>>simulate-total : 0.87912  seconds ---
    CPU times: user 6.6 s, sys: 244 ms, total: 6.84 s
    Wall time: 1.58 s
    -178748866.65472293 {'lnprob': -178748866.65472293, 'chisq': 627572160.4978713, 'ndata': 80455719.0, 'npar': 18}


-178748872.1410836 {‘lnprob’: -178748872.1410836, ‘chisq’:
627572171.4705925, ‘ndata’: 80455719.0, ‘npar’: 14}

++++++++++++++++++++++++++++++++++++++++ @ co76 method: disk3d
—————————————- ++++++++++++++++++++++++++++++++++++++++ @ ci21 method:
disk3d —————————————- ++++++++++++++++++++++++++++++++++++++++ @ h2o
method: disk3d —————————————- ++++++++++++++++++++++++++++++++++++++++ @
cont method: disk2d —————————————- >>>>>initialize-total : 0.10390
seconds —

++++++++++++++++++++++++++++++++++++++++ @ co76 method: disk3d
—————————————- (21, 110, 110) –> (1, 79, 256, 256) —fill:
co76–>../data/bx610/alma/band6/bx610_band6.bb2.cube3.ms disk3d : 0.07991
seconds — ++++++++++++++++++++++++++++++++++++++++ @ ci21 method: disk3d
—————————————- (21, 95, 95) –> (1, 79, 256, 256) —fill:
ci21–>../data/bx610/alma/band6/bx610_band6.bb2.cube3.ms disk3d : 0.07804
seconds — ++++++++++++++++++++++++++++++++++++++++ @ h2o method: disk3d
—————————————- (20, 79, 79) –> (1, 79, 256, 256) —fill:
h2o–>../data/bx610/alma/band6/bx610_band6.bb3.cube3.ms disk3d : 0.07822
seconds — ++++++++++++++++++++++++++++++++++++++++ @ cont method: disk2d
—————————————- (1, 1, 59, 59) –> (1, 1, 256, 256) —fill:
cont–>../data/bx610/alma/band6/bx610_band6.bb1.mfs.ms disk2d : 0.01697
seconds — (1, 79, 61, 61) –> (1, 79, 256, 256) —fill:
cont–>../data/bx610/alma/band6/bx610_band6.bb2.cube3.ms disk2d : 0.01645
seconds — (1, 79, 55, 55) –> (1, 79, 256, 256) —fill:
cont–>../data/bx610/alma/band6/bx610_band6.bb3.cube3.ms disk2d : 0.01396
seconds — (1, 1, 57, 57) –> (1, 1, 256, 256) —fill:
cont–>../data/bx610/alma/band6/bx610_band6.bb4.mfs.ms disk2d : 0.01095
seconds — >>>>>fill-total : 0.34662 seconds —

../data/bx610/alma/band6/bx610_band6.bb2.cube3.ms image model shape: (1,
79, 256, 256) nchan,nrecord: 79 515942 uvsampling plane counts: 43 —
uvsample : 0.78571 seconds — out=in+model: True

../data/bx610/alma/band6/bx610_band6.bb3.cube3.ms image model shape: (1,
79, 256, 256) nchan,nrecord: 79 489423 uvsampling plane counts: 21 —
uvsample : 0.39530 seconds — out=in+model: True

../data/bx610/alma/band6/bx610_band6.bb1.mfs.ms image model shape: (1,
1, 256, 256) nchan,nrecord: 1 515942 uvsampling plane counts: 1 —
uvsample : 0.01611 seconds — out=in+model: True

../data/bx610/alma/band6/bx610_band6.bb4.mfs.ms image model shape: (1,
1, 256, 256) nchan,nrecord: 1 515942 uvsampling plane counts: 1 —
uvsample : 0.01723 seconds — out=in+model: True >>>>>simulate-total :
1.21742 seconds — CPU times: user 6.99 s, sys: 426 ms, total: 7.41 s
Wall time: 2.09 s -178748873.92085266 {‘lnprob’: -178748873.92085266,
‘chisq’: 627572175.0301305, ‘ndata’: 80455719.0, ‘npar’: 14}

.. code:: ipython3

    import numpy as np
    import numexpr as ne
    test1=np.arange(515942,dtype='float64')
    %time test1*=1/100.0
    #print(test1)
    %time ne.evaluate("a*0.01",local_dict={'a':test1},out=test1)


.. parsed-literal::

    CPU times: user 352 µs, sys: 292 µs, total: 644 µs
    Wall time: 354 µs
    CPU times: user 3.64 ms, sys: 419 µs, total: 4.06 ms
    Wall time: 489 µs




.. parsed-literal::

    array([0.00000e+00, 1.00000e-04, 2.00000e-04, ..., 5.15939e+01,
           5.15940e+01, 5.15941e+01])



.. code:: ipython3

    from gmake.tests.test_model_build import *
    test_gmake_model_disk2d()


.. parsed-literal::

    --- 0.0295867919921875 seconds ---


.. code:: ipython3

    import gmake
    gmake.__demo__




.. parsed-literal::

    '/Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake'




.. code:: ipython3

    
    a=np.ones(1000000)
    s=np.arange(100)
    c=np.empty((1000000,100),order='F')
    start=time.time()
    for i in range(len(s)):
        #c[:,i]=a*s[i] # 0.57
        #ne.evaluate("a*b",local_dict={"a":a,'b':s[i]},casting='same_kind',out=c[:,i]) # 0.31954
        c[:,i]*=s[i]
    print("---{0:^10} : {1:<8.5f} seconds ---".format('uvsample',time.time()-start))    
    print(c)


.. parsed-literal::

    --- uvsample  : 0.30309  seconds ---
    [[0. 0. 0. ... 0. 0. 0.]
     [0. 0. 0. ... 0. 0. 0.]
     [0. 0. 0. ... 0. 0. 0.]
     ...
     [0. 0. 0. ... 0. 0. 0.]
     [0. 0. 0. ... 0. 0. 0.]
     [0. 0. 0. ... 0. 0. 0.]]


.. code:: ipython3

    from gmake.tests.test_array_operations import *
    test_numexpr()


.. parsed-literal::

    --->>>>loop-fancy1 : 0.05199  seconds ---
    --->>>>loop-fancy1 : 0.01873  seconds ---
    --->>>>loop-fancy1 : 0.20160  seconds ---
    --->>>>loop-fancy1 : 0.02011  seconds ---


.. code:: ipython3

    import numexpr3 as ne3
    import numexpr as ne
    import numpy as np
    import time
    import scipy
    
    
    plane=np.ones(1000000)
    start=time.time()
    x=np.broadcast_to(plane[:,np.newaxis],(1000000,100))
    print("---{0:^10} : {1:<8.5f} seconds ---".format('uvsample',time.time()-start)) 
    
    #scale=np.arange(100)
    
    c=np.ones((1000000,100),order='F')*2
    
    start=time.time()
    ne.evaluate("c+x*y",local_dict={"x":np.broadcast_to(plane[:,np.newaxis],(1000000,100)),'y':scale},casting='same_kind',out=out) # 0.31954
    print("---{0:^10} : {1:<8.5f} seconds ---".format('uvsample',time.time()-start)) 
    #out=ne.evaluate("x*y",local_dict={"x":c,'y':scale},casting='same_kind') # 0.31954
    #   
    print(out,out.shape)
    print(out[:,1])
    print(out[:,2])


.. parsed-literal::

    --- uvsample  : 0.00088  seconds ---
    --- uvsample  : 0.09021  seconds ---
    [[  2.   3.   4. ...  99. 100. 101.]
     [  2.   3.   4. ...  99. 100. 101.]
     [  2.   3.   4. ...  99. 100. 101.]
     ...
     [  2.   3.   4. ...  99. 100. 101.]
     [  2.   3.   4. ...  99. 100. 101.]
     [  2.   3.   4. ...  99. 100. 101.]] (1000000, 100)
    [3. 3. 3. ... 3. 3. 3.]
    [4. 4. 4. ... 4. 4. 4.]


.. code:: ipython3

    import numpy as np
    np.zeros((2,2),dtype='complex64')




.. parsed-literal::

    array([[0.+0.j, 0.+0.j],
           [0.+0.j, 0.+0.j]], dtype=complex64)



.. code:: ipython3

    s=np.arange(100)

.. code:: ipython3

    (np.broadcast_to(s,(1,100))).shape




.. parsed-literal::

    (1, 100)



.. code:: ipython3

    import numpy as np
    model2d=np.ones(1000)
    model3d=model2d[:,np.newaxis]*np.arange(100)[np.newaxis,:]
    #model2d=np.ones((10,10))
    #model3d=model2d[np.newaxis,:,:]*np.arange(100)[:,np.newaxis]
    print(model3d.shape)


.. parsed-literal::

    (1000, 100)


.. code:: ipython3

    import numpy as np
    %time x=np.zeros((1,30,256,256))


.. parsed-literal::

    CPU times: user 1.22 ms, sys: 776 µs, total: 2 ms
    Wall time: 1.17 ms


.. code:: ipython3

    import numpy as np
    gmake.convert_size(gmake.getsizeof(np.zeros((1000,100,100),dtype=np.float32)))




.. parsed-literal::

    '38.15 MB'



