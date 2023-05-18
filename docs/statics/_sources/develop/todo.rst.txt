To-Do List
==========


##### Low-priority List:
---

+ Basic usage demos

+ Advanced usage demos

+ Documentation/Webpages

+ CASA-simdata wrapper to simulate data for proposals

+ Rename


##### Code Revision
---

- [ ] Handle multi-spw MS (via pyuvdata? casa6? or in-house I/O functions)

- [ ] model.export to intermediate formats: Saving models in multiple MSs is not ideal in terms of I/O;

- [ ] use reference copy if some metadata are found to be redundant (e.g. the same UVW array for different SPWs from the same observation)

- [ ] support .inp with only some parameter sections: e.g. Objects+ optimizer, or just a analyzer section


##### Documentations
---

- [ ] Complete MS Section 4 (examples, BX610, W0355): most importantly, finalize the plots.

- [ ] Summarize main advantages and the difference with existing tools. (benchmarking)

- [ ] describe memory / IO optimizations.

- [ ] readme.md->readme.rst


##### Coding To-Do
---

- [ ] visplotting (test various versions for difference models; w/ or w/o phasecenter shifting)

amp-uvdist; real/img-uvdist; etc.

- [x] improve logging

- [ ] benchmarking

- [ ] link the software dependencies in git via submodule or subtree (only for galario)

- [ ] re-organize the output directory structure

- [ ] tar example data

- [ ] demo on synthetic dataset rather than BX610

- [ ] logging for gmake_casa()

- [ ] color-coded amp/phase plotting?

##### Code Test:
---

- [x] verify the method='emcee' run

- [ ] synthetic data experiments

- [ ] real-data experiments

- [ ] Test on cluster field

- [x] HXMM01 test

- [x] Import BX610 Cycle5 Data (high-volume ~1.8TB in raw)

- [ ] switch to CASA 6 casatools.table for  MS I/O operations


##### Code Revision:
---
- [x] save reference-models (XYV) in "cloudlet"/sparsegrid ([ncloud,3] array) forms (which will be significantly smaller than fine grid cubes/images); gridded reference-Image & UV-sampling happen on-demand, and the code will only require memory enough holding only one plane when save_model=False

- [x] optimize the performance of model_lnprop() for large
UV datasets

- [x] use uvchi2 instead of model_uvsample() so the model visibility won't take memory by default.

- [X] use 2D array for "imod2d" + a flux scaling vector in the case of multi-frequency data; broadcasting happens on-the-fly when running model_simobs()


- [ ] handle multi-point observations 

- [ ] use CASA 6 as I/O alternative solution


##### Documentations
---
- [x] 1D spectra plots with SPW partition highlighted

- [ ] update flowchart with diagnosis/analysis procedures)


- [ ] plots in documentation


- [ ] more specific naming for each procedure (analyze?/plot? too generic)

##### Code Revision:
---

- [x] adopt hdf5 as default I/O format for modeling metadata

- [x] use new *Backends* interface from [emcee 3.0.0](https://emcee.readthedocs.io/en/latest/tutorials/monitor/?highlight=sampler.sample)

- [x] save data / models in hdf5 (rather than non-standard FITS table)

- [x] To reduce the disk space usage, data/model will only be exported to images-FITS or vis-MS on-demand during analysis  (requires **data.h5** and **model_[version]/model.h5**). In addition, I have removed redundant copies of observed data in MS and use symbolic link by default

- [x] remove yaml files

- [x] print out the debug information on the dependency check

- [x] readme.md->readme.rst

- [x] optimize the threading efficiency for optimize.method='emcee' : currently, the modeling threading is on and the emcee threading is off. [Ref1](https://emcee.readthedocs.io/en/stable/tutorials/parallel)
 
- [x] add the primary beam effect into the simulation

- [x] re-define input file syntax
