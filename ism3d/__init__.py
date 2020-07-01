"""Top-level package for ism3d."""

__author__ = """Rui Xue"""
__email__ = 'rx.astro@gmail.com'
__version__ = '0.3.dev1'

############################################

import os
import pkg_resources

"""
about version id: 
    https://www.python.org/dev/peps/pep-0440/
"""

__version__ = pkg_resources.get_distribution('ism3d').version
__email__ = 'rx.astro@gmail.com'
__author__ = 'Rui Xue'
__credits__ = 'University of Iowa'
__tests__ = os.path.dirname(os.path.abspath(__file__))+'/tests/'
__demo__ = os.path.dirname(os.path.abspath(__file__))+'/../examples/'
__demodata__ = os.path.dirname(os.path.abspath(__file__))+'/../examples/data/'
__resource__ = os.path.dirname(os.path.abspath(__file__))+'/resource/'



from .logger import logger_config, logger_status
logger_config(logfile=None,loglevel='INFO',logfilelevel='INFO',reset=True)

from .utils.misc import check_config

from .utils import *
#from .logger import *
#from .io import *
#from .evaluate import *  
#from .opt import *
#from .analyze import *
#from .dynamics import *
#from .discretize import *
#from .model import *
#from .vis_utils import *
#from .meta import *

__all__ = []

# from .ism3d_logger import *
# from .ism3d_init import *  
# #from .ism3d_utils import *
# 
# from .model_eval import *
# from .model_func import *
# from .model_func_kinms import *
# from .model_func_dynamics import *
# import casa_proc
# 
# from .fit_utils import *
# from .fit_emcee import *
# from .fit_amoeba import *
# from .fit_mpfit import *
# from .fit_lmfit import *
# 
# from .ms_utils import *
# from .io_utils import *
# #from casa_proc import casa_script
# from .plt_utils import * 
# 

try:
    import mkl_fft._numpy_fft as fft_use
    import mkl
    import mkl_random
    from scipy.fft import next_fast_len as fft_fastlen
    # we must do a trial at least once to avoid downstream problem from galario
    # not sure why at this moment
    # fft_use.fftn(1)# doesn't work
    # import mkl_random # work
    # fft_use.fftn(np.ones(1)) # work
    mkl.verbose(0)
    import mkl_fft._scipy_fft_backend as mkl_be
except NameError:
    try:
        import pyfftw.interfaces.numpy_fft as fft_use
        from pyfftw import next_fast_len as fft_fastlen
    except NameError:
        """
        Note:
            latestscipy.fft & numpy.fft are using different implementaions of pocketfft
            scipy.fft seems to be slightly faster and has a more clear interface  
        refs:
            https://github.com/scipy/scipy/issues/10175
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.next_fast_len.html
        """
        import scipy.fft as fft_use
        from scipy.fft import next_fast_len as fft_fastlen
        #import numpy.fft as fft_use
        #logger.debug("use numpy.fft for convolve_fft")