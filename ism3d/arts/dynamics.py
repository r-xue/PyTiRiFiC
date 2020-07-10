from astropy.cosmology import Planck13
import numpy as np
from scipy.interpolate import interp1d
import galpy.potential as galpy_pot
from ..interface import eval_func
import matplotlib.pyplot as plt

from .utils import *

import matplotlib as mpl
mpl.use("Agg")
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"

#mpl.rcParams['agg.path.chunksize'] = 10000
#mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#mpl.rc('font',**{'family':'serif','serif':['Palatino']})
#mpl.rc('text',usetex=True)
#from memory_profiler import profile
#import gc
#@profile


   

def model_vcirc(pot_dct):
    """
    take a dictionary describing the potential and calculaet rotation curve
    """
    #mpot=MiyamotoNagaiPotential(amp=pot_dct[''*u.Msun,a=3.*u.kpc,b=300.*u.pc)
    #kpot=KeplerPotential(amp=5e10*u.Msun)
    #npot=NFWPotential(amp=pot_dct['halo_ms']*u.Msun,a=pot_dct['halo_a']*u.kpc)
    
    # c_vir(z,M_vir): concentration, Eq (12) from Klypin+11
    #vcirc_mp=mpot.vcirc(rad*u.kpc)
    #vcirc_kp=kpot.vcirc(rad*u.kpc)
    
    
    rad=np.arange(0,18,0.1)*u.kpc
    vcirc_np=np.broadcast_to(0*u.km/u.s,rad.size)
    vcirc_dp=np.broadcast_to(0*u.km/u.s,rad.size)
    
        
    ro=8.*u.kpc
    vo=220.*u.km/u.s
            
    if  'nfw_mvir' in pot_dct and 'z' in pot_dct:
        
        z=pot_dct['z']
        h=Planck13.h
        z0 = np.array([0.0 ,0.5 ,1.0 ,2.0 ,3.0 ,5.0 ])
        c0 = np.array([9.60,7.08,5.45,3.67,2.83,2.34])
        m0 = np.array([1.5e19,1.5e17,2.5e15,6.8e13,6.3e12,6.6e11]) / h
        ikind='linear'
        if_c=interp1d(np.array(z0),np.array(c0),kind=ikind,bounds_error=False,
                      fill_value=(c0[0],c0[-1]))
        if_m=interp1d(np.array(z0),np.array(m0),kind=ikind,bounds_error=False,
                      fill_value=(m0[0],m0[-1]))        
        m_vir=pot_dct['nfw_mvir']   # values in units if 10^12msun
        #   if m_vir is value, then in units of 1e12msun
        #   https://galpy.readthedocs.io/en/latest/reference/potentialnfw.html
        m_vir_12msun=(pot_dct['nfw_mvir']).to_value(u.Msun)/1e12
        c_vir = if_c(z) * (m_vir_12msun*h)**(-0.075) * (1+(m_vir_12msun*1e12/if_m(z))**0.26)
                                    
        omega_z=Planck13.Om(z)                                           
        delta_c = 18.*(np.pi**2) + 82.*(omega_z-1.) - 39.*(omega_z-1.)**2
        npot=galpy_pot.NFWPotential(conc=c_vir,
                          mvir=m_vir_12msun,
                          H=Planck13.H(z).value,
                          Om=0.3,#dones't matter as wrtcrit=True
                          overdens=delta_c,wrtcrit=True,
                          ro=ro,vo=vo)
        
        vcirc_np=npot.vcirc(rad)
        vcirc_np[0]=0
        
        del npot
    
    if  'disk_sd' in pot_dct and 'disk_rs' in pot_dct:

        dpot=galpy_pot.RazorThinExponentialDiskPotential(amp=pot_dct['disk_sd'],
                                               hr=pot_dct['disk_rs'],ro=ro,vo=vo)
        #   temp modify first data point to get ride of warning from galpy
        rad[0]=rad[1]
        vcirc_dp=dpot.vcirc(rad)
        vcirc_dp[0]=0
        rad[0]=0*u.kpc
        
        del dpot
        
    #pot=npot+dpot
    vcirc=np.sqrt(vcirc_np**2.0+vcirc_dp**2.0)
    
    #cmass=npot.mass(R=10*u.kpc,z=None)
    #print(cmass)
    #print(vcirc_tt)
    #pot=npot+dpot 
    #vcirc_ga=pot.vcirc(rad*u.kpc)
    #cmass=npot.mass(R=np.array([10,2]))
    #print(cmass)
    #cmass=kpot.mass(R=10)
    #print(cmass)    

    
    rc={'rad':rad,
        'vcirc_np':vcirc_np,
        'vcirc_dp':vcirc_dp,
        'vcirc':vcirc}
    
    return rc
    
def model_vcirc_plot(rc,figname='vcirc_plt.pdf'):

    plt.clf()
    fig,ax=plt.subplots(1,1,figsize=(5,3))
    ax.plot(rc['rrad']/rc['kps'],rc['vcirc_np'],color='red',label='NFW')
    ax.plot(rc['rrad']/rc['kps'],rc['vcirc_dp'],color='blue',label='ThinExpDisk')
    ax.plot(rc['rrad']/rc['kps'],rc['vcirc_tt'],color='black',label='All')
    ax.set_xlabel('Radius [arcsec]')
    ax.set_ylabel('Vcirc [km/s]')
    ax.legend()
    #ax1.loglog(rad,vcirc_tp)
    #ax1.loglog(rad,vcirc_tp,color='black')
    #ax2.loglog(rad,cmass_tp)
    fig.savefig(figname)   

def model_vrot_plot(mod_obj_disk3d,figname='vrot_plt.pdf'):
    """
    mod_obj_disk3d:    just a single disk object (unitless)
    """
    plt.clf()
    fig,ax=plt.subplots(1,1,figsize=(5,3))
    if 'vcirc' in mod_obj_disk3d:
        ax.plot(mod_obj_disk3d['vrad'],mod_obj_disk3d['vcirc'],color='red',label='Vcirc')
    ax.plot(mod_obj_disk3d['vrad'],mod_obj_disk3d['vrot'],color='black',label='Vrot')
    ax.set_xlabel('Radius [arcsec]')
    ax.set_ylabel('Vcirc or Vrot [km/s]')
    ax.legend()
    #ax1.loglog(rad,vcirc_tp)
    #ax1.loglog(rad,vcirc_tp,color='black')
    #ax2.loglog(rad,cmass_tp)
    fig.savefig(figname)   

#@profile    
def model_vrot(mod_dct):
    
    """
    generate a RC from the mass-potential model 
    """
    
    ikind='linear'
    
    for tag in list(mod_dct.keys()):
        
        if  'type' not in mod_dct[tag]:
            continue
        elif  mod_dct[tag]['type']!='potential':
            continue
        
        pot_dct=mod_dct[tag]
        rc=model_vcirc(pot_dct)
        
        for obj in mod_dct.keys():
            
            #   we only build RC for the "disk3d" components
            
            if  'type' not in mod_dct[obj]:
                continue
            if  'disk3d' not in mod_dct[obj]['type']:
                continue
            if  not isinstance(mod_dct[obj]['vrot'],str):
                continue
            if  mod_dct[obj]['vrot']!=tag:
                continue
            
            z=mod_dct[obj]['z']
            kps=Planck13.kpc_proper_per_arcmin(z).to(u.kpc/u.arcsec)  

            rad=rc['rad']
            
            if  not mod_dct[obj]['vdis'].isscalar:
                if_vdis=interp1d(np.array(mod_dct[obj]['vrad']),np.array(mod_dct[obj]['vdis']),kind=ikind,
                                 bounds_error=False,fill_value=(mod_dct[obj]['vdis'][0],mod_dct[obj]['vdis'][-1]))
                mod_dct[obj]['vdis']=if_vdis(rad/kps)
            else:
                mod_dct[obj]['vdis']=np.broadcast_to(mod_dct[obj]['vdis'],rad.size,subok=True)             
                    
            #   smooth model
            mod_dct[obj]['vrad']=rad/kps
            mod_dct[obj]['vcirc']=rc['vcirc'].copy()
            mod_dct[obj]['vrot']=rc['vcirc'].copy()
            
            if  'vrot_rpcorr' in mod_dct[obj]:
                if  mod_dct[obj]['vrot_rpcorr']:
                    mod_dct[obj]['vrot']=mod_dct[obj]['vcirc']**2 - 2 * mod_dct[obj]['vdis']**2 * (rad/pot_dct['disk_rs']) 
                    mod_dct[obj]['vrot'][mod_dct[obj]['vrot'] < 0]=0
                    mod_dct[obj]['vrot']=np.sqrt(mod_dct[obj]['vrot'])
                    mod_dct[obj]['vcirc']=rc['vcirc'].copy()
                    
            
            #mod_dct[obj]['vrot_halo']=rc['vcirc_np'].copy()
            #mod_dct[obj]['vrot_disk']=rc['vcirc_dp'].copy()
            
        
    return

###################################################################################################

def potential_fromobj(obj):
    """
    create a abstract galpy.potential object (defined in the galactic plane frame)
    which can be used to calculate circular velocity once cloud position is defined. 
    
    obj:    type='poyential'
    return a list of galpy.potential
    
    https://galpy.readthedocs.io/en/v1.5.0/potential.html
    
    """

    # note: the normalizaton factor doesn't really matter if 
    #       we use astropy.quality when building potentials
    
    ro=8.*u.kpc         
    vo=110.*u.km/u.s
    pots=[]
    
    #   NFW like potential
    
    if  'nfw' in obj:
        
        # https://galpy.readthedocs.io/en/v1.5.0/reference/potentialnfw.html
        z=obj['nfw'][1]
        h=Planck13.h
        z0 = np.array([0.0 ,0.5 ,1.0 ,2.0 ,3.0 ,5.0 ])
        c0 = np.array([9.60,7.08,5.45,3.67,2.83,2.34])
        m0 = np.array([1.5e19,1.5e17,2.5e15,6.8e13,6.3e12,6.6e11]) / h
        ikind='linear'
        if_c=interp1d(np.array(z0),np.array(c0),kind=ikind,bounds_error=False,
                      fill_value=(c0[0],c0[-1]))
        if_m=interp1d(np.array(z0),np.array(m0),kind=ikind,bounds_error=False,
                      fill_value=(m0[0],m0[-1]))        
        m_vir=obj['nfw'][0]   # values in units if 10^12msun
        #   if m_vir is value, then in units of 1e12msun
        #   https://galpy.readthedocs.io/en/latest/reference/potentialnfw.html
        m_vir_12msun=(obj['nfw'][0]).to_value(u.Msun)/1e12
        c_vir = if_c(z) * (m_vir_12msun*h)**(-0.075) * (1+(m_vir_12msun*1e12/if_m(z))**0.26)
                                    
        omega_z=Planck13.Om(z)                                           
        delta_c = 18.*(np.pi**2) + 82.*(omega_z-1.) - 39.*(omega_z-1.)**2
        npot=galpy_pot.NFWPotential(conc=c_vir,
                          mvir=m_vir_12msun,
                          H=Planck13.H(z).value,
                          Om=0.3,#dones't matter as wrtcrit=True
                          overdens=delta_c,wrtcrit=True,
                          ro=ro,vo=vo)
        pots.append(npot)

    #   Thin exp diskpotential
    
    if  'expdisk' in obj:

        dpot=galpy_pot.RazorThinExponentialDiskPotential(amp=obj['expdisk'][0],
                                                         hr=obj['expdisk'][1],
                                                         ro=ro,vo=vo)
        pots.append(dpot)
        
    if  'dexpdisk' in obj:

        dpot=galpy_pot.DoubleExponentialDiskPotential(amp=obj['dexpdisk'][0],
                                                         hr=obj['dexpdisk'][1],
                                                         hz=obj['dexpdisk'][2],
                                                         ro=ro,vo=vo)
        pots.append(dpot)  
        
    if  'nm3expdisk' in obj:

        dpot=galpy_pot.MN3ExponentialDiskPotential(amp=obj['nm3expdisk'][0],
                                                         hr=obj['nm3expdisk'][1],
                                                         hz=obj['nm3expdisk'][2],
                                                         sech=obj['nm3expdisk'][3],
                                                         ro=ro,vo=vo)
        pots.append(dpot)                     
        
    if  'isochrone' in obj:

        dpot=galpy_pot.IsochronePotential(amp=obj['isochrone'][0],
                                          b=obj['isochrone'][1],
                                          ro=ro,vo=vo)
        pots.append(dpot)
        
    if  'kepler' in obj:
        
        dpot=galpy_pot.KeplerPotential(amp=obj['kepler'],
                                          ro=ro,vo=vo)
        pots.append(dpot)     
        
    if  'powerlaw' in obj:
        # https://galpy.readthedocs.io/en/v1.5.0/reference/potentialpowerspher.html
        dpot=galpy_pot.PowerSphericalPotential(amp=obj['powerlaw'][0],
                                               alpha=obj['powerlaw'][1],
                                               r1=obj['powerlaw'][2],
                                               ro=ro,vo=vo)
        pots.append(dpot)          
        
        

    return pots 

def calc_vcirc(pot,rho,interp=True,logr=True):
    """
    use interpolated vcirc to speed up vcirc calculation 
    decide to not use potential/interpRZPotential.py to avoid some overheads
    see https://galpy.readthedocs.io/en/v1.5.0/reference/potentialinterprz.html#interprz
    logr will keep 
    also see: galpy.poteential.vcirc()
    """
    if  interp==True:
        if  logr==False:
            rGrid=np.linspace(np.min(rho),np.max(rho),101)
        else:
            rGrid=np.geomspace(np.min(rho),np.max(rho),101)
        return np.interp(rho,rGrid,pot.vcirc(rGrid))
    else:
        return pot.vcirc(rho)

def pots_to_vcirc(pots,rho,pscorr=None):
    """
    calculate vcirc and vrot from galactocentric distance and galpy.potential
    post is a list of ponetials
    
    optionally, a dispersion-based pressure correcton can be applied to provide partial support (tehrefore, decrease vrot)
    pscorr=(vSigma,ExpDisk_scale_length) 
    note: this is only correct if the non-DM is in a exp-disk
    
        vcirc:   no pressure correction
        vrot:    pressure correction
    optionall
    
    vcirc[0,:] = rotational velocity after the correction
    vcirc[1,:] = rotatipnal velocity before the correction
    vcirc{2:,:] = contribution from individial potentials 
    
    """

    vcirc_pot=[]
    for pot in pots:
        vcirc_pot.append(calc_vcirc(pot,rho,interp=False,logr=True))        

    
    vcirc_pot=np.vstack(vcirc_pot)
    vcirc=np.sqrt(np.sum((np.vstack(vcirc_pot))**2,axis=0))

    pots_name=[(pot.__class__.__name__).split(".")[-1] for pot in pots]
    
    if  pscorr is not None:
        vrot=vcirc**2-2*pscorr[0]**2*(rho/pscorr[1])
        vrot[vrot<0]=0
        vrot=np.sqrt(vrot)
        return np.vstack((vrot,vcirc,vcirc_pot)),['Vrot','Vcirc']+pots_name
    else:          
        return np.vstack((vcirc,vcirc_pot)),['Vrot']+pots_name

def vrot_from_rcProf(rcProf,rho):
    """
    use the value of keyword rcProf to evaluate the rotation curve at specified rho 
    examples of rcProf:
        rcProf=('rho : minimum(rho/p2,1.0)*p1',400*u.km/u.s,5*u.kpc)
        rcProf=('tanh',300*u.km/u.s,10*u.kpc)
        ...
    """
    
    #   lambda function style
    if  ' : ' in rcProf[0]:
        vrot=eval_func(rcProf,{'rho':rho})            
    
    #   table style
    if  rcProf[0]=='table':
        vrot=np.interp(rho,rcProf[1],rcProf[2])
    
    #   arctan style
    if  rcProf[0].lower()=='arctan':
        vrot=rcProf[1]*2.0/np.pi*np.arctan(rho/rcProf[2]*u.rad)

    #   expon style
    if  rcProf[0].lower()=='expon':
        vrot=rcProf[1]*(1-np.exp(-rho/rcProf[2]))

    #   tanh style
    if  rcProf[0].lower()=='tanh':
        vrot=rcProf[1]*np.tanh(rho/rcProf[2]*u.rad)
    
    #   from a potential
    if  rcProf[0].lower()=='potential':
        vrot=(pots_to_vcirc(rcProf[1],rho))[0][0,:]    
    
    return vrot


    
if  __name__=="__main__":

    pass
    #gmake_gravity()
    #gmake_gravity_galpy()