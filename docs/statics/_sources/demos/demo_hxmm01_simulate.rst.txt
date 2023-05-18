Example HXMM01: test the MS-simulation modules
----------------------------------------------

This demo is used to illustrate the capability of produce referecen
model images from model properties #### input file: demo_disk3d.inp

.. code:: ipython3

    import sys
    import glob
    import os
    import io
    import logging
    import emcee
    import pprint as pp
    #from pprint import pprint
    
    print(sys.version)
    
    import socket 
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir('/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output/')
    print(socket.gethostname())
    print(os.getcwd())
    
    import gmake
    pp.pprint(gmake.__version__)
    pp.pprint(gmake.__email__)
    pp.pprint(gmake.__demo__)
    gmake.check_setup()
    
    #pp.pprint(gmake.meta.pars_def,indent=4,width=100)
    #gmake.pprint(gmake.meta.pars_def,indent=4,width=100)
    #gmake.pprint(gmake.meta.xymodel_header,indent=4,width=100)
    
    inpfile=gmake.__demo__+'/../examples/inpfile/hxmm01_b6c3_uv_mc.inp'
    logfile=''
    
    print('>'*40)
    gmake.logger_config()
    gmake.logger_status()
    #gmake.logger_status(root=True)
    
    outdir='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output/hxmm01_b6c3_uv_mc/'
    gmake.logger_config(logfile=outdir+'/gmake.log',loglevel='DEBUG',logfilelevel='DEBUG')
    gmake.logger_status()
    
    print('\n'*5)
    inp_dct=gmake.read_inp(inpfile)
    gmake.pprint(inp_dct,indent=4,width=100)
    
    print()
    #def_dct=gmake.read_inp('/Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake/metadata/parameter_definition.inp') 
    #print("="*80)
    #pprint(def_dct)
    
    
    #import hickle as hkl
    #h5file='test_hickle.h5'
    #hkl.dump(inp_dct, h5file, mode='w')
    #dct_return=hkl.load(h5file)
    #gmake.pprint(dct_return)


.. parsed-literal::

    3.7.5 (default, Oct 19 2019, 11:15:26) 
    [Clang 11.0.0 (clang-1100.0.33.8)]
    hyperion
    /Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output
    **********exe read_inp()**************


.. parsed-literal::

    Python version:   3.7.5 (default, Oct 19 2019, 11:15:26) 
    [Clang 11.0.0 (clang-1100.0.33.8)]
    Host Name:        hyperion
    Num of Core:      8
    Total Memory:     32.0 GB
    Available Memory: 13.08 GB
    ################################################################################
    astropy            >=3.2.2      3.2.2       
    emcee              >=3.0.0      3.0.0       
    corner             >=2.0        2.0.1       
    tqdm               unspecified  4.31.1      
    lmfit              unspecified  0.9.12      
    asteval            >=0.9.14     0.9.14      
    numexpr            >=2.7.0      2.7.0       
    hickle             unspecified  3.4.5       
    alpy               unspecified  0.22.0      
    regions            unspecified  0.5.dev1001 
    scipy              unspecified  1.2.1       
    reproject          unspecified  0.6.dev646  
    python-casacore    >=3.1.1      3.1.1       
    scikit-image       unspecified  0.14.2      
    galpy              unspecified  1.5.dev0    
    mkl-fft            unspecified  1.0.14      
    pvextractor        >=0.2.dev327 0.2.dev327  
    spectral-cube      >=0.4.5.dev  0.4.5.dev2267
    radio-beam         >=0.3        0.3.3.dev397
    reproject          >=0.6.dev    0.6.dev646  
    casa-proc          unspecified  0.1.dev3    


.. parsed-literal::

    '0.2.dev1'
    'rx.astro@gmail.com'
    '/Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake'
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    <Logger gmake (DEBUG)>
    [<StreamHandler stderr (INFO)>]
    <Logger gmake (DEBUG)>
    [<FileHandler /Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output/hxmm01_b6c3_uv_mc/gmake.log (DEBUG)>, <StreamHandler stderr (DEBUG)>]
    
    
    
    
    
    
    **********exe read_inp()**************
    {   'basics': {'object': 'hxmm01', 'z': 2.308},
        'co76': {   'restfreq': <Quantity 806.65181 GHz>,
                    'ncrit': <Quantity 120000. 1 / cm3>,
                    'type': 'disk3d',
                    'vis': '../data/hxmm01/alma/2015.1.00723.S/bb34.ms'},
        'ci21': {   'restfreq': <Quantity 809.34197 GHz>,
                    'ncrit': <Quantity 1300. 1 / cm3>,
                    'type': 'disk3d',
                    'vis': '../data/hxmm01/alma/2015.1.00723.S/bb34.ms'},
        'h2o': {   'restfreq': <Quantity 752.03314 GHz>,
                   'ncrit': <Quantity 21000000. 1 / cm3>,
                   'type': 'disk3d',
                   'vis': '../data/hxmm01/alma/2015.1.00723.S/bb1.ms'},
        'cont': {   'restfreq': <Quantity 800. GHz>,
                    'type': 'disk2d',
                    'vis': '../data/hxmm01/alma/2015.1.00723.S/bb1.ms,../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms,../data/hxmm01/alma/2015.1.00723.S/bb34.ms'},
        'compa': {   'pa': <Quantity -14. deg>,
                     'inc': <Quantity 79. deg>,
                     'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (35.0693875, -6.02831111)>,
                     'vsys': <Quantity 292. km / s>,
                     'vrad': <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6] arcsec>,
                     'vrot': <Quantity [  0., 500., 500., 500., 500., 500., 500.] km / s>,
                     'vdis': <Quantity [120., 120., 120., 120., 120., 120., 120.] km / s>},
        'compb': {   'pa': <Quantity 1. deg>,
                     'inc': <Quantity 60. deg>,
                     'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (35.06940417, -6.02905556)>,
                     'vsys': <Quantity -179. km / s>,
                     'vrad': <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6] arcsec>,
                     'vrot': <Quantity [  0., 480., 480., 480., 480., 480., 480.] km / s>,
                     'vdis': <Quantity [120., 120., 120., 120., 120., 120., 120.] km / s>},
        'compc': {   'pa': <Quantity -2. deg>,
                     'inc': <Quantity 70. deg>,
                     'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (35.0690375, -6.02878333)>,
                     'vsys': <Quantity 189. km / s>,
                     'vrad': <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6] arcsec>,
                     'vrot': <Quantity [  0., 170., 170., 170., 170., 170., 170.] km / s>,
                     'vdis': <Quantity [60., 60., 60., 60., 60., 60., 60.] km / s>},
        'co76-compa': {   'import': 'basics,co76,compa',
                          'lineflux': <Quantity 1.3 Jy km / s>,
                          'sbser': [<Quantity 0.21709 arcsec>, 1.0]},
        'ci21-compa': {   'import': 'basics,ci21,compa',
                          'lineflux': <Quantity 0.65 Jy km / s>,
                          'sbser': [<Quantity 0.18771 arcsec>, 1.0]},
        'h2o-compa': {   'import': 'basics,h2o,compa',
                         'lineflux': <Quantity 0.38 Jy km / s>,
                         'sbser': [<Quantity 0.16759 arcsec>, 1.0]},
        'cont-compa': {   'import': 'basics,cont,compa',
                          'alpha': 3.7,
                          'contflux': <Quantity 1.75 mJy>,
                          'sbser': [<Quantity 0.11831 arcsec>, 1.0]},
        'optimize': {   'xypos.ra@compa': ('o', <Quantity [-2.  ,  2.  ,  0.15] arcsec>),
                        'xypos.dec@compa': ('o', <Quantity [-2.  ,  2.  ,  0.15] arcsec>),
                        'vsys@compa': ('a', <Quantity [-120.,  500.,   40.] km / s>),
                        'vrot[1:5]@compa': ('a', <Quantity [  0., 800.,  40.] km / s>),
                        'vdis[0:5]@compa': ('a', <Quantity [  0., 800.,  10.] km / s>),
                        'pa@compa': ('o', <Quantity [-80.,  80.,   5.] deg>),
                        'inc@compa': ('a', <Quantity [ 5., 85.,  5.] deg>),
                        'lineflux@co76-compa': ('a', <Quantity [1.e-01, 2.e+02, 5.e-02] Jy km / s>),
                        'sbser[0]@co76-compa': ('a', <Quantity [0.01, 1.  , 0.01] arcsec>),
                        'lineflux@ci21-compa': ('a', <Quantity [1.e-01, 2.e+02, 1.e-02] Jy km / s>),
                        'sbser[0]@ci21-compa': ('a', <Quantity [0.01, 1.  , 0.01] arcsec>),
                        'lineflux@h2o-compa': ('a', <Quantity [1.e-01, 2.e+02, 1.e-02] Jy km / s>),
                        'sbser[0]@h2o-compa': ('a', <Quantity [0.01, 1.  , 0.01] arcsec>),
                        'contflux@cont-compa': ('a', <Quantity [0.0001, 0.01  , 0.01  ] Jy>),
                        'sbser[0]@cont-compa': ('a', <Quantity [0.01, 0.3 , 0.01] arcsec>),
                        'alpha@cont-compa': ('a', [3, 4.5, 0.1]),
                        'method': 'emcee',
                        'niter': 10,
                        'nwalkers': 40},
        'general': {   'outdir': 'hxmm01_b6c3_uv_mc',
                       'outname_replace': [('../data/hxmm01/alma/2015.1.00723.S/', 'b6c3_')],
                       'outname_exclude': ['cube.', 'mfs.', 'cube3.']}}
    


.. code:: ipython3

    dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True,save_data=True)
    mod_dct=gmake.inp2mod(inp_dct)
    gmake.pprint(mod_dct)



.. parsed-literal::

    read data (may take some time..)
    
    Read: ../data/hxmm01/alma/2015.1.00723.S/bb34.ms
    
    data@../data/hxmm01/alma/2015.1.00723.S/bb34.ms              (118553, 161)        146 MiB             
    uvw@../data/hxmm01/alma/2015.1.00723.S/bb34.ms               (118553, 3)            1 MiB             
    weight@../data/hxmm01/alma/2015.1.00723.S/bb34.ms            (118553,)            463 KiB             1505.6934
    chanfreq@../data/hxmm01/alma/2015.1.00723.S/bb34.ms          (161,)       242.8624 GHz   245.3623 GHz
    chanwidth@../data/hxmm01/alma/2015.1.00723.S/bb34.ms         (161,)        15.6241 MHz    15.6241 MHz
    phasecenter@../data/hxmm01/alma/2015.1.00723.S/bb34.ms       2h20m16.613s  -6d01m43.15s
    data flagging fraction: 0.008205361199930865
    
    Read: ../data/hxmm01/alma/2015.1.00723.S/bb1.ms
    
    data@../data/hxmm01/alma/2015.1.00723.S/bb1.ms               (118430, 110)         99 MiB             
    uvw@../data/hxmm01/alma/2015.1.00723.S/bb1.ms                (118430, 3)            1 MiB             
    weight@../data/hxmm01/alma/2015.1.00723.S/bb1.ms             (118430,)            463 KiB             1950.195
    chanfreq@../data/hxmm01/alma/2015.1.00723.S/bb1.ms           (110,)       226.3469 GHz   228.0500 GHz
    chanwidth@../data/hxmm01/alma/2015.1.00723.S/bb1.ms          (110,)        15.6241 MHz    15.6241 MHz
    phasecenter@../data/hxmm01/alma/2015.1.00723.S/bb1.ms        2h20m16.613s  -6d01m43.15s
    data flagging fraction: 0.006992546421745105
    
    Read: ../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms
    
    data@../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms           (112404, 1)          878 KiB             
    uvw@../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms            (112404, 3)            1 MiB             
    weight@../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms         (112404,)            439 KiB             224059.97
    chanfreq@../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms       (1,)         229.9984 GHz   229.9984 GHz
    chanwidth@../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms      (1,)           1.7187 GHz     1.7187 GHz
    phasecenter@../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms    2h20m16.613s  -6d01m43.15s
    data flagging fraction: 0.0
    --------------------------------------------------------------------------------
    --- dat_dct size 251.21 Mibyte ---
    --- took 1.79801  seconds ---
    --- save to: hxmm01_b6c3_uv_mc/dat_dct.h5


.. parsed-literal::

    {'co76-compa': {'lineflux': <Quantity 1.3 Jy km / s>,
                    'sbser': [<Quantity 0.21709 arcsec>, 1.0],
                    'object': 'hxmm01',
                    'z': 2.308,
                    'restfreq': <Quantity 806.65181 GHz>,
                    'ncrit': <Quantity 120000. 1 / cm3>,
                    'type': 'disk3d',
                    'vis': '../data/hxmm01/alma/2015.1.00723.S/bb34.ms',
                    'pa': <Quantity -14. deg>,
                    'inc': <Quantity 79. deg>,
                    'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (35.0693875, -6.02831111)>,
                    'vsys': <Quantity 292. km / s>,
                    'vrad': <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6] arcsec>,
                    'vrot': <Quantity [  0., 500., 500., 500., 500., 500., 500.] km / s>,
                    'vdis': <Quantity [120., 120., 120., 120., 120., 120., 120.] km / s>},
     'ci21-compa': {'lineflux': <Quantity 0.65 Jy km / s>,
                    'sbser': [<Quantity 0.18771 arcsec>, 1.0],
                    'object': 'hxmm01',
                    'z': 2.308,
                    'restfreq': <Quantity 809.34197 GHz>,
                    'ncrit': <Quantity 1300. 1 / cm3>,
                    'type': 'disk3d',
                    'vis': '../data/hxmm01/alma/2015.1.00723.S/bb34.ms',
                    'pa': <Quantity -14. deg>,
                    'inc': <Quantity 79. deg>,
                    'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (35.0693875, -6.02831111)>,
                    'vsys': <Quantity 292. km / s>,
                    'vrad': <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6] arcsec>,
                    'vrot': <Quantity [  0., 500., 500., 500., 500., 500., 500.] km / s>,
                    'vdis': <Quantity [120., 120., 120., 120., 120., 120., 120.] km / s>},
     'h2o-compa': {'lineflux': <Quantity 0.38 Jy km / s>,
                   'sbser': [<Quantity 0.16759 arcsec>, 1.0],
                   'object': 'hxmm01',
                   'z': 2.308,
                   'restfreq': <Quantity 752.03314 GHz>,
                   'ncrit': <Quantity 21000000. 1 / cm3>,
                   'type': 'disk3d',
                   'vis': '../data/hxmm01/alma/2015.1.00723.S/bb1.ms',
                   'pa': <Quantity -14. deg>,
                   'inc': <Quantity 79. deg>,
                   'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (35.0693875, -6.02831111)>,
                   'vsys': <Quantity 292. km / s>,
                   'vrad': <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6] arcsec>,
                   'vrot': <Quantity [  0., 500., 500., 500., 500., 500., 500.] km / s>,
                   'vdis': <Quantity [120., 120., 120., 120., 120., 120., 120.] km / s>},
     'cont-compa': {'alpha': 3.7,
                    'contflux': <Quantity 1.75 mJy>,
                    'sbser': [<Quantity 0.11831 arcsec>, 1.0],
                    'object': 'hxmm01',
                    'z': 2.308,
                    'restfreq': <Quantity 800. GHz>,
                    'type': 'disk2d',
                    'vis': '../data/hxmm01/alma/2015.1.00723.S/bb1.ms,../data/hxmm01/alma/2015.1.00723.S/bb2.mfs.ms,../data/hxmm01/alma/2015.1.00723.S/bb34.ms',
                    'pa': <Quantity -14. deg>,
                    'inc': <Quantity 79. deg>,
                    'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (35.0693875, -6.02831111)>,
                    'vsys': <Quantity 292. km / s>,
                    'vrad': <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6] arcsec>,
                    'vrot': <Quantity [  0., 500., 500., 500., 500., 500., 500.] km / s>,
                    'vdis': <Quantity [120., 120., 120., 120., 120., 120., 120.] km / s>},
     'general': {'outdir': 'hxmm01_b6c3_uv_mc',
                 'outname_replace': [('../data/hxmm01/alma/2015.1.00723.S/',
                                      'b6c3_')],
                 'outname_exclude': ['cube.', 'mfs.', 'cube3.']}}


.. code:: ipython3

    from gmake import model_lnprob
    fit_dct,sampler=gmake.fit_setup(inp_dct,dat_dct)
    #gmake.pprint(fit_dct)
    #pp.pprint(fit_dct['p_start'])
    mod_dct=gmake.inp2mod(inp_dct)
    #gmake.pprint(mod_dct)
    obj=mod_dct['co76-compa']
    obj_out=gmake.obj_defunit(obj)
    gmake.pprint(obj)
    gmake.pprint(obj_out)
    lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
                                   savemodel=inp_dct['general']['outdir'],packblobs=True)



.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    optimizer: emcee
    optimizing parameters: index / name / unit / start / lo_limit / up_limit / scale
     0   xypos.ra@compa       deg                   35.0693875    (  35.0688319  ,   35.0699431   )   0.0000056   
     1   xypos.dec@compa      deg                   -6.0283111    (  -6.0288667  ,   -6.0277556   )   0.0000056   
     2   vsys@compa           km / s                  292.00      (    -120.00   ,     500.00     )     4.12      
     3   vrot[1:5]@compa      km / s                  500.00      (     0.00     ,     800.00     )     5.00      
     4   vdis[0:5]@compa      km / s                  120.00      (     0.00     ,     800.00     )     6.80      
     5   pa@compa             deg                     -14.00      (    -94.00    ,      66.00     )     0.80      
     6   inc@compa            deg                      79.00      (     5.00     ,      85.00     )     0.74      
     7   lineflux@co76-compa  Jy km / s                1.30       (     0.10     ,     200.00     )     1.99      
     8   sbser[0]@co76-compa  arcsec                   0.22       (     0.01     ,      1.00      )     0.01      
     9   lineflux@ci21-compa  Jy km / s                0.65       (     0.10     ,     200.00     )     1.99      
     10  sbser[0]@ci21-compa  arcsec                   0.19       (     0.01     ,      1.00      )     0.01      
     11  lineflux@h2o-compa   Jy km / s                0.38       (     0.10     ,     200.00     )     2.00      
     12  sbser[0]@h2o-compa   arcsec                   0.17       (     0.01     ,      1.00      )     0.01      
     13  contflux@cont-compa  Jy                       0.00       (     0.00     ,      0.01      )     0.00      
     14  sbser[0]@cont-compa  arcsec                   0.12       (     0.01     ,      0.30      )     0.00      
     15  alpha@cont-compa                              3.70       (     3.00     ,      4.50      )     0.01      
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    nwalkers:40
    nthreads:8
    ndim:    16
    outdir:  hxmm01_b6c3_uv_mc


.. parsed-literal::

    --> 0.0
    xypos.ra@compa 35.0693875 deg <class 'astropy.units.core.Unit'>
    xypos.dec@compa -6.028311111111111 deg <class 'astropy.units.core.Unit'>
    vsys@compa 292.0 km / s <class 'astropy.units.core.CompositeUnit'>
    vrot[1:5]@compa 500.0 km / s <class 'astropy.units.core.CompositeUnit'>
    vdis[0:5]@compa 120.0 km / s <class 'astropy.units.core.CompositeUnit'>
    pa@compa -14.0 deg <class 'astropy.units.core.Unit'>
    inc@compa 79.0 deg <class 'astropy.units.core.Unit'>
    lineflux@co76-compa 1.3 Jy km / s <class 'astropy.units.core.CompositeUnit'>
    sbser[0]@co76-compa 0.21709 arcsec <class 'astropy.units.core.Unit'>
    lineflux@ci21-compa 0.65 Jy km / s <class 'astropy.units.core.CompositeUnit'>
    sbser[0]@ci21-compa 0.18771 arcsec <class 'astropy.units.core.Unit'>
    lineflux@h2o-compa 0.38 Jy km / s <class 'astropy.units.core.CompositeUnit'>
    sbser[0]@h2o-compa 0.16759 arcsec <class 'astropy.units.core.Unit'>
    contflux@cont-compa 0.00175 Jy <class 'astropy.units.core.Unit'>
    sbser[0]@cont-compa 0.11831 arcsec <class 'astropy.units.core.Unit'>
    alpha@cont-compa 3.7  <class 'astropy.units.core.CompositeUnit'>


::


    ---------------------------------------------------------------------------

    UnitConversionError                       Traceback (most recent call last)

    <ipython-input-6-c4594b9c0fbb> in <module>
          1 from gmake import model_lnprob
    ----> 2 fit_dct,sampler=gmake.fit_setup(inp_dct,dat_dct)
          3 #gmake.pprint(fit_dct)
          4 #pp.pprint(fit_dct['p_start'])
          5 mod_dct=gmake.inp2mod(inp_dct)


    ~/Dropbox/Worklib/projects/GMaKE/gmake/opt.py in fit_setup(inp_dct, dat_dct, initial_model, copydata)
         38         start_time = time.time()
         39         lnl,lnprob,chisq,ndata,npar=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
    ---> 40                                                  savemodel=None)
         41         #lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,packblobs=True,
         42         #                       savemodel='')


    ~/Dropbox/Worklib/projects/GMaKE/gmake/model_eval.py in model_lnprob(theta, fit_dct, inp_dct, dat_dct, savemodel, decomp, nsamps, packblobs, verbose)
        251     lnl,blobs=model_lnlike(theta,fit_dct,inp_dct,dat_dct,
        252                            savemodel=savemodel,decomp=decomp,nsamps=nsamps,
    --> 253                            verbose=verbose)
        254 
        255     if  verbose==True:


    ~/Dropbox/Worklib/projects/GMaKE/gmake/model_eval.py in model_lnlike(theta, fit_dct, inp_dct, dat_dct, savemodel, decomp, nsamps, returnwdev, verbose)
         47 
         48     models=model_api(mod_dct,dat_dct,
    ---> 49                      decomp=decomp,nsamps=nsamps,verbose=verbose)
         50     #print('Took {0} second on one API call'.format(float(time.time()-tic0)))
         51     #gmake_listpars(mod_dct)


    ~/Dropbox/Worklib/projects/GMaKE/gmake/model_build.py in model_api(mod_dct, dat_dct, nsamps, decomp, verbose)
         22 
         23     models=model_init(mod_dct,dat_dct,decomp=decomp,verbose=verbose)
    ---> 24     models=model_fill(models,decomp=decomp,nsamps=nsamps,verbose=verbose)
         25     models=model_simobs(models,decomp=decomp,verbose=verbose)
         26 


    ~/Dropbox/Worklib/projects/GMaKE/gmake/model_build.py in model_fill(models, nsamps, decomp, verbose)
        244                     imodel,imodel_prof=model_disk3d(models['header@'+vis],obj,
        245                                                     model=models['imod3d@'+vis],
    --> 246                                                     nsamps=nsamps,fixseed=False,mod_dct=mod_dct)
        247                     #print("---{0:^10} : {1:<8.5f} seconds ---".format('fill:  '+tag+'-->'+vis+' disk3d',time.time() - test_time))
        248                     #print(imodel.shape)


    ~/Dropbox/Worklib/projects/GMaKE/gmake/model_func.py in model_disk3d(header, objp, model, nsamps, decomp, fixseed, verbose, mod_dct)
        174     w=WCS(header)
        175     if  'Hz' in header['CUNIT3']:
    --> 176         wz=obj['restfreq']/(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
        177         dv=-const.c*header['CDELT3']/(1.0e9*obj['restfreq']/(1.0+obj['z']))/1000.
        178     if  'angstrom' in header['CUNIT3']:


    ~/Library/Python/3.7/lib/python/site-packages/astropy/units/quantity.py in __array_ufunc__(self, function, method, *inputs, **kwargs)
        442         # consistent units between two inputs (e.g., in np.add) --
        443         # and the unit of the result (or tuple of units for nout > 1).
    --> 444         converters, unit = converters_and_unit(function, method, *inputs)
        445 
        446         out = kwargs.get('out', None)


    ~/Library/Python/3.7/lib/python/site-packages/astropy/units/quantity_helper/converters.py in converters_and_unit(function, method, *args)
        187                             "argument is not a quantity (unless the "
        188                             "latter is all zero/infinity/nan)"
    --> 189                             .format(function.__name__))
        190             except TypeError:
        191                 # _can_have_arbitrary_unit failed: arg could not be compared


    UnitConversionError: Can only apply 'subtract' function to dimensionless quantities when other argument is not a quantity (unless the latter is all zero/infinity/nan)


.. code:: ipython3

    from gmake.metadata import template_imheader


::


    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-4-72db95b36947> in <module>
    ----> 1 from gmake.metadata import template_imheader
    

    ImportError: cannot import name 'template_imheader' from 'gmake.metadata' (unknown location)


.. code:: ipython3

    pprint(template_imheader)

.. code:: ipython3

    import gmake

.. code:: ipython3

    gmake.meta.pars_def

.. code:: ipython3

    u.Unit("")

.. code:: ipython3

    import astropy.units as u
    u.Unit("")
    print(type(u.Unit(1)))

.. code:: ipython3

    gmake.inp_def

.. code:: ipython3

    type(u.Unit(1))


