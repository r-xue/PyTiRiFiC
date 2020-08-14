Background
~~~~~~~~~~

The package was initially developed upon the algoirthm used by Xue, Fu, Isbell et al. (2018) ApJL.848.11 [[ApJL](http://iopscience.iop.org/article/10.3847/2041-8213/aad9a9)/[arXiv](http://arxiv.org/abs/1807.04291)/[ADS](http://adsabs.harvard.edu/abs/2018ApJ...864L..11X)],
but quickly evolve into a brand-new package with some brand-new implementaion of some under-line algorithm, including but not limited to:  
    
    * A Python model rendering module of simulating galaxy emission with complex morphology and kinematics structure, including line emission from a rotating disk galaxy with spiral arms structurate (inspired by GIPSY/galmod, GALFIT )
    
    * I/O of visibilities in CASA measurements dataset (via. CASA6) and imlement visibility-based model simulation/fitting capacibity.
    
    * A high-precsion and efffiencet robust algoirthm on simulating a large visibility set from arbitary sky emission models (a lightweight CASA simulator altenrative suitabe for model fitting)
    
    * A user-friendly plain-tex based parameter file syntax for performing model simulation/fitting in a highly flexible fashion
    