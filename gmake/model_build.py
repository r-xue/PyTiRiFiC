from .gmake_init import *
from .model_func import *
from .model_func_dynamics import *
from .io_utils import *

logger = logging.getLogger(__name__)

def model_api(mod_dct,dat_dct,nsamps=100000,decomp=False,verbose=False):
    """
    use model properties (from mod_dct) and data metadata info (from dat_dct) to
    create a data model
    """
    
    if  verbose==True:
        start_time = time.time()
    models=model_init(mod_dct,dat_dct,decomp=decomp,verbose=False)
    if  verbose==True:            
        print("---{0:^10} : {1:<8.5f} seconds ---\n".format('initialize-total',time.time() - start_time))

    if  verbose==True:
        start_time = time.time()        
    models=model_fill(models,decomp=decomp,verbose=False,nsamps=nsamps)
    if  verbose==True:            
        print("---{0:^10} : {1:<8.5f} seconds ---\n".format('fill-total',time.time() - start_time))
            
    if  verbose==True:
        start_time = time.time()    
    models=model_simobs(models,decomp=decomp,verbose=False)
    if  verbose==True:            
        print("---{0:^10} : {1:<8.5f} seconds ---".format('simulate-total',time.time() - start_time))

    return models

def model_init(mod_dct,dat_dct,decomp=False,verbose=False):
    """
    create model container 

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
    note: imod2d                : Hold Emission Conponents with Frequency-Dependent Spatial Distribution
          imod3d                : Hold Emission Conponents with Frequency-Dependent Spatial Distribution
          imodel=imod2d+imod3d  : We always keep a copy of imod2d and imod3d to improve the effeicnecy in simobs() 
          
    """
    models={'mod_dct':mod_dct.copy()}
                
    for tag in list(mod_dct.keys()):
        
        obj=models['mod_dct'][tag]
        
        if  verbose==True:
            print("+"*40); print('@',tag); print('method:',obj['method']) ; print("-"*40)

        if  'vis' in mod_dct[tag].keys():
            
            vis_list=mod_dct[tag]['vis'].split(",")
            
            for vis in vis_list:
                
                if  'data@'+vis not in models.keys():
                    
                    #   pass the data reference (no memory penalty)
                    
                    models['data@'+vis]=dat_dct['data@'+vis]
                    models['type@'+vis]=dat_dct['type@'+vis]
                    models['weight@'+vis]=dat_dct['weight@'+vis]   
                    models['uvw@'+vis]=dat_dct['uvw@'+vis]
                    models['chanfreq@'+vis]=dat_dct['chanfreq@'+vis]
                    models['chanwidth@'+vis]=dat_dct['chanwidth@'+vis]
                    models['phasecenter@'+vis]=dat_dct['phasecenter@'+vis]
                    
                    wv=np.mean(const.c/models['chanfreq@'+vis])
                    
                    nxy, dxy = get_image_size(models['uvw@'+vis][:,0]/wv, models['uvw@'+vis][:,1]/wv, verbose=False)
                    nxy=128
                    
                    data_path=os.path.dirname(os.path.abspath(__file__))+'/data/'
                    header=fits.Header.fromfile(data_path+'image_template.header',endcard=False,sep='\n',padding=False)
                    header['NAXIS1']=nxy
                    header['NAXIS2']=nxy
                    header['NAXIS3']=np.size(models['chanfreq@'+vis])
                    header['CRVAL1']=models['phasecenter@'+vis][0]
                    header['CRVAL2']=models['phasecenter@'+vis][1]
                    crval3=models['chanfreq@'+vis]
                    if  not np.isscalar(crval3):
                        crval3=crval3[0]
                    header['CRVAL3']=crval3
                    header['CDELT1']=-np.rad2deg(dxy)
                    header['CDELT2']=np.rad2deg(dxy)
                    header['CDELT3']=np.mean(dat_dct['chanwidth@'+vis])   
                    header['CRPIX1']=np.floor(nxy/2)+1
                    header['CRPIX2']=np.floor(nxy/2)+1
                    
                    models['header@'+vis]=header.copy()
                    naxis=(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])
                    #   uvmodel: np.complex64
                    #   imodel:  np.float32
                    models['imodel@'+vis]=np.zeros(naxis,dtype=np.float32)
                    models['imod2d@'+vis]=np.zeros(naxis,dtype=np.float32)
                    models['imod3d@'+vis]=np.zeros(naxis,dtype=np.float32)
                                    
                    models['uvmodel@'+vis]=np.zeros((models['data@'+vis].shape)[0:2],
                                                    dtype=models['data@'+vis].dtype,
                                                    order='F')
                    if  decomp==True:
                        models['uvmod2d@'+vis]=np.zeros((models['data@'+vis].shape)[0:2],
                                                    dtype=models['data@'+vis].dtype,
                                                    order='F')                        
                        models['uvmod3d@'+vis]=np.zeros((models['data@'+vis].shape)[0:2],
                                                    dtype=models['data@'+vis].dtype,
                                                    order='F')
                        
                obj['pmodel']=None
                obj['pheader']=None
                if  'pmodel@'+tag in dat_dct.keys():
                    obj['pmodel']=dat_dct['pmodel@'+tag]
                    obj['pheader']=dat_dct['pheader@'+tag]
                                        

                    
        if  'image' in mod_dct[tag].keys():
            
            image_list=mod_dct[tag]['image'].split(",")
            
            for image in image_list:
                                
                if  'data@'+image not in models.keys():
                    
                    #test_time = time.time()
                    models['header@'+image]=dat_dct['header@'+image]
                    models['data@'+image]=dat_dct['data@'+image]
                    models['error@'+image]=dat_dct['error@'+image]   
                    models['mask@'+image]=dat_dct['mask@'+image]
                    models['type@'+image]=dat_dct['type@'+image]
                    
                    if  'sample@'+image in dat_dct.keys():
                        models['sample@'+image]=dat_dct['sample@'+image]
                    else:
                        models['sample@'+image]=None                                        
                    
                    if  'psf@'+image in dat_dct.keys():
                        models['psf@'+image]=dat_dct['psf@'+image]
                    else:
                        models['psf@'+image]=None
                    naxis=models['data@'+image].shape
                    if  len(naxis)==3:
                        naxis=(1,)+naxis
                    models['imodel@'+image]=np.zeros(naxis)
                    models['cmodel@'+image]=np.zeros(naxis)
                    #   save 2d objects (even it has been broadcasted to 3D for spectral cube)
                    #   save 3D objects (like spectral line emission from kinmspy/tirific)
                    models['imod2d@'+image]=np.zeros(naxis)
                    models['imod3d@'+image]=np.zeros(naxis)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('import:'+image,time.time() - test_time))
      
                obj['pmodel']=None
                obj['pheader']=None
                if  'pmodel@'+tag in dat_dct.keys():
                    obj['pmodel']=dat_dct['pmodel@'+tag]
                    obj['pheader']=dat_dct['pheader@'+tag]      
                
        
    return models


def model_fill(models,nsamps=100000,decomp=False,verbose=False):
    """
    create reference/intrinsic models and fill them into the model container

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
    """

    mod_dct=models['mod_dct']
    
    #   add ref models OBJECT by OBJECT
                
    for tag in list(mod_dct.keys()):

        #   skip if no "method" or the item is not a physical model
        
        obj=mod_dct[tag]
        
        if  verbose==True:
            print("+"*40); print('@',tag); print('method:',obj['method']) ; print("-"*40)

        if  'vis' in mod_dct[tag].keys():
            
            vis_list=mod_dct[tag]['vis'].split(",")
            
            for vis in vis_list:
                
                                
                test_time = time.time()
                
                
                if  'disk2d' in obj['method'].lower():
                    test_time = time.time()
                    pintflux=0.0
                    if  'pintflux' in obj:
                        pintflux=obj['pintflux']
                    imodel=model_disk2d(models['header@'+vis],obj['xypos'][0],obj['xypos'][1],
                                             r_eff=obj['sbser'][0],n=obj['sbser'][1],posang=obj['pa'],
                                             ellip=1.-np.cos(np.deg2rad(obj['inc'])),
                                             pintflux=pintflux,
                                             intflux=obj['intflux'],restfreq=obj['restfreq'],alpha=obj['alpha'])
                    print("---{0:^10} : {1:<8.5f} seconds ---".format('fill:  '+tag+'-->'+vis+' disk2d',time.time() - test_time))
                    print(imodel.shape)
                    models['imod2d@'+vis]+=imodel
                    models['imodel@'+vis]+=imodel
                    
                if  'kinmspy' in obj['method'].lower():
                    
                    test_time = time.time()              
                    imodel,imodel_prof=model_disk3d(models['header@'+vis],obj,nsamps=nsamps,fixseed=False,mod_dct=mod_dct)
                    print("---{0:^10} : {1:<8.5f} seconds ---".format('fill:  '+tag+'-->'+vis+' kinmspy',time.time() - test_time))
                    print(imodel.shape)
                    models['imod3d@'+vis]+=imodel
                    models['imod3d_prof@'+tag+'@'+vis]=imodel_prof.copy()
                    models['imodel@'+vis]+=imodel     
                    
        if  'image' in mod_dct[tag].keys():
            
            image_list=mod_dct[tag]['image'].split(",")
            
            for image in image_list:
                
                if  'disk2d' in obj['method'].lower():
                    #test_time = time.time()
                    pintflux=0.0
                    if  'pintflux' in obj:
                        pintflux=obj['pintflux']
                    imodel=model_disk2d(models['header@'+image],obj['xypos'][0],obj['xypos'][1],
                                             r_eff=obj['sbser'][0],n=obj['sbser'][1],posang=obj['pa'],
                                             ellip=1.-np.cos(np.deg2rad(obj['inc'])),
                                             pintflux=pintflux,
                                             intflux=obj['intflux'],restfreq=obj['restfreq'],alpha=obj['alpha'])
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('test:'+image,time.time() - test_time))
                    #print(imodel.shape)
                    models['imod2d@'+image]+=imodel
                    models['imodel@'+image]+=imodel
                    
    
                if  'kinmspy' in obj['method'].lower():
                    #test_time = time.time()              
                    
                    imodel,imodel_prof=model_disk3d(models['header@'+image],obj,nsamps=nsamps,fixseed=False,mod_dct=mod_dct)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('test:'+image,time.time() - test_time))
                    #print(imodel.shape)
                    models['imod3d@'+image]+=imodel
                    models['imod3d_prof@'+tag+'@'+image]=imodel_prof.copy()
                    models['imodel@'+image]+=imodel              
                    
    return models


def model_simobs(models,decomp=False,verbose=False):
    """
    simulate observations VIS BY VIS
    
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
            
    here, models is a mutable dict reference, and we don't really create any new objects
    """
              
    for tag in list(models.keys()):

        if  'imod2d@' in tag:

            if  models[tag.replace('imod2d@','type@')]=='vis':
                if  decomp==True:
                    uvmodel=model_uvsample(models[tag],models[tag.replace('imod2d@','header@')],
                                            models[tag.replace('imod2d@','data@')],
                                            models[tag.replace('imod2d@','uvw@')],
                                            models[tag.replace('imod2d@','phasecenter@')],
                                            average=True,
                                            verbose=False)
                    models[tag.replace('imod2d@','uvmod2d@')]=uvmodel.copy() 
                    models[tag.replace('imod2d@','uvmodel@')]+=uvmodel.copy() 
                else:
                    uvmodel=model_uvsample(models[tag],models[tag.replace('imod2d@','header@')],
                                            models[tag.replace('imod2d@','data@')],
                                            models[tag.replace('imod2d@','uvw@')],
                                            models[tag.replace('imod2d@','phasecenter@')],
                                            uvmodel_in=models[tag.replace('imod2d@','uvmodel@')],
                                            average=True,
                                            verbose=False)                    
                #
            if  models[tag.replace('imod2d@','type@')]=='image':
                cmodel,kernel=model_convol(models[tag],
                                     models[tag.replace('imod2d@','header@')],
                                     psf=models[tag.replace('imod2d@','psf@')],
                                     returnkernel=True,
                                     average=True,
                                     verbose=False)
                                           
                models[tag.replace('imod2d@','cmod2d@')]=cmodel.copy()
                models[tag.replace('imod2d@','cmodel@')]+=cmodel.copy()
                models[tag.replace('imod2d@','kernel@')]=kernel.copy()                      
            
        if  'imod3d@' in tag:

            if  models[tag.replace('imod3d@','type@')]=='vis':
                if  decomp==True:
                    uvmodel=model_uvsample(models[tag],models[tag.replace('imod3d@','header@')],
                                                models[tag.replace('imod3d@','data@')],
                                                models[tag.replace('imod3d@','uvw@')],
                                                models[tag.replace('imod3d@','phasecenter@')],
                                                average=False,
                                                verbose=False)
                    models[tag.replace('imod3d@','uvmod3d@')]=uvmodel.copy() 
                    models[tag.replace('imod3d@','uvmodel@')]+=uvmodel.copy()                     
                else:
                    uvmodel=model_uvsample(models[tag],models[tag.replace('imod3d@','header@')],
                                                models[tag.replace('imod3d@','data@')],
                                                models[tag.replace('imod3d@','uvw@')],
                                                models[tag.replace('imod3d@','phasecenter@')],
                                                uvmodel_in=models[tag.replace('imod3d@','uvmodel@')],
                                                average=False,
                                                verbose=False)                
                 #
             
            if  models[tag.replace('imod3d@','type@')]=='image':
                              #print('-->',tag)
                cmodel,kernel=model_convol(models[tag],
                                     models[tag.replace('imod3d@','header@')],
                                     psf=models[tag.replace('imod3d@','psf@')],
                                     returnkernel=True,
                                     average=False,
                                     verbose=False)
                models[tag.replace('imod3d@','cmod3d@')]=cmodel.copy()
                models[tag.replace('imod3d@','cmodel@')]+=cmodel.copy()
                models[tag.replace('imod3d@','kernel@')]=kernel.copy()
        
        #print(uvmodel.flags)
        #print("--")
        #print(models[tag.replace('imod2d@','uvmodel@')].flags)                                      
        #print(uvmodel is models[tag.replace('imod2d@','uvmodel@')])                               
        

        
    return models