from gmake.model import clouds_morph
from gmake.model import clouds_kin
from gmake.model import clouds_tosky
from gmake.meta import xymodel_header
from gmake.discretize import xy_mapper
from gmake.evaluate import uv_chisq

from astropy.coordinates import SkyCoord
#from gmake.tests.test_cloudlet import test_cloudlet_disk3d_tosky
import astropy.units as u


import numpy as np

def test_discretize_example(size=10000):

    """
    test clouds_morph / clouds_kin / clouds_tosky and plot the results
    
    kernprof -l -v /Users/Rui/Resilio/Workspace/projects/GMaKE/gmake/tests/test_cloudlet.py
    with @profile dec for the testing function
    
    @ the header
    https://jakevdp.github.io/PythonDataScienceHandbook/01.07-timing-and-profiling.html
    """
    
    """
    generate the cloud set
    """
    
    sbProf=('sersic2d',10*u.kpc,2)
    vbProf=('sech',1*u.kpc)
    rotAz=('log',0*u.kpc,20*u.kpc,270*u.deg,5*u.kpc)
    sbQ=0.3   
    car,meta=clouds_morph(sbProf=sbProf,rotPhi=rotAz,sbQ=sbQ,
                        vbProf=vbProf,
                        seeds=[1,2,3],size=size)    

    sbProf=('sersic2d',5*u.kpc,1)
    vbProf=('sech',1*u.kpc)
    rcProf=('rho : minimum(rho/p2,1.0)*p1',400*u.km/u.s,5*u.kpc)
    rcProf=('tanh',400*u.km/u.s,10*u.kpc)
    car_k=clouds_kin(car,rcProf=rcProf,vRadial=-60*u.km/u.s,
                     vSigma=60*u.km/u.s,
                     seed=4,nV=30)
    
    pa=30*u.deg
    inc=45*u.deg
    clouds_tosky(car_k,inc,pa,inplace=True)


    return car_k,None

def test_discretize_mapper():
    
    obj={}
    obj['xypos']=SkyCoord(ra=356.53932590540563,dec=12.82201818705264,unit="deg").to_string(style='hmsdms')
    obj['xypos']=SkyCoord(obj['xypos'],frame='icrs')
    obj['z']=4.0548
    obj['vsys']=0*u.km/u.s
    obj['restfreq']=230.538*u.GHz
    

    header=xymodel_header.copy()
    
    header['NAXIS1']=120
    header['NAXIS2']=120
    header['NAXIS3']=130

    header['CRVAL1']=obj['xypos'].ra.to_value(u.deg)
    header['CRVAL2']=obj['xypos'].dec.to_value(u.deg)
    #header['CRVAL1']=356.53932
    #header['CRVAL2']=12.822018    
    header['CRPIX1']=60
    header['CRPIX2']=60                     
    header['CDELT1']=-0.1/60/60     # degree
    header['CDELT2']=+0.1/60/60     # degree
    
    header['CRVAL3']=4.5533e10      # Hz
    header['CRPIX3']=1
    header['CDELT3']=2e6            # Hz

    car,weights=test_discretize_example()
   
    xy_mapper(obj,header,car,weights=weights)

    
if  __name__=="__main__":
    
    
    test_discretize_mapper()
    
    
    