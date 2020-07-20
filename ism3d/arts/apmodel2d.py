from astropy.modeling import models as apmodels
import astropy.units as u

def eval_apmodel2d(obj,xx,yy,out=None):
    """
    obj:         object prescription
    xx,yy,out    evluation coordinates

    currently, the output will have a normalized peak brigtness of one. 
    """
    px=0; py=0; dp=1
    
    if  not isinstance(obj['sbProf'],(tuple,list)):
        obj['sbProf']=(obj['sbProf'],)
    model_name=obj['sbProf'][0]
    model_par=obj['sbProf'][1:]

    if  model_name == 'AiryDisk2D':
        radius=(model_par[0]/dp).value
        apmodel=getattr(apmodels,model_name)(1,px,py,radius)

    if  model_name == 'Box2D':
        x_width=(model_par[0]/dp).value
        y_width=(model_par[1]/dp).value
        apmodel=getattr(apmodels,model_name)(1,px,py,x_width,y_width)

    if  model_name == 'Const2D':
        apmodel=getattr(apmodels,model_name)(1)

    if  model_name == 'Ellipse2D':
        a=(model_par[0]/dp).value
        b=(model_par[1]/dp).value
        theta=(model_par[2]+90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,model_name)(1, px,py, a, b, theta)

    if  model_name == 'Disk2D':
        R_0=(model_par[0]/dp).value
        apmodel=getattr(apmodels,model_name)(1, px,py, R_0)

    if  model_name == 'Gaussian2D':
        x_stddev=(model_par[0]/dp).value
        y_stddev=(model_par[1]/dp).value
        theta=(model_par[2]+90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,model_name)(1, px,py,x_stddev,y_stddev,theta)
    
    if  model_name == 'Planar2D':
        slope_x=(model_par[0]/dp).value
        slope_y=(model_par[1]/dp).value
        apmodel=getattr(apmodels,model_name)(slope_x,slope_y,1)
    
    if  model_name == 'Sersic2D':
        r_eff=(model_par[0]/dp).value
        n=model_par[1]
        try:
            ellip=model_par[2]
        except:
            ellip=0
        try:
            theta=(model_par[3]+90*u.deg).to_value(u.rad)
        except:
            theta=(90*u.deg).to_value(u.rad)
        apmodel=getattr(apmodels,model_name)(1, r_eff,n,px,py,ellip,theta)   
    
    if  model_name == 'Ring2D':
        r_in=(model_par[0]/dp).value
        width=(model_par[1]/dp).value
        apmodel=getattr(apmodels,model_name)(1, px,py,r_in,width)

    if  model_name == 'RickerWavelet2D':
        sigma=(model_par[0]/dp).value
        apmodel=getattr(apmodels,model_name)(1, px,py,sigma)  
    
    if  out is not None:
        out+=apmodel(xx,yy)
    else:
        out=apmodel(xx,yy)        
    
    return out