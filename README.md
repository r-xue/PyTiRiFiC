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

+ *[KinMSpy](https://github.com/TimothyADavis/KinMSpy)*:      build simple spectral line models
+ *[TiRiFiC](http://gigjozsa.github.io/tirific/)*:     build complicated spectral line models (benchmarking)
+ *[GALFIT](https://users.obs.carnegiescience.edu/peng/work/galfit/galfit.html)*:    make images from more sophisticated galaxy morphology functions (benchmarking)
+ *[galario](https://github.com/mtazzari/galario)*:    transfer model images to visibilities for UV-based fitting
+ *[emcee](https://emcee.readthedocs.io/en/stable/)*: Parameter sampler
+ *[PyMultiNest](https://github.com/JohannesBuchner/PyMultiNest)*: Bayesian inference
+ *Amoeba*: Parameter Fitting
+ *[MPFIT](http://cars9.uchicago.edu/software/python/mpfit.html)*: Parameter Fitting
+ *DM-related*:        tbd.


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

### To-Do List

+ ~~implement hex index~~
+ ~~implement cont fitting~~
+ ~~streamline archival data imaging~~
+ ~~dirty PSF~~
+ ~~galario xy-uv transfer & efficiency~~
+ plotting: 
	- ~~1D: data/model spectra~~
	- 1D: rotation curve
	- 2D: channel map
	- 2D: face-on distribution
	- 2D: ~mom0~ mom1 maps
	- 3D: volume rendering (yt)
+ ~~save metadata~~
+ ~~improve corner plots~~
