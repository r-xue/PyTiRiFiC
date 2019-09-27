GMaKE: Galaxy Morphology and Kinematics Estimator
==============================================================

A Python wrapper code for evaluating galaxy morphology and kinematics from multi-band astronomical images and spectral cubes

We build galaxy line/continuum models from a set of physical parameters describing the galaxy morphology, kinematics, and surface emissivity. Then we map the emission models into the observed images/spectralcube/visibility, and compare predictions with actual data.

Project links:

* Repo: https://github.com/r-xue/GMaKE
* PyPI: https://pypi.python.org/pypi/GMaKE

Installation
~~~~~~~~~~~~
The command line script can be installed via::

    pip install --user .                                                     # from a local copy 
    pip install --user --upgrade casa-proc                                   # from PyPI
    pip install --user https://github.com/r-xue/GMaKE/archive/master.zip 	 # from GitHub

Usage
~~~~~

Although GMaKe is built as a Python package/modules, a user-friendly console command line interface is provided::
	
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





Examples
~~~~~~~~

+ BX610 (two ALMA bands; CO4-3/CI1-0 & CO7-6/CI2-1 & Continuum; one shot)

Additional tutorials are in Jupyter Notebooks:

* `basic_demo_amoeba.ipynb <http://colab.research.google.com/github/r-xue/GMaKE/blob/master/examples/notebook/basic_demo_amoeba.ipynb>`_


* `basic_demo_emcee.ipynb <http://colab.research.google.com/github/r-xue/GMaKE/blob/master/examples/notebook/basic_demo_emcee.ipynb>`_
 
