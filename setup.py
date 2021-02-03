#!/usr/bin/env python

# encoding: utf-8


# Workaround: 
#   See https://github.com/pypa/pip/issues/7953

import site
import sys
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]


"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Rui Xue",
    author_email='rx.astro@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Python package for simulating and modeling astronomical sources from radio interferometric observations",
# uvrx: A small Python library that provides a collection of utility functions helping process, analyze, and plot interferometry visibility data.",    
    entry_points={
        'console_scripts': [
            'ism3d = ism3d.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ism3d',
    name='ism3d',
    packages=find_packages(include=['ism3d', 'ism3d.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/r-xue/ism3d',
    version='0.3.dev1',
    zip_safe=False
)
