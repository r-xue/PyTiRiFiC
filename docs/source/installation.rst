.. highlight:: shell

============
Installation
============

From sources
------------

The sources for ism3d can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/r-xue/ism3d

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/r-xue/ism3d/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install --user .

To install the latest ism3d from GitHub in one step, you can also run this command in your terminal:

.. code-block:: console

    $ pip install --user --upgrade git+https://github.com/r-xue/ism3d.git

.. _Github repo: https://github.com/r-xue/ism3d
.. _tarball: https://github.com/r-xue/ism3d/tarball/master

Stable release
--------------

Alternatively, the stable version is also available at Pypi. To install ism3d, run this command in your terminal:

.. code-block:: console

    $ pip install --user ism3d

This is the preferred method to install ism3d, as it will always install the most recent stable release.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Dependencies
------------

While most dependecies will be automatically checked and installed from the standard Pypi installation (specified in setup.cfg),
we note the ones requiring manual installation here:

**Required**: for basic image-based modeling/fitting functions

- `FINUFF <https://finufft.readthedocs.io/en/latest/>`_
- `casa6 <https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage>`_

**Optional**: for some special features

- `galpy <https://github.com/jobovy/galpy>`_ *(only used when the kinematic model is built upon the galaxy mass distribution and potentials)*
- `skimage <https://scikit-image.org>`_ *(image 2D transform)*

**Recommaned**: for performance improvements

- `mkl_fft <https://github.com/IntelPython/mkl_fft>`_ *(improve FFT speed)*
- `pyfftw <https://pypi.org/project/pyFFTW/>`_ *(improve FFT speed)*


**test-only**:  only needed for running the test suite or some benchmarking-related tutorils

- `galario <https://github.com/mtazzari/galario>`_  *(used for visibility-based modeling, but may fail in mutiple-source cases)*
- `python-casacore <https://github.com/casacore/python-casacore>`_ & `casacore <https://github.com/casacore/casacore>`_  
