#from .discretize import sample_prep, uv_sample, pickplane
from casatools import simulator
#from .model import makepb, get_image_size
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from casatasks import importfits
from casatools import calibrater
from casatools import msmetadata
from casatools import table
import numexpr as ne
from .proc import rmColumns
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
import os
import logging
from astropy import constants as const
import numpy as np


from ..utils.misc import human_unit, human_to_string, get_obj_size
from ..utils.utils import paste_array

import astropy.units as u
from astropy.coordinates import Angle
from ast import literal_eval
from astropy.io import fits
logger = logging.getLogger(__name__)


"""
ref: about taql:
    https://casacore.github.io/casacore-notes/199.html
ref:
     C-contiguous order (last index varies the fastest
     FORTRAN-contiguous order in memory (first index varies the fastest)
"""

# for instance constructed from classes, we use shorter names: tb, msmd, cb, etc...
# see at the end:
#    https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage


def read_ms(vis='',
            polaverage=True, flagdata=False, saveflag=True,
            includedata=True, usedouble=False,
            dataset=None,keyrule='basename'):
    """
    Note:
        the different output sequence
        casacore.table.getcol():     nrecord x nchan x ncorr
        casatools.table.getcol():    ncorr x nchan x nrecord

    flagdata: default=False
        set flagged data value to np.nan, which may lead to troubles of calculating chisq2
    saveflag: default=True
        save flagging (bool) column, which is need to figure out channel-wise bad data

    uvw in units of meters
    
    includedata=False
        only read the MS "framework" from MS, not the actual dataset

    dataset:    a dataset container (list or dictionary) for the readout data
                if it's provieded, not return from the function.
                if it's not provide, the readout data will be return as a dictionary. 
                 
    keyrule:   'number':      data_0, data_1, data_3
               'basename':    basename1, basename2, basename3
               'abspath':     absolute name
               
    note: we on purpose preserve the data shape to ensure write_ms will work properly
    """
    
    vis_dict={'relpath':os.path.relpath(vis),
              'abspath':os.path.abspath(vis),
              'basename':os.path.basename(vis),
              'type':'uv'}
    
    if usedouble == False:
        rtype = np.float32
        ctype = np.complex64
    else:
        rtype = np.float64
        ctype = np.complex128

    # set order='F' for the quick access of u/v/w seperately
    # assuming xx/yy, we decide to save data as stokes=I to reduce the data size by x2
    # then the data/weight in numpy as nrecord x nchan / nrecord

    textout = '\nREADing: '+vis
    logger.info(textout)
    logger.info('')
    logger.info('-'*90)

    t = table()
    t.open(vis)

    vis_dict['uvw'] = (t.getcol('UVW')).T.astype(rtype, order='F')
    vis_dict['type'] = 'vis'
    # spectrum_weight is not considered here
    vis_dict['weight'] = (t.getcol('WEIGHT')).T.astype(rtype, order='F')
    if includedata == True:
        vis_dict['data'] = (t.getcol('DATA')).T.astype(ctype, order='F')

    vis_dict['flag'] = (t.getcol('FLAG')).T
    if flagdata == True:
        vis_dict['data'][vis_dict['flag'] == True] = np.nan
    t.close()

    if polaverage == True:

        if 'data' in vis_dict:
            vis_dict['data'] = np.mean(vis_dict['data'], axis=-1)
        if 'weight' in vis_dict:
            vis_dict['weight'] = np.sum(vis_dict['weight'] , axis=-1)
        if 'flag' in vis_dict:
            vis_dict['flag'] = np.any(vis_dict['flag'], axis=-1)

    # flag all data with zero weight
    vis_dict['flag'][vis_dict['weight'] == 0, :] = 1
    # set weight=0 record with weight=1 for speeding log(wt)
    vis_dict['weight'][vis_dict['weight'] == 0] = 1

    #   use the "last" and "only" spw in the SPECTRAL_WINDOW table
    #   We don't handle mutipl-spw MS here.
    ts = table()
    ts.open(vis+'/SPECTRAL_WINDOW')
    vis_dict['chanfreq'] = ts.getcol('CHAN_FREQ')[:, -1]*u.Hz
    vis_dict['chanwidth'] = ts.getcol('CHAN_WIDTH')[:, -1]*u.Hz
    ts.close()

    #   use the "last" and "only" field phase center in the FIELD table

    mymsmd = msmetadata()
    mymsmd.open(vis)
    phasecenter = mymsmd.phasecenter(0)
    telescope = mymsmd.observatorynames()[0]
    mymsmd.close()

    
    phasecenter = SkyCoord(phasecenter['m0']['value'], 
                           phasecenter['m1']['value'], unit="rad")
    # phasecenter.isscalar
    vis_dict['phasecenter'] = phasecenter
    vis_dict['telescope'] = telescope

    #   only for unflagged data we calculate the below values
    #   we precacluate the value to avoid redundant calcualtion during likelihood calculate
    #   use ne.evaluate(sum(**)) could lead to wrong results due to the weight dtype=float32
    uvflag =vis_dict['flag']
    uvweight = vis_dict['weight']
    vis_dict['ndata'] = np.sum(~uvflag)
    vis_dict['sumwt'] = np.sum(~uvflag*uvweight[:, np.newaxis])
    vis_dict['sumlogwt'] = np.sum((~uvflag)*np.log(uvweight[:, np.newaxis]))

    if includedata == True:
        uvdata = vis_dict['data']
        vis_dict['chanchi2'] = np.sum(
            (uvdata.real**2+uvdata.imag**2) * (~uvflag*uvweight[:, np.newaxis]), axis=0)

    vars = ['data', 'uvw', 'weight', 'flag']
    for var in vars:
        if saveflag == False and var == 'flag':
            del vis_dict['flag']
        if var not in vis_dict.keys():
            continue
        size = human_unit(get_obj_size(vis_dict[var])*u.byte)
        size = human_to_string(
            size, format_string='{0.value:3.0f} {0.unit:shortname}')
        textout = '{:15} {:15} {:20} {:20}'.format(
            var, str(vis_dict[var].dtype), str(vis_dict[var].shape),
            size)
        if var == 'weight':
            pickweight = np.broadcast_to(
                vis_dict['weight'][:, np.newaxis], vis_dict['flag'].shape)
            pickweight = pickweight[np.where(
                vis_dict['flag'] == False)]
            pt_select = [0, 16, 50, 84, 100]
            pt_level = np.percentile(pickweight, pt_select)
            for pt_ind in range(len(pt_select)):
                textout += '\n{:15} {:15} {:<20.0%} {:<20f}'.format(
                    '', 'ptile:', pt_select[pt_ind]*0.01, pt_level[pt_ind])
        logger.info(textout)

    vars = ['chanfreq', 'chanwidth']
    for ind in range(2):
        tag = vars[ind]
        if tag not in vis_dict.keys():
            continue
        textout = '{:15} {:10} {:10.4f} {:10.4f}'.format(
            tag,
            str(vis_dict[tag].shape),
            human_unit(np.min(vis_dict[tag])),
            human_unit(np.max(vis_dict[tag])))
        logger.info(textout)

    vars = ['chanchi2']
    for ind in range(1):
        tag = vars[ind]
        if tag not in vis_dict.keys():
            continue
        textout = '{:15} {:10} {:10.4f} {:10.4f}'.format(
            tag,
            str(vis_dict[tag].shape),
            np.min(vis_dict[tag]),
            np.max(vis_dict[tag]))
        logger.info(textout)



    for key in ['ndata','sumwt','sumlogwt','telescope']:
        logger.info('{:15} {:10}'.format(key, vis_dict[key]))
    logger.info('{:15} {:10}'.format('phasecenter', vis_dict['phasecenter'].to_string(style='hmsdms')))
    
    count_flag = np.count_nonzero(vis_dict['flag'])
    count_record = np.size(vis_dict['flag'])
    logger.info('-'*90)
    logger.info('flagging fraction: {0:.0%}'.format(
        count_flag*1./count_record))
    logger.info('-'*90)


    if dataset is None:
        return vis_dict
    else:
        if  isinstance(dataset,dict):
            idx = 1
            while 'data_'+str(idx) in dataset: idx+=1
            key='data_'+str(idx)
            if  keyrule in vis_dict:
                key=vis_dict[keyrule].replace('/','|')
            if  key in dataset:
                logger.warning("you are overwriting in the dataset: {}".format(key))
            dataset[key]=vis_dict
            
        if  isinstance(dataset,list):
            dataset.append(vis_dict)        
        
        return


def write_ms(vis, value,
             datacolumn='corrected', inputvis=None):
    """
    attach new visibility data/model values into an MS

    if the specified datacolumn doesn't exist, it will be created on-the-fly.

    note:
        the input data shape is nrecord x nchan x ncorr following the rule in casacore.table.getcol(),
        which is reversed from casa6.casatools.table.getcol() (ncorr x nchan x nrecord)
        alternatively, ncrecord x nchan (stokes-I) is also fine and will be broadcasted to all correlations 
        (assumed to be RR, LL, XX, or YY) 

    """

    if inputvis is not None:
        if inputvis == vis:
            logger.info("vis and inputvis must be different!")
            return
        os.system("rm -rf "+vis)
        os.system('cp -rf '+inputvis+' '+vis)

    addcorr = addmodel = False
    if datacolumn == 'data':
        colname = 'DATA'
    if datacolumn == 'corrected':
        colname = 'CORRECTED_DATA'
        addcorr = True
    if datacolumn == 'model':
        colname = 'MODEL_DATA'
        addmodel = True

    tb = table()

    if datacolumn == 'corrected' or datacolumn == 'model':
        tb.open(vis)
        colnames = tb.colnames()
        tb.close()
        if colnames.count(colname) == 0:
            cb = calibrater()
            cb.open(vis, addcorr=addcorr, addmodel=addmodel)
            cb.close()

    tb.open(vis, nomodify=False)

    colshape = tb.getcolshapestring(colname)
    colshape = tuple(literal_eval(colshape[0]))+(len(colshape),)
    if value.ndim < len(colshape):
        value_in = (value.T)[np.newaxis, :, :]
    else:
        value_in = (value.T)

    tb.putcol(colname, np.broadcast_to(value_in, colshape))
    tb.close()

    return


if __name__ == "__main__":

    pass
