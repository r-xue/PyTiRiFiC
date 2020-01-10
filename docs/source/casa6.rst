CASA6 Installation
==================

Install ``casatools`` on MacOS 10.14/15 within Python 3.7
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently, ``casatools`` for MacOS (as to 6.1.0.33) is only available as a Py36 `wheel <https://packaging.python.org/discussions/wheel-vs-egg>`_.
If using Py36, just use the standard method to install ``casatools``:

::
   
   pip-3.6 install --user --upgrade --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casatools

For other setups (specifically, MacOS 10.14/15+Python3.7), a workaround is provided here:

::

   # look up the latest version from https://casa-pip.nrao.edu/#browse/browse:pypi-group:casatools      
   whlversion='6.1.0.33'
   
   pip download --python-version 36 --abi cp36m --no-deps  --extra-index-url https://casa-pip.nrao.edu/repository/pypi-group/simple casatools==${whlversion}
   #curl -O https://casa-pip.nrao.edu/repository/pypi-group/packages/casatools/${whlversion}/casatools-${whlversion}-cp36-cp36m-macosx_10_14_x86_64.whl
   
   wheel unpack casatools-${whlversion}-cp36-cp36m-macosx_10_14_x86_64.whl
   casatools_whl_cp36to37_macos.py ${whlversion}
   wheel pack --build-number cp37 casatools-${whlversion}
   mv casatools-${whlversion}-cp37-cp36-cp36m-macosx_10_14_x86_64.whl casatools-${whlversion}-cp37-cp37m-macosx_10_14_x86_64.whl
   pip uninstall --yes casatools casatasks casaviewer casashell
   pip install --user casatools-${whlversion}-cp37-cp37m-macosx_10_14_x86_64.whl

Install other components from CASA6
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The other CASA6 components (casatasks,casashell,casaviewer,casaplotms,casampi) are not platform specific and the installation can be done using the standard method.
 
::

   # look up the latest version number and examine dependency (e.g. the casatools version requirement)
   # https://casa-pip.nrao.edu/#browse/browse:pypi-group:casatasks
   # https://casa-pip.nrao.edu/#browse/browse:pypi-group:casashell
   
   whlversion='6.1.0.33'
   
   pip install --user --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casatasks==${whlversion}
   pip install --user --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casashell==${whlversion}
   pip install --user --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casaviewer
   pip install --user --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casaplotms

   sudo port install py37-mpi4py
   pip install --user --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casampi


Note:

    ``casaviewer``/``casaplotms`` locations::
    
        ~/Library/Python/3.7/lib/python/site-packages/casaviewer/__bin__/casaviewer.app
        ~/Library/Python/3.7/lib/python/site-packages/casaviewer/__bin__/casaplotms.app
        
    ``casacore`` location::
        
        site-packages/casatools/__casac__/

    ``logsink``::
        
        site-packages/casatools/__casac__/logsink.py
