import os

# version id: 
#   https://www.python.org/dev/peps/pep-0440/

__version__ = '0.1.dev3'
__email__ = 'rx.astro@gmail.com'
__author__ = 'Rui Xue'
__credits__ = 'University of Iowa'
__demo__ = os.path.dirname(os.path.abspath(__file__))


from .gmake_logger import *
from .gmake_init import *  
#from .gmake_utils import *

from .model_eval import *
from .model_func import *
from .model_func_kinms import *
from .model_func_dynamics import *
import casa_proc

from .fit_utils import *
from .fit_emcee import *
from .fit_amoeba import *
from .fit_mpfit import *
from .fit_lmfit import *

from .ms_utils import *
from .io_utils import *
#from casa_proc import casa_script
from .plt_utils import * 

logger_config(logfile=None,loglevel='DEBUG',logfilelevel='DEBUG',reset=True)

