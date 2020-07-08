"""source model: analytic form"""

from astropy.modeling import models as apmodels

def analytic_from_apmodels(obj):
    """
    type='apmodel'
    """
    obj['apmodel']=getattr(apmodels,obj['sbProf'][0])(*((1,)+obj['sbProf'][1:]))
    obj['apmodel_flux']=obj['contflux'] 
    
def analytic_from_point(obj):
    
def xy_render_point(objs,w,):
    
    
def uv_render_point()




:

def analytic_from_obj(obj,
                    nc=100000,nv=20,seeds=[None,None,None,None]):
    
    
    obj['apmodel']=getattr(apmodels,obj['sbProf'][0])(*((1,)+obj['sbProf'][1:]))
    obj['apmodel_flux']=obj['contflux']      
    
    if  obj['type']=='disk3d':
        clouds_from_disk3d(obj,nc=nc,nv=nv,seeds=seeds)
    
    if  obj['type']=='point':
        clouds_from_point(obj)
    
    return