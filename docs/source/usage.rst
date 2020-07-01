=====
Usage
=====

To use ism3d in a project::

    import ism3d

To use uvrx utility functions in your Python script or package::

    >>> import uvrx

All functions will be available under its namespace::

    >>> help(uvrx.invert)

    invert(vis='', imagename='', datacolumn='data', antenna='', weighting='briggs', robust=1.0, npixels=0, cell=0.04, imsize=[128, 128], phasecenter='', specmode='cube', start=0, width=1, nchan=-1, perchanweightdensity=True, restoringbeam='', onlydm=True, pbmask=0, pblimit=0)
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


Python API: Tuturials / Examples

The command line usages..

Although GMaKe is written as a Python package/module, a user-friendly console command-line interface is provided::
    
    hyperion:output Rui$ gmake_cli -h
    
    usage: gmake_cli [-h] [-f] [-a] [-p] [-d] [-t] [-l LOGFILE] inpfile

    The GMAKE CL entry point: 
        gmake path/example.inp

        model fitting:
            gmake -f path/example.inp
        analyze fitting results (saved in FITS tables / HDFs?) and export model/data for diagnostic plotting  
            gmake -a path/example.inp 
        generate diagnostic plots
            gmake -p path/example.inp 

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