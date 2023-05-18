|Open In Colab|

Example BX610: perform model fitting using method=‘amoeba’
----------------------------------------------------------

.. |Open In Colab| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/r-xue/casa_proc/blob/master/demo/test_casaproc.ipynb

.. code:: ipython3

    import sys
    import glob
    import os
    import io
    import logging
    from pprint import pprint
    
    print(sys.version)
    
    import socket 
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir('/Users/Rui/Documents/Workspace/projects/GMaKE/examples/output/')
    print(socket.gethostname())
    print(os.getcwd())
    
    import gmake
    print(gmake.__version__)
    print(gmake.__email__)
    print(gmake.__demo__)
    
    inpfile=gmake.__demo__+'/../examples/inpfile/bx610_b6c3_uv_ab.inp'
    logfile=''
    
    print('>'*40)
    #gmake.logger_config()
    #gmake.logger_status()
    #import pprint
    #pprint.pprint(logging.Logger.manager.loggerDict) 
    gmake.logger_config()
    inp_dct=gmake.read_inp(inpfile)
    inp_dct=gmake.inp_validate(inp_dct)
    outdir=inp_dct['general']['outdir']
    gmake.logger_config(logfile=outdir+'/gmake.log',loglevel='DEBUG',logfilelevel='DEBUG')
    gmake.logger_status()



.. parsed-literal::

    3.7.5 (default, Oct 19 2019, 11:15:26) 
    [Clang 11.0.0 (clang-1100.0.33.8)]
    hyperion
    /Users/Rui/Documents/Workspace/projects/GMaKE/examples/output
    0.2.dev1
    rx.astro@gmail.com
    /Users/Rui/Documents/Workspace/projects/GMaKE/gmake
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    **********exe read_inp()**************
    <Logger gmake (DEBUG)>
    [<FileHandler /Users/Rui/Documents/Workspace/projects/GMaKE/examples/output/bx610_b6c3_uv_ab/gmake.log (DEBUG)>, <StreamHandler stderr (DEBUG)>]


.. code:: ipython3

    dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True)


.. parsed-literal::

    read data (may take some time..)
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb2.ms
    
    data@../data/bx610/alma/2015.1.00250.S/bb2.ms                (56354, 238)         102 MiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb2.ms                 (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb2.ms              (56354,)             220 KiB             161.43835
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb2.ms            (238,)     250752859438.0543 Hz 252604264234.0391 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb2.ms           (238,)     7811834.5822 Hz 7811834.5822 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb2.ms         23h46m09.44s  12d49m19.3s
    data flagging fraction: 0.0
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb3.ms
    
    data@../data/bx610/alma/2015.1.00250.S/bb3.ms                (53466, 238)          97 MiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb3.ms                 (53466, 3)           627 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb3.ms              (53466,)             209 KiB             187.34055
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb3.ms            (238,)     233254349973.6942 Hz 235105754769.6790 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb3.ms           (238,)     -7811834.5822 Hz -7811834.5822 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb3.ms         23h46m09.44s  12d49m19.3s
    data flagging fraction: 0.0
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms
    
    data@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms            (56354, 1)           440 KiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms             (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms          (56354,)             220 KiB             35061.727
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms        (1,)       250073373567.0543 Hz 250073373567.0543 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms       (1,)       1859216630.5597 Hz 1859216630.5597 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms     23h46m09.44s  12d49m19.3s
    data flagging fraction: 0.0
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms
    
    data@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms            (56354, 1)           440 KiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms             (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms          (56354,)             220 KiB             48239.17
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms        (1,)       235879907576.7765 Hz 235879907576.7765 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms       (1,)       -1859216630.5670 Hz -1859216630.5670 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms     23h46m09.44s  12d49m19.3s
    data flagging fraction: 0.0
    --------------------------------------------------------------------------------
    --- dat_dct size 203.68 Mibyte ---
    --- took 1.65307  seconds ---


.. code:: ipython3

    #
    #mod_dct=gmake.inp2mod(inp_dct)
    #gmake.pprint(mod_dct)
    #gmake.model_vrot(mod_dct)
    #gmake.pprint(mod_dct)
    #gmake.model_vrot_plot(mod_dct['co76'])

.. code:: ipython3

    inp_dct=gmake.read_inp(inpfile)
    inp_dct=gmake.inp_validate(inp_dct)
    mod_dct=gmake.inp2mod(inp_dct)
    gmake.model_vrot(mod_dct)
    #mod_dct['co76']
    fit_dct=gmake.fit_setup(inp_dct,dat_dct)
    gmake.fit_iterate(fit_dct,inp_dct,dat_dct)


.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    optimizer: amoeba
    optimizing parameters:
    ----------------------------------------------------------------------------------------------------
    index    name    unit    start    lo_limit    up_limit    scale
     0   vsys@basics       km / s               117.50      (     0.00     ,     220.00     )    117.50     
     1   disk_sd@diskdyn   solMass / pc2       10000.00     (    100.00    ,    50000.00    )   40000.00    
     2   disk_rs@diskdyn   kpc                   2.00       (     0.20     ,      30.00     )     28.00     
     3   vdis@basics       km / s                50.00      (     0.00     ,     200.00     )    150.00     
     4   pa@basics         deg                  -52.40      (    -132.40   ,      27.60     )     80.00     
     5   inc@basics        deg                   44.06      (     5.00     ,      85.00     )     40.94     
     6   xypos.ra@basics   deg                356.5393258   (  356.5390481 ,   356.5396036  )   0.0002778   
     7   xypos.dec@basics  deg                12.8220182    (  12.8217404  ,   12.8222960   )   0.0002778   
     8   lineflux@co76     Jy km / s             1.30       (     0.10     ,     200.00     )    198.70     
     9   sbser[0]@co76     arcsec                0.22       (     0.01     ,      2.00      )     1.78      
     10  lineflux@ci21     Jy km / s             0.65       (     0.10     ,     200.00     )    199.35     
     11  sbser[0]@ci21     arcsec                0.19       (     0.01     ,      2.00      )     1.81      
     12  lineflux@h2o      Jy km / s             0.38       (     0.10     ,     200.00     )    199.62     
     13  sbser[0]@h2o      arcsec                0.17       (     0.01     ,      2.00      )     1.83      
     14  contflux@cont     Jy                    0.00       (     0.00     ,      0.01      )     0.01      
     15  sbser[0]@cont     arcsec                0.12       (     0.01     ,      2.00      )     1.88      
     16  alpha@cont                              3.72       (     3.00     ,      4.50      )     0.78      
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ndim:    17
    outdir:  bx610_b6c3_uv_ab


.. parsed-literal::

    **********exe read_inp()**************


.. parsed-literal::

    one trial                                          : 1.16144  seconds
    ndata->26249868.0
    chisq->66854351.59356616
    --- save to: bx610_b6c3_uv_ab/fit.h5
     
    Running AMOEBA...
    >>bx610_b6c3_uv_ab/amoeba_chain.h5
     
         0   66853460        inf


.. parsed-literal::

    /Users/Rui/Documents/Workspace/projects/GMaKE/gmake/opt_amoeba.py:284: RuntimeWarning: invalid value encountered in double_scalars
      
    


.. parsed-literal::

         1   66853460  103117350
         2   66853460   97238672
         3   66853460   92439498
         4   66853460   67247620
         5   66853460   67128299
         6   66853460   67093474
         7   66853460   67004703
         8   66853460   66883205
         9   66853460   66882621
        10   66853460   66872296
        11   66853460   66870894
        13   66853460   66870758
        15   66853460   66868658
        16   66853460   66867928
        18   66853460   66867860
        20   66853460   66867301
        22   66853460   66866986
        24   66853460   66863612
        25   66853460   66863205
        27   66853460   66863015
        29   66853460   66862396
        31   66853460   66861680
        32   66853460   66861273
        34   66853460   66859180
        36   66853460   66859109
        38   66853460   66859062
        40   66853460   66858418
        42   66853460   66858217
        43   66853460   66858109
        45   66853460   66857834
        46   66853460   66857361
        48   66853460   66857221
        49   66853460   66857002
        51   66853460   66856883
        53   66853460   66856816
        54   66853460   66856575
        56   66853460   66856498
        57   66853460   66856488
        59   66853460   66856400
        60   66853460   66856266
        61   66853460   66856245
        63   66853460   66856213
        65   66853460   66856123
        67   66853460   66856027
        68   66853460   66855990
        69   66853460   66855917
        71   66853460   66855755
        73   66853460   66855724
        74   66853460   66855699
        75   66853460   66855603
        76   66853460   66855600
        78   66853460   66855522
        79   66853460   66855519
        98   66853460   66855138
       100   66853460   66854966
       102   66853460   66854679
       103   66853460   66854612
       104   66853460   66854477
       105   66853460   66854416
       107   66853460   66854391
       108   66853460   66854349
       109   66853460   66854329
       110   66853460   66854323
       111   66853460   66854316
       113   66853460   66854299
       114   66853460   66854283
       116   66853460   66854245
       118   66853460   66854192
       120   66853460   66854185
       122   66853460   66854121
       124   66853460   66854073
       125   66853460   66854029
       127   66853460   66854012
       128   66853460   66853991
       129   66853460   66853980
       130   66853460   66853975
       131   66853460   66853958
       132   66853460   66853951
       134   66853460   66853918
       135   66853460   66853914
       137   66853460   66853905
       139   66853460   66853885
       140   66853460   66853868
       142   66853460   66853833
       143   66853460   66853828
       145   66853460   66853825
       146   66853460   66853797
       148   66853460   66853792
       150   66853460   66853787
       152   66853460   66853775
       154   66853420   66853774
       155   66853420   66853762
       156   66853420   66853742
       157   66853420   66853726
       158   66853420   66853724
       160   66853420   66853721
       161   66853420   66853716
       162   66853420   66853709
       163   66853420   66853705
       164   66853420   66853686
       166   66853420   66853668
       167   66853420   66853667
       168   66853420   66853667
       170   66853406   66853666
       171   66853406   66853649
       173   66853406   66853642
       174   66853406   66853624
       175   66853406   66853614
       176   66853406   66853612
       177   66853406   66853611
       179   66853370   66853608
       180   66853370   66853593
       181   66853370   66853572
       183   66853370   66853570
       184   66853370   66853563
       186   66853370   66853544
       188   66853370   66853542
       190   66853370   66853540
       191   66853370   66853539
       192   66853370   66853526
       193   66853370   66853511
       195   66853370   66853498
       196   66853370   66853492
       197   66853370   66853480
       198   66853370   66853475
       200   66853370   66853473
    --- save to: bx610_b6c3_uv_ab/amoeba_chain.h5


.. code:: ipython3

    #from hickle import SerializedWarning
    %matplotlib inline
    #%matplotlib notebook
    gmake.fit_analyze(inpfile,export=True)
    #print(fit_dct['p_scale'])


.. parsed-literal::

    --- save to: bx610_b6c3_uv_ab/fit.h5
    Check optimized parameters:
     0   vsys@basics       =    115.73      <-    117.50      (     0.00     ,     220.00     )
     1   disk_sd@diskdyn   =    4640.10     <-   10000.00     (    100.00    ,    50000.00    )
     2   disk_rs@diskdyn   =     9.59       <-     2.00       (     0.20     ,      10.00     )
     3   xypos.ra@basics   =  356.5393263   <-  356.5393258   (  356.5390481 ,   356.5396036  )
     4   xypos.dec@basics  =  12.8220172    <-  12.8220182    (  12.8217404  ,   12.8222960   )
     5   lineflux@co76     =     1.33       <-     1.30       (     0.10     ,     200.00     )
     6   sbser[0]@co76     =     0.19       <-     0.22       (     0.01     ,      2.00      )
     7   lineflux@ci21     =     0.68       <-     0.65       (     0.10     ,     200.00     )
     8   sbser[0]@ci21     =     0.14       <-     0.19       (     0.01     ,      2.00      )
     9   lineflux@h2o      =     0.32       <-     0.38       (     0.10     ,     200.00     )
     10  sbser[0]@h2o      =     0.12       <-     0.17       (     0.01     ,      2.00      )
     11  contflux@cont     =     0.00       <-     0.00       (     0.00     ,      0.01      )
     12  sbser[0]@cont     =     0.13       <-     0.12       (     0.01     ,      2.00      )
     13  alpha@cont        =     3.93       <-     3.72       (     3.00     ,      4.50      )


.. parsed-literal::

    **********exe read_inp()**************
    vsys@basics [km / s]
    2.546807307723002 3.9277176507191527
    vsys@basics [km / s]
    2.546807307723002 2.5468435993013947
    disk_sd@diskdyn [solMass / pc2]
    2.546807307723002 3.9277176507191527
    disk_sd@diskdyn [solMass / pc2]
    2.546807307723002 2.5468435993013947
    disk_rs@diskdyn [kpc]
    2.546807307723002 3.9277176507191527
    disk_rs@diskdyn [kpc]
    2.546807307723002 2.5468435993013947
    xypos.ra@basics [arcsec]
    2.546807307723002 3.9277176507191527
    xypos.ra@basics [arcsec]
    2.546807307723002 2.5468435993013947
    xypos.dec@basics [arcsec]
    2.546807307723002 3.9277176507191527
    xypos.dec@basics [arcsec]
    2.546807307723002 2.5468435993013947
    lineflux@co76 [Jy km / s]
    2.546807307723002 3.9277176507191527
    lineflux@co76 [Jy km / s]
    2.546807307723002 2.5468435993013947
    sbser[0]@co76 [arcsec]
    2.546807307723002 3.9277176507191527
    sbser[0]@co76 [arcsec]
    2.546807307723002 2.5468435993013947
    lineflux@ci21 [Jy km / s]
    2.546807307723002 3.9277176507191527
    lineflux@ci21 [Jy km / s]
    2.546807307723002 2.5468435993013947
    sbser[0]@ci21 [arcsec]
    2.546807307723002 3.9277176507191527
    sbser[0]@ci21 [arcsec]
    2.546807307723002 2.5468435993013947
    lineflux@h2o [Jy km / s]
    2.546807307723002 3.9277176507191527
    lineflux@h2o [Jy km / s]
    2.546807307723002 2.5468435993013947
    sbser[0]@h2o [arcsec]
    2.546807307723002 3.9277176507191527
    sbser[0]@h2o [arcsec]
    2.546807307723002 2.5468435993013947
    contflux@cont [Jy]
    2.546807307723002 3.9277176507191527
    contflux@cont [Jy]
    2.546807307723002 2.5468435993013947
    sbser[0]@cont [arcsec]
    2.546807307723002 3.9277176507191527
    sbser[0]@cont [arcsec]
    2.546807307723002 2.5468435993013947
    alpha@cont []
    2.546807307723002 3.9277176507191527
    alpha@cont []
    2.546807307723002 2.5468435993013947


.. parsed-literal::

    analyzing outfolder:bx610_b6c3_uv_ab
    plotting...bx610_b6c3_uv_ab/iteration.pdf


.. parsed-literal::

    /Users/Rui/Library/Python/3.7/lib/python/site-packages/galpy/potential/RazorThinExponentialDiskPotential.py:128: RuntimeWarning: invalid value encountered in multiply
      return -2.*nu.pi*y*(special.i0(y)*special.k0(y)-special.i1(y)*special.k1(y))
    


.. parsed-literal::

    export the model set:              bx610_b6c3_uv_ab/model_0              (may take some time..)
     
    -->data_b6c3_bb2.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/imod2d_b6c3_bb2.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/imod3d_b6c3_bb2.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/pbeam_b6c3_bb2.fits


.. parsed-literal::

    bx610_b6c3_uv_ab/model_0
    ['cube.', 'mfs.', 'cube3.']
    [('../data/bx610/alma/2015.1.00250.S/', 'b6c3_')]


.. parsed-literal::

    write reference model profile: 
        imod3d_prof@co76@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/imodrp_co76_b6c3_bb2.fits
    write reference model profile: 
        imod3d_prof@ci21@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/imodrp_ci21_b6c3_bb2.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb2.ms  to  bx610_b6c3_uv_ab/model_0/model_b6c3_bb2.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb2.ms to data@bx610_b6c3_uv_ab/model_0/model_b6c3_bb2.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb2.ms  to  bx610_b6c3_uv_ab/model_0/data_b6c3_bb2.ms
     
    -->data_b6c3_bb3.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_0/imod2d_b6c3_bb3.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_0/imod3d_b6c3_bb3.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_0/pbeam_b6c3_bb3.fits
    write reference model profile: 
        imod3d_prof@h2o@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_0/imodrp_h2o_b6c3_bb3.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb3.ms  to  bx610_b6c3_uv_ab/model_0/model_b6c3_bb3.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb3.ms to data@bx610_b6c3_uv_ab/model_0/model_b6c3_bb3.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb3.ms  to  bx610_b6c3_uv_ab/model_0/data_b6c3_bb3.ms
     
    -->data_b6c3_bb1.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms to bx610_b6c3_uv_ab/model_0/imod2d_b6c3_bb1.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms to bx610_b6c3_uv_ab/model_0/imod3d_b6c3_bb1.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms to bx610_b6c3_uv_ab/model_0/pbeam_b6c3_bb1.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms  to  bx610_b6c3_uv_ab/model_0/model_b6c3_bb1.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms to data@bx610_b6c3_uv_ab/model_0/model_b6c3_bb1.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb1.mfs.ms  to  bx610_b6c3_uv_ab/model_0/data_b6c3_bb1.ms
     
    -->data_b6c3_bb4.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms to bx610_b6c3_uv_ab/model_0/imod2d_b6c3_bb4.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms to bx610_b6c3_uv_ab/model_0/imod3d_b6c3_bb4.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms to bx610_b6c3_uv_ab/model_0/pbeam_b6c3_bb4.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms  to  bx610_b6c3_uv_ab/model_0/model_b6c3_bb4.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms to data@bx610_b6c3_uv_ab/model_0/model_b6c3_bb4.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb4.mfs.ms  to  bx610_b6c3_uv_ab/model_0/data_b6c3_bb4.ms
    --------------------------------------------------------------------------------
    --- took 5.89455  seconds ---
    --- save to: bx610_b6c3_uv_ab/model_0/models.h5
    save the model input parameter: bx610_b6c3_uv_ab/model_0/model.inp
    model_0: 
    {'chisq': 66854343.77148066,
     'lnprob': 10222658.292523397,
     'ndata': 26249868.0,
     'npar': 14}


.. parsed-literal::

    {'basics': {'object': 'bx610',
                'z': 2.21,
                'pa': <Quantity -52.4 deg>,
                'inc': <Quantity 44.06 deg>,
                'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (356.53932583, 12.82201819)>,
                'vsys': <Quantity 117.5 km / s>,
                'vrad': <Quantity [0.  , 0.12, 0.24, 0.36, 0.48] arcsec>,
                'vrot': 'diskdyn',
                'vdis': <Quantity 50. km / s>,
                'vrot_rpcorr': True},
     'diskdyn': {'disk_sd': <Quantity 10000. solMass / pc2>,
                 'disk_rs': <Quantity 2. kpc>,
                 'nfw_mvir': <Quantity 5.e+11 solMass>,
                 'type': 'potential'},
     'co76': {'type': 'disk3d',
              'import': 'basics',
              'note': 'CO76 of BX610 in BB2',
              'vis': '../data/bx610/alma/2015.1.00250.S/bb2.ms',
              'restfreq': <Quantity 806.65181 GHz>,
              'lineflux': <Quantity 1.3025217 Jy km / s>,
              'sbser': [<Quantity 0.21709428 arcsec>, 1.0]},
     'ci21': {'type': 'disk3d',
              'import': 'basics',
              'note': 'CI21 of BX610 in BB2',
              'vis': '../data/bx610/alma/2015.1.00250.S/bb2.ms',
              'restfreq': <Quantity 809.34197 GHz>,
              'lineflux': <Quantity 0.6493 Jy km / s>,
              'sbser': [<Quantity 0.18771502 arcsec>, 1.0]},
     'h2o': {'type': 'disk3d',
             'import': 'basics',
             'note': 'H2O of BX610 in BB3',
             'vis': '../data/bx610/alma/2015.1.00250.S/bb3.ms',
             'restfreq': <Quantity 752.03314 GHz>,
             'lineflux': <Quantity 0.38320318 Jy km / s>,
             'sbser': [<Quantity 0.16759061 arcsec>, 1.0]},
     'cont': {'type': 'disk2d',
              'import': 'basics',
              'note': 'submm cont of BX610 in BB-1/2/3/4',
              'vis': '../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms,../data/bx610/alma/2015.1.00250.S/bb2.ms,../data/bx610/alma/2015.1.00250.S/bb3.ms,../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms',
              'restfreq': <Quantity 251.68251775 GHz>,
              'alpha': <Quantity 3.718318>,
              'contflux': <Quantity 0.00175222 Jy>,
              'sbser': [<Quantity 0.11831162 arcsec>, 1.0]},
     'optimize': {'vsys@basics': ('a', <Quantity [  0., 220.] km / s>),
                  'disk_sd@diskdyn': ('a',
                                      <Quantity [  100., 50000.] solMass / pc2>),
                  'disk_rs@diskdyn': ('a', <Quantity [ 0.2, 10. ] kpc>),
                  'xypos.ra@basics': ('o', <Quantity [-1.,  1.] arcsec>),
                  'xypos.dec@basics': ('o', <Quantity [-1.,  1.] arcsec>),
                  'lineflux@co76': ('a', <Quantity [1.e-01, 2.e+02] Jy km / s>),
                  'sbser[0]@co76': ('a', <Quantity [0.01, 2.  ] arcsec>),
                  'lineflux@ci21': ('a', <Quantity [1.e-01, 2.e+02] Jy km / s>),
                  'sbser[0]@ci21': ('a', <Quantity [0.01, 2.  ] arcsec>),
                  'lineflux@h2o': ('a', <Quantity [1.e-01, 2.e+02] Jy km / s>),
                  'sbser[0]@h2o': ('a', <Quantity [0.01, 2.  ] arcsec>),
                  'contflux@cont': ('a', <Quantity [0.0001, 0.01  ] Jy>),
                  'sbser[0]@cont': ('a', <Quantity [0.01, 2.  ] arcsec>),
                  'alpha@cont': ('a', [3, 4.5]),
                  'method': 'amoeba',
                  'niter': 200},
     'general': {'outdir': 'bx610_b6c3_uv_ab',
                 'outname_replace': [('../data/bx610/alma/2015.1.00250.S/',
                                      'b6c3_')],
                 'outname_exclude': ['cube.', 'mfs.', 'cube3.']}}


.. parsed-literal::

    export the model set:              bx610_b6c3_uv_ab/model_1              (may take some time..)
     
    -->data_b6c3_bb2.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/imod2d_b6c3_bb2.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/imod3d_b6c3_bb2.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/pbeam_b6c3_bb2.fits
    write reference model profile: 
        imod3d_prof@co76@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/imodrp_co76_b6c3_bb2.fits
    write reference model profile: 
        imod3d_prof@ci21@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/imodrp_ci21_b6c3_bb2.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb2.ms  to  bx610_b6c3_uv_ab/model_1/model_b6c3_bb2.ms


.. parsed-literal::

    bx610_b6c3_uv_ab/model_1
    ['cube.', 'mfs.', 'cube3.']
    [('../data/bx610/alma/2015.1.00250.S/', 'b6c3_')]


.. parsed-literal::

    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb2.ms to data@bx610_b6c3_uv_ab/model_1/model_b6c3_bb2.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb2.ms  to  bx610_b6c3_uv_ab/model_1/data_b6c3_bb2.ms
     
    -->data_b6c3_bb3.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_1/imod2d_b6c3_bb3.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_1/imod3d_b6c3_bb3.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_1/pbeam_b6c3_bb3.fits
    write reference model profile: 
        imod3d_prof@h2o@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_1/imodrp_h2o_b6c3_bb3.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb3.ms  to  bx610_b6c3_uv_ab/model_1/model_b6c3_bb3.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb3.ms to data@bx610_b6c3_uv_ab/model_1/model_b6c3_bb3.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb3.ms  to  bx610_b6c3_uv_ab/model_1/data_b6c3_bb3.ms
     
    -->data_b6c3_bb1.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms to bx610_b6c3_uv_ab/model_1/imod2d_b6c3_bb1.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms to bx610_b6c3_uv_ab/model_1/imod3d_b6c3_bb1.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms to bx610_b6c3_uv_ab/model_1/pbeam_b6c3_bb1.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms  to  bx610_b6c3_uv_ab/model_1/model_b6c3_bb1.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms to data@bx610_b6c3_uv_ab/model_1/model_b6c3_bb1.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb1.mfs.ms  to  bx610_b6c3_uv_ab/model_1/data_b6c3_bb1.ms
     
    -->data_b6c3_bb4.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms to bx610_b6c3_uv_ab/model_1/imod2d_b6c3_bb4.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms to bx610_b6c3_uv_ab/model_1/imod3d_b6c3_bb4.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms to bx610_b6c3_uv_ab/model_1/pbeam_b6c3_bb4.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms  to  bx610_b6c3_uv_ab/model_1/model_b6c3_bb4.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms to data@bx610_b6c3_uv_ab/model_1/model_b6c3_bb4.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb4.mfs.ms  to  bx610_b6c3_uv_ab/model_1/data_b6c3_bb4.ms
    --------------------------------------------------------------------------------
    --- took 5.83713  seconds ---
    --- save to: bx610_b6c3_uv_ab/model_1/models.h5
    save the model input parameter: bx610_b6c3_uv_ab/model_1/model.inp
    model_1: 
    {'chisq': 66853351.67874838,
     'lnprob': 10223154.33888954,
     'ndata': 26249868.0,
     'npar': 14}


.. parsed-literal::

    {'basics': {'object': 'bx610',
                'z': 2.21,
                'pa': <Quantity -52.4 deg>,
                'inc': <Quantity 44.06 deg>,
                'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (356.53932627, 12.82201718)>,
                'vsys': <Quantity 115.73308903 km / s>,
                'vrad': <Quantity [0.  , 0.12, 0.24, 0.36, 0.48] arcsec>,
                'vrot': 'diskdyn',
                'vdis': <Quantity 50. km / s>,
                'vrot_rpcorr': True},
     'diskdyn': {'disk_sd': <Quantity 4640.101353 solMass / pc2>,
                 'disk_rs': <Quantity 9.587171 kpc>,
                 'nfw_mvir': <Quantity 5.e+11 solMass>,
                 'type': 'potential'},
     'co76': {'type': 'disk3d',
              'import': 'basics',
              'note': 'CO76 of BX610 in BB2',
              'vis': '../data/bx610/alma/2015.1.00250.S/bb2.ms',
              'restfreq': <Quantity 806.65181 GHz>,
              'lineflux': <Quantity 1.33293503 Jy km / s>,
              'sbser': [<Quantity 0.1931354 arcsec>, 1.0]},
     'ci21': {'type': 'disk3d',
              'import': 'basics',
              'note': 'CI21 of BX610 in BB2',
              'vis': '../data/bx610/alma/2015.1.00250.S/bb2.ms',
              'restfreq': <Quantity 809.34197 GHz>,
              'lineflux': <Quantity 0.68025995 Jy km / s>,
              'sbser': [<Quantity 0.14071556 arcsec>, 1.0]},
     'h2o': {'type': 'disk3d',
             'import': 'basics',
             'note': 'H2O of BX610 in BB3',
             'vis': '../data/bx610/alma/2015.1.00250.S/bb3.ms',
             'restfreq': <Quantity 752.03314 GHz>,
             'lineflux': <Quantity 0.32195598 Jy km / s>,
             'sbser': [<Quantity 0.12408947 arcsec>, 1.0]},
     'cont': {'type': 'disk2d',
              'import': 'basics',
              'note': 'submm cont of BX610 in BB-1/2/3/4',
              'vis': '../data/bx610/alma/2015.1.00250.S/bb1.mfs.ms,../data/bx610/alma/2015.1.00250.S/bb2.ms,../data/bx610/alma/2015.1.00250.S/bb3.ms,../data/bx610/alma/2015.1.00250.S/bb4.mfs.ms',
              'restfreq': <Quantity 251.68251775 GHz>,
              'alpha': <Quantity 3.93398175>,
              'contflux': <Quantity 0.0017653 Jy>,
              'sbser': [<Quantity 0.12518406 arcsec>, 1.0]},
     'optimize': {'vsys@basics': ('a', <Quantity [  0., 220.] km / s>),
                  'disk_sd@diskdyn': ('a',
                                      <Quantity [  100., 50000.] solMass / pc2>),
                  'disk_rs@diskdyn': ('a', <Quantity [ 0.2, 10. ] kpc>),
                  'xypos.ra@basics': ('o', <Quantity [-1.,  1.] arcsec>),
                  'xypos.dec@basics': ('o', <Quantity [-1.,  1.] arcsec>),
                  'lineflux@co76': ('a', <Quantity [1.e-01, 2.e+02] Jy km / s>),
                  'sbser[0]@co76': ('a', <Quantity [0.01, 2.  ] arcsec>),
                  'lineflux@ci21': ('a', <Quantity [1.e-01, 2.e+02] Jy km / s>),
                  'sbser[0]@ci21': ('a', <Quantity [0.01, 2.  ] arcsec>),
                  'lineflux@h2o': ('a', <Quantity [1.e-01, 2.e+02] Jy km / s>),
                  'sbser[0]@h2o': ('a', <Quantity [0.01, 2.  ] arcsec>),
                  'contflux@cont': ('a', <Quantity [0.0001, 0.01  ] Jy>),
                  'sbser[0]@cont': ('a', <Quantity [0.01, 2.  ] arcsec>),
                  'alpha@cont': ('a', [3, 4.5]),
                  'method': 'amoeba',
                  'niter': 200},
     'general': {'outdir': 'bx610_b6c3_uv_ab',
                 'outname_replace': [('../data/bx610/alma/2015.1.00250.S/',
                                      'b6c3_')],
                 'outname_exclude': ['cube.', 'mfs.', 'cube3.']}}



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>


.. code:: ipython3

    models=gmake.hdf2dct(inp_dct['general']['outdir']+'/model_1/models.h5')
    gmake.pprint(models['mod_dct']['co76'])
    gmake.model_vrot_plot(models['mod_dct']['co76'])


.. parsed-literal::

    {'inc': <Quantity 44.06 deg>,
     'lineflux': <Quantity 1.3025217 Jy km / s>,
     'note': 'CO76 of BX610 in BB2',
     'object': 'bx610',
     'pa': <Quantity -52.4 deg>,
     'pheader': None,
     'pmodel': None,
     'restfreq': <Quantity 806.65181 GHz>,
     'sbser': [<Quantity 0.21709428 arcsec>, 1.0],
     'type': 'disk3d',
     'vcirc': <Quantity [  0.        ,  15.00096531,  27.74695665,  39.50948423,
                50.58967016,  61.13696008,  71.24232142,  80.967526  ,
                90.35753577,  99.44669697, 108.26219918, 116.82616573,
               125.15699475, 133.27026058, 141.17934302, 148.89588045,
               156.43010476, 163.79109446, 170.98696967, 178.02504491,
               184.91195053, 191.65373052, 198.25592221, 204.72362192,
               211.06153943, 217.27404381, 223.36520198, 229.33881162,
               235.19842932, 240.9473949 , 246.58885238, 252.12576836,
               257.56094805, 262.89704936, 268.13659543, 273.28198558,
               278.33550523, 283.29933466, 288.17555685, 292.96616461,
               297.6730669 , 302.29809466, 306.84300597, 311.30949087,
               315.69917563, 320.01362673, 324.2543545 , 328.42281639,
               332.52042003, 336.54852606, 340.5084507 , 344.40146813,
               348.22881274, 351.99168112, 355.69123402, 359.3285981 ,
               362.90486757, 366.42110574, 369.87834645, 373.27759541,
               376.61983144, 379.90600771, 383.13705276, 386.31387158,
               389.4373466 , 392.50833858, 395.5276875 , 398.49621333,
               401.41471688, 404.28398045, 407.10476855, 409.87782858,
               412.6038914 , 415.28367195, 417.91786979, 420.50716964,
               423.05224188, 425.55374301, 428.01231613, 430.42859137,
               432.80318629, 435.13670628, 437.42974496, 439.68288448,
               441.89669595, 444.07173967, 446.20856555, 448.30771332,
               450.36971286, 452.39508449, 454.38433922, 456.33797898,
               458.25649691, 460.14037757, 461.99009717, 463.80612379,
               465.58891757, 467.33893096, 469.05660884, 470.74238879,
               472.39670121, 474.0199695 , 475.61261026, 477.17503342,
               478.70764241, 480.21083431, 481.68499999, 483.13052426,
               484.547786  , 485.93715828, 487.29900851, 488.63369856,
               489.94158486, 491.22301853, 492.47834549, 493.70790658,
               494.91203763, 496.09106962, 497.24532872, 498.37513641,
               499.48080959, 500.56266066, 501.62099759, 502.65612402,
               503.66833935, 504.65793882, 505.62521356, 506.57045072,
               507.49393349, 508.39594121, 509.27674942, 510.13662993,
               510.97585092, 511.79467694, 512.59336905, 513.37218481,
               514.1313784 , 514.87120063, 515.59189904, 516.29371793,
               516.97689842, 517.64167851, 518.28829311, 518.91697413,
               519.52795049, 520.12144821, 520.69769039, 521.25689735,
               521.79928659, 522.32507289, 522.83446831, 523.32768228,
               523.8049216 , 524.26639051, 524.7122907 , 525.14282138,
               525.55817929, 525.95855877, 526.34415175, 526.71514784,
               527.07173432, 527.41409619, 527.74241623, 528.05687497,
               528.35765078, 528.6449199 , 528.91885642, 529.17963236,
               529.42741767, 529.66238029, 529.88468615, 530.09449921,
               530.29198148, 530.47729306, 530.65059215, 530.8120351 ,
               530.96177641, 531.09996876, 531.22676306, 531.34230844] km / s>,
     'vdis': <Quantity [50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.] km / s>,
     'vis': '../data/bx610/alma/2015.1.00250.S/bb2.ms',
     'vrad': <Quantity [0.        , 0.01165143, 0.02330286, 0.03495428, 0.04660571,
               0.05825714, 0.06990857, 0.08156   , 0.09321142, 0.10486285,
               0.11651428, 0.12816571, 0.13981714, 0.15146856, 0.16311999,
               0.17477142, 0.18642285, 0.19807428, 0.2097257 , 0.22137713,
               0.23302856, 0.24467999, 0.25633142, 0.26798284, 0.27963427,
               0.2912857 , 0.30293713, 0.31458856, 0.32623998, 0.33789141,
               0.34954284, 0.36119427, 0.3728457 , 0.38449712, 0.39614855,
               0.40779998, 0.41945141, 0.43110284, 0.44275426, 0.45440569,
               0.46605712, 0.47770855, 0.48935998, 0.5010114 , 0.51266283,
               0.52431426, 0.53596569, 0.54761711, 0.55926854, 0.57091997,
               0.5825714 , 0.59422283, 0.60587425, 0.61752568, 0.62917711,
               0.64082854, 0.65247997, 0.66413139, 0.67578282, 0.68743425,
               0.69908568, 0.71073711, 0.72238853, 0.73403996, 0.74569139,
               0.75734282, 0.76899425, 0.78064567, 0.7922971 , 0.80394853,
               0.81559996, 0.82725139, 0.83890281, 0.85055424, 0.86220567,
               0.8738571 , 0.88550853, 0.89715995, 0.90881138, 0.92046281,
               0.93211424, 0.94376567, 0.95541709, 0.96706852, 0.97871995,
               0.99037138, 1.00202281, 1.01367423, 1.02532566, 1.03697709,
               1.04862852, 1.06027995, 1.07193137, 1.0835828 , 1.09523423,
               1.10688566, 1.11853709, 1.13018851, 1.14183994, 1.15349137,
               1.1651428 , 1.17679423, 1.18844565, 1.20009708, 1.21174851,
               1.22339994, 1.23505137, 1.24670279, 1.25835422, 1.27000565,
               1.28165708, 1.29330851, 1.30495993, 1.31661136, 1.32826279,
               1.33991422, 1.35156565, 1.36321707, 1.3748685 , 1.38651993,
               1.39817136, 1.40982279, 1.42147421, 1.43312564, 1.44477707,
               1.4564285 , 1.46807993, 1.47973135, 1.49138278, 1.50303421,
               1.51468564, 1.52633706, 1.53798849, 1.54963992, 1.56129135,
               1.57294278, 1.5845942 , 1.59624563, 1.60789706, 1.61954849,
               1.63119992, 1.64285134, 1.65450277, 1.6661542 , 1.67780563,
               1.68945706, 1.70110848, 1.71275991, 1.72441134, 1.73606277,
               1.7477142 , 1.75936562, 1.77101705, 1.78266848, 1.79431991,
               1.80597134, 1.81762276, 1.82927419, 1.84092562, 1.85257705,
               1.86422848, 1.8758799 , 1.88753133, 1.89918276, 1.91083419,
               1.92248562, 1.93413704, 1.94578847, 1.9574399 , 1.96909133,
               1.98074276, 1.99239418, 2.00404561, 2.01569704, 2.02734847,
               2.0389999 , 2.05065132, 2.06230275, 2.07395418, 2.08560561] arcsec>,
     'vrot': <Quantity [  0.        ,  12.97441221,  25.62238137,  37.29502085,
                48.29638055,  58.77295252,  68.81356577,  78.47856491,
                87.81193293,  96.84731925, 105.61140039, 114.12591087,
               122.40894689, 130.4758434 , 138.33978698, 146.01225769,
               153.50335589, 160.82204957, 167.97636504, 174.9735364 ,
               181.82012454, 188.52211295, 195.08498599, 201.51379319,
               207.81320294, 213.98754734, 220.04086022, 225.97690952,
               231.79922496, 237.51112197, 243.1157224 , 248.61597262,
               254.01465931, 259.31442336, 264.51777221, 269.62709074,
               274.64465096, 279.57262073, 284.41307147, 289.16798522,
               293.83926089, 298.42872001, 302.93811186, 307.3691182 ,
               311.72335751, 316.00238897, 320.20771597, 324.34078943,
               328.40301081, 332.3957349 , 336.32027235, 340.17789209,
               343.96982345, 347.69725828, 351.36135275, 354.96322918,
               358.50397763, 361.98465743, 365.40629862, 368.76990324,
               372.07644666, 375.32687863, 378.5221245 , 381.66308615,
               384.75064301, 387.78565295, 390.76895318, 393.70136099,
               396.58367458, 399.41667375, 402.20112061, 404.93776017,
               407.62732105, 410.27051596, 412.86804233, 415.42058281,
               417.92880574, 420.39336568, 422.81490382, 425.19404842,
               427.53141524, 429.82760791, 432.08321832, 434.29882696,
               436.47500329, 438.61230603, 440.7112835 , 442.77247392,
               444.79640569, 446.78359766, 448.73455941, 450.64979147,
               452.52978561, 454.37502505, 456.18598467, 457.96313127,
               459.70692372, 461.41781321, 463.09624343, 464.74265072,
               466.3574643 , 467.94110644, 469.49399257, 471.0165315 ,
               472.50912557, 473.97217075, 475.40605685, 476.81116761,
               478.18788087, 479.53656868, 480.85759744, 482.15132801,
               483.41811584, 484.65831107, 485.87225867, 487.06029852,
               488.22276553, 489.35998974, 490.47229641, 491.56000612,
               492.62343488, 493.66289419, 494.67869116, 495.67112856,
               496.64050495, 497.5871147 , 498.51124812, 499.41319152,
               500.29322728, 501.15163392, 501.98868618, 502.80465508,
               503.59980799, 504.37440869, 505.12871746, 505.86299109,
               506.577483  , 507.27244325, 507.94811862, 508.60475267,
               509.24258579, 509.86185523, 510.46279519, 511.04563686,
               511.61060844, 512.15793523, 512.68783966, 513.20054131,
               513.69625701, 514.17520083, 514.63758418, 515.08361579,
               515.51350178, 515.92744573, 516.32564866, 516.70830911,
               517.07562318, 517.42778455, 517.7649845 , 518.087412  ,
               518.39525368, 518.68869391, 518.96791483, 519.23309636,
               519.48441623, 519.72205006, 519.94617132, 520.15695141,
               520.35455969, 520.53916349, 520.71092811, 520.87001694,
               521.01659137, 521.15081092, 521.2728332 , 521.38281397,
               521.48090714, 521.56726483, 521.64203735, 521.70537325] km / s>,
     'vrot_rpcorr': True,
     'vsys': <Quantity 117.5 km / s>,
     'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        [(356.53932439, 12.82201906)]>,
     'z': 2.21}



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_amoeba_files/demo_bx610_amoeba_6_2.png


