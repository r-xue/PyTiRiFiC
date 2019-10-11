.. _package-template:

Welcome to GMaKE's documentation!
====================================================



TaskList
---------

MS:

* improve the flowchart
* Complete MS Section 4 (examples, BX610, W0355): most importantly, finalize the plots.
* Summarize main advantages and the difference with existing tools.

Code:

* finish the code packaging (currently broken) and fix the plotting module
* link some software dependencies in git via submodule or subtree (especially those not on PyPI: casacore, galario)
* verify the pip-based installation method on a vanilla system

quickstart
-----------

This is intended to be a quick reference for the program. The current task list is `here`_

1. Introduction
2. `Parameter File Format`_
3. Examples
4. More options

.. _Parameter File Format: ./par_def.html
.. _here: https://github.com/r-xue/GMaKE/wiki/Task-List

Installation
~~~~~~~~~~~~
The command line script can be installed via::

    pip install --user .                                                  # from a local copy 
    pip install --user --upgrade casa-proc                                # from PyPI
    pip install --user https://github.com/r-xue/GMaKE/archive/master.zip  # from GitHub

Usage
~~~~~

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


Dependencies:
=====
- `Python 3.7 <https://www.python.org>`_
- `numpy <https://www.numpy.org>`_
- `scipy <https://www.scipy.org>`_
- `astropy <https://www.astropy.org>`_
- `matplotlib <https://matplotlib.org>`_
- `skimage <https://scikit-image.org>`_
- `emcee <http://dfm.io/emcee>`_
- `corner <https://corner.readthedocs.io/en/latest>`_
- `lmfit <https://lmfit.github.io/lmfit-py//>`_
- `asteval <https://newville.github.io/asteval/>`_
- `numexpr <https://github.com/pydata/numexpr>`_
- `pvextractor <https://pvextractor.readthedocs.io>`_
- `spectral-cube <https://spectral-cube.readthedocs.io>`_
- `galario <https://github.com/mtazzari/galario>`_  *(optional: only used for visibility-based modeling)*
- `python-casacore <https://github.com/casacore/python-casacore>`_ & `casacore <https://github.com/casacore/casacore>`_  *(optional: only used for visibility-based modeling)*
- `galpy <https://github.com/jobovy/galpy>`_ *(optional: only used when the kinmeatic model is built upon the galaxy mass distribution)*
- `mkl_fft <https://github.com/IntelPython/mkl_fft>`_ *(optional: for improving FFT speed)*
- `pyfftw <https://pypi.org/project/pyFFTW/>`_ *(optional: for improving FFT speed)*


ChangeLog:
=====
::

 04-24-2019     add wiki-based documentation

Parameter File Format
---------------

The basic syntax for the .inp file format is explained in the parameter definition file: `parameters.inp`_ .

After a comparison among several readable plain-text syntaxes potentially suitable for the input file choice (e.g., csv/json/yaml/yanny/xml), I decide to keep using the native .inp format while gradually adding the support the traditional Python config file format (from the `ConfigParser`_ module).


.. _ConfigParser: https://docs.python.org/3/library/configparser.html
.. _parameters.inp: https://github.com/r-xue/GMaKE/blob/master/gmake/parameters.inp


Getting Started
---------------


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   par_def
   
.. toctree::
    maxdepth: 1
    :caption: Tutorials
    
    demos/demo_hxmm01
    demos/demo_hxmm01_simulate
    demos/demo_bx610_amoeba
    demos/demo_bx610_emcee

.. toctree::
    maxdepth: 1
    :caption: Tests
    
    tests/test_uvsample_performance


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
