## GMaKE

GMaKE: Galaxy Morphology and Kinematics Estimator

A Python wrapper code for evaluating galaxy morphology and kinematics from multiple-band astronomical images and spectral cubes

### Brief

We build galaxy line/continuum models from a set of physical parameters describing the galaxy morphology, kinematics, and surface emissivity. Then we map the emission models into the observed images/spectralcube/visibility, and compare predictions with actual data.

### Examples

+ BX610 (two ALMA bands; CO4-3/CI1-0 & CO7-6/CI2-1 & Continuum; one shot)

### Guide Lines

+ flexible and expandable modeling algorithm implementation
+ provide various parameter optimization choices and robust error estimations
+ the comparison can be made in either image and visibility domain
+ handle multiple images/cubes simultaneously and treat blended line/objects together
+ straightforward parameter setting: the emission model was built upon parameters describing "physical" properties of each object; the emission models can be easiliy translated into the data obatined in radio (frequency) or optical (wavelength) with pre-defined system response functions
+ provide data/model visulizations (xy/pv-moms) and clear diagnostic plots for parameter fitting goodness (chi^2/posterior-prob)

A prototype of GMaKE was used in Xue, Fu, Isbell et al. (2018) ApJL.848.11 [[ApJL](http://iopscience.iop.org/article/10.3847/2041-8213/aad9a9)/[arXiv](http://arxiv.org/abs/1807.04291)/[ADS](http://adsabs.harvard.edu/abs/2018ApJ...864L..11X)]

### Drawback

+ The models need to be "parameterized".

### Borrowed Algorithms

To minimize our effort to achieve the above goals, we implement some existing modeling algorithms into our code:

+ ~~*[KinMSpy](https://github.com/TimothyADavis/KinMSpy)*:      build simple spectral line models~~
+ ~~*[TiRiFiC](http://gigjozsa.github.io/tirific/)*:     build complicated spectral line models (benchmarking)~~
+ ~~*[GALFIT](https://users.obs.carnegiescience.edu/peng/work/galfit/galfit.html)*:    make images from more sophisticated galaxy morphology functions (benchmarking)~~
+ *[galario](https://github.com/mtazzari/galario)*:    transfer model images to visibilities for UV-based fitting
+ ~~*[emcee](https://emcee.readthedocs.io/en/stable/)*: Parameter sampler~~
+ *[PyMultiNest](https://github.com/JohannesBuchner/PyMultiNest)*: Bayesian inference
+ *Amoeba*: Parameter Fitting
+ ~~*[MPFIT](http://cars9.uchicago.edu/software/python/mpfit.html)*: Parameter Fitting (replaced with python.lmfit)~~
+ ~~*DM-related*:~~


### Keywords:

+ Toolbox
+ Toolkit
+ Disk
+ Galactic
+ Modeling
+ Analysis
+ Spectral
+ Continuum
+ Emission
+ Kinematics
+ Dynamics
+ Visibility
+ Images
+ Morphology
+ Kinematics
+ Inference
+ Parameter
+ Estimation
+ Analysis
+ Assessment

### Ideas

+ grant proposal oppertunity
+ +ALMA GilDAS


+ tools
+ archiveal pipeline
+ science
+ NFS Ureka

check GalFIT papers
+ parameter format yybp


### To-Do List

+ ~~implement hex index~~
+ ~~implement cont fitting~~
+ ~~streamline archival data imaging~~
+ ~~dirty PSF~~
+ ~~galario xy-uv transfer & efficiency~~
+ plotting: 
	- ~~1D: data/model spectra~~
	- ~~1D: rotation curve~~
	- 2D: channel map
	- 2D: face-on distribution
	- 2D: ~mom0~ mom1 maps
	- 3D: volume rendering (yt) Check ER.s YT exampels
	- ~~add intrinsic models~~
	- SB profile along major/minor axes
+ ~~save metadata~~
+ ~~improve corner plots~~
+ ~~automatically minimize sub-cube sizes~~
+ ~~fix the undersampling problem in kinmspy~~
+ ~~import MS natively~~
+ Add more panel models
+ fitting on ~~the robust=0 dataset~~
+ ~~use random process to avoid undersamping pixelization~~
+ ~~Consider to add a "bar" or a "hole" / add assymetric cloudlets sampling in kinmspy~~
+ ~~return radial profile~~
+ ~~fix WCS header from KinMSpy (don't really care for our implementation)~~
+ ~~automatically balance computing expense based on the dynamicalrange/precision requirement~~
+ refit with an elliptical face-on morplogy 
+ ~~h-alpha ALMA/SINFONI comparison (side-by-side)~~
+ ~~add CO 4-3 CI 1-0 into the fitting~~
+ ~~add A.B.'s VLA C/D-config CO 1-0 data~~
+ update the manuscript
+ comparison with the "busy" fit
+ ~~Sofia / Model / gen_mask.pro For the different masking creation~~
+ ~~merge the amoeba & mpfit & lmfit code pieces~~
+ ~~add options for sherpa~~
+ plot band4->band8 cont flux model
+ verify the flux units Jy*km/s
+ generate intrinsic face-on / sky-on mom0/mom1/mom2 maps
+ build the code around a "gmake" class
+ improve the halo/disk model calculation
+ evaluate halotools
+ evaluate documentation tools
+ add other fitting examples: MUSE-type cube; batch fitting stacking replacement (for extracting population average property; shared keywords)
+ ~~test sb_min/sb_max~~
+ ~~test varying sersic n~~
+ ~~check rad vector~~
+ ~~bruttle force grid~~
+ fill model in CASA: casa.sm / casa.ft
+ ~~python-casacore->Galario~~
+ write the recipe for sw installation
+ ~~examine UVMUTIFITS https://www.oso.nordic-alma.se/software-tools.php~~
+ plot band by band plots 1D
+ uvplot / uvplot by chan; vis-uvdist 
+ actually this FFT one is faster?
+ add angular size in uvamp
+ UV averging vector vs. scaler
+ MUSE / Stacking Transfer Filtering
+ machine learning object identification
+ check https://photutils.readthedocs.io/en/stable/background.html
+ reduce memory footprint
+ switch to single precsion-float as the data is single
