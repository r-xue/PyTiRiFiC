|Open In Colab|

Example BX610: perform model fitting using method=‘amoeba’ for the Band 6 Cycle 3 DataSet
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
    /Volumes/S1/projects/GMaKE/examples/output
    0.2.dev1
    rx.astro@gmail.com
    /Users/Rui/Documents/Workspace/projects/GMaKE/gmake
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    <Logger gmake (DEBUG)>
    [<FileHandler /Volumes/S1/projects/GMaKE/examples/output/bx610_b6c3_uv_ab/gmake.log (DEBUG)>, <StreamHandler stderr (DEBUG)>]


.. code:: ipython3

    dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True)


.. parsed-literal::

    read data (may take some time..)
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb2.ms
    
    data@../data/bx610/alma/2015.1.00250.S/bb2.ms                complex64       (56354, 238)         102 MiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb2.ms                 float32         (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb2.ms              float32         (56354,)             220 KiB             
      >>percentiles (0,16,50,84,100)%: [ 25.42425919 120.59348969 161.43834686 222.05312988 274.09368896]
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb2.ms            (238,)     250752859438.0543 Hz 252604264234.0391 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb2.ms           (238,)     7811834.5822 Hz 7811834.5822 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb2.ms         23h46m09.44s  12d49m19.3s
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb3.ms
    
    data@../data/bx610/alma/2015.1.00250.S/bb3.ms                complex64       (53466, 238)          97 MiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb3.ms                 float32         (53466, 3)           627 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb3.ms              float32         (53466,)             209 KiB             
      >>percentiles (0,16,50,84,100)%: [ 28.95802307 136.6611145  187.34054565 248.30665283 289.60601807]
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb3.ms            (238,)     233254349973.6942 Hz 235105754769.6790 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb3.ms           (238,)     -7811834.5822 Hz -7811834.5822 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb3.ms         23h46m09.44s  12d49m19.3s
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs
    
    data@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs            complex64       (56354, 1)           440 KiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs             float32         (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs          float32         (56354,)             220 KiB             
      >>percentiles (0,16,50,84,100)%: [ 5420.21582031 26262.67539063 35061.7265625  47476.43703125
     59263.3984375 ]
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs        (1,)       250073373567.0543 Hz 250073373567.0543 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs       (1,)       1859216630.5597 Hz 1859216630.5597 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs     23h46m09.44s  12d49m19.3s
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs
    
    data@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs            complex64       (56354, 1)           440 KiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs             float32         (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs          float32         (56354,)             220 KiB             
      >>percentiles (0,16,50,84,100)%: [ 7370.546875   35357.1671875  48239.16992188 64150.5290625
     75806.0703125 ]
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs        (1,)       235879907576.7765 Hz 235879907576.7765 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs       (1,)       -1859216630.5670 Hz -1859216630.5670 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs     23h46m09.44s  12d49m19.3s
    --------------------------------------------------------------------------------
    --- dat_dct size 203.68 Mibyte ---
    --- took 1.85573  seconds ---


.. code:: ipython3

    inp_dct=gmake.read_inp(inpfile)
    inp_dct=gmake.inp_validate(inp_dct)
    mod_dct=gmake.inp2mod(inp_dct)
    gmake.model_vrot(mod_dct)
    #mod_dct['co76']
    %mprun -f gmake.fit_setup fit_dct=gmake.fit_setup(inp_dct,dat_dct,initial_model=False)
    #gmake.model_lnlike2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct)
    
    #mod_dct=gmake.inp2mod(inp_dct)
    #gmake.pprint(mod_dct)
    #gmake.model_vrot(mod_dct)
    #gmake.pprint(mod_dct)
    #gmake.model_vrot_plot(mod_dct['co76'])


.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    optimizer: amoeba
    optimizing parameters:
    ----------------------------------------------------------------------------------------------------
    index    name    unit    start    lo_limit    up_limit    scale
     0   vsys@basics      km / s              117.50      (     0.00     ,     220.00     )    117.50     
     1   disk_sd@diskdyn  solMass / pc2       3000.00     (    100.00    ,    50000.00    )   47000.00    
     2   disk_rs@diskdyn  kpc                  5.00       (     0.20     ,      30.00     )     25.00     
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ndim:    3
    outdir:  bx610_b6c3_uv_ab
    --- save to: bx610_b6c3_uv_ab/fit.h5


.. parsed-literal::

    



.. parsed-literal::

    Filename: /Users/Rui/Documents/Workspace/projects/GMaKE/gmake/opt.py
    
    Line #    Mem usage    Increment   Line Contents
    ================================================
        24    529.8 MiB    529.8 MiB   def fit_setup(inp_dct,dat_dct,initial_model=False,save_model=False,copydata=False):
        25                                 """
        26                                 for method='emcee': sampler is an emcee object
        27                                 for method=others: sampler is a dict
        28                                 """
        29                             
        30    529.8 MiB      0.0 MiB       fit_dct=opt_setup(inp_dct,dat_dct)
        31                                 
        32    529.8 MiB      0.0 MiB       outfolder=fit_dct['outfolder']
        33                                 
        34    529.8 MiB      0.0 MiB       if  copydata==True:
        35                                 
        36                                     dat_dct_path=outfolder+'/data.h5'
        37                                     dct2hdf(dat_dct,outname=dat_dct_path)    
        38                                 
        39    529.8 MiB      0.0 MiB       if  initial_model==True:
        40                             
        41                                     start_time = time.time()
        42                                     if  save_model==True:
        43                                         lnl,lnprob,chisq,ndata,npar=model_lnprob2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
        44                                                                              savemodel=outfolder+'/model_0')
        45                                     else:
        46                                         lnl,lnprob,chisq,ndata,npar=model_lnprob2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
        47                                                                              savemodel=None)            
        48                                     #lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,packblobs=True,
        49                                     #                       savemodel='')     
        50                                     logger.debug("{0:50} : {1:<8.5f} seconds".format('one trial',time.time()-start_time))
        51                                     
        52                                     logger.debug('ndata->'+str(ndata))
        53                                     logger.debug('chisq->'+str(chisq))
        54                                     """
        55                                     lnl,blobs=model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,dat_dct,
        56                                                            savemodel=fit_dct['outfolder']+'/model_0')
        57                                     logger.debug('p_start:    ')
        58                                     logger.debug(pformat(blobs))
        59                                     """    
        60                             
        61    529.8 MiB      0.0 MiB       dct2hdf(fit_dct,outname=outfolder+'/fit.h5')
        62                             
        63    529.8 MiB      0.0 MiB       return fit_dct


.. code:: ipython3

    #%mprun -f gmake.model_dynamics.model_vrot gmake.model_lnlike2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct)
    #%memit gmake.model_lnlike2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct)
    %lprun -f gmake.model_lnlike2 gmake.model_lnlike2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct)
    #%mprun -f gmake.model_uvchi2 gmake.model_lnlike2(fit_dct['p_start'],fit_dct,inp_dct,dat_dct)
    #%lprun gmake.fit_iterate(fit_dct,inp_dct,dat_dct)


.. parsed-literal::

    imodel@../data/bx610/alma/2015.1.00250.S/bb2.ms 34430412.38956993
    imodel@../data/bx610/alma/2015.1.00250.S/bb3.ms 32123415.550489213
    imodel@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs 160324.93087314288
    imodel@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs 148850.44333369774



.. parsed-literal::

    Timer unit: 1e-06 s
    
    Total time: 1.83022 s
    File: /Users/Rui/Documents/Workspace/projects/GMaKE/gmake/model_eval.py
    Function: model_lnlike2 at line 23
    
    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
        23                                           def model_lnlike2(theta,fit_dct,inp_dct,dat_dct,
        24                                                            savemodel=None,decomp=False,nsamps=1e5,
        25                                                            returnwdev=False,
        26                                                            verbose=False,test_threading=False):
        27                                               """
        28                                               the likelihood function
        29                                               
        30                                                   step:    + fill the varying parameter into inp_dct
        31                                                            + convert inp_dct to mod_dct
        32                                                            + use mod_dct to regenerate RC
        33                                               """
        34                                           
        35                                               
        36         1          2.0      2.0      0.0      blobs={'lnprob':0.0,
        37         1          1.0      1.0      0.0             'chisq':0.0,
        38         1          0.0      0.0      0.0             'ndata':0.0,
        39         1          8.0      8.0      0.0             'wdev':np.array([]),
        40         1          1.0      1.0      0.0             'npar':len(theta)}
        41         1          1.0      1.0      0.0      if  returnwdev==False:
        42         1          2.0      2.0      0.0          del blobs['wdev']
        43                                           
        44                                               #models_size=human_unit(get_obj_size(fit_dct)*u.byte)
        45                                               #logger.info("before models size {:0.2f} ---".format(models_size))
        46                                               #models_size=human_unit(get_obj_size(inp_dct)*u.byte)
        47                                               #logger.info("before models size {:0.2f} ---".format(models_size))    
        48                                               
        49                                           
        50                                               
        51                                               """
        52                                               if  test_threading==True:
        53                                                   #   don't actually calculate model
        54                                                   #   used for testing threading overheads.
        55                                                   x=dat_dct       
        56                                                   t = time.time() + np.random.uniform(0.1, 0.2)
        57                                                   while True:
        58                                                       if time.time() >= t:
        59                                                           break
        60                                                   return 0.0,blobs
        61                                               """
        62                                               
        63         1       1377.0   1377.0      0.1      inp_dct0=deepcopy(inp_dct)
        64                                           
        65                                                   
        66         4          7.0      1.8      0.0      for ind in range(len(fit_dct['p_name'])):
        67                                                   #print(fit_dct['p_name'][ind],theta[ind],fit_dct['p_unit'][ind],type(fit_dct['p_unit'][ind]))
        68         3        173.0     57.7      0.0          write_par(inp_dct0,fit_dct['p_name'][ind],theta[ind]*fit_dct['p_unit'][ind],verbose=False)
        69                                               
        70                                            
        71                                                   
        72                                               #tic0=time.time()
        73         1       1712.0   1712.0      0.1      mod_dct=inp2mod(inp_dct0)   # in physical units
        74         1       9976.0   9976.0      0.5      model_vrot(mod_dct)         # in natural (default internal units)
        75                                               #print('Took {0} second on inp2mod'.format(float(time.time()-tic0))) 
        76                                           
        77                                           
        78         1          2.0      2.0      0.0      if  test_threading==True:
        79                                                   #   don't actually calculate model
        80                                                   #   used for testing threading overheads.
        81                                                   x=dat_dct       
        82                                                   t = time.time() + np.random.uniform(1.1, 1.2)
        83                                                   while True:
        84                                                       if time.time() >= t:
        85                                                           break
        86                                                   return 0.0,blobs         
        87                                                   
        88                                               
        89                                               #tic0=time.time()
        90                                               #models=gmake_kinmspy_api(mod_dct,dat_dct=dat_dct)
        91                                           
        92                                               #if  savemodel is not None:
        93                                               #    nsamps=nsamps*10
        94                                           
        95                                               #print('before',process.memory_info().rss/1024/1024)
        96                                               #logger.info("before models size {:0.2f} ---".format(models_size))    
        97                                                
        98         1      33106.0  33106.0      1.8      models=model_init2(mod_dct,dat_dct,decomp=decomp,verbose=verbose)
        99         1      15094.0  15094.0      0.8      models_size=human_unit(get_obj_size(models)*u.byte)
       100                                           
       101                                                  
       102         1     237395.0 237395.0     13.0      model_fill2(models,decomp=decomp,nsamps=nsamps,verbose=verbose)
       103                                               
       104                                               #print('before',process.memory_info().rss/1024/1024)
       105                                                 
       106                                               
       107                                               #models_size=human_unit(get_obj_size(models)*u.byte)
       108                                               #logger.info("--- models size {:0.2f} ---".format(models_size))      
       109                                               
       110                                               #models_size=human_unit(get_obj_size(models)*u.byte)
       111                                               #logger.info("before models size {:0.2f} ---".format(models_size))
       112                                               #for key in models:
       113                                               #    print(key,get_obj_size(models[key])/1024/1024)    
       114                                               
       115                                           
       116                                           
       117                                               
       118                                               
       119                                               #print(get_obj_size(models))
       120                                               #print(blobs['lnprob'])
       121                                               #models_size=human_unit(get_obj_size(models)*u.byte)
       122                                               #logger.info("after models size {:0.2f} ---".format(models_size))    
       123                                               
       124                                           
       125                                                   
       126                                               
       127                                               #models_size=human_unit(get_obj_size(models)*u.byte)
       128                                               #logger.info("--- models size {:0.2f} ---".format(models_size))
       129                                               
       130                                           
       131                                               
       132                                                   
       133                                               #for key in models:
       134                                               #    print(key,get_obj_size(models[key])/1024/1024)
       135                                                   
       136        21         28.0      1.3      0.0      for tag in list(models.keys()):
       137                                                   
       138        20         22.0      1.1      0.0          if  'imodel@' in tag:
       139                                                       
       140         4          9.0      2.2      0.0              if  models[tag.replace('imodel@','type@')]=='vis':
       141                                                           #print(models[tag])
       142         4          7.0      1.8      0.0                  chi2=model_uvchi2(models[tag],#*models[tag.replace('imod3d@','pbeam@')],
       143                                                                                #models[tag.replace('imod3d@','imod2d@')],#*models[tag.replace('imod3d@','pbeam@')],
       144         4          4.0      1.0      0.0                                       models[tag.replace('imodel@','header@')],
       145         4          7.0      1.8      0.0                                       dat_dct[tag.replace('imodel@','data@')],
       146         4          6.0      1.5      0.0                                       dat_dct[tag.replace('imodel@','uvw@')],
       147         4          5.0      1.2      0.0                                       dat_dct[tag.replace('imodel@','phasecenter@')],
       148         4          4.0      1.0      0.0                                       dat_dct[tag.replace('imodel@','weight@')],
       149         4          3.0      0.8      0.0                                       average=True,
       150         4    1528166.0 382041.5     83.5                                       verbose=verbose)
       151                                                           #print(chi2)
       152         4         10.0      2.5      0.0                  blobs['chisq']+=chi2
       153         4       3094.0    773.5      0.2                  logger.debug("{0} {1}".format(tag,chi2))
       154                                               
       155         1          1.0      1.0      0.0      lnl=blobs['lnprob']
       156                                               #print('after',process.memory_info().rss/1024/1024)
       157                                               #logger.debug("{0} {1}".format('-->',blobs['chisq']))
       158         1          1.0      1.0      0.0      return lnl,blobs


.. code:: ipython3

    inp_dct=gmake.read_inp(inpfile)
    inp_dct=gmake.inp_validate(inp_dct)
    mod_dct=gmake.inp2mod(inp_dct)
    gmake.model_vrot(mod_dct)
    #mod_dct['co76']
    fit_dct=gmake.fit_setup(inp_dct,dat_dct,initial_model=True)
    gmake.fit_iterate(fit_dct,inp_dct,dat_dct)


.. parsed-literal::

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    optimizer: amoeba
    optimizing parameters:
    ----------------------------------------------------------------------------------------------------
    index    name    unit    start    lo_limit    up_limit    scale
     0   vsys@basics      km / s              117.50      (     0.00     ,     220.00     )    117.50     
     1   disk_sd@diskdyn  solMass / pc2       3000.00     (    100.00    ,    50000.00    )   47000.00    
     2   disk_rs@diskdyn  kpc                  5.00       (     0.20     ,      30.00     )     25.00     
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ndim:    3
    outdir:  bx610_b6c3_uv_ab
    --> 66862999.715953484
    one trial                                          : 1.53849  seconds
    ndata->0.0
    chisq->66862999.715953484
    --- save to: bx610_b6c3_uv_ab/fit.h5
     
    Running AMOEBA...
    >>bx610_b6c3_uv_ab/amoeba_chain.h5
     
    --> 66863006.92562753
    --> 66862422.22514197
    --> 66862158.710540414
         0   66862159        inf


.. parsed-literal::

    /Users/Rui/Documents/Workspace/projects/GMaKE/gmake/opt_amoeba.py:284: RuntimeWarning: invalid value encountered in double_scalars
      rtol=2.0*np.abs(y[ihi]-y[ilo])/d
    


.. parsed-literal::

    --> 66862706.98227224
         1   66862159   66863007


::


    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-57-ddceeea01f29> in <module>
          5 #mod_dct['co76']
          6 fit_dct=gmake.fit_setup(inp_dct,dat_dct,initial_model=True)
    ----> 7 gmake.fit_iterate(fit_dct,inp_dct,dat_dct)
    

    ~/Documents/Workspace/projects/GMaKE/gmake/opt.py in fit_iterate(fit_dct, inp_dct, dat_dct)
        226 
        227     if  'amoeba' in fit_dct['method']:
    --> 228         amoeba_iterate(fit_dct,inp_dct,dat_dct,nstep=inp_dct['optimize']['niter'])
        229         return
        230     if  'emcee' in fit_dct['method']:


    ~/Documents/Workspace/projects/GMaKE/gmake/opt_amoeba.py in amoeba_iterate(fit_dct, inp_dct, dat_dct, nstep)
         36                        funcargs={'fit_dct':fit_dct,'inp_dct':inp_dct,'dat_dct':dat_dct},
         37                        ftol=1e-10,temperature=0,
    ---> 38                        maxiter=nstep,verbose=True)
         39     #lnl,blobs=model_lnlike(p_amoeba['p_best'],fit_dct,inp_dct,dat_dct)
         40     #p_amoeba['blobs']=blobs


    ~/Documents/Workspace/projects/GMaKE/gmake/opt_amoeba.py in amoeba_sa(func, p0, scale, p_lo, p_up, funcargs, ftol, maxiter, temperature, format_prec, verbose)
        295                        temperature=temperature,
        296                        p_up=p_up,p_lo=p_lo,
    --> 297                        pars=pars,chi2=chi2,funcargs=funcargs)
        298         #print '<-',psum
        299         if  ytry<=y[ilo]:


    ~/Documents/Workspace/projects/GMaKE/gmake/opt_amoeba.py in amotry_sa(func, p, psum, ihi, fac, y, temperature, p_up, p_lo, pars, chi2, funcargs)
        350     ptry=np.maximum(np.minimum(psum*fac1-p[:,ihi]*fac2,p_up),p_lo)
        351 
    --> 352     ytry=func(ptry,**funcargs)
        353 
        354 


    ~/Documents/Workspace/projects/GMaKE/gmake/model_eval.py in model_chisq2(theta, fit_dct, inp_dct, dat_dct, savemodel, verbose)
        623         return +np.inf
        624 
    --> 625     lnl,blobs=model_lnlike2(theta,fit_dct,inp_dct,dat_dct,savemodel=savemodel)
        626 
        627     if  verbose==True:


    ~/Documents/Workspace/projects/GMaKE/gmake/model_eval.py in model_lnlike2(theta, fit_dct, inp_dct, dat_dct, savemodel, decomp, nsamps, returnwdev, verbose, test_threading)
        148                                      dat_dct[tag.replace('imodel@','weight@')],
        149                                      average=True,
    --> 150                                      verbose=verbose)
        151                 #print(chi2)
        152                 blobs['chisq']+=chi2


    ~/Documents/Workspace/projects/GMaKE/gmake/model_func.py in model_uvchi2(xymod3d, xyheader, uvdata, uvw, phasecenter, uvweight, average, verbose)
       1172                                                         dRA=dRA.astype(np.float32),dDec=dDec.astype(np.float32),
       1173                                                         PA=0.,check=False,origin='lower'),
    -> 1174                                              'b':uvdata[:,i]})
       1175                 chi2+=ne.evaluate('sum( ( (a.real)**2+(a.imag)**2 ) *c)',
       1176                                  local_dict={'a':delta_uv,


    ~/Library/Python/3.7/lib/python/site-packages/numexpr/necompiler.py in evaluate(ex, local_dict, global_dict, out, order, casting, **kwargs)
        811         raise ValueError("must specify expression as a string")
        812     # Get the names for this expression
    --> 813     context = getContext(kwargs, frame_depth=1)
        814     expr_key = (ex, tuple(sorted(context.items())))
        815     if expr_key not in _names_cache:


    ~/Library/Python/3.7/lib/python/site-packages/numexpr/necompiler.py in getContext(kwargs, frame_depth)
        539         value = d.pop(name, default)
        540         if value in allowed:
    --> 541             context[name] = value
        542         else:
        543             raise ValueError("'%s' must be one of %s" % (name, allowed))


    KeyboardInterrupt: 


.. code:: ipython3

    #from hickle import SerializedWarning
    %matplotlib inline
    #%matplotlib notebook
    gmake.fit_analyze(inpfile,export=True)
    #print(fit_dct['p_scale'])


.. parsed-literal::

    --- save to: bx610_b6c3_uv_ab/fit.h5
    Check optimized parameters:
     0   vsys@basics       =    117.50      <-    117.50      (     0.00     ,     220.00     )
     1   disk_sd@diskdyn   =    3000.00     <-    3000.00     (    100.00    ,    50000.00    )
     2   disk_rs@diskdyn   =     5.00       <-     5.00       (     0.20     ,      30.00     )
     3   vdis@basics       =     50.00      <-     50.00      (     0.00     ,     200.00     )
     4   pa@basics         =    -52.40      <-    -52.40      (    -132.40   ,      27.60     )
     5   inc@basics        =     44.06      <-     44.06      (     5.00     ,      85.00     )
     6   xypos.ra@basics   =  356.5393258   <-  356.5393258   (  356.5390481 ,   356.5396036  )
     7   xypos.dec@basics  =  12.8220182    <-  12.8220182    (  12.8217404  ,   12.8222960   )
     8   lineflux@co76     =     1.30       <-     1.30       (     0.10     ,     200.00     )
     9   sbser[0]@co76     =     0.22       <-     0.22       (     0.01     ,      2.00      )
     10  lineflux@ci21     =     0.65       <-     0.65       (     0.10     ,     200.00     )
     11  sbser[0]@ci21     =     0.19       <-     0.19       (     0.01     ,      2.00      )
     12  lineflux@h2o      =     0.32       <-     0.32       (     0.10     ,     200.00     )
     13  sbser[0]@h2o      =     0.17       <-     0.17       (     0.01     ,      2.00      )
     14  contflux@cont     =     0.00       <-     0.00       (     0.00     ,      0.01      )
     15  sbser[0]@cont     =     0.12       <-     0.12       (     0.01     ,      2.00      )
     16  alpha@cont        =     3.72       <-     3.72       (     3.00     ,      4.50      )
    analyzing outfolder:bx610_b6c3_uv_ab
    plotting...bx610_b6c3_uv_ab/iteration.pdf
    read data (may take some time..)
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb2.ms
    
    data@../data/bx610/alma/2015.1.00250.S/bb2.ms                complex64       (56354, 238)         102 MiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb2.ms                 float32         (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb2.ms              float32         (56354,)             220 KiB             
      >>percentiles (0,16,50,84,100)%: [ 25.42425919 120.59348969 161.43834686 222.05312988 274.09368896]
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb2.ms            (238,)     250752859438.0543 Hz 252604264234.0391 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb2.ms           (238,)     7811834.5822 Hz 7811834.5822 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb2.ms         23h46m09.44s  12d49m19.3s
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb3.ms
    
    data@../data/bx610/alma/2015.1.00250.S/bb3.ms                complex64       (53466, 238)          97 MiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb3.ms                 float32         (53466, 3)           627 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb3.ms              float32         (53466,)             209 KiB             
      >>percentiles (0,16,50,84,100)%: [ 28.95802307 136.6611145  187.34054565 248.30665283 289.60601807]
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb3.ms            (238,)     233254349973.6942 Hz 235105754769.6790 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb3.ms           (238,)     -7811834.5822 Hz -7811834.5822 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb3.ms         23h46m09.44s  12d49m19.3s
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs
    
    data@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs            complex64       (56354, 1)           440 KiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs             float32         (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs          float32         (56354,)             220 KiB             
      >>percentiles (0,16,50,84,100)%: [ 5420.21582031 26262.67539063 35061.7265625  47476.43703125
     59263.3984375 ]
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs        (1,)       250073373567.0543 Hz 250073373567.0543 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs       (1,)       1859216630.5597 Hz 1859216630.5597 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs     23h46m09.44s  12d49m19.3s
    
    Read: ../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs
    
    data@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs            complex64       (56354, 1)           440 KiB             
    uvw@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs             float32         (56354, 3)           661 KiB             
    weight@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs          float32         (56354,)             220 KiB             
      >>percentiles (0,16,50,84,100)%: [ 7370.546875   35357.1671875  48239.16992188 64150.5290625
     75806.0703125 ]
    chanfreq@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs        (1,)       235879907576.7765 Hz 235879907576.7765 Hz
    chanwidth@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs       (1,)       -1859216630.5670 Hz -1859216630.5670 Hz
    phasecenter@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs     23h46m09.44s  12d49m19.3s
    --------------------------------------------------------------------------------
    --- dat_dct size 203.68 Mibyte ---
    --- took 2.25172  seconds ---
    --- save to: bx610_b6c3_uv_ab/data.h5
    data@../data/bx610/alma/2015.1.00250.S/bb2.ms 34423407.26352863 13412252
    data@../data/bx610/alma/2015.1.00250.S/bb3.ms 32120841.42345846 12724908
    data@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs 160325.06165286465 56354
    data@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs 148848.5579627467 56354
    export the model set:              bx610_b6c3_uv_ab/model_0              (may take some time..)
     
    -->data_b6c3_bb2.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/imod2d_b6c3_bb2.ms.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/imod3d_b6c3_bb2.ms.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/pbeam_b6c3_bb2.ms.fits
    write reference model profile: 
        imod3d_prof@co76@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/imodrp_co76_b6c3_bb2.ms.fits
    write reference model profile: 
        imod3d_prof@ci21@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_0/imodrp_ci21_b6c3_bb2.ms.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb2.ms  to  bx610_b6c3_uv_ab/model_0/model_b6c3_bb2.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb2.ms to data@bx610_b6c3_uv_ab/model_0/model_b6c3_bb2.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb2.ms  to  bx610_b6c3_uv_ab/model_0/data_b6c3_bb2.ms
     
    -->data_b6c3_bb3.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_0/imod2d_b6c3_bb3.ms.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_0/imod3d_b6c3_bb3.ms.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_0/pbeam_b6c3_bb3.ms.fits
    write reference model profile: 
        imod3d_prof@h2o@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_0/imodrp_h2o_b6c3_bb3.ms.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb3.ms  to  bx610_b6c3_uv_ab/model_0/model_b6c3_bb3.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb3.ms to data@bx610_b6c3_uv_ab/model_0/model_b6c3_bb3.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb3.ms  to  bx610_b6c3_uv_ab/model_0/data_b6c3_bb3.ms
     
    -->data_b6c3_bb1.ms.mfs
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs to bx610_b6c3_uv_ab/model_0/imod2d_b6c3_bb1.ms.mfs.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs to bx610_b6c3_uv_ab/model_0/imod3d_b6c3_bb1.ms.mfs.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs to bx610_b6c3_uv_ab/model_0/pbeam_b6c3_bb1.ms.mfs.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs  to  bx610_b6c3_uv_ab/model_0/model_b6c3_bb1.ms.mfs
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs to data@bx610_b6c3_uv_ab/model_0/model_b6c3_bb1.ms.mfs
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb1.ms.mfs  to  bx610_b6c3_uv_ab/model_0/data_b6c3_bb1.ms.mfs
     
    -->data_b6c3_bb4.ms.mfs
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs to bx610_b6c3_uv_ab/model_0/imod2d_b6c3_bb4.ms.mfs.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs to bx610_b6c3_uv_ab/model_0/imod3d_b6c3_bb4.ms.mfs.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs to bx610_b6c3_uv_ab/model_0/pbeam_b6c3_bb4.ms.mfs.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs  to  bx610_b6c3_uv_ab/model_0/model_b6c3_bb4.ms.mfs
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs to data@bx610_b6c3_uv_ab/model_0/model_b6c3_bb4.ms.mfs
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb4.ms.mfs  to  bx610_b6c3_uv_ab/model_0/data_b6c3_bb4.ms.mfs
    --------------------------------------------------------------------------------
    --- took 6.74652  seconds ---
    --- save to: bx610_b6c3_uv_ab/model_0/models.h5
    save the model input parameter: bx610_b6c3_uv_ab/model_0/model.inp
    model_0: 
    {'chisq': 66853422.306602694,
     'lnprob': 10223119.024962375,
     'ndata': 26249868.0,
     'npar': 17}
    data@../data/bx610/alma/2015.1.00250.S/bb2.ms 34423512.11909051 13412252
    data@../data/bx610/alma/2015.1.00250.S/bb3.ms 32120841.556975596 12724908
    data@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs 160325.06165286465 56354
    data@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs 148848.5579627467 56354
    export the model set:              bx610_b6c3_uv_ab/model_1              (may take some time..)
     
    -->data_b6c3_bb2.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/imod2d_b6c3_bb2.ms.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/imod3d_b6c3_bb2.ms.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb2.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/pbeam_b6c3_bb2.ms.fits
    write reference model profile: 
        imod3d_prof@co76@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/imodrp_co76_b6c3_bb2.ms.fits
    write reference model profile: 
        imod3d_prof@ci21@../data/bx610/alma/2015.1.00250.S/bb2.ms to bx610_b6c3_uv_ab/model_1/imodrp_ci21_b6c3_bb2.ms.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb2.ms  to  bx610_b6c3_uv_ab/model_1/model_b6c3_bb2.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb2.ms to data@bx610_b6c3_uv_ab/model_1/model_b6c3_bb2.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb2.ms  to  bx610_b6c3_uv_ab/model_1/data_b6c3_bb2.ms
     
    -->data_b6c3_bb3.ms
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_1/imod2d_b6c3_bb3.ms.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_1/imod3d_b6c3_bb3.ms.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb3.ms
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_1/pbeam_b6c3_bb3.ms.fits
    write reference model profile: 
        imod3d_prof@h2o@../data/bx610/alma/2015.1.00250.S/bb3.ms to bx610_b6c3_uv_ab/model_1/imodrp_h2o_b6c3_bb3.ms.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb3.ms  to  bx610_b6c3_uv_ab/model_1/model_b6c3_bb3.ms
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb3.ms to data@bx610_b6c3_uv_ab/model_1/model_b6c3_bb3.ms
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb3.ms  to  bx610_b6c3_uv_ab/model_1/data_b6c3_bb3.ms
     
    -->data_b6c3_bb1.ms.mfs
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs to bx610_b6c3_uv_ab/model_1/imod2d_b6c3_bb1.ms.mfs.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs to bx610_b6c3_uv_ab/model_1/imod3d_b6c3_bb1.ms.mfs.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs to bx610_b6c3_uv_ab/model_1/pbeam_b6c3_bb1.ms.mfs.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs  to  bx610_b6c3_uv_ab/model_1/model_b6c3_bb1.ms.mfs
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb1.ms.mfs to data@bx610_b6c3_uv_ab/model_1/model_b6c3_bb1.ms.mfs
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb1.ms.mfs  to  bx610_b6c3_uv_ab/model_1/data_b6c3_bb1.ms.mfs
     
    -->data_b6c3_bb4.ms.mfs
     
    imod2d@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs
    write reference model image: 
        imod2d@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs to bx610_b6c3_uv_ab/model_1/imod2d_b6c3_bb4.ms.mfs.fits
    imod3d@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs
    write reference model image: 
        imod3d@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs to bx610_b6c3_uv_ab/model_1/imod3d_b6c3_bb4.ms.mfs.fits
    pbeam@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs
    write reference model image: 
        pbeam@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs to bx610_b6c3_uv_ab/model_1/pbeam_b6c3_bb4.ms.mfs.fits
    copy ms container: 
        ../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs  to  bx610_b6c3_uv_ab/model_1/model_b6c3_bb4.ms.mfs
    write ms column: 
        uvmodel@../data/bx610/alma/2015.1.00250.S/bb4.ms.mfs to data@bx610_b6c3_uv_ab/model_1/model_b6c3_bb4.ms.mfs
    create symlink:
        /Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/bb4.ms.mfs  to  bx610_b6c3_uv_ab/model_1/data_b6c3_bb4.ms.mfs
    --------------------------------------------------------------------------------
    --- took 8.97731  seconds ---
    --- save to: bx610_b6c3_uv_ab/model_1/models.h5
    save the model input parameter: bx610_b6c3_uv_ab/model_1/model.inp
    model_1: 
    {'chisq': 66853527.295681715,
     'lnprob': 10223066.530422866,
     'ndata': 26249868.0,
     'npar': 17}



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>


.. code:: ipython3

    models=gmake.hdf2dct(inp_dct['general']['outdir']+'/model_1/models.h5')
    #gmake.pprint(models['mod_dct']['co76'])
    gmake.model_vrot_plot(models['mod_dct']['co76'])



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_b6c3_uv_ab_files/demo_bx610_b6c3_uv_ab_7_1.png


