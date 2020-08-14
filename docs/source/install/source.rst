.. highlight:: shell


From sources
------------

The sources for ism3d can be downloaded from the `Github repo`_.

You can either clone the public repository and install the copy of source with:

.. code-block:: console

    $ git clone git://github.com/r-xue/ism3d
    $ pip install --user .


To do this in one step, you can also run this command in your terminal:

.. code-block:: console

    $ pip install --user --upgrade git+https://github.com/r-xue/ism3d.git

.. _Github repo: https://github.com/r-xue/ism3d


..  comment
    Stable release
    --------------

    Alternatively, the stable version is also available at Pypi. To install ism3d, run this command in your terminal:

    .. code-block:: console

        $ pip install --user ism3d

    This is the preferred method to install ism3d, as it will always install the most recent stable release.

    .. _pip: https://pip.pypa.io
    .. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Dependencies
^^^^^^^^^^^^

While most dependecies will be automatically checked and installed from the standard PyPI installation (specified in `setup.cfg`_),
we note that some *might* require manual installations on certain platforms (most likley on macOS):

- **required**, for Measurement Sets I/O

    - `FINUFFT <https://finufft.readthedocs.io/en/latest/>`_
    - `casa6 <https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage>`_

- **required**, for galactic dynamics modeling from mass potentials

    - `galpy <https://github.com/jobovy/galpy>`_

- **optional**, for moderate performance improvement

    - `mkl_fft <https://github.com/IntelPython/mkl_fft>`_/`mkl_random <https://github.com/IntelPython/mkl_random>`_ *(improve FFT speed)*


- **test-only**, for running certain benchmarking tests and tutorials

    - `galario <https://github.com/mtazzari/galario>`_  
    - `python-casacore <https://github.com/casacore/python-casacore>`_ & `casacore <https://github.com/casacore/casacore>`_  

.. _setup.cfg: https://github.com/r-xue/ism3d/blob/master/setup.cfg

For development, one can manually install most dependencies with:

.. code-block:: console

    $ pip install --user -r ./requirements_dev.txt