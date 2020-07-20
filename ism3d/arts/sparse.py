"""source model: sparse form"""

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

#from .utils import rng_seeded,fft_fastlen,fft_use,eval_func,one_beam,sample_grid

from ..maths.stats import rng_seeded
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

from .dynamics import vrot_from_rcProf
from copy import deepcopy

logger = logging.getLogger(__name__)

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
            if  sbProf[0].lower()=='expon2d':   rho*=0.5    
            if  sbProf[0].lower()=='sersic2d':  rho*=0.5**sbProf[-1]
            if  sbProf[0].lower()=='norm2d':  rho*=0.5**0.5   
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
       
        # get v_rot
        
        v_rot=vrot_from_rcProf(rcProf,rho)

            
        
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
        #print('view:',xyz.flags['OWNDATA'])
        erfa_ufunc.rxp(rots,xyz,out=xyz)
        
        if  car.differentials:
            d_xyz=car.differentials['s'].get_d_xyz(xyz_axis=-1)
            erfa_ufunc.rxp(rots,d_xyz,out=d_xyz)
        
        return car
    
    else:
        
        xyz=car.get_xyz(xyz_axis=-1)    # view
        xyz=erfa_ufunc.rxp(rots,xyz)
    
        if  car.differentials:
            d_xyz=car.differentials['s'].get_d_xyz(xyz_axis=-1)
            d_xyz=erfa_ufunc.rxp(rots,d_xyz)
            return CartesianRepresentation(xyz,xyz_axis=-1,
                                differentials=CartesianDifferential(d_xyz,xyz_axis=-1))  
    
        return CartesianRepresentation(xyz,xyz_axis=-1)


def clouds_from_disk3d(obj,
                       nc=100000,nv=20,
                       seeds=[None,None,None,None]):
    """
    for an spatial 3D disk (includingline or continuue)
    """
    car,cloudmeta=clouds_morph(sbProf=obj['sbProf'],
                          rotPhi=obj['rotAz'] if  'rotAz' in obj else None,
                          sbQ=obj['sbQ'] if  'sbQ' in obj else None,
                          vbProf=obj['vbProf'] if  'vbProf' in obj else None,
                          seeds=seeds[0:3],size=nc)       
    
    if  'rcProf' in obj and 'vRadial' in obj and 'vSigma' in obj:
        if  'rcProf' in obj:
            rcProf=list(obj['rcProf'])
            if  rcProf[0]=='potential':
                rcProf[1]=obj['pots']
        else:
            rcProf=None        
        car=clouds_kin(car,
                       rcProf=rcProf,
                       vRadial=obj['vRadial'] if  'vRadial' in obj else None,
                       vSigma=obj['vSigma'] if  'vSigma' in obj else None,
                       seed=seeds[3],nV=nv) 

    obj['clouds_source']=deepcopy(car).ravel()
    #car=deepcopy(car)
    #car=car.copy()
    #print('before:',car)
    car=clouds_tosky(car,obj['inc'],obj['pa'],inplace=False)
    #print('after:',out_car)
    #print(car is out_car)
    obj['clouds_loc']=car.ravel()
    obj['clouds_wt']=None
    #for fluxtype in ['lineflux','contflux']:
    #    if  fluxtype in obj:
    #        obj['clouds_flux']=obj[fluxtype]/obj['clouds_loc'].size    
    
    return


def clouds_from_point(obj):
    
    car=CartesianRepresentation(0*u.kpc,0*u.kpc,0*u.kpc)
    
    obj['clouds_loc']=car.ravel()
    obj['clouds_wt']=None
    #for fluxtype in ['lineflux','contflux']:
    #    if  fluxtype in obj:
    #        obj['clouds_flux']=obj[fluxtype]/obj['clouds_loc'].size        
    
    return

def clouds_from_obj(obj,
                    nc=100000,nv=20,seeds=[None,None,None,None]):
    
    if  obj['type']=='disk3d':
        clouds_from_disk3d(obj,nc=nc,nv=nv,seeds=seeds)
    
    if  obj['type']=='point':
        clouds_from_point(obj)
    
    return




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



def clouds_realize(mod_dict,
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


# def clouds_fromobj(obj,
#                    nc=100000,nv=20,seeds=[None,None,None,None]):
#     """
#     This is a wrapper function to create a cloudlet model from a object dict 
#         it will handle type='disk2d'/'disk3d'/'point'
#     """
#     if  'disk2d' in obj['type'] or  'disk3d' in obj['type']:
#         car,cloudmeta=clouds_morph(sbProf=obj['sbProf'],
#                               rotPhi=obj['rotAz'] if  'rotAz' in obj else None,
#                               sbQ=obj['sbQ'] if  'sbQ' in obj else None,
#                               vbProf=obj['vbProf'] if  'vbProf' in obj else None,
#                               seeds=seeds[0:3],size=nc)    
# 
#     if  'point' in obj['type']:
#         car=CartesianRepresentation(0*u.kpc,0*u.kpc,0*u.kpc)
#                 
#     if  'disk3d' in obj['type']:
#         if  'rcProf' in obj:
#             rcProf=list(obj['rcProf'])
#             if  rcProf[0]=='potential':
#                 rcProf[1]=obj['pots']
#         else:
#             rcProf=None        
#         car=clouds_kin(car,
#                        rcProf=rcProf,
#                        vRadial=obj['vRadial'] if  'vRadial' in obj else None,
#                        vSigma=obj['vSigma'] if  'vSigma' in obj else None,
#                        seed=seeds[3],nV=nv)
#     
#     if  'disk2d' in obj['type'] or 'disk3d' in obj['type']:
#         clouds_tosky(car,obj['inc'],obj['pa'],inplace=True)
#     
#     return car.ravel(),None
