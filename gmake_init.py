#import matplotlib.pyplot as plt
#import numpy as np
#from galpy.potential import MiyamotoNagaiPotential
#from galpy.potential import KeplerPotential
from __future__ import print_function
from past.builtins import execfile

import uuid
import random
import copy
import sys

import numpy as np

from astropy.cosmology import Planck13


#import reikna.cluda as cluda
#from reikna.cluda import any_api
#import reikna.fft as cluda_fft
#import pyopencl as cl
#import pyopencl.array as cla
#import gpyfft.fft as gpyfft_fft

from reikna.cluda import dtypes, any_api
from reikna.core import Annotation, Type, Transformation, Parameter
import scipy.integrate
import astropy.units as u
from tqdm import tqdm as tqdm
import scipy.stats
from spectral_cube import SpectralCube

#import gala.integrate as gi
#import gala.dynamics as gd
#import gala.potential as gp
#from gala.units import galactic
#from gala.potential.scf import compute_coeffs, compute_coeffs_discrete

from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from astropy.wcs.utils import skycoord_to_pixel
import scipy.constants as const
import time
from astropy.modeling.models import Sersic2D
from astropy.modeling.models import Sersic1D
from astropy.modeling.models import Gaussian2D
from astropy.coordinates import SkyCoord
from scipy.interpolate import interp1d
from scipy import interpolate
import scipy.stats 
import os
import emcee

#import cPickle as pickle
from reproject import reproject_interp
import matplotlib
#from astropy.io.fits.diff import indent
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import subprocess
import corner
from copy import deepcopy
from astropy.io import ascii
import fnmatch
import pprint
import fitsio
import shutil
#import commands
import multiprocessing

#import FITS_tools
from past.builtins import map
from astropy.convolution import convolve_fft
from astropy.convolution import convolve
from astropy.convolution import discretize_model
#   FFT related
import scipy.fftpack 
import pyfftw #pyfftw3 doesn't work
#pyfftw.config.NUM_THREADS = 1#multiprocessing.cpu_count()
#pyfftw.interfaces.cache.enable()

###
#   Note:
#       not sure why?
#       but I need to run mkl_fft.fft() before import galpy
#       to get mkl_fft working properly
###
import mkl_fft
rng = np.random.RandomState(42)
# X_c = rng.rand(16,16, 1).astype(np.complex128)
# X_f = X_c.astype(X_c.dtype, order='F')
# np.abs(np.fft.fft2(X_c, axes=(0, 1))).max()
# np.abs(mkl_fft.fft2(X_c, axes=(0, 1))).max()
# np.abs(scipy.fftpack.fft2(X_c, axes=(0, 1))).max()
X_c = rng.rand(16).astype(np.complex128)
X_f = X_c.astype(X_c.dtype, order='F')
np.abs(np.fft.fft(X_c).max())
np.abs(mkl_fft.fft(X_c).max())
np.abs(scipy.fftpack.fft(X_c).max())



# turn off THREADS
#export OMP_NUM_THREADS=8
#export MKL_NUM_THREADS=8
#import reikna.fft
import re
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
#import numpy as np 
import matplotlib.pyplot as plt 
import corner 
from astropy.convolution import convolve, Gaussian1DKernel
from astropy.io import fits 
import scipy.integrate as integrate
from scipy.interpolate import Rbf
from scipy.interpolate import interpn
from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans, convolve
from scipy.ndimage.interpolation import shift
from scipy import stats
from astropy.table import Table
from astropy.table import Column
import astropy.convolution as conv
import FITS_tools
from scipy._lib._numpy_compat import suppress_warnings
np.warnings.filterwarnings('ignore')
from lmfit import minimize, Parameters

try:
    from numpy.core.multiarray_tests import internal_overlap
except ImportError:
    # Module has been renamed in NumPy 1.15
    from numpy.core._multiarray_tests import internal_overlap
    
import galpy.potential as galpy_pot



#from KinMS import KinMS
execfile('/Users/Rui/Dropbox/Worklib/progs/KinMSpy/KinMS.py')
execfile('/Users/Rui/Dropbox/Worklib/projects/xlibpy/xlib/amoeba_sa.py')
execfile('/Users/Rui/Dropbox/Worklib/projects/xlibpy/xlib/amoeba_sa.py')
#execfile('/Users/Rui/Library/Python/2.7/lib/python/site-packages/mgefit/cap_mpfit.py')

execfile('gmake_model_func.py')
execfile('gmake_model.py')
execfile('gmake_utils.py')
execfile('gmake_emcee.py')
execfile('gmake_amoeba.py')
#execfile('gmake_mpfit.py')
execfile('gmake_lmfit.py')
execfile('gmake_gravity.py')


