|Open In Colab|

Example BX610: perform model fitting using method=‘emcee’
---------------------------------------------------------

.. |Open In Colab| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/r-xue/casa_proc/blob/master/demo/test_casaproc.ipynb

.. code:: ipython3

    import sys
    import glob
    import os
    import io
    import logging
    import emcee
    from pprint import pprint
    
    print(sys.version)
    
    
    import socket 
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir('/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output/')
    print(socket.gethostname())
    print(os.getcwd())
    
    import gmake
    print(gmake.__version__)
    print(gmake.__email__)
    print(gmake.__demo__)
    gmake.check_deps()
    
    #inpfile=gmake.__demo__+'/../examples/inpfile/bx610_b4c5_uv_mc.inp'
    inpfile=gmake.__demo__+'/../examples/inpfile/bx610_b6c3_uv_mc.inp'
    logfile=''
    
    print('>'*40)
    #gmake.logger_config()
    #gmake.logger_status()
    #import pprint
    #pprint.pprint(logging.Logger.manager.loggerDict) 
    gmake.logger_config()
    inp_dct=gmake.read_inp(inpfile)
    outdir=inp_dct['general']['outdir']
    gmake.logger_config(logfile=outdir+'/gmake.log',loglevel='DEBUG',logfilelevel='DEBUG')
    gmake.logger_status()
    gmake.pprint(inp_dct)
    inp_dct=gmake.inp_validate(inp_dct)


.. parsed-literal::

    3.7.5 (default, Oct 19 2019, 11:15:26) 
    [Clang 11.0.0 (clang-1100.0.33.8)]
    hyperion
    /Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output
    **********exe read_inp()**************


.. parsed-literal::

    astropy            >=3.2.2      3.2.2       
    emcee              >=3.0.0      3.0.1       
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

    0.2.dev1
    rx.astro@gmail.com
    /Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    **********exe read_inp()**************
    <Logger gmake (DEBUG)>
    [<FileHandler /Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output/bx610_b6c3_uv_mc/gmake.log (DEBUG)>, <StreamHandler stderr (DEBUG)>]
    {'basics': {'object': 'bx610',
                'z': 2.21,
                'pa': <Quantity -52.4 deg>,
                'inc': <Quantity 44.06 deg>,
                'xypos': <SkyCoord (ICRS): (ra, dec) in deg
        (356.53932583, 12.82201819)>,
                'vsys': <Quantity 117.5 km / s>,
                'vrad': <Quantity [0.  , 0.12, 0.24, 0.36, 0.48] arcsec>,
                'vrot': <Quantity [  0.        , 197.03794218, 197.03794218, 197.03794218,
               197.03794218] km / s>,
                'vdis': <Quantity [50.82245316, 50.82245316, 50.82245316, 50.82245316, 50.82245316] km / s>},
     'dynamics   (not implemented yet)': {'disk_sd': <Quantity 5.e+09 solMass / kpc2>,
                                          'disk_rs': <Quantity 1. kpc>,
                                          'halo_mvir': <Quantity 5.e+11 solMass>},
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
              'pa': <Quantity 12.05551076 deg>,
              'inc': <Quantity 27.53227189 deg>,
              'restfreq': <Quantity 251.68251775 GHz>,
              'alpha': 3.7183180041434882,
              'contflux': <Quantity 0.00175222 Jy>,
              'sbser': [<Quantity 0.11831162 arcsec>, 1.0]},
     'optimize': {'vsys@basics': ('a', <Quantity [-120.,  280.,   40.] km / s>),
                  'vrot[1:5]@basics': ('a', <Quantity [  0., 800.,  40.] km / s>),
                  'vdis[0:5]@basics': ('a', <Quantity [  0., 200.,  10.] km / s>),
                  'xypos.ra@basics': ('o', <Quantity [-1. ,  1. ,  0.1] arcsec>),
                  'xypos.dec@basics': ('o', <Quantity [-1. ,  1. ,  0.1] arcsec>),
                  'method': 'emcee',
                  'niter': 100,
                  'nwalkers': 20},
     'general': {'outdir': 'bx610_b6c3_uv_mc',
                 'outname_replace': [('../data/bx610/alma/2015.1.00250.S/',
                                      'b6c3_')],
                 'outname_exclude': ['cube.', 'mfs.', 'cube3.']}}


dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True,save_data=True)

from gmake import model_lnprob
#import gmake

#mod_dct=gmake.inp2mod(inp_dct)
#gmake.pprint(mod_dct)
#obj_dct=gmake.obj_defunit(mod_dct['co76'])
#gmake.pprint(obj_dct)
inp_dct=gmake.read_inp(inpfile)
fit_dct=gmake.fit_setup(inp_dct,dat_dct)
gmake.fit_iterate(fit_dct,inp_dct,dat_dct)

#lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
#                               savemodel=inp_dct['general']['outdir'],packblobs=True)
#
#import numpy as np
#print(type(blobs))
#print(np.shape(blobs))

.. code:: ipython3

    gmake.fit_analyze(inpfile)


.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    >>>  vsys@basics:
     median(sigma) = 149.16      -99.80      -70.84      82.17       126.46     
     median(ptile) = 149.16      49.36       78.32       231.33      275.62     
     start(iscale) = 117.50     /2.38       
     mode          = 94.35      
    >>>  vrot[1:5]@basics:
     median(sigma) = 242.03           -214.42          -152.68          338.48           463.74          
     median(ptile) = 242.03           27.61            89.35            580.51           705.77          
     start(iscale) = 197.04          /6.03            
     mode          = 199.54          
    >>>  vdis[0:5]@basics:
     median(sigma) = 65.87            -63.34           -48.12           73.44            120.69          
     median(ptile) = 65.87            2.53             17.75            139.30           186.56          
     start(iscale) = 50.82           /1.49            
     mode          = 10.80           


.. parsed-literal::

    **********exe read_inp()**************


.. parsed-literal::

    >>>  xypos.ra@basics:
     median(sigma) = 356.5393255     -0.0000009      -0.0000005      0.0000005       0.0000009      
     median(ptile) = 356.5393255     356.5393246     356.5393249     356.5393260     356.5393263    
     start(iscale) = 356.5393258    /0.0000028      
     mode          = 356.5393258    
    >>>  xypos.dec@basics:
     median(sigma) = 12.8220191       -0.0000009       -0.0000004       0.0000005        0.0000010       
     median(ptile) = 12.8220191       12.8220182       12.8220187       12.8220196       12.8220200      
     start(iscale) = 12.8220182      /0.0000028       
     mode          = 12.8220189      
    ------------------------------------------------------------------------------------------
    analyzing outfolder:bx610_b6c3_uv_mc
    plotting...bx610_b6c3_uv_mc/emcee-iteration.pdf
    analyzing outfolder:bx610_b6c3_uv_mc
    plotting...bx610_b6c3_uv_mc/emcee-iteration-blobs.pdf
    plotting...bx610_b6c3_uv_mc/line-triangle.pdf
    input data size:(1000, 5)
    Took 1.1343879699707031 seconds
    /Users/Rui/Library/Python/3.7/lib/python/site-packages/hickle/hickle.py:403: SerializedWarning: <class 'astropy.units.core.CompositeUnit'> type not understood, data have been serialized
      SerializedWarning)
    /Users/Rui/Library/Python/3.7/lib/python/site-packages/hickle/hickle.py:403: SerializedWarning: <class 'astropy.units.core.Unit'> type not understood, data have been serialized
      SerializedWarning)
    --- save to: bx610_b6c3_uv_mc/fit.h5


