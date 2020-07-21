from astropy.modeling import models as apmodels
import astropy.units as u


def get_apmodel2d(obj,px=0,py=0,pscale=1):
    """
    define a astropy.model:
        wrap around the pre-defined 2D models
        https://docs.astropy.org/en/stable/modeling/#pre-defined-models
    
    px,py        model center
    pscale       pixel scale (e.g. kpc per pixel / arcsec per pixel)
    
    Note: model.render is working the pixel-domain
          model.discretize has oversampling capaibility and also work better in the pixel-domain
    """

    apmodel=None
    
    if  not isinstance(obj['sbProf'],(tuple,list)):
        obj['sbProf']=(obj['sbProf'],)
    model_name=obj['sbProf'][0].lower()
    model_par=obj['sbProf'][1:]

    if  model_name == 'airydisk2d':
        radius=(model_par[0]/pscale).value
        apmodel=getattr(apmodels,'AiryDisk2D')(1,px,py,radius)

    if  model_name == 'box2d':
        x_width=(model_par[0]/pscale).value
        y_width=(model_par[1]/pscale).value
        apmodel=getattr(apmodels,'Box2D')(1,px,py,x_width,y_width)

    if  model_name == 'const2d':
        apmodel=getattr(apmodels,'Const2D')(1)

    if  model_name == 'ellipse2d':
        a=(model_par[0]/pscale).value
        b=(model_par[1]/pscale).value
        theta=(model_par[2]+90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,'Ellipse2D')(1, px,py, a, b, theta)

    if  model_name == 'disk2d':
        R_0=(model_par[0]/pscale).value
        apmodel=getattr(apmodels,'Disk2D')(1, px,py, R_0)

    if  model_name == 'gaussian2d':
        x_stddev=(model_par[0]/pscale).value
        y_stddev=(model_par[1]/pscale).value
        theta=(model_par[2]+90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,'Gaussian2D')(1, px,py,x_stddev,y_stddev,theta)
    
    if  model_name == 'planar2d':
        slope_x=(model_par[0]/pscale).value
        slope_y=(model_par[1]/pscale).value
        apmodel=getattr(apmodels,'Planar2D')(slope_x,slope_y,1)
    
    if  model_name == 'sersic2d':
        r_eff=(model_par[0]/pscale).value
        n=model_par[1]
        try:
            ellip=model_par[2]
        except:
            ellip=0
        try:
            theta=(model_par[3]+90*u.deg).to_value(u.rad)
        except:
            theta=(90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,'Sersic2D')(1, r_eff,n,px,py,ellip,theta)   
    
    if  model_name == 'ring2d':
        r_in=(model_par[0]/pscale).value
        width=(model_par[1]/pscale).value
        apmodel=getattr(apmodels,'Ring2D')(1, px,py,r_in,width)

    if  model_name == 'rickerwavelet2d':
        sigma=(model_par[0]/pscale).value
        apmodel=getattr(apmodels,'RickerWavelet2D')(1, px,py,sigma)  

    return apmodel    
    
def eval_apmodel2d(obj,xx,yy,out=None):
    """
    obj:         object prescription
    xx,yy,out    evluation coordinates

    currently, the output will have a normalized peak brigtness of one. 
    """
    apmodel=get_apmodel2d(obj,px=0,py=0,pscale=1)
    
    if  out is not None:
        out+=apmodel(xx,yy)
    else:
        out=apmodel(xx,yy)        
    
    return out