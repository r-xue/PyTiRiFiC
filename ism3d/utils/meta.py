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

from .. import __resource__




__all__ = ['read_inp']

try:
    db_global
except NameError:
    db_global={'dat_dct':{},'models':{}}
    
    
def inp_config(file=None):
    """
    supposed configuration setup
    """
    cfg=ConfigParser(interpolation=ExtendedInterpolation())

    cfg.read_string("""
[inp.component]

[inp.dynamics]

    id = gravity,potential,dynamics

[inp.optimizer]

    id = optimize,fitter,optimizer

[inp.analyzer]

    id = analysis,diagnostics,analyzer

[inp.comment]

    id = comments,skip,ignore,changelog
    
[inp.general]

    id = general
""")
    return cfg
    
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
SIMPLE  =                    T /Written by ism3d     
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
TELESCOP= 'ism3d   '                                                            
OBSERVER= 'ism3d   '                                                            
DATE-OBS= '2020-01-01T00:00:00.000000'                                          
TIMESYS = 'UTC     '                                                            
OBSRA   =   3.565393333333E+02                                                  
OBSDEC  =   1.282202777778E+01                                                  
OBSGEO-X=   2.225142180269E+06                                                  
OBSGEO-Y=  -5.440307370349E+06                                                  
OBSGEO-Z=  -2.481029851874E+06                                                  
INSTRUME= 'ism3d   '                                                            
DISTANCE=   0.000000000000E+00                                                  
DATE    = '2019-01-01T00:00:00.000000' /Date FITS file was written              
ORIGIN  = 'ism3d.create_header'                                                               
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





#inp_def=read_inp(__resource__+'input_def.inp',log=False)



