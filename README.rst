GMaKE: Galaxy Morphology and Kinematics Estimator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Python-based package for evaluating galaxy morphology and kinematics properties 


**Major features:**

*Efficient forward-modeling of Galaxy Emission in Astronomical Data*

-   Construct high-precision spatially/spectroscopically-resolved galaxy emission models, from
    analytical or physical prescriptions of galaxy geometry, emissivity,  kinematics, and dynamics.
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
-   The package is specially optimized for efficiently performing joint model fitting on large heterogeneous multiple-wavelength datasets, and performance Bayesian-based model sampling for robust statistical error estimation with proper prior assumption. This is done by taking the advantages of multi-threading computation, with careful memory footprint management.

GMaKE is originally designed to be a special tool to extract galaxy morphology and kinematics property from large modern interferometer datasets (specifically VLA and ALMA). We integrate some convenient utility-type functions (based on CASA 6's Python modules) for helping process, image, and visualize calibrated viability data from the interferometer data archive, as we realize the importance of properly preparing visibility data, which may require additional effort due to large dataset size and "complex" nature of interferometer visibility data forms.

On the other hand, although we have demonstrated that visibility-domain modeling can eliminate the non-linear imaging process for interferometer data and offers a unique advantage on the marginally-resolved moderate SNR data (e.g., noteably for high-z observations), we note that GMaKE is still equivalently equipped to analyze imaging or data products under the same modeling and fitting framework.

Project Links:
~~~~~~~~~~~~~~

- Repo: https://github.com/r-xue/GMaKE
- PyPI: https://pypi.python.org/pypi/GMaKE
- Documentation: https://r-xue.github.io/GMaKE/d811bb3037aca6a6b0e0ea7bbca033e2e396f67c
