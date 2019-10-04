from .gmake_init import *
from .model_func import *
from .model_func_dynamics import *
from .io_utils import *
from .metadata import template_imheader

#from galario.double import get_image_size
#from galario.double import sampleImage
#from galario.double import chi2Image
from galario.single import get_image_size

logger = logging.getLogger(__name__)

def model_api(mod_dct,dat_dct,nsamps=100000,decomp=False,verbose=False):
    """
    use model properties (from mod_dct) and data metadata info (from dat_dct) to
    create a data model
    """
    
    models=model_init(mod_dct,dat_dct,decomp=decomp,verbose=verbose)
    models=model_fill(models,decomp=decomp,nsamps=nsamps,verbose=verbose)
    models=model_simobs(models,decomp=decomp,verbose=verbose)

    return models

def model_init(mod_dct,dat_dct,decomp=False,verbose=False):
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
                    
                    header=template_imheader.copy()
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
                    models['pbeam@'+vis]=((makepb(header)).astype(np.float32))[np.newaxis,np.newaxis,:,:]
                    
                    models['imod2d@'+vis]=np.zeros(naxis,dtype=np.float32)     # ny * nx
                    models['imod3d@'+vis]=np.zeros(naxis,dtype=np.float32)     # nz * ny * nx
                    
                                    
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
                
    if  verbose==True:            
        print(">>>>>{0:^10} : {1:<8.5f} seconds ---\n".format('initialize-total',time.time() - start_time))
                
    return models


def model_fill(models,nsamps=100000,decomp=False,verbose=False):
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

        #   skip if no "method" or the item is not a physical model
        
        obj=mod_dct[tag]
        
        if  verbose==True:
            print("+"*40); print('@',tag); print('method:',obj['method']) ; print("-"*40)

        if  'vis' in mod_dct[tag].keys():
            
            vis_list=mod_dct[tag]['vis'].split(",")
            
            for vis in vis_list:
                
                test_time = time.time()
                
                if  'disk2d' in obj['method'].lower():
                    #test_time = time.time()
                    pintflux=0.0
                    if  'pintflux' in obj:
                        pintflux=obj['pintflux']
                    imodel=model_disk2d(models['header@'+vis],obj['xypos'][0],obj['xypos'][1],
                                        model=models['imod2d@'+vis],
                                        r_eff=obj['sbser'][0],n=obj['sbser'][1],posang=obj['pa'],
                                        ellip=1.-np.cos(np.deg2rad(obj['inc'])),
                                        pintflux=pintflux,
                                        intflux=obj['intflux'],restfreq=obj['restfreq'],alpha=obj['alpha'])
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('fill:  '+tag+'-->'+vis+' disk2d',time.time() - test_time))
                    #print(imodel.shape)
                    #models['imod2d@'+vis]+=imodel
                    #models['imodel@'+vis]+=imodel
                    
                if  'disk3d' in obj['method'].lower():
                    
                    #test_time = time.time()              
                    imodel,imodel_prof=model_disk3d(models['header@'+vis],obj,
                                                    model=models['imod3d@'+vis],
                                                    nsamps=nsamps,fixseed=False,mod_dct=mod_dct)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('fill:  '+tag+'-->'+vis+' disk3d',time.time() - test_time))
                    #print(imodel.shape)
                    #models['imod3d@'+vis]+=imodel
                    models['imod3d_prof@'+tag+'@'+vis]=imodel_prof.copy()
                    #models['imodel@'+vis]+=imodel     
                    
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
                    
    
                if  'disk3d' in obj['method'].lower():
                    #test_time = time.time()              
                    
                    imodel,imodel_prof=model_disk3d(models['header@'+image],obj,nsamps=nsamps,fixseed=False,mod_dct=mod_dct)
                    #print("---{0:^10} : {1:<8.5f} seconds ---".format('test:'+image,time.time() - test_time))
                    #print(imodel.shape)
                    models['imod3d@'+image]+=imodel
                    models['imod3d_prof@'+tag+'@'+image]=imodel_prof.copy()
                    models['imodel@'+image]+=imodel              
                    
    if  verbose==True:            
        print(">>>>>{0:^10} : {1:<8.5f} seconds ---\n".format('fill-total',time.time() - start_time))
    
    return models


def model_simobs(models,decomp=False,verbose=False):
    """
    Simulate observations (dataset by dataset)
    
    models is expected to be a mutable dict reference, and we don't really create any new objects
    
    Notes (on evaluating efficiency):
    
        While building the intrinsic data-model from a physical model can be expensive,
        the simulated observation (i.e. 2D/3D convol or UV sampling) is usually the bottle-neck.
        
        To improve the performance, we implement some optimizations:
            for imaging-domain simulation:
                + merge all components (e.g.overlapping objects, lines) in the intrinsic/reference model before simulations, e.g.
                + exclude empty (masked/flux=0) regions
            for spectral-domain simulation:
                + seperate 2D component (continuum) from 3D component (line) and do simulation independently,
                  so only channels with the same emission morphology are process in a single simulation.
                  this is epsecially important if line emission only occapy a small number of channels
            
        
    print(uvmodel.flags)
    print(models[tag.replace('imod2d@','uvmodel@')].flags)                                      
    print(uvmodel is models[tag.replace('imod2d@','uvmodel@')])             
    
    the performance of model_uvsample is not very sensitive to the input image size.
    
    """
    
    if  verbose==True:
        start_time = time.time()    
              
    for tag in list(models.keys()):
        
        if  'imod3d@' in tag:
            
            if  models[tag.replace('imod3d@','type@')]=='vis':
                #print('\n',tag.replace('imod3d@',''),' image model shape: ',models[tag].shape)
                if  decomp==True:
                    uvmodel=model_uvsample(models[tag]*models[tag.replace('imod3d@','pbeam@')],None,
                                                models[tag.replace('imod3d@','header@')],
                                                models[tag.replace('imod3d@','uvw@')],
                                                models[tag.replace('imod3d@','phasecenter@')],
                                                uvdtype=models[tag.replace('imod3d@','data@')].dtype,
                                                average=True,
                                                verbose=verbose)
                    models[tag.replace('imod3d@','uvmod3d@')]=uvmodel.copy() 
                    models[tag.replace('imod3d@','uvmodel@')]+=uvmodel.copy()
                    uvmodel=model_uvsample(None,models[tag.replace('imod3d@','imod2d@')]*models[tag.replace('imod3d@','pbeam@')],
                                            models[tag.replace('imod3d@','header@')],
                                            models[tag.replace('imod3d@','uvw@')],
                                            models[tag.replace('imod3d@','phasecenter@')],
                                            uvdtype=models[tag.replace('imod3d@','data@')].dtype,
                                            average=True,
                                            verbose=verbose)
                    models[tag.replace('imod3d@','uvmod2d@')]=uvmodel.copy() 
                    models[tag.replace('imod3d@','uvmodel@')]+=uvmodel.copy()                                          
                else:
                    uvmodel=model_uvsample(models[tag]*models[tag.replace('imod3d@','pbeam@')],
                                           models[tag.replace('imod3d@','imod2d@')]*models[tag.replace('imod3d@','pbeam@')],
                                           models[tag.replace('imod3d@','header@')],
                                           models[tag.replace('imod3d@','uvw@')],
                                           models[tag.replace('imod3d@','phasecenter@')],
                                           uvmodel=models[tag.replace('imod3d@','uvmodel@')],
                                           uvdtype=models[tag.replace('imod3d@','data@')].dtype,
                                           average=True,
                                           verbose=verbose)                                   
            if  models[tag.replace('imod3d@','type@')]=='image':
                cmodel,kernel=model_convol(models[tag],
                                     models[tag.replace('imod3d@','header@')],
                                     psf=models[tag.replace('imod3d@','psf@')],
                                     returnkernel=True,
                                     average=False,
                                     verbose=verbose)
                models[tag.replace('imod3d@','cmod3d@')]=cmodel.copy()
                models[tag.replace('imod3d@','cmodel@')]+=cmodel.copy()
                models[tag.replace('imod3d@','kernel@')]=kernel.copy()
                cmodel,kernel=model_convol(models[tag.replace('imod3d@','imod2d@')],
                                     models[tag.replace('imod2d@','header@')],
                                     psf=models[tag.replace('imod2d@','psf@')],
                                     returnkernel=True,
                                     average=True,
                                     verbose=verbose)              
                models[tag.replace('imod3d@','cmod2d@')]=cmodel.copy()
                models[tag.replace('imod3d@','cmodel@')]+=cmodel.copy()
                models[tag.replace('imod3d@','kernel@')]=kernel.copy()                   
                              
        
    if  verbose==True:            
        print(">>>>>{0:^10} : {1:<8.5f} seconds ---".format('simulate-total',time.time() - start_time))
        
    return models