import os
import configparser
from astropy.io import fits

from io import StringIO
import astropy.units as u
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from numbers import Number
from astropy.units import Quantity

import numpy as np

import logging
from pprint import pformat



from io import StringIO
import astropy.units as u
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from numbers import Number
from astropy.units import Quantity

from asteval import Interpreter
aeval = Interpreter(use_numpy=True,err_writer=StringIO())
aeval.symtable['u']=u
aeval.symtable['SkyCoord']=SkyCoord
aeval.symtable['Angle']=Angle
aeval.symtable['Number']=Number
aeval.symtable['Quantity']=Quantity
aeval.symtable['np'] = np

from pprint import pprint

from copy import deepcopy

from .utils.meta import inp_config
#import copy
#from copy import copy

logger = logging.getLogger(__name__)

def read_inp(parfile,log=False):
    """
    read parameters/setups from a .inp file into a dictionary nest:
        inp_dct[id][keywords]=values.
        inp_dct['comments']='??'
        inp_dct['changlog']='??'
        inp_dct['optimize']='??'
        
    keyword value formatting
        1.remove trailing/prefix space / comments
        2.split my space
        3.first element is the key
        4.the rest elements will be filled into value
            more than one element : list
            one element: scaler
    """
    cfg=configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    cfg.optionxform = str   # make the key case sensitive
    cfg.read(parfile)
    inp_dict=deepcopy(cfg._sections)
    
    for section in inp_dict:
        # logger.debug(section)
        for key in inp_dict[section]:
            expr=inp_dict[section][key]
            value=aeval(expr)
            if  len(aeval.error)>0 and value is None:
                exprs=expr.split()
                value=[aeval(expr) for expr in exprs]
            value=key_intepreter(key,value)
            # logger.debug('    {} : {}'.format(key,expr))
            # logger.debug('        {} : {}'.format(type(value).__name__,value))
            inp_dict[section][key]=value
    inp_dict['ism3d.inp']=cfg
    
    return inp_dict

def key_intepreter(key,value):
    """
    additional customized interpretaion of key values 
    """
    value_int=value
    
    if  key=='xypos':
        if  isinstance(value,str):
            value_int=SkyCoord(value,frame='icrs')
        if  isinstance(value,(tuple,list)):
            value_int=SkyCoord(value[0],value[1],frame='icrs',unit='deg')
    
    return value_int

def eval_func(vs_func_ps, var_dict):
    """
    Do an inline calculation from a string expression in a lambda function-like syntax


        1st: element
    expr    :    expected to be a tuple
        expr[0]   string: 
            lamabda function-like syntax defining a anonymous function and its variable(s)
            the variables' name and content should exist in the dictionary "locals" 
        expr[1],expr[2],expr[3]
            function parameters
    output:
        the function's value at each points of variables under the given parameters

    example: 
        eval_func(('rho : minimum(rho/p2,1.0)*p1',200*u.km/u.s,5*u.kpc),locals())

        the function call will calculate "minimum(rho/p2,1.0)*p1" assuming 
        p1=200*u.km/u.s & p2=5*u.kpc at each "rho" value. 
        Here, "rho" is a local-scope variable containing a numpy array 
    """

    vs = vs_func_ps[0].split(" : ")[0].split(",")
    func = vs_func_ps[0].split(" : ")[1].strip()

    # add variable into the symtable
    for v in vs:
        aeval.symtable[v.strip()] = var_dict[v.strip()]

    # add parameters (p1,p2,p3..) into the symtable
    for ind in range(1, len(vs_func_ps)):
        aeval.symtable["p"+str(ind)] = vs_func_ps[ind]

    return aeval(func)

def write_inp(inp_dict,
              parfile='test,inp',overwrite=True):
    """
    """
    with open(parfile,'w') as configfile:
        inp_dict['ism3d.inp'].write(configfile)

def inp_to_mod(inp_dict):
    """
    """
    
    mod_dict=deepcopy(inp_dict)
    imported_sections=[]
    
    #   import reference keys
    
    for section in mod_dict:
        for key in list(mod_dict[section]):
            if  not (key.lower()=='import' and isinstance(mod_dict[section][key], str)):
                continue
            import_list = (mod_dict[section][key]).split(',')
            del mod_dict[section][key]
            for import_section in import_list:
                if  import_section in mod_dict:
                    imported_sections.append(import_section)
                    for import_key in list(mod_dict[import_section]):
                        mod_dict[section][import_key] = mod_dict[import_section][import_key]

    #   remove imported sections
    
    for imported_section in list(set(imported_sections)):
        del mod_dict[imported_section]  
        
    #   remove unrelated configuration sections
    
    for section in list(mod_dict):
        if  section.startswith('ism3d.'):
            del mod_dict[section]
            
                            
    return mod_dict

                    #logger.debug('{:16}'.format(key+'@'+tag)+' : '+'{:16}'.format(value)+'-->'+str(objs[tag][key]))

# def inp2mod(inp_dct):
#     """
#     Convert Input Parameter Dictionary to Model Properties Dictionary
# 
#     The code will make a dictionary ready for model constructions, including:
#         + add the default values
#         + fill optional keywords
#         + fill the "tied" values
# 
#     inp_dct
# 
#     --> write_par (changed some modeling parameter values, e.g. shifting during the optimization iteration) 
# 
#     inp_dct_modified
# 
#     --> inp2mod (fullfill the default value / ties / reject comments <-- act as a formatter) 
# 
#     mod_dct
# 
#     """
# 
#     objs = deepcopy(inp_dct)
# 
#     ids_ignore = cfg['inp.comment']['id'].split(',') +\
#         cfg['inp.analyzer']['id'].split(',') +\
#         cfg['inp.general']['id'].split(',') +\
#         cfg['inp.optimizer']['id'].split(',')
# 
#     #   assemble all parameters
# 
#     par_list = []
#     for sec_name in objs.keys():
#         for key_name in objs[sec_name].keys():
#             if '@' not in key_name:
#                 par_list += [key_name+'@'+sec_name]
# 
#     secs_imported = []
# 
#     for tag in list(objs.keys()):
# 
#         #   remove sections not related to model component properties
# 
#         if any(section in tag.lower() for section in ids_ignore):
#             tmp = objs.pop(tag, None)
#             continue
# 
#         for key in list(objs[tag].keys()):
# 
#             # fill the cross reference keyword-value
# 
#             if isinstance(objs[tag][key], (list, tuple)):
#                 value_list = [value for value in objs[tag][key]]
#             else:
#                 value_list = [objs[tag][key]]
# 
#             for idx, value in enumerate(value_list):
#                 if isinstance(value, str):
#                     pars = [par for par in par_list if par in value]
#                     if pars != []:
#                         value_expr = value
#                         for idp, par in enumerate(pars):
#                             #par=max(pars, key=len)
#                             keyobjname = par.split("@")
#                             aeval.symtable["t" +
#                                            str(idp)] = objs[keyobjname[1]][keyobjname[0]]
#                             value_expr = value_expr.replace(par, "t"+str(idp))
#                         value_list[idx] = aeval(value_expr)
# 
#             if isinstance(objs[tag][key], tuple):
#                 objs[tag][key] = tuple(value_list)
#             elif isinstance(objs[tag][key], list):
#                 objs[tag][key] = value_list
#             else:
#                 objs[tag][key] = value_list[0]
# 
#             # fill "import" sections
# 
#             if key.lower() == 'import' and isinstance(objs[tag][key], str):
# 
#                 import_list = (objs[tag][key]).split(',')
#                 del objs[tag][key]
#                 for value0 in import_list:
#                     if value0 in list(objs.keys()):
#                         secs_imported += [value0]
#                         for import_key in list(objs[value0].keys()):
#                             objs[tag][import_key] = objs[value0][import_key]
# 
#                     #logger.debug('{:16}'.format(key+'@'+tag)+' : '+'{:16}'.format(value)+'-->'+str(objs[tag][key]))
# 
#     #   for "imported" parameter group sections, we delete them one by one
# 
#     for par_group in list(set(secs_imported)):
#         del objs[par_group]
# 
#     #   for "non-general" sections, we delete those without keyword "type"
# 
#     for section in list(objs.keys()):
#         if ('type' not in list(objs[section].keys())) and ('general' not in section.lower()):
#             del objs[section]
# 
#     return objs

#from configparser import ConfigParser, ExtendedInterpolation
#cfg=ConfigParser(interpolation=ExtendedInterpolation())
#cfg=ConfigParser(interpolation=ExtendedInterpolation())
#cfg.read(inpfile)
#cfg_dict=cfg._sections

#pprint(cfg_dict)

#cfg_out = ConfigParser()
#cfg_out.read_dict(cfg_dict)
#cfg_out['database']['pb']=['../test_discretize/mockup_multiobjs_withnoise.ms/dm.pb.fits',
#                           '../test_discretize/mockup_multiobjs_withnoise.ms']
#with open('example.cfg', 'w') as configfile:
#    cfg_out.write(configfile)

        

# def write_inp(inp_dct,
#               inpfile='example.inp', overwrite=False):
#     """
#     write out inp files from inp_dct
#     if overwrite=False, the function will try to append .0/.1/.2... to the .inp file name
#     writepar is two-element tuple, first element is the key name to be modified
#                                    second element is the value
# 
#     note: py>=3.7 use the ordered dict by default (so the output keyword order is preserved) 
#     """
# 
#     logger.info('save the model input parameter: '+inpfile)
# 
#     inp_dct0 = deepcopy(inp_dct)
# 
#     outname = inpfile
# 
#     ind = 0
#     if overwrite == False:
#         while os.path.isfile(outname):
#             outname = inpfile+'.'+str(ind)
#             ind += 1
# 
#     f = open(outname, 'w')
#     output = ''
#     for obj in inp_dct0.keys():
#         output += '#'*80+'\n'
#         output += '@'+obj+'\n'
#         output += '#'*80+'\n\n'
#         for key in inp_dct0[obj].keys():
#             # print(repr_parameter(inp_dct0[obj][key]))
#             output += '{:20} {}\n'.format(key,
#                                           repr_parameter(inp_dct0[obj][key]), format=200)
#         output += '\n'
#     f.write(output)
#     f.close()



# def read_inp(parfile,log=False):
#     """
#     read parameters/setups from a .inp file into a dictionary nest:
#         inp_dct[id][keywords]=values.
#         inp_dct['comments']='??'
#         inp_dct['changlog']='??'
#         inp_dct['optimize']='??'
#         
#     keyword value formatting
#         1.remove trailing/prefix space / comments
#         2.split my space
#         3.first element is the key
#         4.the rest elements will be filled into value
#             more than one element : list
#             one element: scaler
#     """
    
#     #print("**********exe read_inp()**************")
#     
# 
#     cfg=inp_config(file=None)
#     
#     inp_dct={}
#     with open(parfile,'r') as f:
#         lines=f.readlines()
#     lines= filter(None, (line.split('#')[0].strip() for line in lines))

#     tag='default'
#     
#     for line in lines:
#         if  line.startswith('@'):
#             tag=line.replace('@','',1).strip()
#             #pars={'content':''}
#             pars={}
#             #pars['content']+=line+"\n"
#             if  log==True:
#                 logger.debug("+"*40)
#                 logger.debug('@ {}'.format(tag))
#                 logger.debug("-"*40)
#         else:
#             
#             if  any(section in tag.lower() for section in cfg['inp.comment']['id'].split(',')):
#                 pass
#                 #pars['content']+=line+"\n"
#                 #inp_dct[tag]=pars
#             else:
#                 #pars['content']+=line+"\n"               
#                 #   identify the "key"
#                 key=line.split()[0]
#                 #   remove leading/trailing space to get the "value" portion
#                 expr=line.replace(key,'',1).strip()
#                 if  log==True:
#                     logger.debug('{:20}'.format(key)+" : "+str(expr))
#                 
#                 """                    
#                 try:                #   likely mutiple-elements are provided, 
#                                     #   but be careful of eval() usage here
#                                     #   e.g.:"tuple (1)" will be a valid statement
#                     #pars[key]=eval(value)
#                     #pars[key]=ast.literal_eval(value)
#                     pars[key]=aeval(value)
#                 except SyntaxError: #   pack the value content into a list
#                     values=value.split()
#                     #pars[key]=[eval(value0) for value0 in value]
#                     #pars[key]=[ast.literal_eval(value0) for value0 in value]
#                     pars[key]=[aeval(value0) for value0 in values]
#                 """
#                 value=aeval(expr)
#                 if  len(aeval.error)>0 and value is None:
#                     exprs=expr.split()
#                     value=[aeval(expr) for expr in exprs]
#                 
#                 pars[key]=pars_interp(key,value)
#                 inp_dct[tag]=pars
# 
#     
#     if  'general' in inp_dct.keys():
#         if  'outdir' in (inp_dct['general']).keys():
#             outdir=inp_dct['general']['outdir']
#             if  isinstance(outdir,str): 
#                 if  not os.path.exists(outdir):
#                     os.makedirs(outdir)
#                 #np.save(outdir+'/inp_dct.npy',inp_dct)
#                 #write_inp(inp_dct,inpfile=outdir+'/p_start.inp',
#                 #          overwrite=True)
       

