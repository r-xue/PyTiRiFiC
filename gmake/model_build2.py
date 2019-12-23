from .model_func import *
from .model_func2 import *
from .model_dynamics import *
from .io import *
from .meta import xymodel_header

#from galario.double import get_image_size
#from galario.double import sampleImage
#from galario.double import chi2Image
from galario.single import get_image_size

logger = logging.getLogger(__name__)

import scipy.constants as const

from astropy.modeling.models import Gaussian2D

from memory_profiler import profile

def model_init2(mod_dct,dat_dct,decomp=False,verbose=False):
    """
    create model container 
        this function can be ran only once before starting fitting iteration, so that
        the memory allocation/ allication will happen once during a fitting run.

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
    
    if  verbose==True:
        start_time = time.time()
            
    models={'mod_dct':mod_dct.copy()}
                
    for tag in list(mod_dct.keys()):
        
        obj=models['mod_dct'][tag]
        
        if  verbose==True:
            print("+"*40); print('@',tag); print('type:',obj['type']) ; print("-"*40)

        if  'vis' in mod_dct[tag].keys():
            
            vis_list=mod_dct[tag]['vis'].split(",")
            
            for vis in vis_list:
                
                if  'type@'+vis not in models.keys():
                    
                    models['type@'+vis]=dat_dct['type@'+vis]
                    #   pass the data reference (no memory penalty)
                    
                    wv=np.mean(const.c/dat_dct['chanfreq@'+vis].to_value(u.Hz)) # in meter
                    
                    #
                    ant_size=12.0 # hard coded in meter
                    f_max=2.0
                    f_min=3.0/3.0
                    """
                    f_max: determines the UV grid size, or set a image cell-size upper limit
                           a valeu of >=2 would be a safe choice
                    f_min: set the UV cell-size upper limit, or a lower limit of image FOV.                            
                           a value of >=3 would be translated into a FOV lager than >=3 of interfeormetry sensitive scale
                    PB:    primary beam size, help set a lower limit of FOV
                           however, in terms of imaging quality metric, this is not crucial
                    The rule of thumbs are:
                        * make sure f_max and f_min are good enought that all spatial frequency information is presented in
                        the reference models
                        * the FOV is large enough to covert the object.
                        * keep the cube size within the memory limit
                    """
                    nxy, dxy = get_image_size(dat_dct['uvw@'+vis][:,0]/wv, dat_dct['uvw@'+vis][:,1]/wv,
                                              PB=1.22*wv/ant_size*0.0,f_max=f_max,f_min=f_min,
                                              verbose=False)
                    #print("-->",nxy,np.rad2deg(dxy)*60.*60.,vis)
                    #print(np.rad2deg(dxy)*60.*60,0.005,nxy)
                    # note: if dxy is too large, uvsampling will involve extrapolation which is not stable.
                    #       if nxy is too small, uvsampling should be okay as long as you believe no stucture-amp is above that scale.
                    #          interplate is more or less stable.  
                    #dxy=np.deg2rad(0.02/60/60)
                    #nxy=128
                    
                    header=xymodel_header.copy()
                    header['NAXIS1']=nxy
                    header['NAXIS2']=nxy
                    header['NAXIS3']=np.size(dat_dct['chanfreq@'+vis])
                    
                    header['CRVAL1']=dat_dct['phasecenter@'+vis][0].to_value(u.deg)
                    header['CRVAL2']=dat_dct['phasecenter@'+vis][1].to_value(u.deg)
                    
                    header['CRVAL1']=obj['xypos'].ra.to_value(u.deg)
                    header['CRVAL2']=obj['xypos'].dec.to_value(u.deg)                 
                    
                    crval3=dat_dct['chanfreq@'+vis].to_value(u.Hz)
                    if  not np.isscalar(crval3):
                        crval3=crval3[0]
                    header['CRVAL3']=crval3
                    header['CDELT1']=-np.rad2deg(dxy)
                    header['CDELT2']=np.rad2deg(dxy)
                    header['CDELT3']=np.mean(dat_dct['chanwidth@'+vis].to_value(u.Hz))   
                    header['CRPIX1']=np.floor(nxy/2)+1
                    header['CRPIX2']=np.floor(nxy/2)+1
                    
                    models['header@'+vis]=header.copy()
                    
                    models['pbeam@'+vis]=((makepb(header)).astype(np.float32))[np.newaxis,np.newaxis,:,:]
                    naxis=(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])
                    
                    models['imodel@'+vis]=[]                  
                        
                obj['pmodel']=None
                obj['pheader']=None
                if  'pmodel@'+tag in dat_dct.keys():
                    obj['pmodel']=dat_dct['pmodel@'+tag]
                    obj['pheader']=dat_dct['pheader@'+tag]
                                              
                
    if  verbose==True:            
        print(">>>>>{0:^10} : {1:<8.5f} seconds ---\n".format('initialize-total',time.time() - start_time))
                
    return models



def model_fill2(models,nsamps=100000,decomp=False,verbose=False):
    """
    create reference/intrinsic models and fill them into the model container

    Notes (on evaluating efficiency):
    
        While building the intrinsic data-model from a physical model can be expensive,
        the simulated observation (2D/3D convolution or UV sampling) is usually the bottle-neck.
        
        some tips to improve the effeciency:
            + exclude empty (masked/flux=0) region for the convolution
            + joint all objects in the intrinsic model before the convolution, e.g.
                overlapping objects, lines
            + use to low-dimension convolution when possible (e.g. for the narrow-band continumm) 
            
        before splitting line & cont models:
            --- apicall   : 2.10178  seconds ---
        after splitting line & cont models:
            --- apicall   : 0.84662  seconds ---
    
    
    """
    
    if  verbose==True:
        start_time = time.time()    

    mod_dct=models['mod_dct']
    
    #   add ref models OBJECT by OBJECT
                
    for tag in list(mod_dct.keys()):

        #   skip if no "type" or the item is not a physical model
        
        obj=mod_dct[tag]
        
        if  verbose==True:
            print("+"*40); print('@',tag); print('type:',obj['type']) ; print("-"*40)

        if  'vis' in mod_dct[tag].keys():
            
            vis_list=mod_dct[tag]['vis'].split(",")
            
            for vis in vis_list:
                
                test_time = time.time()
                
                if  'disk2d' in obj['type'].lower():
                    #test_time = time.time()

                    model_disk2d2(models['header@'+vis],obj,
                                        model=models['imodel@'+vis],
                                        factor=5)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('fill:  '+tag+'-->'+vis+' disk2d',time.time() - test_time))
                    #print(imodel.shape)
                    #models['imod2d@'+vis]+=imodel
                    #models['imodel@'+vis]+=imodel
                    
                if  'disk3d' in obj['type'].lower():
                    #pprint(obj)
                    #test_time = time.time()              
                    imodel_prof=model_disk3d2(models['header@'+vis],obj,
                                                    model=models['imodel@'+vis],
                                                    nsamps=nsamps,fixseed=False,mod_dct=mod_dct)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('fill:  '+tag+'-->'+vis+' disk3d',time.time() - test_time))
                    #print(imodel.shape)
                    #models['imod3d@'+vis]+=imodel
                    models['imod3d_prof@'+tag+'@'+vis]=imodel_prof.copy()
                    #models['imodel@'+vis]+=imodel     
                    
          
                    
    if  verbose==True:            
        print(">>>>>{0:^10} : {1:<8.5f} seconds ---\n".format('fill-total',time.time() - start_time))
    
    return
