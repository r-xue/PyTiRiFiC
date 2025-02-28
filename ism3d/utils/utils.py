"""
General-purpose utility Functions used by other modules
"""

#import inspect

from numpy.random import Generator, SFC64, PCG64
from astropy.io import fits
from radio_beam import Beams
import emcee
from galario.single import threads as galario_threads
import datetime
import os
import pyfftw
from spectral_cube import SpectralCube
from scipy import interpolate
import scipy.integrate
from unittest.mock import patch
import gc
import sys
from asteval import Interpreter
from io import StringIO
from numbers import Number
from astropy.units import Quantity
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
import astropy.units as u
from copy import deepcopy
import logging
import socket
import multiprocessing

import numpy as np

import pprint as pp
import re

#from .meta import cfg
#from .meta import inp_def
from scipy._build_utils.compiler_helper import try_add_flag

logger = logging.getLogger(__name__)
# get a logger named after a function name
# logger=logging.getLogger(inspect.stack()[0][3])


#   Choice of the FFT implementation
#   mkl could cut the evluate time by 40% in single-thread tests
#       mkl 8-thread    1.27s
#       mkl 1-thread    1.40s
#       pyfftw 8-thread 1.50s
#       pyfftw 1-thread 2.00s







"""
import ast, operator

binOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod
}

def arithmeticEval (s):
    node = ast.parse(s, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise Exception('Unsupported type {}'.format(node))

    return _eval(node.body)
"""








def repr_parameter(v):
    """
    Similiar to the built-in repr(), but can handle Quantity / SkyCoord
    used for writing input files
    """
    if isinstance(v, Quantity):
        # replace line break from repr(numpy.array)
        str_value = repr(v.value).replace('\n', '')
        # remove double/triple.. spacing
        str_value = ' '.join(str_value.split())
        # remove leading white space
        str_value = str_value.replace(' , ', ', ')
        str_value = str_value.replace('[ ', '[')  # remove leading white space
        str_unit = "u.Unit('{0.unit}')".format(v)
        str_repr = str_value+" * "+str_unit
    elif isinstance(v, SkyCoord):
        str_coord = repr(v.to_string(style='hmsdms'))
        str_repr = "SkyCoord(" + str_coord + ",frame='icrs')"
    elif isinstance(v, list):
        str_repr = []
        for v0 in v:
            str_repr.append(repr_parameter(v0))
        str_repr = '[ '+' , '.join(str_repr)+' ]'
    elif isinstance(v, tuple):
        str_repr = []
        for v0 in v:
            str_repr.append(repr_parameter(v0))
        str_repr = '( '+' , '.join(str_repr)+' )'
    else:
        str_repr = repr(v)

    return str_repr


def pprint(*args, **kwargs):
    """
    A modified pprint.pprint without sorting dictionary keys

    this may not be neccsary with Py38+ as optional keyword sort_dicts become available
        https://docs.python.org/3/library/pprint.html
    """
    with patch('builtins.sorted', new=lambda l, **_: l):
        pp.pprint(*args, **kwargs)



def read_range(center=0, delta=0, mode='a'):
    """
        modifiy the parameter exploring bounrdary according to the info from opt section
        a:    absolute


    """
    if mode == 'a':
        return delta
    if mode == 'o':
        return center+delta
    if mode == 'r':
        return center*delta


def moments(imagename, outname='test',
            maskname='', linechan=None):

    cube = SpectralCube.read(imagename, mode='readonly')

    if linechan is not None:
        subcube = cube.spectral_slab(linechan[0], linechan[1])
    else:
        subcube = cube

    moment_0 = subcube.moment(order=0)
    moment_1 = subcube.moment(order=1)
    moment_2 = subcube.moment(order=2)

    moment_0.write(outname+'_mom0.fits', overwrite=True)
    moment_1.write(outname+'_mom1.fits', overwrite=True)
    moment_2.write(outname+'_mom2.fits', overwrite=True)


def imcontsub(imagename, linefile='', contfile='',
              fitorder=0,   # not implemented yet
              linechan=None, contchan=None):
    """
    linechan / contchan: tuple with [fmin,fmax] in each element 
    """
    cube = SpectralCube.read(imagename, mode='readonly')
    spectral_axis = cube.spectral_axis
    if linechan is not None:
        if isinstance(linechan, tuple):
            linechan = [linechan]
        bad_chans = [(spectral_axis > linechan0[0]) & (
            spectral_axis < linechan0[1]) for linechan0 in linechan]
        bad_chans = np.logical_or.reduce(bad_chans)
        good_chans = ~bad_chans
    if contchan is not None:
        if isinstance(contchan, tuple):
            contchan = [contchan]
        good_chans = [(spectral_axis > contchan0[0]) & (
            spectral_axis < contchan0[1]) for contchan0 in contchan]
        good_chans = np.logical_or.reduce(good_chans)

    masked_cube = cube.with_mask(good_chans[:, np.newaxis, np.newaxis])
    cube_mean = masked_cube.mean(axis=0)
    cube_imcontsub = cube-cube_mean

    cube_imcontsub.write(linefile, overwrite=True)
    cube_mean.write(contfile, overwrite=True)


def gal_flat(im, ang, inc, cen=None, interp=True,
             align_major=False,
             fill_value=None):
    """
    translated from IDL/gal_flat.pro
    im in (nz,ny,nx)
    cen is (xc,yc)
    """
    angr = np.deg2rad(ang+90.)
    tanang = np.tan(angr)
    cosang = np.cos(angr)
    cosinc = np.cos(np.deg2rad(inc))

    dims = im.shape

    if cen is None:
        xcen = dims[-1]/2.0
        ycen = dims[-2]/2.0
    else:
        xcen = cen[0]
        ycen = cen[1]

    b = ycen-xcen*tanang

    gridx = xcen + np.array([[-1, 1], [-1, 1]]) * dims[-1]/6.0
    gridy = ycen + np.array([[-1, -1], [1, 1]]) * dims[-2]/6.0

    yprime = gridx*tanang + b
    r0 = (gridy-yprime)*np.cos(angr)
    delr = r0*(1.0-cosinc)
    dely = -delr*np.cos(angr)
    delx = delr*np.sin(angr)
    distx = gridx + delx
    disty = gridy + dely

    x0 = dims[1]/3.0
    y0 = dims[0]/3.0
    dx = x0
    dy = y0

    t = transform.PolynomialTransform()
    source = np.array((gridx.flatten(), gridy.flatten()))
    destination = np.array((distx.flatten(), disty.flatten()))
    t.estimate(source.T, destination.T, 1)

    if fill_value is None:
        cval = float('nan')
    else:
        cval = fill_value
    im_wraped = transform.warp(im, t, order=1, mode='constant', cval=cval)

    if align_major == True:
        # print('-->',90+ang)
        # (0,0)  sckit-image is the left-top corner, so the presentation is actually flipped along the x-axis
        # counter-clockwise in sckit-image is eqaveulent with clockwise in FITS
        im_wraped = transform.rotate(im_wraped, 90+ang-180, center=(xcen, ycen),
                                     resize=False,
                                     order=1, cval=cval)

    return im_wraped


def sort_on_runtime(p):
    p = np.atleast_2d(p)
    idx = np.argsort(p[:, 0])[::-1]
    return p[idx], idx


def gmake_listpars(objs, showcontent=True):
    """
    print out the parameter dict
    """
    for tag in objs.keys():
        logger.info("+"*40)
        logger.info('@'+tag)
        logger.info("-"*40)
        for key in objs[tag].keys():
            if key == 'content':
                print(objs[tag][key])
            else:
                print(key, " : ", objs[tag][key])





def paste_slice(tup):
    """
    make slice for the overlapping region
    """
    pos, w, max_w = tup

    #wall_min = max(pos, 0)
    #wall_max = min(pos+w, max_w)
    #block_min = -min(pos, 0)
    #block_max = max_w-max(pos+w, max_w)
    #block_max = block_max if block_max != 0 else None

    wall_min = +pos
    wall_max = +pos+w
    wall_min = min(max(wall_min, 0), max_w)
    wall_max = min(max(wall_max, 0), max_w)

    block_min = -pos
    block_max = -pos+max_w
    block_min = min(max(block_min, 0), w)
    block_max = min(max(block_max, 0), w)

    return slice(wall_min, wall_max), slice(block_min, block_max)


def paste_array(wall, block, loc, method='replace'):
    """
    past a small array into a larger array with shifting
    works for high dimension or off-edge cases
    wall/block requires in the same dimension number 
    loc: the index of left-bottom pixel of block in wall. 
    """
    loc_zip = zip(loc, block.shape, wall.shape)
    # print(loc,block.shape,wall.shape)
    wall_slices, block_slices = zip(*map(paste_slice, loc_zip))
    #print(wall_slices, block_slices)
    if block[block_slices].size != 0:
        if method == 'replace':
            wall[wall_slices] = block[block_slices].copy()
        if method == 'add':
            wall[wall_slices] += block[block_slices]
    else:
        logger.info('no overlapping region')

    return wall


def make_slice(expr):
    """
    parsing the slicing syntax in STRING
    """
    if len(expr.split(':')) > 1:
        s = slice(*map(lambda x: int(x.strip())
                       if x.strip() else None, expr.split(':')))
    else:
        s = int(expr.strip())
    return s


def read_par(inp_dct, par_name, to_value=False):
    """
    read parameter quantity / values (in default units) from a parameter dictionary
    this function can handle literal slicing and attribute syntax
        e.g.:   par_str[ind_str]@section_name
                par_str.attrubute@section_name
    """

    po_key = par_name.split("@")
    slicing_expr = re.findall("\[(.*?)\]", po_key[0])

    if len(slicing_expr) == 0:
        p_key = po_key[0]
        o_key = po_key[1]
        par_name = p_key.split('.')
        if len(par_name) == 2:
            par_value = getattr(inp_dct[o_key][par_name[0]], par_name[1])
            par_name = par_name[0]
        else:
            par_value = inp_dct[o_key][par_name[0]]
            par_name = par_name[0]
    else:
        p_key = (po_key[0].split("["))[0]
        o_key = po_key[1]
        slicing_expr = slicing_expr[0]
        par_value = inp_dct[o_key][p_key][make_slice(slicing_expr)]
        par_name = p_key

    if to_value == True:
        if isinstance(par_value, u.Quantity):
            units = inp_def['pars_def'][par_name][-1]
            if isinstance(units, list):
                unit = units[make_slice(slicing_expr)]
            else:
                unit = units
            par_value = par_value.to_value(unit=unit)
            par_unit = unit
            return par_value, u.Unit(par_unit)
        else:
            return par_value, u.Unit("")
    else:
        return par_value


def write_par(inp_dct, par_name, par_value, verbose=False):
    """
    write parameter values
        key:    par_str[ind_str]@obj_str

    example:
        test=read_par(inp_dct,'xypos[0]@co76')
        print(test)
        test=read_par(inp_dct,'vrot@co76')
        print(test)
        test=read_par(inp_dct,'vrot[0:2]@co76')
        print(test)    
        write_par(inp_dct,'vrot[0:2]@co76',[2,5])
        test=read_par(inp_dct,'vrot@co76')
        print(test)
    """
    # print(par_name)

    if verbose == True:
        print('before: {} : {}'.format(par_name, read_par(inp_dct, par_name)))

    po_key = par_name.split("@")
    i_key = re.findall("\[(.*?)\]", po_key[0])

    if len(i_key) == 0:
        p_key = po_key[0]
        o_key = po_key[1]
        par_name = p_key.split('.')

        if len(par_name) == 2:
            if par_name[1] == 'ra':
                cc = inp_dct[o_key][par_name[0]]
                cc.data.lon[()] = par_value
                cc.cache.clear()
            elif par_name[1] == 'dec':
                cc = inp_dct[o_key][par_name[0]]
                cc.data.lat[()] = par_value
                cc.cache.clear()
            else:
                setattr(inp_dct[o_key][par_name[0]], par_name[1], par_value)
            par_name = par_name[0]
        else:
            inp_dct[o_key][par_name[0]] = par_value
            par_name = par_name[0]

    else:
        p_key = (po_key[0].split("["))[0]
        o_key = po_key[1]
        i_key = i_key[0]
        if isinstance(inp_dct[o_key][p_key][make_slice(i_key)], list) and \
                not isinstance(par_value, list):
            par_value = [par_value] * \
                len(inp_dct[o_key][p_key][make_slice(i_key)])
        if isinstance(inp_dct[o_key][p_key], tuple):
            tmp = list(inp_dct[o_key][p_key])
            tmp[make_slice(i_key)] = par_value
            inp_dct[o_key][p_key] = tuple(tmp)
        else:
            inp_dct[o_key][p_key][make_slice(i_key)] = par_value

    if verbose == True:
        print('after: {} : {}'.format(par_name, read_par(inp_dct, par_name)))


def inp_validate(inp_dct, verbose=False):
    """
    validate the input parameters, will do the follows step by step
        1. check if the variable type against its type definition
        2. for quanity, check the physical_type use .is_eqivalent(default_unit)
    """

    inp_out = deepcopy(inp_dct)
    pars_def = inp_def['pars_def']

    for sec in inp_out:
        if verbose == True:
            print('sec:'+sec)
        for key in inp_out[sec]:
            if key in pars_def:
                value = inp_out[sec][key]
                default_value = pars_def[key][0]
                default_format = pars_def[key][1]
                default_type = pars_def[key][2]
                if verbose == True:
                    print(key, value, pars_def[key], '--->\n\n')
                valid = True
                if isinstance(value, list):
                    for ind in range(len(value)):
                        type0 = default_type
                        if isinstance(default_type, list):
                            type0 = default_type[ind]
                        if not isinstance(inp_out[sec][key][ind], type0):
                            valid = False
                else:
                    if not isinstance(inp_out[sec][key], default_type):
                        valid = False
                if valid == False:
                    str_out = 'The input is supposed to be {0}, got {1} instead...'.format(
                        default_type, value)
                    raise ValueError(str_out)

    return inp_out


def obj_defunit(obj):
    """
    convert quatity to values in default internal units
    """

    obj_out = deepcopy(obj)
    pars_def = inp_def['pars_def']
    for key in obj_out:
        if key in pars_def:
            if isinstance(pars_def[key][-1], list):
                for ind in range(len(pars_def[key][-1])):
                    if isinstance(obj_out[key][ind], u.Quantity):
                        obj_out[key][ind] = obj_out[key][ind].to_value(
                            pars_def[key][-1][ind])
            else:
                if isinstance(obj_out[key], u.Quantity):
                    obj_out[key] = obj_out[key].to_value(pars_def[key][-1])
            if isinstance(obj_out[key], SkyCoord):
                obj_out[key] = [obj_out[key].ra.to_value(
                    u.deg), obj_out[key].dec.to_value(u.deg)]

    return obj_out


def gmake_pformat(fit_dct):
    """
    fill..
    p_format            : format for values
    p_format_keys       : format for p_name
    """
    p_format = []
    p_format_keys = []
    p_format_prec = []

    logger.debug("+"*100)
    #print("outdir:               ",fit_dct['optimize']['outdir'])
    logger.debug("optimizer: "+fit_dct['method'])
    logger.debug("optimizing parameters:")
    logger.debug("-"*100)
    logger.debug(
        "index    name    unit    start    lo_limit    up_limit    scale")

    pars_def = inp_def['pars_def']
    opt_def = inp_def['optimize']

    maxlen = len(max(fit_dct['p_name'], key=len))
    for ind in range(len(fit_dct['p_name'])):

        p_key = fit_dct['p_name'][ind]
        p_start = fit_dct['p_start'][ind]
        p_lo = fit_dct['p_lo'][ind]
        p_up = fit_dct['p_up'][ind]
        p_up = fit_dct['p_up'][ind]
        p_scale = fit_dct['p_scale'][ind]

        smin = len(p_key)
        for keyword in pars_def.keys():
            if keyword+'@' in p_key or keyword+'[' in p_key or keyword+'.' in p_key:
                # print(keyword,def_dct_obj[keyword])
                p_format0_prec = pars_def[keyword][1]
                p_format0_keys = ''+str(max(smin, 5))

        #  same widths for all parameters in one trial
        textout = ' {:{align}{width}} '.format(ind, align='<', width=2)
        textout += ' {:{align}{width}} '.format(p_key, align='<', width=maxlen)
        textout += ' {:{align}{width}{prec}} '.format(
            p_start, align='^', width=13, prec=p_format0_prec)
        textout += ' ( {:{align}{width}{prec}}, '.format(p_lo,
                                                         align='^', width=13, prec=p_format0_prec)
        textout += ' {:{align}{width}{prec}} )'.format(
            p_up, align='^', width=13, prec=p_format0_prec)
        textout += ' {:{align}{width}{prec}} '.format(
            p_scale, align='^', width=13, prec=p_format0_prec)
        logger.debug(textout)

        #   used for emcee table output
        p_format0 = '<'+str(max(smin, 5))+p_format0_prec
        p_format0_keys = '<'+str(max(smin, 5))
        p_format += [p_format0]
        p_format_keys += [p_format0_keys]
        p_format_prec += [p_format0_prec]

    logger.debug("+"*100)

    fit_dct['p_format'] = deepcopy(p_format)
    fit_dct['p_format_keys'] = deepcopy(p_format_keys)
    fit_dct['p_format_prec'] = deepcopy(p_format_prec)





def get_dirsize(dir):
    """
    get the size of a file or directory
    """
    dirsize = sum([os.path.getsize(fp) for fp in (os.path.join(dirpath, f) for dirpath,
                                                  dirnames, filenames in os.walk(dir) for f in filenames) if not os.path.islink(fp)])

    return dirsize


def h5ls_print(name, obj):
    print(name, dict(obj.attrs))


def h5ls(filename, logfile=None):

    if logfile is None:
        with h5py.File(filename, 'r') as hf:
            hf.visititems(h5ls_print)
    else:
        with open(logfile, 'w') as f:
            with redirect_stdout(f):
                with h5py.File(filename, 'r') as hf:
                    hf.visititems(h5ls_print)

    # objs=gmake_read_inp('examples/bx610/bx610xy.inp',=False)

    # print("\n"*2)
    # print(objs.keys())
    # gmake_listpars(objs)
    # objs=gmake_fillpars(objs)
    # print("\n"*10)
    # gmake_listpars(objs)

    # data=np.zeros((100,100,200))
    # model=np.ones((10,10,90))
    # offset=[20,20,100]
    # data=gmake_insertmodel(data,model,offset=offset)
    # fits.writeto('test.fits',data.T,overwrite=True)


def set_threads(num=None):
    """
    some underline alrgoithm library can use OMP
    turn on OMP is beneficial for iteration optimizwer but not for parallele optimizer
    this function can turn on / turn off OMP in modelling alrothjm

    ref:
        looks like os.environ will only work before import packages
        after the packages are imported, changing os.environ can not dynamically
        switching nthreads
    https://software.intel.com/en-us/mkl-linux-developer-guide-mkl-domain-num-threads
    http://www.diracprogram.org/doc/release-17/installation/mkl.html
    https://software.intel.com/en-us/blogs/2018/10/18/mkl-service-package-controlling-mkl-behavior-through-python-interfaces

    """
    if num is None:
        num = multiprocessing.cpu_count()

    #os.environ["OMP_NUM_THREADS"] = str(num)
    #os.environ["MKL_NUM_THREADS"] = str(num)
    # os.environ['MKL_DOMAIN_NUM_THREADS']="MKL_DOMAIN_FFT="+str(num)
    # os.environ["NUMEXPR_NUM_THREADS"] = str(num) # OMP_NUM_THREADS will override NUMEXPR_NUM_THREADS

    logger.info('set modeling threading: {0}'.format(num))
    galario_threads(num)

    mkl.domain_set_num_threads(num, domain='fft')
    mkl.set_num_threads(num)
    #mkl.domain_set_num_threads(num, domain='all')
    # default=True; set to False will give worse performance for small array when threading turned on
    mkl.set_dynamic(True)
    pyfftw.config.NUM_THREADS = num

    return


def backup(filename, move=True):
    """
    backup file / dirwectiory to be overwrite
    """
    if os.path.exists(filename):
        mt = os.path.getmtime(filename)
        newname = filename +\
            datetime.datetime.fromtimestamp(mt).strftime("-%Y-%m%d-%H%M%S")
        if move == True:
            os.system('mv '+filename+' '+newname)
        else:
            os.system('cp -rf '+filename+' '+newname)


def get_autocoor_time(h5name):

    reader = emcee.backends.HDFBackend(h5name, read_only=True)
    tau = reader.get_autocorr_time(quiet=True)

    return tau


def rotate_xy(x, y, angle, xo=0, yo=0):
    """
    rotate points in a 2D coordinate system
    angle:    rotate points by angle in CCW
    ref:    rotate_xy.pro rot_3d.pro
    performance consideration:
        https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302
        https://stackoverflow.com/questions/33004551/why-is-b-numpy-dota-x-so-much-slower-looping-through-doing-bi-numpy
        https://en.wikipedia.org/wiki/Rotation_matrix
    """
    cs = np.cos(angle)
    sn = np.sin(angle)

    xd = x-xo
    yd = y-yo

    X2 = xd*cs - yd*sn + xo
    Y2 = xd*sn + yd*cs + yo

    return xd*cs-yd*sn+xo, xd*sn+yd*cs+yo


def one_beam(fitsname):

    try:
        header = fits.getheader(fitsname)
        one_beam = Beam.from_fits_header(header)
    except:
        table_beam = fits.open(fitsname)[1]
        beams = Beams.from_fits_bintable(table_beam)
        one_beam = beams.largest_beam()

    return one_beam


def sample_grid(spacing, xrange=[-100, 100], yrange=[-100, 100], center=None,
                ratio=1, angle=0):
    """
    this is loosely based on my sample_grid.pro in IDL with improvement on defining x-/y-range
    angle in rad 
    ratio=major/minor

    """

    if center is None:
        center = [(xrange[0]+xrange[1])/2, (yrange[0]+yrange[1])/2]

    # calculate x_lim/y_lim in a homoegnoused coordinates
    xx, yy = np.meshgrid(xrange, yrange)
    xx_tr, yy_tr = rotate_xy(xx, yy, -angle, xo=center[0], yo=center[1])
    xx_tr = (xx_tr-center[0])*ratio+center[0]

    xrange_tr = [np.min(xx_tr)-spacing, np.max(xx_tr)+spacing]
    yrange_tr = [(np.min(yy_tr)-center[1])/np.sin(np.deg2rad(60))+center[1]-spacing,
                 (np.max(yy_tr)-center[1])/np.sin(np.deg2rad(60))+center[1]+spacing]

    x_tr = np.arange(xrange_tr[0], xrange_tr[1], spacing)
    y_tr = np.arange(yrange_tr[0], yrange_tr[1], spacing)
    x_idx = np.argmin(np.abs(x_tr-center[0]))
    y_idx = np.argmin(np.abs(y_tr-center[1]))
    x_tr -= x_tr[x_idx]-center[0]
    y_tr -= y_tr[y_idx]-center[1]

    xx_tr, yy_tr = np.meshgrid(x_tr, y_tr)

    xx_tr = xx_tr+0.5*np.mod(np.abs(yy_tr-center[0]), 2*spacing)
    yy_tr = (yy_tr-center[1])*np.sin(np.deg2rad(60))+center[1]

    xx_tr = (xx_tr-center[0])/ratio+center[0]

    xx_grid, yy_grid = rotate_xy(
        xx_tr, yy_tr, angle, xo=center[0], yo=center[1])
    idx = np.where(np.logical_and(np.logical_and(xx_grid > xrange[0], xx_grid < xrange[1]),
                                  np.logical_and(yy_grid > yrange[0], yy_grid < yrange[1])))
    xx_grid = xx_grid[idx]
    yy_grid = yy_grid[idx]

    return xx_grid, yy_grid


def chi2red_to_lognsigma(chi2red):

    return np.log(np.sqrt(1./chi2red))


