History
~~~~~~~

The package was initially developed upon the algoirthm used by Xue, Fu, Isbell et al. (2018) ApJL.848.11 [[ApJL](http://iopscience.iop.org/article/10.3847/2041-8213/aad9a9)/[arXiv](http://arxiv.org/abs/1807.04291)/[ADS](http://adsabs.harvard.edu/abs/2018ApJ...864L..11X)],
but quickly evolve into a brand-new package with some brand-new implementaion of some under-line algorithm, including but not limited to:  
    
    * A Python model rendering module of simulating galaxy emission with complex morphology and kinematics structure, including line emission from a rotating disk galaxy with spiral arms structurate (inspired by GIPSY/galmod, GALFIT )
    
    * I/O of visibilities in CASA measurements dataset (via. CASA6) and imlement visibility-based model simulation/fitting capacibity.
    
    * A high-precsion and efffiencet robust algoirthm on simulating a large visibility set from arbitary sky emission models (a lightweight CASA simulator altenrative suitabe for model fitting)
    
    * A user-friendly plain-tex based parameter file syntax for performing model simulation/fitting in a highly flexible fashion
    
Design Goals
~~~~~~~~~~~~

+ flexible and expandable modeling algorithm implementation
+ provide various parameter optimization choices and robust error estimations
+ the comparison can be made in either image and visibility domain
+ handle multiple images/cubes simultaneously and treat blended line/objects together
+ straightforward parameter setting: the emission model was built upon parameters describing "physical" properties of each object; the emission models can be easiliy translated into the data obatined in radio (frequency) or optical (wavelength) with pre-defined system response functions
+ provide data/model visulizations (xy/pv-moms) and clear diagnostic plots for parameter fitting goodness (chi^2/posterior-prob)


Credit
~~~~~~

University of Iowa

This project is built-upon several other open-sources projects (e.g. astropy,emcee,lmfit),  which are constributed by numeriousc devlopers, which are credited here.


See also
~~~~~~~~~

GMaKE is inspired by several well-developed open-source packages, which are usually designed for specific user cases and data types, or provide some equivalent module functions/algorithms within GMaKE.
We greatly appreciate their open-source knowledge sharing efforts, and list them here as important reference for the general topics here with a short description.
offer a subset of GMaKE's capabilities or serve as a backbone of some specific usage cases (i.a)
Some package offering some similar functions or moldeing capacibilt with what GMaKE offer, although they are mostly specified for specific data form or optimized for 
some user case covered by GMaKE. We list them here as reference for this general topic here:

- `galmod <https://www.astro.rug.nl/~gipsy/tsk/galmod.dc1>`_

	Likely the first popular implementation of the tiled-ring algorithm
	
- `Bbarolo <https://editeodoro.github.io/Bbarolo/>`_

	Improve upon the tiled-ring algorithm from galmod, with full model fitting features (likely for a single-line/disk user case)

- `KinMS <https://github.com/TimothyADavis/KinMSpy>`_

	another Python and IDL implantation of tilet-ring model method to simulate spectral-cube from a rotating disk galaxy 

- `TiRiFiC <http://gigjozsa.github.io/tirific>`_

	a fortran-based spectral line models with full fitting function
	
- `GALFIT <https://users.obs.carnegiescience.edu/peng/work/galfit/galfit.html>`_

	 widely used 2D images from more sophisticated galaxy morphology functions
	 
- `galario <https://github.com/mtazzari/galario>`_

	a C-based package wiich can transfer model images to visibilities for UV-based fitting (see note here)

- `UVMULTIFIT <UVMULTIFIT>`_

	a packge for, required instatltion into a stand-alone Python package

- `PDSPY <https://github.com/psheehan/pdspy:>`_
