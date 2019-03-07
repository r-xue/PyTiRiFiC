
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from galpy.potential import MiyamotoNagaiPotential
from galpy.potential import KeplerPotential
from galpy.potential import NFWPotential
from galpy.potential import RazorThinExponentialDiskPotential
from astropy.cosmology import Planck13

def gmake_gravity_galpy(inp_dct,plotrc=False):
    
    """
    generate a RC from the mass-potential model 
    """
    if  'rc' in inp_dct.keys():
        
        rc=inp_dct['rc']

        for obj in inp_dct.keys():
            
            if  'method' not in inp_dct[obj]:
                continue
            if   'kinmspy' not in inp_dct[obj]['method']:
                continue
            
            z=inp_dct[obj]['z']
        
            #mpot=MiyamotoNagaiPotential(amp=rc[''*u.Msun,a=3.*u.kpc,b=300.*u.pc)
            #kpot=KeplerPotential(amp=5e10*u.Msun)
            #npot=NFWPotential(amp=rc['halo_ms']*u.Msun,a=rc['halo_a']*u.kpc)
            
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
            m_vir=rc['halo_mvir']   # 10^12msun
            c_vir = if_c(z) * (m_vir*h)**(-0.075) * (1+(m_vir*1e12/if_m(z))**0.26)
                                        
            omega_z=Planck13.Om(z)                                           
            delta_c = 18.*(np.pi**2) + 82.*(omega_z-1.) - 39.*(omega_z-1.)**2
    
            npot=NFWPotential(conc=c_vir,
                              mvir=m_vir,
                              H=Planck13.H(z).value,
                              Om=0.3,#dones't matter as wrtcrit=True
                              overdens=delta_c,wrtcrit=True,
                              ro=1,vo=1)
            dpot=RazorThinExponentialDiskPotential(amp=rc['disk_sd']*u.Msun/u.kpc/u.kpc,
                                                   hr=rc['disk_rs']*u.kpc,ro=1,vo=1)
        
            rad=np.arange(0,18,0.1)
            #vcirc_mp=mpot.vcirc(rad*u.kpc)
            #vcirc_kp=kpot.vcirc(rad*u.kpc)
            vcirc_np=npot.vcirc(rad*u.kpc)
            vcirc_dp=dpot.vcirc(rad*u.kpc)
    
     
            kps=Planck13.kpc_proper_per_arcmin(z).value/60.0
    
            vcirc_tt=np.sqrt(vcirc_np.value**2.0+vcirc_dp.value**2.0)
            vcirc_tt[0]=0
            
            inp_dct[obj]['velrad']=(rad/kps).copy()
            inp_dct[obj]['velprof']=vcirc_tt.copy()
            
        
        #print(vcirc_tt)
        #pot=npot+dpot
        #vcirc_ga=pot.vcirc(rad*u.kpc)
        #cmass=npot.mass(R=np.array([10,2]))
        #print(cmass)
        #cmass=kpot.mass(R=10)
        #print(cmass)    

    if  plotrc==True:
        plt.clf()
        fig,ax1=plt.subplots(1,1,figsize=(5,3))
        ax1.plot(rad/kps,vcirc_np,color='red')
        ax1.plot(rad/kps,vcirc_dp,color='blue')
        ax1.plot(rad/kps,vcirc_tt,color='black')
        #ax1.loglog(rad,vcirc_tp)
        #ax1.loglog(rad,vcirc_tp,color='black')
        #ax2.loglog(rad,cmass_tp)
        fig.savefig('pot2rc.pdf')
        plt.close()
        
    return
    
if  __name__=="__main__":

    pass
    #gmake_gravity()
    #gmake_gravity_galpy()