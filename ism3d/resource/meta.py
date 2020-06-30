"""
Container for internal metadata/configuration variables under the program namespace


    inp_dct:    input parameter set (using quantities)
    mod_dct:    model parameter set (using quantities)
    obj_dct:    component parameter set (dimensionless, values in internal units)
    
    
Input metadata                    inp_dct (can be hacked) (fixed)
Component metadata                mod_dct (lightweight) (dynamical(
Component Reference model            mod_dct (lightweight (dynamical)
Data                                dat_dct (heavy) (transite)
Models                            models (heavy) not nesscarilly filled with data (transite only exporting data)
    
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

import numpy as np

from asteval import Interpreter
aeval = Interpreter(use_numpy=True,err_writer=StringIO())
aeval.symtable['u']=u
aeval.symtable['SkyCoord']=SkyCoord
aeval.symtable['Angle']=Angle
aeval.symtable['Number']=Number
aeval.symtable['Quantity']=Quantity


package_path=os.path.dirname(os.path.abspath(__file__))
metadata_path=os.path.dirname(os.path.abspath(__file__))+'/resource/'

cfg=ConfigParser(interpolation=ExtendedInterpolation())
cfg.read(package_path+"/default.cfg") 


__all__ = ['read_inp']


try:
    db_global
except NameError:
    db_global={'dat_dct':{},'models':{}}

def create_header(file=None,
                  objname=None,
                  naxis=None, crval=None, crpix=None, cdelt=None):
    """
    ref: https://docs.astropy.org/en/stable/io/fits/api/headers.html
        xymodel_header=create_header(file=metadata_path+'xymodel.header')
        xymodel_header=create_header(
    """
    
                   
            
    if  file is None:
        hdr=fits.Header.fromstring("""\
SIMPLE  =                    T /Written by GMaKe     
BITPIX  =                  -32 /Floating point (32 bit)                         
NAXIS   =                    4 /                                                
NAXIS1  =                  128 /                                                
NAXIS2  =                  128 /                                                
NAXIS3  =                  238 /                                                
NAXIS4  =                    1 /                                                
EXTEND  =                    T                                                  
BSCALE  =   1.000000000000E+00 /PHYSICAL = PIXEL*BSCALE + BZERO                 
BZERO   =   0.000000000000E+00                                                  
BMAJ    =   0.0E-05                                                             
BMIN    =   0.0E-05                                                             
BPA     =   0.0E+01                                                             
BTYPE   = 'Intensity'                                                           
OBJECT  = 'TEMPLATE '                                                           
BUNIT   = 'Jy/pixel'           /Brightness (pixel) unit                         
RADESYS = 'ICRS    '                                                            
LONPOLE =   1.800000000000E+02                                                  
LATPOLE =   1.282202777778E+01                                                  
PC1_1   =   1.000000000000E+00                                                  
PC2_1   =   0.000000000000E+00                                                  
PC3_1   =   0.000000000000E+00                                                  
PC4_1   =   0.000000000000E+00                                                  
PC1_2   =   0.000000000000E+00                                                  
PC2_2   =   1.000000000000E+00                                                  
PC3_2   =   0.000000000000E+00                                                  
PC4_2   =   0.000000000000E+00                                                  
PC1_3   =   0.000000000000E+00                                                  
PC2_3   =   0.000000000000E+00                                                  
PC3_3   =   1.000000000000E+00                                                  
PC4_3   =   0.000000000000E+00                                                  
PC1_4   =   0.000000000000E+00                                                  
PC2_4   =   0.000000000000E+00                                                  
PC3_4   =   0.000000000000E+00                                                  
PC4_4   =   1.000000000000E+00                                                  
CTYPE1  = 'RA---SIN'                                                            
CRVAL1  =   0.0E+02                                                             
CDELT1  =  -1.111111111111E-05                                                  
CRPIX1  =        66.0000000000 /                                                
CUNIT1  = 'deg     '                                                            
CTYPE2  = 'DEC--SIN'                                                            
CRVAL2  =   0.0E+01                                                             
CDELT2  =   1.111111111111E-05                                                  
CRPIX2  =        66.0000000000 /                                                
CUNIT2  = 'deg     '                                                            
CTYPE3  = 'FREQ    '                                                            
CRVAL3  =   2.349542341980E+11                                                  
CDELT3  =   7.812133295105E+06                                                  
CRPIX3  =   1.000000000000E+00                                                  
CUNIT3  = 'Hz      '                                                            
CTYPE4  = 'STOKES  '                                                            
CRVAL4  =   1.000000000000E+00                                                  
CDELT4  =   1.000000000000E+00                                                  
CRPIX4  =   1.000000000000E+00                                                  
CUNIT4  = '        '                                                            
PV2_1   =   0.000000000000E+00                                                  
PV2_2   =   0.000000000000E+00                                                  
RESTFRQ =   7.573097700000E+11 /Rest Frequency (Hz)                             
SPECSYS = 'LSRK    '           /Spectral reference frame                        
VELREF  =                  257 /1 LSR, 2 HEL, 3 OBS, +256 Radio                 
COMMENT casacore non-standard usage: 4 LSD, 5 GEO, 6 SOU, 7 GAL                 
TELESCOP= 'ALMA    '                                                            
OBSERVER= 'GMAKE'                                                               
DATE-OBS= '2016-08-03T07:35:49.824000'                                          
TIMESYS = 'UTC     '                                                            
OBSRA   =   3.565393333333E+02                                                  
OBSDEC  =   1.282202777778E+01                                                  
OBSGEO-X=   2.225142180269E+06                                                  
OBSGEO-Y=  -5.440307370349E+06                                                  
OBSGEO-Z=  -2.481029851874E+06                                                  
INSTRUME= 'ALMA    '                                                            
DISTANCE=   0.000000000000E+00                                                  
DATE    = '2019-01-01T00:00:00.000000' /Date FITS file was written              
ORIGIN  = 'GMAKE'                                                               
HISTORY FROM TCLEAN STANDARD OUTPUT                                             
        """, sep='\n')
    else:
        hdr=fits.Header.fromfile(file,endcard=False,sep='\n',padding=False)
        #hdr=fits.Header.fromtextfile(file)
        
    if  naxis is not None:
        for idx, value in enumerate(naxis):
            hdr['NAXIS'+str(idx+1)]=value
    if  naxis is not None and crpix is None:
        for idx, value in enumerate(naxis):
            if  idx==0 or idx==1:
                hdr['CRPIX'+str(idx+1)]=np.floor(hdr['NAXIS'+str(idx+1)]/2)+1
            if  idx==2:
                hdr['CRPIX3']=1  
            
    if  crval is not None:
        for idx, value in enumerate(crval):
            hdr['CRVAL'+str(idx+1)]=value
            
    if  cdelt is not None:
        for idx, value in enumerate(cdelt):
            hdr['CDELT'+str(idx+1)]=value
     
    if  objname is not None:
        hdr['OBJECT']=objname
     
    return hdr



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



