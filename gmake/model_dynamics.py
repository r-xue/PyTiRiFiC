from astropy.cosmology import Planck13
import numpy as np
from scipy.interpolate import interp1d
import galpy.potential as galpy_pot
import matplotlib.pyplot as plt

from .utils import *

import matplotlib as mpl
mpl.use("Agg")
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"
mpl.rcParams['agg.path.chunksize'] = 10000
#mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#mpl.rc('font',**{'family':'serif','serif':['Palatino']})
#mpl.rc('text',usetex=True)

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
    
    if  'disk_sd' in pot_dct and 'disk_rs' in pot_dct:

        dpot=galpy_pot.RazorThinExponentialDiskPotential(amp=pot_dct['disk_sd'],
                                               hr=pot_dct['disk_rs'],ro=ro,vo=vo)

        vcirc_dp=dpot.vcirc(rad)
        vcirc_dp[0]=0
        
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

def model_vrot_plot(rc,figname='vrot_plt.pdf'):

    plt.clf()
    fig,ax=plt.subplots(1,1,figsize=(5,3))
    ax.plot(rc['vrad'],rc['vcirc'],color='red',label='Vcirc')
    ax.plot(rc['vrad'],rc['vrot'],color='black',label='Vrot')
    ax.set_xlabel('Radius [arcsec]')
    ax.set_ylabel('Vcirc or Vrot [km/s]')
    ax.legend()
    #ax1.loglog(rad,vcirc_tp)
    #ax1.loglog(rad,vcirc_tp,color='black')
    #ax2.loglog(rad,cmass_tp)
    fig.savefig(figname)   
    
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
            

            # <Quantity 8.58263899 kpc / arcsec>
            kps=Planck13.kpc_proper_per_arcmin(2).to(u.kpc/u.arcsec)  

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
    
if  __name__=="__main__":

    pass
    #gmake_gravity()
    #gmake_gravity_galpy()