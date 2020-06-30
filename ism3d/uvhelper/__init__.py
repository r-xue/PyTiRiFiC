"""Top-level package for uvrx."""

__author__ = """Rui Xue"""
__email__ = 'rx.astro@gmail.com'
__version__ = '0.1.dev1'

from .logger import logger_config
logger_config(logfile=None,loglevel='DEBUG',logfilelevel='DEBUG',reset=True)

from .imager import *
from .proc import *
from .ft import *

#__all__ = ['logger']

#__all__ = ['SpectralCube', 'VaryingResolutionSpectralCube',
#            'StokesSpectralCube', 'CompositeMask', 'LazyComparisonMask',
#            'LazyMask', 'BooleanArrayMask', 'FunctionMask',
#            'OneDSpectrum', 'Projection', 'Slice'
#            ]