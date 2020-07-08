
import os,sys, socket, multiprocessing

from psutil import virtual_memory
from pip._vendor import pkg_resources

import numpy as np

import logging
logger = logging.getLogger(__name__)

import gc

from astropy.units import Quantity
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
import astropy.units as u

import operator

import ism3d

def check_config():
    
    logger.info("\n"+"#"*80)
    logger.info("Python version:   {}".format(sys.version))
    logger.info("Host Name:        {}".format(socket.gethostname()))
    logger.info("Num of Core:      {}".format(multiprocessing.cpu_count()))
    mem=virtual_memory()
    logger.info("Total Memory:     {}".format(convert_size(mem.total)))
    logger.info("Available Memory: {}".format(convert_size(mem.available)))
    
    logger.info("#"*80)
    check_deps()
    logger.info("#"*80)
    check_fftpack()
    logger.info("#"*80+'\n')    
    
    
    
def check_deps(package_name='ism3d'):
    
    package = pkg_resources.working_set.by_key[package_name]
    deps = package.requires()
    for r in deps:
        name=str(r.name)
        version_required=str(r.specifier)
        if  version_required=='':
            version_required='unspecified'
        version_installed=pkg_resources.working_set.by_key[name].version
        logger.info('{0:<18} {1:<12} {2:<12}'.format(name,version_required,version_installed))

    return    

def check_fftpack():
    
    logger.info('fft_use:          {}'.format(ism3d.fft_use.__name__))
    logger.info('fft_fastlen:      {}.{}'.format(ism3d.fft_fastlen.__module__,ism3d.fft_fastlen.__name__))
    
    return

def convert_size(size_bytes): 
    """
    **obsolete** now we use human_unit()/human_to_string()
    """
    if size_bytes == 0: 
        return "0B" 
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB") 
    i = int(np.floor(np.log(size_bytes)/np.log(1024)))
    power = np.power(1024, i) 
    size = round(size_bytes / power, 2) 
    return "{} {}".format(size, size_name[i])

def unit_shortname(unit, nospace=True, options=False):
    """
    convert unit to shortest name
    e.g.: (unit_shortname(u.Jy*u.km/u.s,nospace=False)

    In [5]: unit_shortname(u.Jy*u.km/u.s,nospace=False)                                                                 
    Out[5]: 'Jy km / s'

    In [6]: unit_shortname(u.Jy*u.km/u.s,nospace=True)                                                                  
    Out[6]: 'Jykm/s'    

    ref:
    https://docs.astropy.org/en/stable/units/format.html#astropy-units-format
    """

    format_all = ['generic', 'unscaled', 'cds', 'console',
                  'latex', 'latex_inline', 'ogip', 'unicode', 'vounit']
    unit_names = []
    try:
        unit_names += unit.names
    except AttributeError as error:
        unit_names += [unit.to_string(format=f) for f in format_all]
    if options == True:
        print(unit_names)
    unit_string = min(unit_names, key=len)
    if nospace == True:
        unit_string = unit_string.replace(' ', '')

    return unit_string

def human_unit(quantity, return_unit=False, base_index=0, scale_range=None):

    """
    Sugguest a better unit for the quantity and make it more human readable
    e.g. 1200 m/s -> 1.2 km/s
        
    return_unit:
        False:          return the input quantity in a suggested unit
        True:           just return a suggested unit

    base_index:
        the index of the unitbase which we examine its prefix possibility.
            
    For time:           try built-in astropy.utils.console.human_time()
    For file size:      one may also use astropy.utils.concolse.human_file_size()

    reference:    https://docs.astropy.org/en/stable/_modules/astropy/units/core.html
    
    have tried the functions below,they work similar for PrefixUnit, but they dont work well 
    with composited units (e.g. u.km/u.s)
        get_current_unit_registry().get_units_with_physical_type(unit)
        unit.find_equivalent_units(include_prefix_units=True)
        unit.compose(include_prefix_units=True) might work but the results can be unexpected
    note:
        get_units_with_same_physical_type() is a private method, since end users should be encouraged
        to use the more powerful `compose` and `find_equivalent_units`
        methods (which use this under the hood).
        
    help find the best human readable unit
    then you can do q.to_string(unit='*')        
    
    """

    
    if  not quantity.isscalar:
        raise Exception("given quantity is not scalar")
   
    human_unit=quantity.unit

    bases=human_unit.bases.copy()
    powers=human_unit.powers.copy()
    base=bases[base_index]
    candidate_list=(base).compose(include_prefix_units=True,max_depth=1)
    
    if  base.is_equivalent(u.byte):
        base_factor=2**10
    elif    base.is_equivalent(u.s):
        base_factor=60
    else:
        base_factor=1e3

    for candidate in candidate_list:
    
        if  scale_range is not None:
            if  candidate.scale < min(scale_range) or candidate.scale > max(scale_range):
                continue
        
        if  1 <= abs(quantity.value)*candidate.scale < base_factor and \
            (np.log(candidate.scale)/np.log(base_factor)).is_integer():
            
            human_base=(candidate.bases)[0]
            bases[base_index]=human_base
            human_unit=u.Unit(1)
            for b, p in zip(bases, powers): 
                human_unit *= b if p == 1 else b**p # make sure back to PrefixUnit when possible
            break

    if  return_unit==False:
        return quantity.to(human_unit)
    else:
        return human_unit

def human_to_string(q,format_string='{0.value:0.2f} {0.unit:shortname}',nospace=True):
    """
    A slightly more fancy version of quality.to_string()
    add the option of 0.units:shortname in formating string syntax
    # https://docs.astropy.org/en/stable/units/format.html#astropy-units-format
    
    format: forwarded to .to_string(format):
        options: generic, unscaled, cds, console, fits, latex, latex_inline, ogip, unicode, vounit
    
    format_string: {0:0.2f} {1}
        help format you output when output='string'
        
    output: 
        'string':       a string represent the input quantity in best-guess unit

            
    For time:           try built-in astropy.utils.console.human_time()
    For file size:      one may also use astropy.utils.concolse.human_file_size()

    print(human_to_string(q,format_string='{0.value:0.2f} {0.unit:shortname}',nospace=False))
    print(human_to_string(q,format_string='{0.value:0.2f}{0.unit:shortname}',nospace=True))
    print(human_to_string(q,format_string='{0.value:0.2f}{0.unit:cds}',nospace=True))
    print(human_to_string(q,format_string='{0.value:0.2f} in {0.unit:shortname}',nospace=True))
    print(human_to_string(q,format_string='{0.value:0.2f} in {0.unit:cds}',nospace=True))
    
    """
    format_use=format_string
    if  '0.unit:shortname' in format_use:
        format_use=format_string.replace("0.unit:shortname",'1')
        return format_use.format(q,unit_shortname(q.unit,nospace=nospace))
    else:
        return format_string.format(q)

    
    #if  'lmfit' in inp_dct['optimize']['method']:
    #    gmake_lmfit_analyze(fit_dct,sampler['inp_dct'],sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)        

def get_obj_size(obj,to_string=False):
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    if  to_string==True:
        sz=human_unit(sz*u.byte)
        sz=human_to_string(sz,format_string='{0.value:3.0f} {0.unit:shortname}')
        
    return sz   

def prepdir(filename):
    """
    """
    dirname = os.path.dirname(filename)
    if (not os.path.exists(dirname)) and (dirname != ''):
        os.makedirs(dirname)   
        
        
def render_component(out,im,scale=1,mode='iadd'):
    """
    in-plane-add model components into spectral-cube or mutil-freq MS
    see other mode options: e.g. iadd/isub
        https://docs.python.org/3.8/library/operator.html
    
    out=None return a new obect
    out!=None return a reference point to the updated out
    
    Note:
        this may return a view of numpy if out is a slice 
        
    from gmake.discretize import render_component
    cube=np.zeros((3,3,3))
    
    cube[0,:,:]=render_component(cube[0,:,:],np.ones((3,3)),scale=5)
    x=render_component(cube[0,:,:],np.ones((3,3)),scale=5) 
    np.may_share_memory(x,cube)
    
    warning: 
        cube=render_component(cube[0,:,:],np.ones((3,3)),scale=5)
        will override your cube values.. 
        one should use instead:
        cube[0,:,:]=render_component(cube[0,:,:],np.ones((3,3)),scale=5)
    if im=[], it will do nothing...          
    
    
    if  you're not sure out is None, maybe use:
        out=render_component(out)
    if  you know out is not None, use
        render_component(out)
    
    """
    if  out is not None:
        
        if  isinstance(im,list):
            for i in range(len(im)):
                out=render_component(out,im[i],scale=scale[i],mode=mode)
        else:
            out=getattr(operator,mode)(out,im*scale)
    else:
        if  isinstance(im,list):
            for i in range(len(im)):
                out=render_component(out,im[i],scale=scale[i],mode=mode)
        else:
            out=im*scale
            
    return out

def pickplane(im,iz):
    """
    pick a channel plane from a "cube"
    """
    if  im.ndim==2:
        return im
    if  im.ndim==3:
        return im[iz,:,:]
    if  im.ndim==4:
        return im[0,iz,:,:]            
    


    
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