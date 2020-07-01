
import sys, socket, multiprocessing

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