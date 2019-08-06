#!/usr/bin/env python
# encoding: utf-8
"""

The module can be installed via one of these commands:

    python setup.py install --user      # from a local copy
    pip install --user gmake            # or, from PyPI
    pip install --user -e .             # or, "Editable" install
    
 usage:

     >import gmake
     >help(gmake.gmake_read_data)
     >print(gmake.gmake_read_data())    

"""

import setuptools
import os
import sys
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

version='unknown'
with open("gmake/__version__.py", "r") as fh:
    version_file = fh.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if  version_match:
        version=version_match.group(1)                              

if  sys.argv[-1] == "publish":
    os.system("python3 setup.py sdist; twine upload dist/*")
    sys.exit()


setuptools.setup(name='GMaKE',
                 version=version,
                 description='Galaxy Morphology and Kinematics Estimator',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='http://github.com/r-xue/gmake',
                 author='Rui Xue',
                 author_email='rx.astro@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 install_requires=[
                    'astropy',
                    'scikit-image','alpy',
                    'scipy','reproject','fitsio','FITS_tools','yt','memory_profiler',
                    'python-casacore','galpy',
                    'reikna','tqdm',
                    'asteval>=0.9.14','numexpr',
                    'pvextractor','spectral-cube',
                    'emcee','corner','lmfit','mkl-fft','Cython',
                    'pyyaml'],
                project_urls={'Bug Reports': 'https://github.com/r-xue/gmake/issues',
                    'Source': 'https://github.com/r-xue/gmake/'},                    
                #dependency_links=[
                #    'https://github.com/IntelPython/mkl_fft/archive/v1.0.14.zip',],
                 zip_safe=False)
