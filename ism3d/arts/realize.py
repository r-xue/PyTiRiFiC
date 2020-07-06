import numpy as np
from .stats import pdf2rv
from .stats import cdf2rv
from .stats import custom_rvs
from .stats import custom_pdf
import astropy.units as u
import fast_histogram as fh
import pprint

import time
from astropy.coordinates.matrix_utilities import rotation_matrix,matrix_product,matrix_transpose
from astropy.coordinates.representation import SphericalRepresentation, CylindricalRepresentation, CartesianRepresentation
from astropy.coordinates.representation import SphericalDifferential, CylindricalDifferential, CartesianDifferential
from io import StringIO
from asteval import Interpreter
#aeval = Interpreter(err_writer=StringIO())
aeval = Interpreter()
aeval.symtable['u']=u

from .utils import rng_seeded,fft_fastlen,fft_use,eval_func,one_beam,sample_grid
from astropy._erfa import ufunc as erfa_ufunc
from astropy import constants as const

from astropy.modeling.models import Gaussian2D
from astropy.convolution import discretize_model
from .meta import create_header
from astropy.stats import sigma_clipped_stats
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.wcs import WCS
from scipy.interpolate import interpn

import galpy.potential as galpy_pot
from astropy.cosmology import Planck13
from scipy.interpolate import interp1d
import logging
from astropy.modeling import models as apmodels
from .discretize import uv_render, xy_render


logger = logging.getLogger(__name__)


def model_realize(mod_dict,
                  nc=100000,nv=20,seeds=[None,None,None,None]):
    
    """
    attach clouds to "mod_dict"
    This is a wrapper function to attached a cloudlet model from a object-group dict  
    """
    
    # first pass:   build potentials
    
    for objname, obj in mod_dict.items():
        if  'type' not in obj:
            continue
        if  obj['type']!='potential':
            continue
        obj['pots']=potential_fromobj(obj)
        
    # second pass:   attach potential (if requested) and fill cloudlet
    
    clouds_types=['disk3d','disk2d','point']
    
    for objname, obj in mod_dict.items():
        if  'type' not in obj:
            continue
        if  obj['type'] not in clouds_types:
            continue
        # attach potentials
        if  'rcProf' in obj:
            if  obj['rcProf'][0]=='potential':
                obj['pots']=mod_dict[obj['rcProf'][1]]['pots']

        obj['clouds_loc'],obj['clouds_wt']=\
            clouds_fromobj(obj,
                           nc=nc,nv=nv,seeds=seeds)
        
        for fluxtype in ['lineflux','contflux']:
            if  fluxtype in obj:
                obj['clouds_flux']=obj[fluxtype]/obj['clouds_loc'].size
                
    # third pass: insert astropy.modelling.models
    
    for objname, obj in mod_dict.items():
        
        if  'type' not in obj:
            continue
        if  obj['type']!='apmodel':
            continue
        
        obj['apmodel']=getattr(apmodels,obj['sbProf'][0])(*((1,)+obj['sbProf'][1:]))
        obj['apmodel_flux']=obj['contflux']  
        
    return   


# def model_realize(mod_dct,
#                 nc=100000,nv=20,seeds=[None,None,None,None]):
#     
#     """
#     attach clouds to "mod_dct"
#     This is a wrapper function to attached a cloudlet model from a object-group dict  
#     """
#     
#     # first pass:   build potentials
#     
#     for objname, obj in mod_dct.items():
#         if  'type' not in obj:
#             continue
#         if  obj['type']!='potential':
#             continue
#         obj['pots']=potential_fromobj(obj)
#         
#     # second pass:   attach potential (if requested) and fill cloudlet
#     
#     clouds_types=['disk3d','disk2d','point']
#     
#     for objname, obj in mod_dct.items():
#         if  'type' not in obj:
#             continue
#         if  obj['type'] not in clouds_types:
#             continue
#         # attach potentials
#         if  'rcProf' in obj:
#             if  obj['rcProf'][0]=='potential':
#                 obj['pots']=mod_dct[obj['rcProf'][1]]['pots']
# 
#         obj['clouds_loc'],obj['clouds_wt']=\
#             clouds_fromobj(obj,
#                            nc=nc,nv=nv,seeds=seeds)
#         
#         for fluxtype in ['lineflux','contflux']:
#             if  fluxtype in obj:
#                 obj['clouds_flux']=obj[fluxtype]/obj['clouds_loc'].size
#                 
#     # third pass: insert astropy.modelling.models
#     
#     for objname, obj in mod_dct.items():
#         
#         if  'type' not in obj:
#             continue
#         if  obj['type']!='apmodel':
#             continue
#         
#         obj['apmodel']=getattr(apmodels,obj['sbProf'][0])(*((1,)+obj['sbProf'][1:]))
#         obj['apmodel_flux']=obj['contflux']  
#         
#     return   