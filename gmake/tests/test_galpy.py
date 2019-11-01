from astropy.cosmology import Planck13
import numpy as np
from scipy.interpolate import interp1d
import galpy.potential as galpy_pot
import matplotlib.pyplot as plt
https://docs.astropy.org/en/stable/known_issues.html
import astropy.units as u

import matplotlib as mpl
mpl.use("Agg")
#mpl.rcParams['xtick.direction'] = 'in'
#mpl.rcParams['ytick.direction'] = 'in'
#mpl.rcParams.update({'font.size': 12})
#mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"
#mpl.rcParams['agg.path.chunksize'] = 10000

#dpot=galpy_pot.RazorThinExponentialDiskPotential(amp=2000*u.Msun/u.pc/u.pc,
#                                       hr=5*u.kpc,
#                                       ro=1*u.kpc,vo=230.*u.km/u.s)
"""
When you specify the parameters of a Potential, Orbit, etc. in physical units 
(e.g., the Miyamoto-Nagai setup above), the internal set of units is unimportant 
as long as you receive output in physical units (see below) and it is unnecessary 
to change the values of ro and vo, unless you are modeling a system with very 
different distance and velocity scales from the default set (for example, if you 
are looking at internal globular cluster dynamics rather than galaxy dynamics). 
"""

ro=8*u.kpc
vo=220*u.km/u.s
dpot=galpy_pot.RazorThinExponentialDiskPotential(amp=200*u.Msun/u.pc/u.pc,
                                       hr=8*u.kpc,
                                       ro=ro,vo=vo)


rad=np.arange(0.1,50,0.1)*u.kpc

vrad=dpot.vcirc(rad)
#print(vrad)
frad=dpot.Rforce(rad,z=0)
print(frad)
#cmass=dpot.mass(R=100)


import astropy.constants as const

# should be the same as vrad

v=np.sqrt(np.abs(frad*rad))
print(v.to(u.km/u.s))
#

cmass=dpot.mass(R=1.0,z=None,forceint=True)
print(cmass)

dens=dpot.dens(R=1.0,z=0.0)
print(dens)

figname='test_galpy.pdf'
plt.clf()
fig = plt.figure()  # create a figure object
ax = fig.add_subplot(1, 1, 1)  # create an axes object in the figure
ax.plot(rad,vrad,color='red',label='Disk')
ax.set_xlabel('Radius [kpc]')
ax.set_ylabel('Vcirc [km/s]')
ax.legend()
#ax1.loglog(rad,vcirc_tp)
#ax1.loglog(rad,vcirc_tp,color='black')
#ax2.loglog(rad,cmass_tp)
fig.savefig(figname)  



def model_dynamics(obj,dyn,rad_as):
    
    """
    generate a RC from the mass-potential model 
    """
    z=obj['z']

    #mpot=MiyamotoNagaiPotential(amp=dyn[''*u.Msun,a=3.*u.kpc,b=300.*u.pc)
    #kpot=KeplerPotential(amp=5e10*u.Msun)
    #npot=NFWPotential(amp=dyn['halo_ms']*u.Msun,a=dyn['halo_a']*u.kpc)
    
    # c_vir(z,M_vir): concentration, Eq (12) from Klypin+11
    h=Planck13.h
    z0 = np.array([0.0 ,0.5 ,1.0 ,2.0 ,3.0 ,5.0 ])
    c0 = np.array([9.60,7.08,5.45,3.67,2.83,2.34])
    m0 = np.array([1.5e19,1.5e17,2.5e15,6.8e13,6.3e12,6.6e11]) / h
    ikind='linear'
    if_c=interp1d(np.array(z0),np.array(c0),kind=ikind,bounds_error=False,
                  fill_value=(c0[0],c0[-1]))
    if_m=interp1d(np.array(z0),np.array(m0),kind=ikind,bounds_error=False,
                  fill_value=(m0[0],m0[-1]))        
    m_vir=dyn['halo_mvir']   # 10^12msun
    c_vir = if_c(z) * (m_vir*h)**(-0.075) * (1+(m_vir*1e12/if_m(z))**0.26)
                                
    omega_z=Planck13.Om(z)                                           
    delta_c = 18.*(np.pi**2) + 82.*(omega_z-1.) - 39.*(omega_z-1.)**2

    npot=galpy_pot.NFWPotential(conc=c_vir,
                      mvir=m_vir,
                      H=Planck13.H(z).value,
                      Om=0.3,#dones't matter as wrtcrit=True
                      overdens=delta_c,wrtcrit=True,
                      ro=1,vo=1)
    dpot=galpy_pot.RazorThinExponentialDiskPotential(amp=dyn['disk_sd']*u.Msun/u.kpc/u.kpc,
                                           hr=dyn['disk_rs']*u.kpc,ro=1,vo=1)

    kps=Planck13.kpc_proper_per_arcmin(z).value/60.0
    rad=rad_as*kps
    #rad=np.arange(0,18,0.1)
    #vcirc_mp=mpot.vcirc(rad*u.kpc)
    #vcirc_kp=kpot.vcirc(rad*u.kpc)
    vcirc_np=npot.vcirc(rad*u.kpc)
    vcirc_dp=dpot.vcirc(rad*u.kpc)


    

    vcirc_tt=np.sqrt(vcirc_np.value**2.0+vcirc_dp.value**2.0)
    vcirc_tt[0]=0
    
    
    if  isinstance(obj['vdis'], (list, tuple, np.ndarray)):
        if_vdis=interp1d(np.array(obj['vrad']),np.array(obj['vdis']),kind=ikind,
                         bounds_error=False,fill_value=(obj['vdis'][0],obj['vdis'][-1]))
        obj['vdis']=if_vdis(rad/kps)
    else:
        obj['vdis']=rad/kps*0.0+obj['vdis']
            
    #   smooth model
    obj['vrad']=(rad/kps).copy()
    obj['vrot']=vcirc_tt.copy()
    obj['vrot_halo']=vcirc_np.value.copy()
    obj['vrot_disk']=vcirc_dp.value.copy()
        

        
    #print(vcirc_tt)
    #pot=npot+dpot
    #vcirc_ga=pot.vcirc(rad*u.kpc)
    #cmass=npot.mass(R=np.array([10,2]))
    #print(cmass)
    #cmass=kpot.mass(R=10)
    #print(cmass)    

        
    return obj['vrot']
