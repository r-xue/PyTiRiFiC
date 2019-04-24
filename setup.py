# -*- coding: utf-8 -*-

import setuptools
import os
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

if  sys.argv[-1] == "publish":
    os.system("python3 setup.py sdist; twine upload dist/*")
    sys.exit()

setuptools.setup(name='GMaKE',
                 version='0.0.1',
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
                    'emcee'],
                 #dependency_links=[
                 #    'http://github.com/user/repo/tarball/master#egg=package-1.0',],
                 zip_safe=False)


"""
 install local editable
     pip3 install --user -e .
 
 pypi:
     python3 -m pip install --user --upgrade setuptools wheel
     pip3 install --user --upgrade setuptools wheel
     python3 setup.py sdist #bdist_wheel
     twine upload dist/*
     python3 setup.py --help-commands
     
 usage:
 
     >import gmake
     >help(gmake.gmake_read_data)
     >print(gmake.gmake_read_data()) 
"""