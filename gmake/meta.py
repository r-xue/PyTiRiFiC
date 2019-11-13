"""
Container for internal metadata/configuration variables under the program namespace


    inp_dct:    input parameter set (using quantities)
    mod_dct:    model parameter set (using quantities)
    obj_dct:    component parameter set (dimensionless, values in internal units)
"""

import os
from configparser import ConfigParser, ExtendedInterpolation
from astropy.io import fits

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



package_path=os.path.dirname(os.path.abspath(__file__))
metadata_path=os.path.dirname(os.path.abspath(__file__))+'/metadata/'

cfg=ConfigParser(interpolation=ExtendedInterpolation())
cfg.read(package_path+"/default.cfg") 

xymodel_header=fits.Header.fromfile(metadata_path+'xymodel.header',endcard=False,sep='\n',padding=False)

dat_dct_global={}

__all__ = ['read_inp']

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
    #print("**********exe read_inp()**************")
    
    inp_dct={}
    with open(parfile,'r') as f:
        lines=f.readlines()
    lines= filter(None, (line.split('#')[0].strip() for line in lines))

    tag='default'
    
    for line in lines:
        if  line.startswith('@'):
            tag=line.replace('@','',1).strip()
            #pars={'content':''}
            pars={}
            #pars['content']+=line+"\n"
            if  log==True:
                logger.debug("+"*40)
                logger.debug('@ {}'.format(tag))
                logger.debug("-"*40)
        else:
            
            if  any(section in tag.lower() for section in cfg['inp.comment']['id'].split(',')):
                pass
                #pars['content']+=line+"\n"
                #inp_dct[tag]=pars
            else:
                #pars['content']+=line+"\n"               
                #   identify the "key"
                key=line.split()[0]
                #   remove leading/trailing space to get the "value" portion
                expr=line.replace(key,'',1).strip()
                if  log==True:
                    logger.debug('{:20}'.format(key)+" : "+str(expr))
                
                """                    
                try:                #   likely mutiple-elements are provided, 
                                    #   but be careful of eval() usage here
                                    #   e.g.:"tuple (1)" will be a valid statement
                    #pars[key]=eval(value)
                    #pars[key]=ast.literal_eval(value)
                    pars[key]=aeval(value)
                except SyntaxError: #   pack the value content into a list
                    values=value.split()
                    #pars[key]=[eval(value0) for value0 in value]
                    #pars[key]=[ast.literal_eval(value0) for value0 in value]
                    pars[key]=[aeval(value0) for value0 in values]
                """
                value=aeval(expr)
                if  len(aeval.error)>0 and value is None:
                    exprs=expr.split()
                    value=[aeval(expr) for expr in exprs]
                
                pars[key]=pars_interp(key,value)
                inp_dct[tag]=pars

    
    if  'general' in inp_dct.keys():
        if  'outdir' in (inp_dct['general']).keys():
            outdir=inp_dct['general']['outdir']
            if  isinstance(outdir,str): 
                if  not os.path.exists(outdir):
                    os.makedirs(outdir)
                #np.save(outdir+'/inp_dct.npy',inp_dct)
                #write_inp(inp_dct,inpfile=outdir+'/p_start.inp',
                #          overwrite=True)
                                
                
    return inp_dct

def pars_interp(key,value):

    value_int=value
    
    if  key=='xypos':
        if  isinstance(value,str):
            value_int=SkyCoord(value,frame='icrs')
    
    return value_int

inp_def=read_inp(metadata_path+'input_def.inp',log=False)






