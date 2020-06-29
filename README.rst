===============================================
ISM3D: Interferometric Source Modeling up to 3D
===============================================


.. image:: https://img.shields.io/pypi/v/ism3d.svg
        :target: https://pypi.python.org/pypi/ism3d

.. image:: https://img.shields.io/travis/r-xue/ism3d.svg
        :target: https://travis-ci.com/r-xue/ism3d

.. image:: https://readthedocs.org/projects/ism3d/badge/?version=latest
        :target: https://ism3d.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/r-xue/ism3d/shield.svg
     :target: https://pyup.io/repos/github/r-xue/ism3d/
     :alt: Updates


A Python package for simulating and modeling astronomical sources from radio interferometric observations

* Free software: BSD license
* Documentation: https://www.magclouds.org/ism3d
* Repo: https://github.com/r-xue/ism3d
* PyPI: https://pypi.org/project/ism3d


Features
--------

*Efficient forward-modeling of Galaxy Emission in Astronomical Data*

-   Construct high-precision spatially/spectroscopically-resolved galaxy emission models, from analytical or physical prescriptions of galaxy geometry, emissivity,  kinematics, and dynamics.
-   Implement various model elements (e.g., line, continuum, sky background) to provide a realistic presentation of expected galaxy sky emission. multi-frequency synthetic visibility or 
-   The galaxy model can incorporate with multiple line/continuum components.
-   Perform simulated observations of galaxy emission model and render them within a wide range of astronomical data forms 
    (e.g. radio interferometer visibility, 
    radio single-dish or optical IFU spectral cube, 
    multiple-band photometric images, 
    1D spectra, etc.)

*Flexible Model Fitting/Optimization Interface*

-   We offer several model fitting/optimization algorithms under the same interface for a flexible user-friendly modeling experience through either a command-line approach or a serial of Python API functions).
-   All modeling details are summarized in a single parameter file with a very flexible/readable syntax, which is easy to re-use for progressive modeling iterations.
-   The package is specially optimized for efficiently performing joint model fitting on large heterogeneous multiple-wavelength datasets and performance Bayesian-based model sampling for robust statistical error estimation with proper prior assumption. This is done by taking the advantages of multi-threading computation, with careful memory footprint management.

ISM3D is originally designed to be a special tool to extract galaxy morphology and kinematics property from large modern interferometer datasets (specifically VLA and ALMA). We integrate some convenient utility-type functions (based on CASA 6's Python modules) for helping process, image, and visualize calibrated viability data from the interferometer data archive, as we realize the importance of properly preparing visibility data, which may require additional effort due to large dataset size and "complex" nature of interferometer visibility data forms.

On the other hand, although we have demonstrated that visibility-domain modeling can eliminate the non-linear imaging process for interferometer data and offers a unique advantage on the marginally-resolved moderate SNR data (e.g., notably for high-z observations), we note that ISM3D is still equivalently equipped to analyze imaging or data products under the same modeling and fitting framework.

Currently, ism3d is organized into several sub-packages

- arts:      generate artificial sources up to 3d (position-position-frequency/wavelength/velocity) in the sparse array (a.k.a. cloudlet) or regular grid (e.g. spectral cube) (see examples in the yt documents)

- simuv: a simulator for radio interferometric observations

- simxy: a simulator for spectroscopic imaging observations, as well as photometric imaging and 1D spectroscopy (not fully implemented)

- modelling: a model fitting/optimizer framework

- uvhelper:   help prepare and analyze "uv" data for modeling (using CASA6): A small Python library that provides a collection of utility functions helping process, analyze, and visualize interferometric visibility data.

- xyhelper:   help prepare and analyze "xy" data for modeling

- utils: utility functions to support other modules

- maths:      pseudo-random generator / other math-related functions

- plots:      general plotting modules  


While the current effort is still a work in progress: inconsistent documentation, many non-working function placeholders, etc., fast-paced changes are expected soon.
Any comments and suggestions are appreciated and `code/documentation contributions`_ are very welcome.

.. _ism3d: https://www.magclouds.org/ism3d
.. _code/documentation contributions: https://www.magclouds.org/ism3d/html/contributing.html
.. _the CASA6 modular framework: https://ui.adsabs.harvard.edu/abs/2019arXiv191209439R



