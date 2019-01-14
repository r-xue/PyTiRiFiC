## GMaKE

GMaKE: Galaxy Morphology and Kinematics Estimator

A Python wrapper code for evaluating galaxy morphology and kinematics from multiple-band astronomical images and spectral cubes

### Outline

We build galaxy line/continuum models from a set of physical parameters describing the galaxy morphology, kinematics, and surface emissivity. Then we map the emission models into the observed images/spectralcube/visibility, and compare predictions with actual data.

### Examples

+ BX610 (two ALMA bands; CO4-3/CI1-0 & CO7-6/CI2-1 & Continuum; one shot)

### GuideLines

+ flexible and expandable modeling algorithm implementation
+ provide various parameter optimization choices and robust error estimations
+ the comparison can be made in either image and visibility domain
+ handle multiple images/cubes simultaneously and treat blended line/objects together
+ straightforward parameter setting: the emission model was built upon parameters describing "physical" properties of each object.


### Borrowed Algorithms

To minimize our effort to achieve the above goals, we implement some existing modeling algorithms into our code:

+ *KinMS*:      build simple spectral line models
+ *TiRiFiC*:     build complicated spectral line models (benchmarking)
+ *GALFIT*:    make images from more sophisticated galaxy morphology functions (benchmarking)
+ *Galario*:    transfer model images to visibilities for UV-based fitting
+ *DM-RELATED*:        ??
