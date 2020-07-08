import numpy as np

from ..maths.stats import pdf2rv, cdf2rv, custom_rvs, custom_pdf

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

#from .utils import rng_seeded,fft_fastlen,fft_use,eval_func,one_beam,sample_grid
from astropy._erfa import ufunc as erfa_ufunc
from astropy import constants as const

from astropy.modeling.models import Gaussian2D
from astropy.convolution import discretize_model
#from .meta import create_header
from astropy.stats import sigma_clipped_stats
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.wcs import WCS
from scipy.interpolate import interpn

import galpy.potential as galpy_pot
from astropy.cosmology import Planck13
from scipy.interpolate import interp1d
import logging
from astropy.modeling import models as apmodels
#from .discretize import uv_render, xy_render


logger = logging.getLogger(__name__)


import numpy as np
from ..maths.stats import pdf2rv, cdf2rv, custom_rvs, custom_pdf
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

#from .utils import rng_seeded,fft_fastlen,fft_use,eval_func,one_beam,sample_grid
from astropy._erfa import ufunc as erfa_ufunc
from astropy import constants as const

from astropy.modeling.models import Gaussian2D
from astropy.convolution import discretize_model
#from .meta import create_header
from astropy.stats import sigma_clipped_stats
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.wcs import WCS
from scipy.interpolate import interpn

import galpy.potential as galpy_pot
from astropy.cosmology import Planck13
from scipy.interpolate import interp1d
import logging
from astropy.modeling import models as apmodels
#from .discretize import uv_render, xy_render

from ..arts.sparse import clouds_from_obj

logger = logging.getLogger(__name__)

"""
    Note: 
        performance on Quanitu/Units
        https://docs.astropy.org/en/stable/units/#performance-tips
        https://docs.astropy.org/en/stable/units/quantity.html#astropy-units-quantity-no-copy
        https://docs.astropy.org/en/stable/units/quantity.html (add functiomn argument check)
        
    .xyz / .d_xyz is not effecient as it's combined on-the-fly
    .d_xyz
"""

def model_setup(mod_dct,dat_dct,verbose=False):
    """
    create model container 
        this function can be ran only once before starting fitting iteration, so that
        the memory allocation/ allication will happen once during a fitting run.
        The output will provide the dataframework where the reference model can be mapped into.
        
    it will also initilize some informationed used for modeling (e.g. sampling array / header / WCS)

    notes on evaluating efficiency:
    
        While building the intrinsic data-model from a physical model can be expensive,
        the simulated observation (2D/3D convolution) is usually the bottle-neck.
        
        some tips to improve the effeciency:
            + exclude empty (masked/flux=0) region for the convolution
            + joint all objects in the intrinsic model before the convolution, e.g.
                overlapping objects, lines
            + use to low-dimension convolution when possible (e.g. for the narrow-band continumm) 
            
        before splitting line & cont models:
            --- apicall   : 2.10178  seconds ---
        after splitting line & cont models:
            --- apicall   : 0.84662  seconds ---
    note: imod2d                : Hold emission componnets with Frequency-Dependent Spatial Distribution
          imod3d                : Hold emission conponents with Frequency-Dependent Spatial Distribution
          imodel=imod2d+imod3d  : We always keep a copy of imod2d and imod3d to improve the effeicnecy in simobs() 

          uvmodel: np.complex64
           imodel:  np.float32
                              
    """

            
    models={}
                
    for tag in list(mod_dct.keys()):
        
        obj=mod_dct[tag]
        
        if  verbose==True:
            print("+"*40); print('@',tag); print('type:',obj['type']) ; print("-"*40)

        if  'vis' in mod_dct[tag].keys():
            
            vis_list=mod_dct[tag]['vis'].split(",")
            
            for vis in vis_list:
                
                if  'type@'+vis not in models.keys():
                    
                    models['type@'+vis]=dat_dct['type@'+vis]
                    
                    if  'pbeam@'+vis not in dat_dct:
                        logger.debug('make imaging-header / pb model for:'+vis)
                        antsize=12*u.m
                        if  'VLA' in dat_dct['telescope@'+vis]:
                            antsize=25*u.m
                        if  'ALMA' in dat_dct['telescope@'+vis]:
                            antsize=12*u.m
                        #   pass the data reference (no memory penalty)
                        
                        #or [obj['xypos'].ra,obj['xypos'].dec]
                        center=dat_dct['phasecenter@'+vis]
                        # right now we are using the first object RA/DEC to make reference model imaging center
                        # also we hard-code the antenna size to 25*u.m
                        #center=[obj['xypos'].ra,obj['xypos'].dec]                                                    
                        
                        models['header@'+vis]=uv_to_header(dat_dct['uvw@'+vis],center,
                                                         dat_dct['chanfreq@'+vis],
                                                         dat_dct['chanwidth@'+vis])
                        models['pbeam@'+vis]=((makepb(models['header@'+vis],
                                                      phasecenter=dat_dct['phasecenter@'+vis],
                                                      antsize=antsize)).astype(np.float32)) #[np.newaxis,np.newaxis,:,:]
                    else:
                        models['header@'+vis]=dat_dct['header@'+vis]
                        models['pbeam@'+vis]=dat_dct['pbeam@'+vis]
                    
                    models['wcs@'+vis]=WCS(models['header@'+vis])
                    
                    #naxis=(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])
                    
                    models['imodel@'+vis]=None
                    models['objs@'+vis]=[]                  
                
                # get a lookup table when looping over dataset.
                if  obj['type']=='disk3d':
                    models['objs@'+vis].append(tag)
                
                """
                obj['pmodel']=None
                obj['pheader']=None
                if  'pmodel@'+tag in dat_dct.keys():
                    obj['pmodel']=dat_dct['pmodel@'+tag]
                    obj['pheader']=dat_dct['pheader@'+tag]
                """ 
        if  'image' in mod_dct[tag].keys():
            
            image_list=mod_dct[tag]['image'].split(",")
            
            for image in image_list:
                
                if  'data@'+image not in models.keys():
                    
                    models['type@'+image]=dat_dct['type@'+image]
                    #test_time = time.time()
                    models['header@'+image]=dat_dct['header@'+image]
                    models['wcs@'+image]=WCS(models['header@'+image])
                    models['data@'+image]=dat_dct['data@'+image]
                    
                    if  'error@'+image not in dat_dct:
                        models['error@'+image]=(sigma_clipped_stats(dat_dct['data@'+image], sigma=3, maxiters=1))[2]+\
                            dat_dct['data@'+image]*0.0                
                    else:
                        models['error@'+image]=dat_dct['error@'+image]
                    
                    if  'sample@'+image in dat_dct.keys():
                        models['mask@'+image]=dat_dct['mask@'+image]
                    else:
                        models['mask@'+image]=None
                                    
                    if  'pbeam@'+image in dat_dct.keys():
                        models['pbeam@'+image]=dat_dct['pbeam@'+image]
                    else:
                        models['pbeam@'+image]=None                    
                    
                    dshape=dat_dct['data@'+image].shape
                    header=dat_dct['header@'+image]
                    cell=np.sqrt(abs(header['CDELT1']*header['CDELT2']))                   
                    if  'psf@'+image in dat_dct.keys():
                        if  isinstance(dat_dct['psf@'+image],tuple):
                            beam=dat_dct['psf@'+image]
                            models['psf@'+image]=makepsf(header,beam=dat_dct['psf@'+image])
                        else:
                            models['psf@'+image]=dat_dct['psf@'+image]
                    else:
                        models['psf@'+image]=makepsf(header)
                        
                    #   sampling array
                    
                    if  'sample@'+image in dat_dct.keys():
                        models['sample@'+image]=dat_dct['sample@'+image]
                    else:
                        beam0=one_beam(image)
                        bmaj=beam0.major.to_value(u.deg)
                        bmin=beam0.minor.to_value(u.deg)
                        bpa=beam0.pa
                        xx_hexgrid,yy_hexgrid=sample_grid(bmaj/cell,
                                                          xrange=[0,dshape[-1]-1],
                                                          yrange=[0,dshape[-2]-1],
                                                          ratio=bmaj/bmin,angle=bpa)
                        nsp=xx_hexgrid.size
                        xx_hexgrid=(np.broadcast_to( xx_hexgrid[:,None], (nsp,dshape[-3]))).flatten()
                        yy_hexgrid=(np.broadcast_to( yy_hexgrid[:,None], (nsp,dshape[-3]))).flatten()
                        zz_hexgrid=(np.broadcast_to( (np.arange(dshape[-3]))[None,:], (nsp,dshape[-3]) )).flatten()
                        models['sample@'+image]=( np.vstack((xx_hexgrid,yy_hexgrid,zz_hexgrid)) ).T
                        
                        sp=models['sample@'+image]
                    if  models['sample@'+image] is not None:
                        models['data-sp@'+image]=interpn( (np.arange(dshape[-3]),np.arange(dshape[-2]),np.arange(dshape[-1])),
                                                          np.squeeze(models['data@'+image]),
                                                          models['sample@'+image][:,::-1],method='linear')
                        models['error-sp@'+image]=interpn( (np.arange(dshape[-3]),np.arange(dshape[-2]),np.arange(dshape[-1])),
                                                          np.squeeze(models['error@'+image]),
                                                          models['sample@'+image][:,::-1],method='linear')                        
                        
                    naxis=models['data@'+image].shape
                    if  len(naxis)==3:
                        naxis=(1,)+naxis
                        
                    models['imodel@'+image]=None
                    models['objs@'+image]=[]
                
                if  mod_dct[tag]['type']=='disk3d':                    
                    models['objs@'+image].append(tag) 
                
                """           
                models['imodel@'+image]=np.zeros(naxis)
                models['cmodel@'+image]=np.zeros(naxis)
                    #   save 2d objects (even it has been broadcasted to 3D for spectral cube)
                    #   save 3D objects (like spectral line emission from kinmspy/tirific)
                models['imod2d@'+image]=np.zeros(naxis)
                models['imod3d@'+image]=np.zeros(naxis)
                #print("---{0:^10} : {1:<8.5f} seconds ---".format('import:'+image,time.time() - test_time))            
                """
    
    return models


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
        
        clouds_from_obj(obj,
                       nc=nc,nv=nv,seeds=seeds)

                
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

def model_render(mod_dct, dat_dct, models=None,
                 saveimodel=False,verbose=False):
    """render component models into the data model container.
    
    Parameters
    ----------
    mod_dct : dict
        component container with realized reference models in physical units
    dat_dct : dict
        data container
    models : dict, optional
        model container
    
    Returns
    -------
    models : dict
        model container with rendered model inside
    
    """
    
    # build the model container (usually skipped during iterative optimization)
    
    if  models is None:
        models=model_setup(mod_dct,dat_dct,verbose=verbose)

    # calculate chisq 
           
    for tag in list(models.keys()):
        
        if  'imodel@' in tag:
            
            dname=tag.replace('imodel@','')
            objs=[mod_dct[obj] for obj in models[tag.replace('imodel@','objs@')]]
            w=models['wcs@'+dname]
            if  models[tag.replace('imodel@','type@')]=='vis':                
                model_one=uv_render(objs,w,
                                    dat_dct['uvw@'+dname],
                                    dat_dct['phasecenter@'+dname],
                                    pb=models['pbeam@'+dname])
            if  models[tag.replace('imodel@','type@')]=='image':
                imodel,model_one=xy_render(objs,w,
                                    psf=models['psf@'+dname],normalize_kernel=False,
                                    pb=models['pbeam@'+dname])

            models['model@'+dname]=model_one
            
            if  saveimodel==True:
                if  models[tag.replace('imodel@','type@')]=='vis': 
                    imodel=xy_render(objs,w,
                                    normalize_kernel=False)                    
                models['imodel@'+dname]=imodel
                
    return models

###################################################################################################

    