#!/usr/bin/env python
# encoding: utf-8
"""

The module can be installed via one of these commands:

    python setup.py install --user      # from a local copy
    pip install --user gmake            # or, from PyPI
    pip install --user --editable .     # or, "Editable" install
    
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
with open("gmake/__init__.py", "r") as fh:
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
                 classifiers=['Development Status :: 4 - Beta',
                             'Programming Language :: Python :: 3',
                             'Programming Language :: Python :: 3.6',
                             'Programming Language :: Python :: 3.7',
                             "Topic :: Astronomy"],
                 keywords="Galaxy Dynamics",           
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 entry_points={'console_scripts': ['gmake_cli = gmake.gmake_cli:main']},
                 install_requires=[
                    'astropy>=3.0',
                    'scikit-image','alpy','regions',
                    'scipy','reproject','fitsio','FITS_tools','yt','memory_profiler',
                    'python-casacore>=3.1.1','galpy',
                    'reikna','tqdm',
                    'asteval>=0.9.14','numexpr>=2.6.9',
                    'pvextractor','spectral-cube',
                    'emcee','corner','lmfit','mkl-fft','Cython',
                    'pyyaml'],
                 python_requires='>=3.6, <4',
                 project_urls={'Bug Reports': 'https://github.com/r-xue/gmake/issues',
                               'Source': 'https://github.com/r-xue/gmake/'},                    
                #dependency_links=[
                #    'https://github.com/IntelPython/mkl_fft/archive/v1.0.14.zip',],
                 zip_safe=False)
