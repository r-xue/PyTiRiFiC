|Open In Colab|

Example BX610: perform model fitting using method=‘amoeba’ for the Band 4 Cycle 5 DataSet
-----------------------------------------------------------------------------------------

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
    
    inpfile=gmake.__demo__+'/../examples/inpfile/bx610_b4c5_uv_ab.inp'
    logfile=''
    
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
    
    %reload_ext line_profiler
    %reload_ext memory_profiler



.. parsed-literal::

    3.7.5 (default, Oct 19 2019, 11:15:26) 
    [Clang 11.0.0 (clang-1100.0.33.8)]
    hyperion
    /Volumes/S1/projects/GMaKE/examples/output
    0.2.dev1
    rx.astro@gmail.com
    /Users/Rui/Documents/Workspace/projects/GMaKE/gmake
    <Logger gmake (DEBUG)>
    [<FileHandler /Volumes/S1/projects/GMaKE/examples/output/bx610_b4c5_uv_ab/gmake.log (DEBUG)>, <StreamHandler stderr (DEBUG)>]


.. code:: ipython3

    #%time dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True)
    #%prun dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True)
    #%lprun -f gmake.read_data dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True)
    #del dat_dct
    #%memit dat_dct=gmake.read_data(inp_dct)
    #%mprun -f gmake.read_data dat_dct=gmake.read_data(inp_dct)
    dat_dct=gmake.read_data(inp_dct)


.. parsed-literal::

    read data (may take some time..)
    
    Read: ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2
    
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2            complex64       (275794, 128)        269 MiB             
    uvw@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2             float32         (275794, 3)            3 MiB             
    weight@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2          float32         (275794,)              1 MiB             
      >>percentiles (0,16,50,84,100)%: [ 39.59812164 185.1169751  253.05403137 324.3769751  594.16479492]
    chanfreq@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2        (128,)     143301022036.5513 Hz 143797143423.9031 Hz
    chanwidth@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2       (128,)     -3906467.6169 Hz -3906467.6169 Hz
    phasecenter@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2     23h46m09.438s  12d49m19.25s
    
    Read: ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2
    
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2            complex64       (276124, 179)        377 MiB             
    uvw@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2             float32         (276124, 3)            3 MiB             
    weight@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2          float32         (276124,)              1 MiB             
      >>percentiles (0,16,50,84,100)%: [ 36.37529755 156.95782593 215.15796661 281.27739258 531.50854492]
    chanfreq@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2        (179,)     153003656218.1177 Hz 153699007453.9771 Hz
    chanwidth@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2       (179,)     3906467.6172 Hz 3906467.6172 Hz
    phasecenter@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2     23h46m09.438s  12d49m19.25s
    
    Read: ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1
    
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1            complex64       (275794, 1)            2 MiB             
    uvw@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1             float32         (275794, 3)            3 MiB             
    weight@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1          float32         (275794,)              1 MiB             
      >>percentiles (0,16,50,84,100)%: [  6731.69726562  31469.71625     43019.20117188  55143.775
     101009.09375   ]
    chanfreq@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1        (1,)       142967019055.3026 Hz 142967019055.3026 Hz
    chanwidth@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1       (1,)       -664099494.8804 Hz -664099494.8804 Hz
    phasecenter@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1     23h46m09.438s  12d49m19.25s
    
    Read: ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3
    
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3            complex64       (275794, 1)            2 MiB             
    uvw@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3             float32         (275794, 3)            3 MiB             
    weight@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3          float32         (275794,)              1 MiB             
      >>percentiles (0,16,50,84,100)%: [  7088.08105469  33135.7590625   45296.69335938  58063.151875
     106356.640625  ]
    chanfreq@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3        (1,)       144148725509.4280 Hz 144148725509.4280 Hz
    chanwidth@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3       (1,)       -699257703.4329 Hz -699257703.4329 Hz
    phasecenter@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3     23h46m09.438s  12d49m19.25s
    
    Read: ../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs
    
    data@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs            complex64       (276124, 1)            2 MiB             
    uvw@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs             float32         (276124, 3)            3 MiB             
    weight@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs          float32         (276124,)              1 MiB             
      >>percentiles (0,16,50,84,100)%: [ 10749.33203125  71887.625625   100576.19921875 129892.62875
     242941.46875   ]
    chanfreq@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs        (1,)       141738204024.6475 Hz 141738204024.6475 Hz
    chanwidth@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs       (1,)       -1863385053.3984 Hz -1863385053.3984 Hz
    phasecenter@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs     23h46m09.438s  12d49m19.25s
    
    Read: ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1
    
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1            complex64       (276124, 1)            2 MiB             
    uvw@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1             float32         (276124, 3)            3 MiB             
    weight@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1          float32         (276124,)              1 MiB             
      >>percentiles (0,16,50,84,100)%: [ 3019.16308594 13027.213125   17858.26757812 23346.20828125
     44115.19140625]
    chanfreq@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1        (1,)       152839584578.1958 Hz 152839584578.1958 Hz
    chanwidth@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1       (1,)       324236812.2266 Hz 324236812.2266 Hz
    phasecenter@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1     23h46m09.438s  12d49m19.25s
    
    Read: ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3
    
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3            complex64       (276124, 1)            2 MiB             
    uvw@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3             float32         (276124, 3)            3 MiB             
    weight@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3          float32         (276124,)              1 MiB             
      >>percentiles (0,16,50,84,100)%: [  7820.72753906  33745.1590625   46259.30664062  60475.089375
     114274.328125  ]
    chanfreq@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3        (1,)       154120905956.6333 Hz 154120905956.6333 Hz
    chanwidth@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3       (1,)       839890537.6953 Hz 839890537.6953 Hz
    phasecenter@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3     23h46m09.438s  12d49m19.25s
    
    Read: ../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs
    
    data@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs            complex64       (276124, 1)            2 MiB             
    uvw@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs             float32         (276124, 3)            3 MiB             
    weight@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs          float32         (276124,)              1 MiB             
      >>percentiles (0,16,50,84,100)%: [ 10978.32617188  60905.94515625  85937.25       113244.640625
     218176.15625   ]
    chanfreq@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs        (1,)       155441364443.2279 Hz 155441364443.2279 Hz
    chanwidth@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs       (1,)       1863385053.3984 Hz 1863385053.3984 Hz
    phasecenter@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs     23h46m09.438s  12d49m19.25s
    --------------------------------------------------------------------------------
    --- dat_dct size 692.76 Mibyte ---
    --- took 14.62557 seconds ---


.. code:: ipython3

    #
    #mod_dct=gmake.inp2mod(inp_dct)
    #gmake.pprint(mod_dct)
    #gmake.model_vrot(mod_dct)
    #gmake.pprint(mod_dct)
    #gmake.model_vrot_plot(mod_dct['co76'])
    
    inp_dct=gmake.read_inp(inpfile)
    inp_dct=gmake.inp_validate(inp_dct)
    mod_dct=gmake.inp2mod(inp_dct)
    gmake.model_vrot(mod_dct)
    #mod_dct['co76']
    %mprun -f gmake.model_eval.model_lnlike2 fit_dct=gmake.fit_setup(inp_dct,dat_dct,save_model=False,initial_model=False)
    #fit_dct=gmake.fit_setup(inp_dct,dat_dct,initial_model=True,save_model=False)
    #%mprun -f gmake.fit_iterate gmake.fit_iterate(fit_dct,inp_dct,dat_dct)


.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    optimizer: amoeba
    optimizing parameters:
    ----------------------------------------------------------------------------------------------------
    index    name    unit    start    lo_limit    up_limit    scale
     0   vsys@basics       km / s               100.00      (     0.00     ,     220.00     )    120.00     
     1   disk_sd@diskdyn   solMass / pc2        3000.00     (    100.00    ,    50000.00    )   47000.00    
     2   disk_rs@diskdyn   kpc                   2.00       (     0.20     ,      10.00     )     8.00      
     3   vdis@basics       km / s                50.00      (     0.00     ,     200.00     )    150.00     
     4   pa@basics         deg                  -52.40      (    -132.40   ,      27.60     )     80.00     
     5   inc@basics        deg                   44.06      (     5.00     ,      85.00     )     40.94     
     6   xypos.ra@basics   deg                356.5393258   (  356.5390481 ,   356.5396036  )   0.0002778   
     7   xypos.dec@basics  deg                12.8220182    (  12.8217404  ,   12.8222960   )   0.0002778   
     8   lineflux@co43     Jy km / s             1.00       (     0.10     ,     200.00     )    199.00     
     9   sbser[0]@co43     arcsec                0.22       (     0.01     ,      2.00      )     1.78      
     10  lineflux@ci10     Jy km / s             0.50       (     0.10     ,     200.00     )    199.50     
     11  sbser[0]@ci10     arcsec                0.19       (     0.01     ,      2.00      )     1.81      
     12  contflux@cont     Jy                    0.00       (     0.00     ,      0.01      )     0.01      
     13  sbser[0]@cont     arcsec                0.15       (     0.01     ,      2.00      )     1.85      
     14  alpha@cont                              3.72       (     3.00     ,      4.50      )     0.78      
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ndim:    15
    outdir:  bx610_b4c5_uv_ab
    --- save to: bx610_b4c5_uv_ab/fit.h5


.. parsed-literal::

    



.. parsed-literal::

    


.. code:: ipython3

    #%mprun -f gmake.model_eval.model_lnprob lnl,lnprob,chisq,ndata,npar=gmake.model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,savemodel=None)
    #%timeit lnl,lnprob,chisq,ndata,npar=gmake.model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,savemodel=None)
    #%timeit lnl,lnprob,chisq,ndata,npar=gmake.model_lnprob2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,savemodel=None)
    #%lprun -f gmake.model_func.model_uvchi2  lnl,lnprob,chisq,ndata,npar=gmake.model_lnprob2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,savemodel=None)
    %mprun -f gmake.model_func.model_uvchi2 lnl,lnprob,chisq,ndata,npar=gmake.model_lnprob2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,savemodel=None)


.. parsed-literal::

    



.. parsed-literal::

    Filename: /Users/Rui/Documents/Workspace/projects/GMaKE/gmake/model_func.py
    
    Line #    Mem usage    Increment   Line Contents
    ================================================
       783   3115.3 MiB   2523.8 MiB   def model_uvchi2(xymod3d,xymod2d,xyheader,
       784                                                 uvdata,uvw,phasecenter,uvweight,
       785                                                 average=True,verbose=True):
       786                                 """
       787                                 simulate the observation in the UV-domain
       788                                 The input reference 2D / 3D model (e.g. continuume+line) is expected in units of Jy/pix
       789                                 
       790                                 uvw shape:           nrecord x 3  
       791                                 uvmodel shape:       nrecord x nchan (less likely: nrecord x nchan x ncorr)
       792                                 xymodel shape:       nstokes x nchan x ny x nx
       793                                 
       794                                 note1:
       795                                     Because sampleImaging() can be only applied to single-wavelength dataset, we have to loop over
       796                                     all channels for multi-frequency dataset (e.g. spectral cubes). This loop operations is typically
       797                                     the bottle-neck. To reduce the number of operation, we can only do uvsampling for frequency-plane
       798                                     with varying morphology and process frequency-inpdent emission using one operation:  
       799                                     the minimal number of operations required  is:
       800                                             nplane(with varying morphology) + 1 x sampleImage()
       801                                       we already trim any else overhead (e.g. creating new array) and reach close to this limit.
       802                                 
       803                                 note2:
       804                                     when <uvmodel> is provided as input, a new model will be added into the array without additional memory usage 
       805                                       the return variable is just a reference of mutable <uvmodel>
       806                             
       807                                 """
       808                             
       809                                 #print('3d:',xymod3d is not None)
       810                                 #print('2d:',xymod2d is not None)
       811                                 
       812   3115.3 MiB      0.0 MiB       cell=np.sqrt(abs(xyheader['CDELT1']*xyheader['CDELT2']))
       813   3115.3 MiB      0.0 MiB       nchan=xyheader['NAXIS3']
       814   3115.3 MiB      0.0 MiB       nrecord=(uvw.shape)[0]
       815                                 
       816                                 # + zeros_like vs. zeros()
       817                                 #   the memory of an array created by zeros() can allocated on-the-fly
       818                                 #   the creation will appear to be faster but the looping+plan initialization may be slightly slower (or comparable?) 
       819                                 # + set order='F' as we want to have quick access to each column:
       820                                 #   i.a. first dimension is consequential in memory 
       821                                 #   this will improve on the performance of picking uvdata from each channel  
       822                                 # we force order='F', so the first dimension is continiuous and we can quicky fetch each channel
       823                                 # as the information in a single channel is saved in a block  
       824                             
       825                             
       826   3115.3 MiB      0.0 MiB       if  verbose==True:
       827                                     start_time = time.time()
       828                                     print('nchan,nrecord:',nchan,nrecord)    
       829                                         
       830                                 # assume that CRPIX1/CRPIX2 is at model image "center" floor(naxis/2);
       831                                 # which is true for the mock-up/reference model image xyheader 
       832                                 # more information on the pixel index /ra-dec mapping, see:
       833                                 #       https://mtazzari.github.io/galario/tech-specs.html     
       834   3115.3 MiB      0.0 MiB       dRA=np.deg2rad(+(xyheader['CRVAL1']-phasecenter[0].to_value(u.deg)))
       835   3115.3 MiB      0.0 MiB       dDec=np.deg2rad(+(xyheader['CRVAL2']-phasecenter[1].to_value(u.deg)))
       836                                 
       837   3115.3 MiB      0.0 MiB       cc=0
       838   3115.3 MiB      0.0 MiB       chi2=0
       839                             
       840   3115.3 MiB      0.0 MiB       if  xymod2d is not None:
       841   3115.3 MiB      0.0 MiB           i0=int(nchan/2.0)
       842   3115.3 MiB      0.0 MiB           xymodelsum=xymod2d.sum(axis=(0,2,3))
       843   3115.3 MiB      0.0 MiB           xymodel_zscale=xymodelsum/xymodelsum[i0]        
       844   3115.3 MiB      0.0 MiB           wv=const.c/(xyheader['CDELT3']*i0+xyheader['CRVAL3'])
       845   3115.3 MiB      0.0 MiB           cc+=1
       846                                     #ss=time.time()
       847   3115.3 MiB      0.0 MiB           uvmod2d=sampleImage((xymod2d[0,i0,:,:]),
       848   3115.3 MiB      0.0 MiB                                (np.deg2rad(cell)).astype(np.float32),
       849   3115.3 MiB      0.0 MiB                                (uvw[:,0]/wv),
       850   3115.3 MiB      0.0 MiB                                (uvw[:,1]/wv),                                   
       851   3115.3 MiB      0.0 MiB                                dRA=dRA.astype(np.float32),dDec=dDec.astype(np.float32),
       852   3115.3 MiB      0.2 MiB                                PA=0.0,check=False,origin='lower')
       853                                 
       854   3115.3 MiB      0.0 MiB       if  xymod3d is not None:
       855   3115.3 MiB      0.0 MiB           for i in range(nchan):
       856   3115.3 MiB      0.0 MiB               if  ne.evaluate("sum(a)",local_dict={'a':xymod3d[0,i,:,:]})==0.0:
       857   3115.3 MiB      0.0 MiB                   delta_uv=ne.evaluate('a2*a3-b',
       858   3115.3 MiB      0.0 MiB                                    local_dict={'a2':uvmod2d,
       859   3115.3 MiB      0.0 MiB                                                'a3':xymodel_zscale[i],
       860   3115.3 MiB      4.2 MiB                                                'b':uvdata[:,i]})
       861   3115.3 MiB      0.0 MiB                   chi2+=ne.evaluate('sum( ( (a.real)**2+(a.imag)**2 ) *c)',
       862   3115.3 MiB      0.0 MiB                                    local_dict={'a':delta_uv,
       863   3115.3 MiB      0.0 MiB                                                'c':uvweight})                
       864                                             #chi2+=ne.evaluate('sum( abs(a)**2*c)',
       865                                             #                 local_dict={'a':delta_uv,
       866                                             #                             'c':uvweight})
       867                                         else:
       868   3115.3 MiB      0.0 MiB                   wv=const.c/(xyheader['CDELT3']*i+xyheader['CRVAL3'])
       869   3115.3 MiB      0.0 MiB                   cc+=1
       870                                             #uvmod3d=sampleImage((xymod3d[0,i,:,:]),
       871                                             #                                        (np.deg2rad(cell)).astype(np.float32),
       872                                             #                                        (uvw[:,0]/wv),
       873                                             #                                        (uvw[:,1]/wv),                                   
       874                                             #                                        dRA=dRA.astype(np.float32),dDec=dDec.astype(np.float32),
       875                                             #                                        PA=0.,check=False,origin='lower')
       876                                             #uvmodel=uvmod3d+uvmod2d*xymodel_zscale[i]
       877   3115.3 MiB      0.0 MiB                   delta_uv=ne.evaluate('a2*a3+a1-b',
       878   3115.3 MiB      0.0 MiB                                    local_dict={'a1':sampleImage((xymod3d[0,i,:,:]),
       879   3115.3 MiB      0.0 MiB                                                           (np.deg2rad(cell)).astype(np.float32),
       880   3115.3 MiB      0.0 MiB                                                           (uvw[:,0]/wv),
       881   3115.3 MiB      0.0 MiB                                                           (uvw[:,1]/wv),                                   
       882   3115.3 MiB      0.0 MiB                                                           dRA=dRA.astype(np.float32),dDec=dDec.astype(np.float32),
       883   3115.3 MiB      2.1 MiB                                                           PA=0.,check=False,origin='lower'),
       884   3115.3 MiB      0.0 MiB                                                'a2':uvmod2d,
       885   3115.3 MiB      0.0 MiB                                                'a3':xymodel_zscale[i],
       886   3115.3 MiB      4.3 MiB                                                'b':uvdata[:,i]})
       887   3115.3 MiB      0.0 MiB                   chi2+=ne.evaluate('sum( ( (a.real)**2+(a.imag)**2 ) *c)',
       888   3115.3 MiB      0.0 MiB                                    local_dict={'a':delta_uv,
       889   3115.3 MiB      0.0 MiB                                                'c':uvweight})
       890                                             #chi2+=ne.evaluate('sum( abs(a)**2*c)',
       891                                             #                 local_dict={'a':delta_uv,
       892                                             #                             'c':uvweight})                
       893                             
       894                                
       895   3115.3 MiB      0.0 MiB       return chi2


.. code:: ipython3

    #
    #mod_dct=gmake.inp2mod(inp_dct)
    #gmake.pprint(mod_dct)
    #gmake.model_vrot(mod_dct)
    #gmake.pprint(mod_dct)
    #gmake.model_vrot_plot(mod_dct['co76'])
    import gmake
    inp_dct=gmake.read_inp(inpfile)
    inp_dct=gmake.inp_validate(inp_dct)
    mod_dct=gmake.inp2mod(inp_dct)
    gmake.model_vrot(mod_dct)
    #mod_dct['co76']
    %mprun -f gmake.model_eval.model_lnprob fit_dct=gmake.fit_setup(inp_dct,dat_dct)
    #fit_dct=gmake.fit_setup(inp_dct,dat_dct,initial_model=True,save_model=False)
    #%mprun -f gmake.fit_iterate gmake.fit_iterate(fit_dct,inp_dct,dat_dct)


.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    optimizer: amoeba
    optimizing parameters:
    ----------------------------------------------------------------------------------------------------
    index    name    unit    start    lo_limit    up_limit    scale
     0   vsys@basics       km / s               100.00      (     0.00     ,     220.00     )    120.00     
     1   disk_sd@diskdyn   solMass / pc2        3000.00     (    100.00    ,    50000.00    )   47000.00    
     2   disk_rs@diskdyn   kpc                   2.00       (     0.20     ,      10.00     )     8.00      
     3   vdis@basics       km / s                50.00      (     0.00     ,     200.00     )    150.00     
     4   pa@basics         deg                  -52.40      (    -132.40   ,      27.60     )     80.00     
     5   inc@basics        deg                   44.06      (     5.00     ,      85.00     )     40.94     
     6   xypos.ra@basics   deg                356.5393258   (  356.5390481 ,   356.5396036  )   0.0002778   
     7   xypos.dec@basics  deg                12.8220182    (  12.8217404  ,   12.8222960   )   0.0002778   
     8   lineflux@co43     Jy km / s             1.00       (     0.10     ,     200.00     )    199.00     
     9   sbser[0]@co43     arcsec                0.22       (     0.01     ,      2.00      )     1.78      
     10  lineflux@ci10     Jy km / s             0.50       (     0.10     ,     200.00     )    199.50     
     11  sbser[0]@ci10     arcsec                0.19       (     0.01     ,      2.00      )     1.81      
     12  contflux@cont     Jy                    0.00       (     0.00     ,      0.01      )     0.01      
     13  sbser[0]@cont     arcsec                0.15       (     0.01     ,      2.00      )     1.85      
     14  alpha@cont                              3.72       (     3.00     ,      4.50      )     0.78      
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ndim:    15
    outdir:  bx610_b4c5_uv_ab
    one trial                                          : 4.98618  seconds
    ndata->0.0
    chisq->149336333.31762546
    --- save to: bx610_b4c5_uv_ab/fit.h5


.. parsed-literal::

    



.. parsed-literal::

    Filename: /Users/Rui/Documents/Workspace/projects/GMaKE/gmake/model_eval.py
    
    Line #    Mem usage    Increment   Line Contents
    ================================================
       348   4518.4 MiB   4518.4 MiB   def model_lnprob(theta,fit_dct,inp_dct,dat_dct,
       349                                              savemodel=None,decomp=False,nsamps=1e5,
       350                                              packblobs=False,
       351                                              verbose=False):
       352                                 """
       353                                 this is the evaluating function for emcee
       354                                 packblobs=True:
       355                                     lnl,blobs
       356                                 packblobs=False:
       357                                     lnl,lnp,chisq,ndata,npar
       358                                 """
       359                             
       360   4518.4 MiB      0.0 MiB       if  verbose==True:
       361                                     start_time = time.time()
       362                                     
       363   4518.4 MiB      0.0 MiB       lp = model_lnprior(theta,fit_dct)
       364                                 
       365   4518.4 MiB      0.0 MiB       if  not np.isfinite(lp):
       366                                     blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
       367                                     if  packblobs==True:
       368                                         return -np.inf,blobs
       369                                     else:
       370                                         return -np.inf,-np.inf,+np.inf,0.0,len(theta)
       371                             
       372                                  
       373                                          
       374   4518.4 MiB      0.0 MiB       lnl,blobs=model_lnlike2(theta,fit_dct,inp_dct,dat_dct,
       375   4518.4 MiB      0.0 MiB                              savemodel=savemodel,decomp=decomp,nsamps=nsamps,
       376   4518.4 MiB      0.0 MiB                              verbose=verbose)
       377                                 
       378   4518.4 MiB      0.0 MiB       if  verbose==True:
       379                                     print("try ->",theta)
       380                                     print("---{0:^10} : {1:<8.5f} seconds ---".format('lnprob',time.time()-start_time))    
       381                                 
       382                                 # np.array: to creat a zero-d object array 
       383   4518.4 MiB      0.0 MiB       if  packblobs==True:
       384                                     return lp+lnl,blobs
       385                                 else:
       386   4518.4 MiB      0.0 MiB           return lp+lnl,blobs['lnprob'],blobs['chisq'],blobs['ndata'],blobs['npar']


.. code:: ipython3

    #%mprun -f gmake.model_eval.model_lnprob lnl,lnprob,chisq,ndata,npar=gmake.model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,savemodel=None)
    %timeit lnl,lnprob,chisq,ndata,npar=gmake.model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,savemodel=None)


.. parsed-literal::

    3.96 s ± 65.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)



.. code:: ipython3

    #from hickle import SerializedWarning
    %matplotlib inline
    #%matplotlib notebook
    gmake.fit_analyze(inpfile,export=True)
    #print(fit_dct['p_scale'])


.. parsed-literal::

    --- save to: bx610_b4c5_uv_ab/fit.h5
    Check optimized parameters:
     0   vsys@basics       =    104.63      <-    100.00      (     0.00     ,     220.00     )
     1   disk_sd@diskdyn   =    3194.29     <-    3000.00     (    100.00    ,    50000.00    )
     2   disk_rs@diskdyn   =     2.78       <-     2.00       (     0.20     ,      10.00     )
     3   vdis@basics       =     50.43      <-     50.00      (     0.00     ,     200.00     )
     4   pa@basics         =    -54.23      <-    -52.40      (    -132.40   ,      27.60     )
     5   inc@basics        =     46.25      <-     44.06      (     5.00     ,      85.00     )
     6   xypos.ra@basics   =  356.5393221   <-  356.5393258   (  356.5390481 ,   356.5396036  )
     7   xypos.dec@basics  =  12.8220133    <-  12.8220182    (  12.8217404  ,   12.8222960   )
     8   lineflux@co43     =     1.08       <-     1.00       (     0.10     ,     200.00     )
     9   sbser[0]@co43     =     0.21       <-     0.22       (     0.01     ,      2.00      )
     10  lineflux@ci10     =     0.49       <-     0.50       (     0.10     ,     200.00     )
     11  sbser[0]@ci10     =     0.27       <-     0.19       (     0.01     ,      2.00      )
     12  contflux@cont     =     0.00       <-     0.00       (     0.00     ,      0.01      )
     13  sbser[0]@cont     =     0.18       <-     0.15       (     0.01     ,      2.00      )
     14  alpha@cont        =     3.79       <-     3.72       (     3.00     ,      4.50      )
    analyzing outfolder:bx610_b4c5_uv_ab
    plotting...bx610_b4c5_uv_ab/iteration.pdf
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 125111663.73342288 35301632
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 168486213.07584742 49426196
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 1118139.3760106005 275794
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 1161359.330965863 275794
    data@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs 1157667.521734547 276124
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 1205064.410572111 276124
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 1156301.2026866334 276124
    data@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs 1160934.690953595 276124
    export the model set:              bx610_b4c5_uv_ab/model_0              (may take some time..)
     
    -->data_b4c5_bb1.ms.pt2
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to bx610_b4c5_uv_ab/model_0/imod2d_b4c5_bb1.ms.pt2.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to bx610_b4c5_uv_ab/model_0/imod3d_b4c5_bb1.ms.pt2.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to bx610_b4c5_uv_ab/model_0/pbeam_b4c5_bb1.ms.pt2.fits
    write reference model profile: 
        imod3d_prof@co43@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to bx610_b4c5_uv_ab/model_0/imodrp_co43_b4c5_bb1.ms.pt2.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2  to  bx610_b4c5_uv_ab/model_0/model_b4c5_bb1.ms.pt2
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to data@bx610_b4c5_uv_ab/model_0/model_b4c5_bb1.ms.pt2
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb1.ms.pt2  to  bx610_b4c5_uv_ab/model_0/data_b4c5_bb1.ms.pt2
     
    -->data_b4c5_bb3.ms.pt2
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to bx610_b4c5_uv_ab/model_0/imod2d_b4c5_bb3.ms.pt2.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to bx610_b4c5_uv_ab/model_0/imod3d_b4c5_bb3.ms.pt2.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to bx610_b4c5_uv_ab/model_0/pbeam_b4c5_bb3.ms.pt2.fits
    write reference model profile: 
        imod3d_prof@ci10@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to bx610_b4c5_uv_ab/model_0/imodrp_ci10_b4c5_bb3.ms.pt2.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2  to  bx610_b4c5_uv_ab/model_0/model_b4c5_bb3.ms.pt2
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to data@bx610_b4c5_uv_ab/model_0/model_b4c5_bb3.ms.pt2
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb3.ms.pt2  to  bx610_b4c5_uv_ab/model_0/data_b4c5_bb3.ms.pt2
     
    -->data_b4c5_bb1.ms.pt1
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 to bx610_b4c5_uv_ab/model_0/imod2d_b4c5_bb1.ms.pt1.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 to bx610_b4c5_uv_ab/model_0/imod3d_b4c5_bb1.ms.pt1.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 to bx610_b4c5_uv_ab/model_0/pbeam_b4c5_bb1.ms.pt1.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1  to  bx610_b4c5_uv_ab/model_0/model_b4c5_bb1.ms.pt1
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 to data@bx610_b4c5_uv_ab/model_0/model_b4c5_bb1.ms.pt1
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb1.ms.pt1  to  bx610_b4c5_uv_ab/model_0/data_b4c5_bb1.ms.pt1
     
    -->data_b4c5_bb1.ms.pt3
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 to bx610_b4c5_uv_ab/model_0/imod2d_b4c5_bb1.ms.pt3.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 to bx610_b4c5_uv_ab/model_0/imod3d_b4c5_bb1.ms.pt3.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 to bx610_b4c5_uv_ab/model_0/pbeam_b4c5_bb1.ms.pt3.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3  to  bx610_b4c5_uv_ab/model_0/model_b4c5_bb1.ms.pt3
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 to data@bx610_b4c5_uv_ab/model_0/model_b4c5_bb1.ms.pt3
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb1.ms.pt3  to  bx610_b4c5_uv_ab/model_0/data_b4c5_bb1.ms.pt3
     
    -->data_b4c5_bb2.ms.mfs
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs to bx610_b4c5_uv_ab/model_0/imod2d_b4c5_bb2.ms.mfs.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs to bx610_b4c5_uv_ab/model_0/imod3d_b4c5_bb2.ms.mfs.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs to bx610_b4c5_uv_ab/model_0/pbeam_b4c5_bb2.ms.mfs.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs  to  bx610_b4c5_uv_ab/model_0/model_b4c5_bb2.ms.mfs
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs to data@bx610_b4c5_uv_ab/model_0/model_b4c5_bb2.ms.mfs
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb2.ms.mfs  to  bx610_b4c5_uv_ab/model_0/data_b4c5_bb2.ms.mfs
     
    -->data_b4c5_bb3.ms.pt1
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 to bx610_b4c5_uv_ab/model_0/imod2d_b4c5_bb3.ms.pt1.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 to bx610_b4c5_uv_ab/model_0/imod3d_b4c5_bb3.ms.pt1.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 to bx610_b4c5_uv_ab/model_0/pbeam_b4c5_bb3.ms.pt1.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1  to  bx610_b4c5_uv_ab/model_0/model_b4c5_bb3.ms.pt1
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 to data@bx610_b4c5_uv_ab/model_0/model_b4c5_bb3.ms.pt1
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb3.ms.pt1  to  bx610_b4c5_uv_ab/model_0/data_b4c5_bb3.ms.pt1
     
    -->data_b4c5_bb3.ms.pt3
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 to bx610_b4c5_uv_ab/model_0/imod2d_b4c5_bb3.ms.pt3.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 to bx610_b4c5_uv_ab/model_0/imod3d_b4c5_bb3.ms.pt3.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 to bx610_b4c5_uv_ab/model_0/pbeam_b4c5_bb3.ms.pt3.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3  to  bx610_b4c5_uv_ab/model_0/model_b4c5_bb3.ms.pt3
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 to data@bx610_b4c5_uv_ab/model_0/model_b4c5_bb3.ms.pt3
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb3.ms.pt3  to  bx610_b4c5_uv_ab/model_0/data_b4c5_bb3.ms.pt3
     
    -->data_b4c5_bb4.ms.mfs
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs to bx610_b4c5_uv_ab/model_0/imod2d_b4c5_bb4.ms.mfs.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs to bx610_b4c5_uv_ab/model_0/imod3d_b4c5_bb4.ms.mfs.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs to bx610_b4c5_uv_ab/model_0/pbeam_b4c5_bb4.ms.mfs.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs  to  bx610_b4c5_uv_ab/model_0/model_b4c5_bb4.ms.mfs
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs to data@bx610_b4c5_uv_ab/model_0/model_b4c5_bb4.ms.mfs
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb4.ms.mfs  to  bx610_b4c5_uv_ab/model_0/data_b4c5_bb4.ms.mfs
    --------------------------------------------------------------------------------
    --- took 29.00081 seconds ---
    --- save to: bx610_b4c5_uv_ab/model_0/models.h5
    save the model input parameter: bx610_b4c5_uv_ab/model_0/model.inp
    model_0: 
    {'chisq': 300557343.3421936,
     'lnprob': 8519061.630641665,
     'ndata': 86383912.0,
     'npar': 15}
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 125111592.61012563 35301632
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 168486258.64972007 49426196
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 1118138.674951935 275794
    data@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 1161366.5592344531 275794
    data@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs 1157663.9855508006 276124
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 1205062.388948932 276124
    data@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 1156303.2738797683 276124
    data@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs 1160942.1459157672 276124
    export the model set:              bx610_b4c5_uv_ab/model_1              (may take some time..)
     
    -->data_b4c5_bb1.ms.pt2
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to bx610_b4c5_uv_ab/model_1/imod2d_b4c5_bb1.ms.pt2.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to bx610_b4c5_uv_ab/model_1/imod3d_b4c5_bb1.ms.pt2.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to bx610_b4c5_uv_ab/model_1/pbeam_b4c5_bb1.ms.pt2.fits
    write reference model profile: 
        imod3d_prof@co43@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to bx610_b4c5_uv_ab/model_1/imodrp_co43_b4c5_bb1.ms.pt2.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2  to  bx610_b4c5_uv_ab/model_1/model_b4c5_bb1.ms.pt2
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt2 to data@bx610_b4c5_uv_ab/model_1/model_b4c5_bb1.ms.pt2
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb1.ms.pt2  to  bx610_b4c5_uv_ab/model_1/data_b4c5_bb1.ms.pt2
     
    -->data_b4c5_bb3.ms.pt2
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to bx610_b4c5_uv_ab/model_1/imod2d_b4c5_bb3.ms.pt2.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to bx610_b4c5_uv_ab/model_1/imod3d_b4c5_bb3.ms.pt2.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to bx610_b4c5_uv_ab/model_1/pbeam_b4c5_bb3.ms.pt2.fits
    write reference model profile: 
        imod3d_prof@ci10@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to bx610_b4c5_uv_ab/model_1/imodrp_ci10_b4c5_bb3.ms.pt2.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2  to  bx610_b4c5_uv_ab/model_1/model_b4c5_bb3.ms.pt2
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt2 to data@bx610_b4c5_uv_ab/model_1/model_b4c5_bb3.ms.pt2
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb3.ms.pt2  to  bx610_b4c5_uv_ab/model_1/data_b4c5_bb3.ms.pt2
     
    -->data_b4c5_bb1.ms.pt1
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 to bx610_b4c5_uv_ab/model_1/imod2d_b4c5_bb1.ms.pt1.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 to bx610_b4c5_uv_ab/model_1/imod3d_b4c5_bb1.ms.pt1.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 to bx610_b4c5_uv_ab/model_1/pbeam_b4c5_bb1.ms.pt1.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1  to  bx610_b4c5_uv_ab/model_1/model_b4c5_bb1.ms.pt1
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt1 to data@bx610_b4c5_uv_ab/model_1/model_b4c5_bb1.ms.pt1
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb1.ms.pt1  to  bx610_b4c5_uv_ab/model_1/data_b4c5_bb1.ms.pt1
     
    -->data_b4c5_bb1.ms.pt3
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 to bx610_b4c5_uv_ab/model_1/imod2d_b4c5_bb1.ms.pt3.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 to bx610_b4c5_uv_ab/model_1/imod3d_b4c5_bb1.ms.pt3.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 to bx610_b4c5_uv_ab/model_1/pbeam_b4c5_bb1.ms.pt3.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3  to  bx610_b4c5_uv_ab/model_1/model_b4c5_bb1.ms.pt3
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb1.ms.pt3 to data@bx610_b4c5_uv_ab/model_1/model_b4c5_bb1.ms.pt3
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb1.ms.pt3  to  bx610_b4c5_uv_ab/model_1/data_b4c5_bb1.ms.pt3
     
    -->data_b4c5_bb2.ms.mfs
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs to bx610_b4c5_uv_ab/model_1/imod2d_b4c5_bb2.ms.mfs.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs to bx610_b4c5_uv_ab/model_1/imod3d_b4c5_bb2.ms.mfs.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs to bx610_b4c5_uv_ab/model_1/pbeam_b4c5_bb2.ms.mfs.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs  to  bx610_b4c5_uv_ab/model_1/model_b4c5_bb2.ms.mfs
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs to data@bx610_b4c5_uv_ab/model_1/model_b4c5_bb2.ms.mfs
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb2.ms.mfs  to  bx610_b4c5_uv_ab/model_1/data_b4c5_bb2.ms.mfs
     
    -->data_b4c5_bb3.ms.pt1
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 to bx610_b4c5_uv_ab/model_1/imod2d_b4c5_bb3.ms.pt1.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 to bx610_b4c5_uv_ab/model_1/imod3d_b4c5_bb3.ms.pt1.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 to bx610_b4c5_uv_ab/model_1/pbeam_b4c5_bb3.ms.pt1.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1  to  bx610_b4c5_uv_ab/model_1/model_b4c5_bb3.ms.pt1
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt1 to data@bx610_b4c5_uv_ab/model_1/model_b4c5_bb3.ms.pt1
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb3.ms.pt1  to  bx610_b4c5_uv_ab/model_1/data_b4c5_bb3.ms.pt1
     
    -->data_b4c5_bb3.ms.pt3
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 to bx610_b4c5_uv_ab/model_1/imod2d_b4c5_bb3.ms.pt3.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 to bx610_b4c5_uv_ab/model_1/imod3d_b4c5_bb3.ms.pt3.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 to bx610_b4c5_uv_ab/model_1/pbeam_b4c5_bb3.ms.pt3.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3  to  bx610_b4c5_uv_ab/model_1/model_b4c5_bb3.ms.pt3
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb3.ms.pt3 to data@bx610_b4c5_uv_ab/model_1/model_b4c5_bb3.ms.pt3
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb3.ms.pt3  to  bx610_b4c5_uv_ab/model_1/data_b4c5_bb3.ms.pt3
     
    -->data_b4c5_bb4.ms.mfs
     
    imod2d@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs
    write reference model image: 
        imod2d@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs to bx610_b4c5_uv_ab/model_1/imod2d_b4c5_bb4.ms.mfs.fits
    imod3d@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs
    write reference model image: 
        imod3d@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs to bx610_b4c5_uv_ab/model_1/imod3d_b4c5_bb4.ms.mfs.fits
    pbeam@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs
    write reference model image: 
        pbeam@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs to bx610_b4c5_uv_ab/model_1/pbeam_b4c5_bb4.ms.mfs.fits
    copy ms container: 
        ../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs  to  bx610_b4c5_uv_ab/model_1/model_b4c5_bb4.ms.mfs
    write ms column: 
        uvmodel@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs to data@bx610_b4c5_uv_ab/model_1/model_b4c5_bb4.ms.mfs
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/bb4.ms.mfs  to  bx610_b4c5_uv_ab/model_1/data_b4c5_bb4.ms.mfs
    --------------------------------------------------------------------------------
    --- took 30.39432 seconds ---
    --- save to: bx610_b4c5_uv_ab/model_1/models.h5
    save the model input parameter: bx610_b4c5_uv_ab/model_1/model.inp
    model_1: 
    {'chisq': 300557328.28832734,
     'lnprob': 8519069.157574806,
     'ndata': 86383912.0,
     'npar': 15}



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>


.. code:: ipython3

    models=gmake.hdf2dct(inp_dct['general']['outdir']+'/model_1/models.h5')
    #gmake.pprint(models['mod_dct']['co43'])
    gmake.model_vrot_plot(models['mod_dct']['co43'])



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_b4c5_uv_ab_files/demo_bx610_b4c5_uv_ab_9_1.png



.. code:: ipython3

    from galario.single import sampleImage
    from galario.single import chi2Image
    import numexpr as ne
    import numpy as np
    def method_sampleImage(dat_dct):
        xymodel=np.ones((512,512),dtype=np.float32)
        data=dat_dct['data@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs']
    
        uvw=dat_dct['uvw@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs']
        weight=dat_dct['weight@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs']
        wv=np.mean(dat_dct['chanfreq@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs'])
        uvmodel=sampleImage(xymodel,np.deg2rad(0.007/60./60.).astype(np.float32),
                            (uvw[:,0]/wv),(uvw[:,1]/wv),
                            dRA=0,dDec=0,PA=0.,check=False,origin='lower')
        #print(uvmodel[:,np.newaxis].shape)
        #print(data.shape)
        #print(weight[:,np.newaxis].shape)
        chi2=ne.evaluate('sum(((a.real-b.real)**2.0+(a.imag-b.imag)**2)*c)',
                    local_dict={'a':data,
                                'b':uvmodel[:,np.newaxis],
                                'c':weight[:,np.newaxis]})
        return chi2
    
    def method_chi2Image(dat_dct):
        xymodel=np.ones((512,512),dtype=np.float32,order='')
        data=dat_dct['data@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs']
        real=np.ascontiguousarray(data[:,0].real)
        imag=np.ascontiguousarray(data[:,0].imag)
        uvw=dat_dct['uvw@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs']
        weight=dat_dct['weight@../data/bx610/alma/2017.1.01045.S/bb2.ms.mfs']
        wv=np.mean(dat_dct['chanfreq@../data/bx610/alma/2017.1.01045.S/bb4.ms.mfs'])
        chi2=chi2Image(xymodel,np.deg2rad(0.007/60./60.).astype(np.float32),
                       uvw[:,0]/wv,uvw[:,1]/wv,
                       real,imag,weight,
                       dRA=0,dDec=0,PA=0.,check=False,origin='lower')
    
        return chi2
    
    #%lprun -f method_sampleImage chi2=method_sampleImage(dat_dct)
    #print(chi2)
    
    %timeit chi2=method_sampleImage(dat_dct)
    print(chi2)
    
    #%lprun -f method_chi2Image chi2=method_chi2Image(dat_dct)
    #print(chi2)
    
    #%timeit chi2=method_chi2Image(dat_dct)
    #print(chi2)


.. parsed-literal::

    9.41 ms ± 376 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    1.926698859779456e+21

