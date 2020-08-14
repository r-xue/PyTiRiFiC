Usage
=====


Use as a command-line tool
--------------------------

``ism`` provides a user-friendly console command-line interface for basic simulation or model fitting tasks/workflows.
The task assignment is specified by a parameter file the `INI`_ format, as well as some CLI optional keywords.
This appraoch is in line with other traditional model fitting programs (e.g. Galfit, Tirific) and doesn't require Python programming in most common user cases.

.. _INI: https://en.wikipedia.org/wiki/INI_file

.. code-block:: console

    Ruis-Mac-mini:~ Rui$ ism3d --help
    usage: ism3d [-h] [-f] [-a] [-p] [-d] [-t] [-l LOGFILE] inpfile

    The ISM3d CL entry point: 
        ism3d path/example.inp

        model fitting:
            ism3d -f path/example.inp
        analyze fitting results (saved in FITS tables / HDFs?) and export model/data for diagnostic plotting  
            ism3d -a path/example.inp 
        generate diagnostic plots
            ism3d -p path/example.inp 

    Note:
        for more complicated / customized user cases, one should build a workflow by
        calling modules/functions directly (e.g. hz_examples.py) 
            
        

    positional arguments:
    inpfile               A parameter input file

    optional arguments:
    -h, --help            show this help message and exit
    -f, --fit             perform parameter optimization
    -a, --analyze         analyze the fitting results / exporting data+model
    -p, --plot            generate diagnotisc plots
    -d, --debug           Debug mode; prints extra statements
    -t, --test            test mode; run benchmarking scripts
    -l LOGFILE, --logfile LOGFILE
                            path to log file  


Use Python APIs and utility functions
-------------------------------------

``ism3d`` itself is written purely in Python, although most of its depedencies are not.
You can use ``ism3d`` as a general utility library for your own program and build your modeling / data analysis workflow.

For example, to use the ``invert`` function in ``ism3d``, try:

.. code-block:: python

    In [1]: from ism3d.uvhelper import invert

    In [2]: help(invert)  

    Help on function invert in module ism3d.uvhelper.imager:

    invert(vis='', imagename='', datacolumn='data', antenna='', weighting='briggs', robust=1.0, npixels=0, cell=0.04, imsize=[128, 128], phasecenter='', specmode='cube', start='', width='', nchan=-1, perchanweightdensity=True, restoringbeam='', onlydm=False, pbmask=0, pblimit=0, exclude_list=['residual', 'residual.tt0', 'residual.tt1', 'sumwt', 'sumwt.tt0', 'sumwt.tt1', 'sumwt.tt2', 'model', 'model.tt0', 'model.tt1'], **kwargs)
        Generate a compact dirty image from a MS dataset as a quick imaging snapshot;
        
        Note about the default setting:
        
        +   restoringbeam='' to preserve the original dirty beam shape:
            if "common" then additional undesired convolution will happen
        +   Another faster way to do this would be using the toolkits:
            imager.open('3C273XC1.MS')  
            imager.defineimage(nx=256, ny=256, cellx='0.7arcsec', celly='0.7arcsec')  
            imager.image(type='corrected', image='3C273XC1.dirty')  
            imager.close()
            But it may be difficult to write a function to cover all setting already in casatasks.tclean()
            
        note:
            apperantly tclean(start='',width='',nchan-1) will not follow the actual spw-channel arrangeent:
            it will sort channel by frequency forst and then start the sequence.
            That means even when negative channel width will still get frequency-increasing cube:
                for such case, width=-1,nchanel=240,start=239 will get a cube following the channel-frequency arrangment.

     