

Installation
~~~~~~~~~~~~
The package can be installed via::
    
    $ pip install --user --upgrade GMaKE                                    # from PyPI
    $ pip install --user --upgrade git+https://github.com/r-xue/GMaKE.git   # from GitHub  
    $ pip install --user .                                                  # from a local copy     

Dependencies:
~~~~~~~~~~~~~

**Required**: for basic image-based modeling/fitting functions

- `Python 3 <https://www.python.org>`_
- `numpy <https://www.numpy.org>`_
- `scipy <https://www.scipy.org>`_
- `astropy <https://www.astropy.org>`_
- `matplotlib <https://matplotlib.org>`_
- `asteval <https://newville.github.io/asteval/>`_
- `lmfit <https://lmfit.github.io/lmfit-py//>`_

**Optional**: for visibility-based capability and advanced diagnostics / analysis

- `casa6 <https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage>`_
- `python-casacore <https://github.com/casacore/python-casacore>`_ & `casacore <https://github.com/casacore/casacore>`_  
- `uvrx <https://r-xue.github.com/uvrx>`_
- `FINUFF <https://finufft.readthedocs.io/en/latest/>`_
- `emcee <http://dfm.io/emcee>`_
- `corner <https://corner.readthedocs.io/en/latest>`_
- `spectral-cube <https://spectral-cube.readthedocs.io>`_
- `pvextractor <https://pvextractor.readthedocs.io>`_

**Suggested**:

- `numexpr <https://github.com/pydata/numexpr>`_
- `galario <https://github.com/mtazzari/galario>`_  *(used for visibility-based modeling, but may fail in mutiple-source cases)*
- `galpy <https://github.com/jobovy/galpy>`_ *(only used when the kinematic model is built upon the galaxy mass distribution and potentials)*
- `mkl_fft <https://github.com/IntelPython/mkl_fft>`_ *(improve FFT speed)*
- `pyfftw <https://pypi.org/project/pyFFTW/>`_ *(improve FFT speed)*
- `skimage <https://scikit-image.org>`_ *(image 2D transform)*
	
Basic Usage
~~~~~~~~~~~

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
