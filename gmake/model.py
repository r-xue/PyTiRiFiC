import numpy as np
from .stats import pdf2rv
from .stats import cdf2rv
from .stats import custom_rvs
from .stats import custom_pdf
import astropy.units as u
import fast_histogram as fh
import pprint
from .utils import eval_func
from .utils import one_beam
from .utils import sample_grid

import time
from astropy.coordinates.matrix_utilities import rotation_matrix,matrix_product,matrix_transpose
from astropy.coordinates.representation import SphericalRepresentation, CylindricalRepresentation, CartesianRepresentation
from astropy.coordinates.representation import SphericalDifferential, CylindricalDifferential, CartesianDifferential
from io import StringIO
from asteval import Interpreter
#aeval = Interpreter(err_writer=StringIO())
aeval = Interpreter()
aeval.symtable['u']=u

from .utils import rng_seeded
from astropy._erfa import ufunc as erfa_ufunc
from astropy import constants as const


from .utils import fft_use
from galario.single import get_image_size



from astropy.modeling.models import Gaussian2D
from astropy.convolution import discretize_model
from .meta import create_header
from astropy.stats import sigma_clipped_stats
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.wcs import WCS
from scipy.interpolate import interpn

import logging
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




def cr_tanh(r,r_in=None,r_out=None,
              theta_out=90*u.deg):
    """
    See Peng+2010 Appendix A. with some scaling correction
    """
    cdef=(20*u.deg).to(u.rad).value
    A=2*cdef/np.abs(theta_out.to(u.rad).value)-1
    B=(2.-np.arctanh(A))*r_out/(r_out-r_in)
    
    return 0.5*(np.tanh((B*(r/r_out-1)+2.)*u.rad)+1.)

def clouds_morph(sbProf,fmPhi=None,fmRho=None,geRho=None,bmY=None,sbQ=None,rotPhi=None,sbPA=None,
                 vbProf=None,
                 size=100000,
                 seeds=[0,1,2],cmode=1):
    """
    cloudlet generator for a 3D disk model
    
    Face-on surface brightness profile, e.g.
            sbProf=('sersic2d',r_e,sersic_n)
            sbProf=('expon2d',r_s)
            sbProf=('norm2d',r_sigma)
            sbProf=('table',rho_quantity,sb_quantity)      # A table, which will be used for liner interepretation
            sbProf=('point')                               # A Point Source
            sbProf=('rho : maximum(1-rho/p1,0.0)',5*u.kpc) # A "Lambda" function defined by three pieces of information:
                                                                + variable: e.g. rho
                                                                + Expression: e.g. maximum(1-rho/p1,0.0)
                                                                + Parameters: e.g. P1, P2... 
            
    Face-on surface brightness model (not implemented), e.g,
    
            xyProf=('x,y : np.exp(-(x^3+y^3')))
            xyProf=('image','model.fits',[[x_min,x_max],[y_min,y_max]])
    
    Additional manupliation:
    
        fmPhi:   Add the Fourier perturbarion along the Azimuth direction
                 the mean surface brightness is still preserved
                 tuple (mode,amplitude,phi_m) 
                     phi_m is the phase angle from (x, or semimajor axis)
                     amplitude is normalized (0<amp<=1)
                 e.g. fmPhi=(2,0.5,30*u.deg)
        
        fmRho/gePho:   
                 Add the Fourier peryurnation and Az-dependence stretching along the radial direction
                 the mean surface brightness is not preserved in the traditional sense
                 fmRho has a similar but not equiavelent affect as fmPhi
                 gePho will control the boxyness of the isophoto contour
                 see Peng+2010 for more details
                 fmRho (mode,amplititde,phi_m) : fmRho=(2,0.5,30*u.deg)
                 geRho C0
                 note: turn on both parameters will slightly slow down the function as
                    numerical intergation is involved
        bmY:
                bending mode as Peng+2010
                bmY Tuple (model,amplitude)
        sbQ:
                the ellipse b/a ratio
        rotPhi:
                see peng+2010 coordinate rotation using alpha-tanh or log-tanh
                this is useful for generateing spiral structures
 
        sbPA:
                ccw Rotate the enture system by sbPA
                
    
    Verticle brightness Structure, e.g.

            vbProf=('sech',zh)
            vbProf=('sech2',zh)
            vbProf=('laplace',zs)
            vbProf=None

    seeds:     3-element vector containing the seeds of random number generators
    
    cmode:     adjust weights for each cloudlet:
        
        https://www.astro.rug.nl/~gipsy/tsk/galmod.dc1
        https://buildmedia.readthedocs.org/media/pdf/bbarolo/latest/bbarolo.pdf
        see cmode
        cmode=0, roughly even number density of cloudlets across the entire "restricted" 3D space.
                 so the discretzation noise will be prop to brightness in each volume 
        cmode=1, the number density of cloudlets is prop to brightness density
                 each cloud will have the same weight. therefore 
                 discretization noise will be prop to square root of cloudnumber
    
    return:
    
        cloudlet positions in astropy.coordinates.representation.CylindiralRepresentation
        The coordinates are presented with the surface-brightness center as origin in the plane of the disc
    
    """
    ###################################
    # radial structure
    ###################################
    weights=None
    cloudmeta={}
    
    if  isinstance(sbProf,(tuple,list)):
        # you'better have sbRad begin with zero, otherwise, the center may have a "hole" spot.
        #   note: for non sersic2d, sersic_n will be skipped anyway in custom_pdf()
        #         even you gave a non-sense number of sbProf[-1]  
        if  cmode==0:
            rho_max=5
            rho = custom_rvs('uniform2d',size=size,seed=seeds[0])*rho_max # got out to r_e*rho_max
            weights= custom_pdf(sbProf[0].replace('2d',''),rho,sersic_n=sbProf[-1])
            rho = rho*sbProf[1]
        if  cmode==1:
            rho = custom_rvs(sbProf[0],size=size,sersic_n=sbProf[-1],seed=seeds[0])*sbProf[1]
            cloudmeta['localSB']=custom_pdf(sbProf[0].replace('2d',''),rho/sbProf[1],sersic_n=sbProf[-1])
        if  cmode==2:
            rho = custom_rvs(sbProf[0],size=size,sersic_n=sbProf[-1],seed=seeds[0])*sbProf[1]
            # the exp dependency makes the scaling equiavelent to addition weight on PDF  
            if  sbProf[0]=='expon2d':   rho*=0.5    
            if  sbProf[0]=='sersic2d':  rho*=0.5**sbProf[-1]
            if  sbProf[0]=='norm2d':  rho*=0.5**0.5   
            weights=1/custom_pdf(sbProf[0].replace('2d',''),rho/sbProf[1],sersic_n=sbProf[-1])
    else:
        # likely vector sampling array
        if  cmode==0:
            rho = custom_rvs('uniform2d',size=size,seed=seeds[0])*np.max(sbRad)
            weights = np.interp(rho,np.abs(sbRad),sbProf)
        if  cmode==1:
            pdf_x = np.abs(sbRad)
            pdf_y = sbProf*np.abs(sbRad)
            rho = pdf2rv(pdf_x,pdf_y,seed=seeds[0],size=size)

    ###################################
    # verticle structure
    ###################################
    
    if  vbProf is None:
        z=rho*0.0
    else:
        if  cmode==0:
            z_max=10
            z=custom_rvs('uniform',size=size,seed=seeds[2])*z_max
            weights*= custom_pdf(vbProf[0],z)
            z = z*vbProf[1]
        if  cmode==1:
            z=custom_rvs(vbProf[0],size=size,seed=seeds[2])*vbProf[1]
        if  cmode==2:
            z=custom_rvs(vbProf[0],size=size,seed=seeds[2])*vbProf[1]
            if  vbProf[0]=='norm':   z*=0.5**0.5
            if  vbProf[0]=='expon':   z*=0.5
            if  vbProf[0]=='sech':  z=custom_rvs(vbProf[0]+'2',size=size,seed=seeds[2])*vbProf[1]
            if  vbProf[0]!='sech2': weights/= custom_pdf(vbProf[0],(z/vbProf[1]).value)

    ###################################
    # AZ structure + additional coordinate transtform
    ###################################    
    """
    Fourier Modes or Uniform along Azimuth
        need to solve: https://en.wikipedia.org/wiki/Kepler%27s_equation
        sbProf stll represent the mean flux density along rings although a perturbation in brightness is introduced
        This phi_Fourier Modes were used in TiriFic (also or see D. Zarisky+2013)
    """
    rng,is_mkl = rng_seeded(seeds[1])
    if  fmPhi is not None:
        m=fmPhi[0]
        am=fmPhi[1]        
        phim=fmPhi[2]
        phi_tb=np.linspace(0,2*np.pi,1000)
        cdf_tb=1/2/np.pi*(phi_tb+am/m*np.sin(m*phi_tb))
        phi=cdf2rv(phi_tb,cdf_tb,size=size,seed=seeds[2])*u.rad+phim
    else:
        if  is_mkl:
            phi = rng.uniform(low=0,high=2*np.pi,size=size)<<u.rad
        else:
            phi = (2*np.pi)*rng.random(size)<<u.rad
    """
    Generalized ellipse + Fourier Modes along Rho (see Galfit3)

        scaling R has a consequence of boosting local brightness to Scale^2.0
        so each iso-"R" circle will contain the same flux fraction (CDF) as the iso-"R" increase,
        but the local brightness at each transformed "R" circle doesn't keep the same
        as simply transfer X or Y
        trasnfer X or Y, local surface brightness will      
    """
    if  fmRho is not None or geRho is not None:
        if  fmRho is not None:
            m=fmRho[0]
            am=fmPhi[1]        
            phim=fmPhi[2]
        else:
            m=1
            am=0.0
            phim=0*u.deg
        if  geRho is not None:
            c0=geRho[0]
        else:
            c0=0
        q=1
        phi_tb=np.linspace(0,360,360)*u.deg
        rho_scale=((np.abs(np.cos(phi_tb)))**(c0+2)+(np.abs(np.sin(phi_tb))/q)**(c0+2))**(1/(c0+2))
        rho_scale/=1+a_m*np.cos(m*(phi_tb+phi_m))                                     
        pdf_tb=1/rho_scale**2
        phi=pdf2rv(phi_tb,pdf_tb,size=size)
        rho/=((np.abs(np.cos(phi)))**(c0+2)+(np.abs(np.sin(phi))/q)**(c0+2))**(1/(c0+2))        
        rho/=1+a_m*np.cos(m*(phi+phim))
        # another way to do this is that scale rho and scale weight; then it's not cmode=1 anymore
        #rho/=((np.abs(np.cos(phi)))**(c0+2)+(np.abs(np.sin(phi))/q)**(c0+2))**(1/(c0+2))
        #weights=weights/((np.abs(np.cos(phi)))**(c0+2)+(np.abs(np.sin(phi))/q)**(c0+2))**(2/(c0+2))        
    
    
    
    cyl=CylindricalRepresentation(rho,phi,z)
    car=cyl.represent_as(CartesianRepresentation)      
    
    """
    cordinate strecth q=b/a
    """
    if  sbQ is not None:
        car=CartesianRepresentation(car.x,car.y*sbQ,car.z)
        cyl=car.represent_as(CylindricalRepresentation) 
    
    """
    CoordRot - Hyperbolic
    """
    if  rotPhi is not None:
        r_in=rotPhi[1]
        r_out=rotPhi[2]
        phi_out=rotPhi[3]
        if  rotPhi[0]=='alpha':
            cr_alpha=rotPhi[4]            
            phi_offset=phi_out*cr_tanh(cyl.rho,r_in=r_in,r_out=r_out,theta_out=phi_out)\
                *(0.5*(cyl.rho/r_out+1.))**cr_alpha
        if  rotPhi[0]=='log':
            rws=rotPhi[4]
            phi_offset=phi_out*cr_tanh(cyl.rho,r_in=r_in,r_out=r_out,theta_out=phi_out)\
                *(np.log(cyl.rho/rws+1)/np.log(r_out/rws+1))
        cyl=CylindricalRepresentation(cyl.rho,phi_offset+cyl.phi,cyl.z)
        car=cyl.represent_as(CartesianRepresentation) 
    
    """
    bending model
    """
    if  bmY is not None:
        m=bmY[0]
        am=bmY[1]
        car=CartesianRepresentation(car.x,
                                             car.y+am*sbProf[1]*(car.x/sbProf[1])**m,
                                             car.z)
        cyl=car.represent_as(CylindricalRepresentation)

    """
    coordinate rotation / linear stretch
    align major "axis" from galactic coordinate system in Fig 1.
    """
    if  sbPA is not None:
        cyl=CylindricalRepresentation(cyl.rho,sbPA+cyl.phi,cyl.z)
        car=cyl.represent_as(CartesianRepresentation) 

    cloudmeta['weight']=weights
    return car,cloudmeta

#@profile
def clouds_kin(car,rcProf=None,
               vSigma=None,vRadial=None,nV=10,seed=3,
               return_cloudmeta=False):
    """
    attached 3D velocity components to a cloudlet model

    return cloudmeta data will slow thing down and use more memory
    
    Rotation Curve, e.g.
            rcProf=('table',r_quantity,vrot_quantity)
                r_quatity=np.minimum(sbRad/rmax,1.)*vmax
                vrot_quantity=np.minimum(sbRad/rmax,1.)*vmax
            rcprof=('arctan',v_ch,rad_ch)
            rcprof=('expon',v_ch,rad_ch)
            rcprof=('tanh',v_ch,rad_ch)
            rcProf=('rho : minimum(rho/p2,1.0)*p1',200*u.km/u.s,5*u.kpc)  # an inline function
            
            #rmax=10*u.kpc
            #vmax=300*u.km/u.s
            #rcProf_r=np.arange(0.0,r_eff.value*10.0,r_eff.value/25.0)*r_eff.unit
            #rcProf_v=np.minimum(rcProf_r/rmax,1.)*vmax                
    
    seeds:     the seed of random number generators for velocity components

    subsize:    equivlent to NV in galmod
                this is to ensure velocity dispersion profile is properly simulated 
                in the random process.
    
    return:
    
        cloudlet positions + velocity componnets in astropy.coordinates.representation.CartersianRepresentation
        coordinates are presented with the surface-brightness center as origin in the plane of the disc
    
    """
    
    size=len(car)
    cloudmeta={}
    #   add ordered motion
    
    #start_time = time.time()
    
    if  rcProf is not None:

        # get cyl
        
        cyl=car.represent_as(CylindricalRepresentation)
        rho=cyl.rho
        phi=cyl.phi
        z=cyl.z
       
        # get v_rot table
        if  ' : ' in rcProf[0]:
            v_rot=eval_func(rcProf,locals())            
        if  rcProf[0]=='table':
            v_rot=np.interp(rho,rcProf[1],rcProf[2])
        if  rcProf[0].lower()=='arctan':
            v_rot=rcProf[1]*2.0/np.pi*np.arctan(rho/rcProf[2]*u.rad)
        if  rcProf[0].lower()=='expon':
            v_rot=rcProf[1]*(1-np.exp(-rho/rcProf[2]))
        if  rcProf[0].lower()=='tanh':
            v_rot=rcProf[1]*np.tanh(rho/rcProf[2]*u.rad)        
        
        # get d_phi/d_z/d_rho
        
        d_phi=(v_rot/rho*u.rad).to(u.rad/u.s)
        d_z=np.zeros(len(d_phi))*u.km/u.s
        if  vRadial is not None:
            d_rho=np.zeros(len(d_phi))*u.km/u.s+vRadial
        else:
            d_rho=np.zeros(len(d_phi))*u.km/u.s
        
        cyl_diff=CylindricalDifferential(d_rho,d_phi,d_z)
        cyl=cyl.with_differentials(cyl_diff)
        car=cyl.represent_as(CartesianRepresentation,differential_class=CartesianDifferential)
        
        if  return_cloudmeta==True:
            cloudmeta['v_ordered']=car.differentials['s']    # (3,ncloud)
    
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_test',time.time()-start_time))
    # add random motion
    
    if  vSigma is not None:

        # (3,n_subcloudlets,n_cloudlets)
        # C-order, last dimension goes first
        #rng=Generator(SFC64(seed))
        rng,is_mkl= rng_seeded(seed)
        #vdisp = rng.standard_normal(size=(3,nV,size))*vSigma
        if  is_mkl:
            vdisp=rng.normal(scale=vSigma.value,size=(3,nV,size))<<vSigma.unit # vSigma,1D dispersion not 3D dispersion        
        else:
            vdisp=rng.standard_normal(size=(3,nV,size))*vSigma.value<<vSigma.unit
        
        #np.broadcast_to(car_diff_ordered.d_xyz[:,np.newaxis,:],(3,nV,size),subok=True)
        
        
        if  return_cloudmeta==True:
            cloudmeta['v_random']=CartesianDifferential(vdisp,copy=True)    # (3,nv,ncloud)
            
        vdisp+=car.differentials['s'].d_xyz[:,np.newaxis,:]
        car=CartesianRepresentation(np.broadcast_to(car.xyz[:,np.newaxis,:],(3,nV,size),subok=True),
                                    xyz_axis=0,
                                    differentials=CartesianDifferential(vdisp,copy=True),copy=True)

    
    if  return_cloudmeta==False:
        return car
    else:
        return car,cloudmeta


def clouds_tosky(car,inc,pa,inplace=True):
    """
    transform the cloudlet representation in galactic cartersian system to the on-sky cartersian system
    here:    we assume:
            sky-x align with RA  (increase with RA)
            sky-y align with DEC (increase with DEC)
            sky-z align with LOC (away from observer)
    therefore , dz in the sky system is 
    """
    
    #cloudlet_cyl.with_differentials()
    # rotation_matrix is doing passive rotation = rotating coordinate system
    # and write out new position in new coordintae system
    # so -inc / -pa is used here.
    #rots=opt3 <- opt2 <- opt1
    
    rot_inc= rotation_matrix(inc, 'y')
    rot_pa= rotation_matrix(-pa, 'z')
    rots=matrix_product(rot_pa,rot_inc)
    
    """
    private > public method (x3 performance boost)
        + avoid copying
        + use erfa.rxp
    #cloudlet_car_sky=cloudlet_car.transform(rots)
        https://github.com/astropy/astropy/pull/7639
        astropy/coordinates/representation.py
    """
    
    if  inplace==True:
    
        xyz=car.get_xyz(xyz_axis=-1)    # view
        erfa_ufunc.rxp(rots,xyz,out=xyz)
        
        if  car.differentials:
            d_xyz=car.differentials['s'].get_d_xyz(xyz_axis=-1)
            erfa_ufunc.rxp(rots,d_xyz,out=d_xyz)
        
        return
    
    else:
        
        xyz=car.get_xyz(xyz_axis=-1)    # view
        xyz=erfa_ufunc.rxp(rots,xyz)
    
        if  car.differentials:
            d_xyz=car.differentials['s'].get_d_xyz(xyz_axis=-1)
            d_xyz=erfa_ufunc.rxp(rots,d_xyz)
            return CartesianRepresentation(xyz,xyz_axis=-1,
                                differentials=CartesianDifferential(d_xyz,xyz_axis=-1))  
    
        return CartesianRepresentation(xyz,xyz_axis=-1)


def clouds_discretize_2d(cloudlet,axes=['y','x'],
                           range=[[-1, 1], [-1, 1]], bins=[10,10],
                           weights=None):
    """
    """
    
    xx=np.ravel(cloudlet.__getattribute__(axes[0]).value)
    yy=np.ravel(cloudlet.__getattribute__(axes[1]).value)
    if  weights is None:
        zz=None
    else:
        zz=np.ravel(weights)                 
    image=fh.histogram2d(xx,yy,weights=zz,range=range,bins=bins)
        
    return image

def cloudlet_moms(cloudlet,
                  range=[[-1, 1], [-1, 1]], bins=[10,10],
                  weights=None):

    i_weights=None if weights is None else weights
    dm_i=cloudls_discretize_2d(cloudlet,
                                  axes=['y','x'],
                                  range=range,bins=bins,
                                  weights=i_weights)
    dz=cloudlet.differentials['s'].d_z.value
    
    iv_weights=dz if weights is None else weights*dz
    dm_iv=cloudls_discretize_2d(cloudlet,
                              axes=['y','x'],
                              range=range, bins=bins,
                              weights=iv_weights)
    np.seterr(invalid='ignore')
    dm_v=dm_iv/dm_i
    np.seterr(invalid=None)
    
    ivv_weights=dz**2 if weights is None else weights*dz**2
    dm_ivv=cloudls_discretize_2d(cloudlet,
                              axes=['y','x'],
                              range=range, bins=bins,
                              weights=ivv_weights)    
    dm_vsigma=np.sqrt((dm_ivv-dm_i*dm_v**2)/dm_i)

    dm_n=cloudls_discretize_2d(cloudlet,
                              axes=['y','x'],
                              range=range, bins=bins,
                              weights=None)
    np.seterr(invalid='ignore')
    dm_ierr=dm_i/(dm_n)**1.5
    np.seterr(invalid=None)

    return dm_i,dm_v,dm_vsigma,dm_ierr


###################################################################################################

def clouds_fromobj(obj,
                   nc=100000,nv=20,seeds=[None,None,None,None]):
    """
    This is a wrapper function to create a cloudlet model from a object dict 
    """
    car,cloudmeta=clouds_morph(sbProf=obj['sbProf'],
                          rotPhi=obj['rotAz'] if  'rotAz' in obj else None,
                          sbQ=obj['sbQ'] if  'sbQ' in obj else None,
                          vbProf=obj['vbProf'],
                          seeds=seeds[0:3],size=nc)    

    car_k=clouds_kin(car,
                     rcProf=obj['rcProf'],
                     vRadial=obj['vRadial'],
                     vSigma=obj['vSigma'],
                     seed=seeds[3],nV=nv)
    
    clouds_tosky(car_k,obj['inc'],obj['pa'],inplace=True)
    
    return car_k.ravel(),None

def clouds_fill(mod_dct,
                nc=100000,nv=20,seeds=[None,None,None,None]):
    
    """
    attach clouds to "mod_dct"
    This is a wrapper function to attached a cloudlet model from a object-group dict  
    """
    
    for objname, obj in mod_dct.items():
        if  'type' not in obj:
            continue
        if  obj['type']!='disk3d':
            continue
        obj['clouds_loc'],obj['clouds_wt']=\
            clouds_fromobj(obj,
                           nc=nc,nv=nv,seeds=seeds)
        for fluxtype in ['lineflux','contflux']:
            if  fluxtype in obj:
                obj['clouds_flux']=obj[fluxtype]/obj['clouds_loc'].size
                
    return  

###################################################################################################  

def model_update(mod_dct,models):
    """
    not used. related to likelihood
    update some model parameters related to likelihood calculation
        In the model properties, we have some keywords related to configing the likelihood
    model and calculate log_propeorbaility:
        lognsigma: used to scale noise level (in case it's overunder estimated)
    They are actually related to data (one value per dataset)
    But it's setup per object due to the input file layout (repeated for different objects, like PSF)
    """
    
    for tag in list(mod_dct.keys()):
         obj=mod_dct[tag]
         if  'vis' in mod_dct[tag].keys():
             vis_list=mod_dct[tag]['vis'].split(",")
             for vis in vis_list:
                if  'lognsigma' not in obj['lognsigma']:
                    models['lognsigma@'+vis]=0.0
                else:
                    models['lognsigma@'+vis]=obj['lognsigma']
                  
    return
    

def model_setup(mod_dct,dat_dct,decomp=False,verbose=False):
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
                    #   pass the data reference (no memory penalty)
                    
                    #or [obj['xypos'].ra,obj['xypos'].dec]
                    #center=dat_dct['phasecenter@'+vis]
                    center=[obj['xypos'].ra,obj['xypos'].dec]
                    
                    if  'pbeam@'+vis not in dat_dct:
                        models['header@'+vis]=makeheader(dat_dct['uvw@'+vis],center,
                                                         dat_dct['chanfreq@'+vis],
                                                         dat_dct['chanwidth@'+vis])
                        models['pbeam@'+vis]=((makepb(models['header@'+vis],
                                                      phasecenter=dat_dct['phasecenter@'+vis],
                                                      antsize=25*u.m)).astype(np.float32))[np.newaxis,np.newaxis,:,:]
                    else:
                        models['header@'+vis]=dat_dct['header@'+vis]
                        models['pbeam@'+vis]=dat_dct['pbeam@'+vis]
                    
                    models['wcs@'+vis]=WCS(models['header@'+vis])
                    
                    #naxis=(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])
                    
                    models['imodel@'+vis]=None
                    models['objs@'+vis]=[]                  
                
                # get a lookup table when looping over dataset.
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


###################################################################################################

def makeheader(uv,center,chanfreq,chanwidth,antsize=None):
    """
    create a header template for discreating cloudlet model before uv sampling
        using accroding to UV sampling and primary beam FOV
        uv.shape (nrecord,2) in units of meter
        chanfreq quantity frequency array
        center this could be phasecenter or somewhere near your target
        antsize=12*u.m
        
    f_max: determines the UV grid size, or set a image cell-size upper limit
           a valeu of >=2 would be a safe choice
           (set a upper limit of cellsize)
    f_min: set the UV cell-size upper limit, or a lower limit of image FOV.                            
           a value of >=3 would be translated into a FOV lager than >=3 of interfeormetry sensitive scale
           ***set a lower limit of imsize
    PB:    primary beam size, help set a lower limit of FOV
           however, in terms of imaging quality metric, this is not crucial
           ***set a lower limit of imsize
    The rule of thumbs are:
        * make sure f_max and f_min are good enought that all spatial frequency information is presented in
        the reference models
        * the FOV is large enough to covert the object.
        * keep the cube size within the memory limit    
    # note: if dxy is too large, uvsampling will involve extrapolation which is not stable.
    #       if nxy is too small, uvsampling should be okay as long as you believe no stucture-amp is above that scale.
    #          interplate is more or less stable.             
    """

    f_max=2.0
    f_min=2.0
    wv=np.mean(chanfreq).to(u.m,equivalencies=u.spectral())
    if  antsize is None:
        pb=0    # no restrictin from PB
    else:
        pb=1.22*wv/antsize*1.0
    
    nxy, dxy = get_image_size(uv[:,0]/wv.value, uv[:,1]/wv.value,
                              PB=pb,f_max=f_max,f_min=f_min,
                              verbose=False)
    logger.debug('make fits-header for vis')
    logger.debug('nxy:  '+str(nxy))
    logger.debug('dxy:  '+(dxy<<u.rad).to(u.arcsec).to_string())

 

    header=create_header()
    header['NAXIS1']=nxy
    header['NAXIS2']=nxy
    header['NAXIS3']=np.size(chanfreq)
    
    header['CRVAL1']=center[0].to_value(u.deg)
    header['CRVAL2']=center[1].to_value(u.deg)
                   
    crval3=chanfreq.to_value(u.Hz)
    if  not np.isscalar(crval3):
        crval3=crval3[0]
    header['CRVAL3']=crval3
    header['CDELT1']=-np.rad2deg(dxy)
    header['CDELT2']=np.rad2deg(dxy)
    header['CDELT3']=np.mean(chanwidth.to_value(u.Hz))   
    header['CRPIX1']=np.floor(nxy/2)+1
    header['CRPIX2']=np.floor(nxy/2)+1
    
    return header
    
def makepsf(header,
            beam=None,size=None,
            mode='oversample',factor=None,norm='peak'):
    """
    make a 2D Gaussian image as PSF, warapping around makekernel()
    beam: tuple (bmaj,bmin,bpa) quatity in fits convention
         otherwise, use header bmaj/bmin/bpa
    size:  (nx,ny) <-- in the FITS convention (not other way around, or so called ij)
    
    norm='peak' would be godo for Jy/pix->Jy/beam 
    output 
    
    Note: we choose not use Gaussian2DKernel as we want to handle customzed PSF case in upstream (as dirty beam)
    """
    #   get size
    if  size is None:
        size=(header['NAXIS1'],header['NAXIS2'])
    cell=np.sqrt(abs(header['CDELT1']*header['CDELT2']))
    #   get beam
    beam_pix=None
    if  isinstance(beam,tuple):
        beam_pix=(beam[0].to_value(u.deg)/cell,
                  beam[1].to_value(u.deg)/cell,
                  beam[2].to_value(u.deg))
    else:
        if  'BMAJ' in header:
            if  header['BMAJ']>0 and header['BMIN']>0: 
                beam_pix=(header['BMAJ']/cell,
                          header['BMIN']/cell,
                          header['BPA'])
    #   get psf
    psf=None
    if  beam_pix is not None:
        if  factor is None:
            factor=max(int(10./beam_pix[1]),1)
        if  factor==1:
            mode='center'
        psf=makekernel(size[0],size[1],
                       [beam_pix[0],beam_pix[1]],pa=beam_pix[2],
                       mode=mode,factor=factor)
        if  norm=='peak':
            psf/=np.max(psf)
        if  norm=='sum':
            psf/=np.sum(psf)
        """
        # kernel object:
        psf=Gaussian2DKernel(x_stddev=beam_pix[1]*gaussian_fwhm_to_sigma,
                             y_stddev=beam_pix[0]*gaussian_fwhm_to_sigma,
                             x_size=int(size[0]),y_size=int(size[1]),
                             theta=np.radians(beam_pix[2]),
                             mode=mode,factor=factor)          
        """
    return psf
    

def makepb(header,phasecenter=None,antsize=12*u.m):
    """
    make a 2D Gaussian image approximated to the ALMA (or VLA?) primary beam
        https://help.almascience.org/index.php?/Knowledgebase/Article/View/90/0/90
    
    note: this is just a apprximate solution, assuming the the pointing is towards the reference pixel in the header 
          and use the first channel as the reference frequency.
    
    """
    
    if  phasecenter is None:
        xc=header['CRPIX1']
        yc=header['CRPIX2']
    else:
        w=WCS(header)
        xc,yc=w.celestial.wcs_world2pix(phasecenter[0],phasecenter[1],0)
    #w.
    
    #   PB size in pixel
    beam=1.13*np.rad2deg(const.c.to_value('m/s')/(header['CDELT3']*0+header['CRVAL3'])/antsize.to_value(u.m))
    beam*=1/np.abs(header['CDELT2'])
    sigma2fwhm=np.sqrt(2.*np.log(2.))*2.
    mod=Gaussian2D(amplitude=1.,
                   x_mean=xc,y_mean=yc,
                   x_stddev=beam/sigma2fwhm,y_stddev=beam/sigma2fwhm,theta=0)
    pb=discretize_model(mod,(0,int(header['NAXIS1'])),(0,int(header['NAXIS1'])))

    return pb

def makekernel(xpixels,ypixels,beam,pa=0.,cent=None,
               mode='center',factor=10,
               verbose=True):
    """
    mode: 'center','linear_interp','oversample','integrate'

    beam=[bmaj,bmin] FWHM not (bmin,bmaj)
    pa=east from north (ccw)deli
    
    in pixel-size units
    
    by default: the resulted kernel is always centered around a single pixel, and the application of
        the kernel will lead to zero offset,
    
    make a "centered" Gaussian PSF kernel:
        e.g. npixel=7, centered at px=3
             npixel=8, centered at px=4
             so the single peak is always at a pixel center (not physical center)
             and the function is symmetric around that pixel
             the purpose of doing this is to avoid offset when the specified kernel size is
             even number and you build a function peaked at a pixel edge. 
             
        is x ks (peak pixel index)
        10 x 7(3) okay
        10 x 8(4) okay
        10 x 8(3.5) offset
        for convolve (non-fft), odd ks is required (the center pixel is undoubtely index=3)
                                even ks is not allowed
        for convolve_fft, you need to use cent=ks/2:
                                technically it's not the pixel index of image center
                                but the center pixel is "considers"as index=4
        the rule of thumb-up:
            cent=floor(ks/2.) or int(ks/2) #  int() try to truncate towards zero.
        
        note:
            
            Python "rounding half to even" rule vs. traditional IDL:
                https://docs.scipy.org/doc/numpy/reference/generated/numpy.around.html
                https://realpython.com/python-rounding/
                Python>round(1.5)    # 2
                Python>round(0.5)    # 0
                IDL>round(1.5)       # 2 
                IDL>round(0.5)       # 1
 
            "forget about how the np.array is stored, just use the array as it is IDL;
             when it comes down to shape/index, reverse the sequence"
             
            About Undersampling Images:
            http://docs.astropy.org/en/stable/api/astropy.convolution.discretize_model.html
            
    """
    
    if  cent is None:
        cent=[np.floor(xpixels/2.),np.floor(ypixels/2.)]
    sigma2fwhm=np.sqrt(2.*np.log(2.))*2.
    mod=Gaussian2D(amplitude=1.,x_mean=cent[0],y_mean=cent[1],
               x_stddev=beam[1]/sigma2fwhm,y_stddev=beam[0]/sigma2fwhm,
               theta=np.deg2rad(pa))
    psf=discretize_model(mod,(0,int(xpixels)),(0,int(ypixels)),
                         mode=mode,factor=factor)
    #x,y=np.meshgrid(np.arange(xpixels),np.arange(ypixels),indexing='xy')
    #psf=mod(x,y)
    
    return psf
    