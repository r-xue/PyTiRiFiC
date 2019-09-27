#import matplotlib.pyplot as plt
#import numpy as np
#from galpy.potential import MiyamotoNagaiPotential
#from galpy.potential import KeplerPotential
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter("ignore", AstropyWarning)


# Stopping the Python rocketship icon
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from past.builtins import execfile
import uuid
import random
import copy
import sys
import numpy as np
from astropy.cosmology import Planck13
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import logging

from pprint import pformat
from io import StringIO
import io
from asteval import Interpreter
aeval = Interpreter(err_writer=StringIO())

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
from astropy.modeling.models import Rotation2D
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
#matplotlib.use("Agg")
import shlex


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
    
    
from astropy.convolution import discretize_model
#   FFT related
import scipy.fftpack 
import pyfftw #pyfftw3 doesn't work
import ast
from matplotlib.colors import LogNorm
from skimage import transform
#pyfftw.config.NUM_THREADS = 1#multiprocessing.cpu_count()
#pyfftw.interfaces.cache.enable()
###
#   Note:
#       not sure why?
#       but I need to run mkl_fft.fft() before import galpy
#       to get mkl_fft working properly
import mkl_fft
import numexpr as ne
#import numexpr3 as ne3

# rebuilt numpy 1.16.2 scipy 1.2.1 to intel-mkl
#import numpy.distutils.system_info as sysinfo
#sysinfo.get_info('atlas')

#np.__config__.show()
#scipy.show_config()


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
from lmfit import minimize, Parameters, report_fit
try:
    from numpy.core.multiarray_tests import internal_overlap
except ImportError:
    # Module has been renamed in NumPy 1.15
    from numpy.core._multiarray_tests import internal_overlap
    
import galpy.potential as galpy_pot
import glob
from radio_beam import beam, Beam
import matplotlib.ticker as plticker
import matplotlib as mpl
#from yt.mods import ColorTransferFunction, write_bitmap
#import yt
#from yt.frontends.fits.misc import PlotWindowWCS
#yt.toggle_interactivity()
#from __builtin__ import False
from astropy.stats import sigma_clipped_stats


mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"

#mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#mpl.rc('font',**{'family':'serif','serif':['Palatino']})
#mpl.rc('text',usetex=True)

import warnings
from spectral_cube.utils import SpectralCubeWarning
warnings.filterwarnings(action='ignore', category=SpectralCubeWarning,append=True)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore")

import aplpy
from pvextractor import Path
from pvextractor import extract_pv_slice
from pvextractor import PathFromCenter

import casacore.tables as ctb



from astropy.io import fits
import numpy as np
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales

from sys import getsizeof
import math
from memory_profiler import profile


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000

import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)
from pip._vendor import pkg_resources

import hickle as hkl
import h5py

from contextlib import redirect_stdout
import socket
from psutil import virtual_memory

from galario.single import threads as galario_threads
#   multi-threading
#       MKL_NUM_THREADS=1
#       export OMP_NUM_THREADS=8
#       export MKL_NUM_THREADS=8
galario_threads(multiprocessing.cpu_count())
