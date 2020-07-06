import numpy as np
from .stats import pdf2rv
from .stats import cdf2rv
from .stats import custom_rvs
from .stats import custom_pdf
import astropy.units as u
import fast_histogram as fh
import pprint

import time
from astropy.coordinates.matrix_utilities import rotation_matrix,matrix_product,matrix_transpose
from astropy.coordinates.representation import SphericalRepresentation, CylindricalRepresentation, CartesianRepresentation
from astropy.coordinates.representation import SphericalDifferential, CylindricalDifferential, CartesianDifferential
from io import StringIO
from asteval import Interpreter
#aeval = Interpreter(err_writer=StringIO())
aeval = Interpreter()
aeval.symtable['u']=u

from .utils import rng_seeded,fft_fastlen,fft_use,eval_func,one_beam,sample_grid
from astropy._erfa import ufunc as erfa_ufunc
from astropy import constants as const

from astropy.modeling.models import Gaussian2D
from astropy.convolution import discretize_model
from .meta import create_header
from astropy.stats import sigma_clipped_stats
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.wcs import WCS
from scipy.interpolate import interpn

import galpy.potential as galpy_pot
from astropy.cosmology import Planck13
from scipy.interpolate import interp1d
import logging
from astropy.modeling import models as apmodels
from .discretize import uv_render, xy_render


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



 

def model_setup(mod_dct,dat_dct,verbose=False):
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
                    
                    if  'pbeam@'+vis not in dat_dct:
                        logger.debug('make imaging-header / pb model for:'+vis)
                        antsize=12*u.m
                        if  'VLA' in dat_dct['telescope@'+vis]:
                            antsize=25*u.m
                        if  'ALMA' in dat_dct['telescope@'+vis]:
                            antsize=12*u.m
                        #   pass the data reference (no memory penalty)
                        
                        #or [obj['xypos'].ra,obj['xypos'].dec]
                        center=dat_dct['phasecenter@'+vis]
                        # right now we are using the first object RA/DEC to make reference model imaging center
                        # also we hard-code the antenna size to 25*u.m
                        #center=[obj['xypos'].ra,obj['xypos'].dec]                                                    
                        
                        models['header@'+vis]=uv_to_header(dat_dct['uvw@'+vis],center,
                                                         dat_dct['chanfreq@'+vis],
                                                         dat_dct['chanwidth@'+vis])
                        models['pbeam@'+vis]=((makepb(models['header@'+vis],
                                                      phasecenter=dat_dct['phasecenter@'+vis],
                                                      antsize=antsize)).astype(np.float32)) #[np.newaxis,np.newaxis,:,:]
                    else:
                        models['header@'+vis]=dat_dct['header@'+vis]
                        models['pbeam@'+vis]=dat_dct['pbeam@'+vis]
                    
                    models['wcs@'+vis]=WCS(models['header@'+vis])
                    
                    #naxis=(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])
                    
                    models['imodel@'+vis]=None
                    models['objs@'+vis]=[]                  
                
                # get a lookup table when looping over dataset.
                if  obj['type']=='disk3d':
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
                
                if  mod_dct[tag]['type']=='disk3d':                    
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

def model_render(mod_dct, dat_dct, models=None,
                 saveimodel=False,verbose=False):
    """render component models into the data model container.
    
    Parameters
    ----------
    mod_dct : dict
        component container with realized reference models in physical units
    dat_dct : dict
        data container
    models : dict, optional
        model container
    
    Returns
    -------
    models : dict
        model container with rendered model inside
    
    """
    
    # build the model container (usually skipped during iterative optimization)
    
    if  models is None:
        models=model_setup(mod_dct,dat_dct,verbose=verbose)

    # calculate chisq 
           
    for tag in list(models.keys()):
        
        if  'imodel@' in tag:
            
            dname=tag.replace('imodel@','')
            objs=[mod_dct[obj] for obj in models[tag.replace('imodel@','objs@')]]
            w=models['wcs@'+dname]
            if  models[tag.replace('imodel@','type@')]=='vis':                
                model_one=uv_render(objs,w,
                                    dat_dct['uvw@'+dname],
                                    dat_dct['phasecenter@'+dname],
                                    pb=models['pbeam@'+dname])
            if  models[tag.replace('imodel@','type@')]=='image':
                imodel,model_one=xy_render(objs,w,
                                    psf=models['psf@'+dname],normalize_kernel=False,
                                    pb=models['pbeam@'+dname])

            models['model@'+dname]=model_one
            
            if  saveimodel==True:
                if  models[tag.replace('imodel@','type@')]=='vis': 
                    imodel=xy_render(objs,w,
                                    normalize_kernel=False)                    
                models['imodel@'+dname]=imodel
                
    return models

###################################################################################################


    
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
    #   PB size in pixel
    freqs=header['CRVAL3']+(np.arange(header['NAXIS3'])+1-header['CRPIX3'])*header['CDELT3'] # in hz
    beam=1.13*np.rad2deg(const.c.to_value('m/s')/freqs/antsize.to_value(u.m))
    beam*=1/np.abs(header['CDELT2'])
    
    pb=np.zeros((header['NAXIS3'],header['NAXIS2'],header['NAXIS1']))
    
    sigma2fwhm=np.sqrt(2.*np.log(2.))*2.
    for i in range(header['NAXIS3']):
        mod=Gaussian2D(amplitude=1.,
                       x_mean=xc,y_mean=yc,
                       x_stddev=beam[i]/sigma2fwhm,y_stddev=beam[i]/sigma2fwhm,theta=0)
        pb[i,:,:]=discretize_model(mod,(0,int(header['NAXIS1'])),(0,int(header['NAXIS2'])))

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
    