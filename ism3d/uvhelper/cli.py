#!/usr/bin/env python

import glob,os,fileinput,sys
from pprint import pprint

from wheel.wheelfile import WheelFile 
from wheel.cli.unpack import unpack as whl_unpack
from wheel.cli.pack import pack as whl_pack

import copy
import shutil

import argparse

import logging
logger=logging.getLogger(__name__)

def casatools_repack():
    """
    Usage:

        casatools_repack casatools-6.1.0.79-cp36-cp36m-macosx_10_15_x86_64.whl cp38
        casatools_repack casatools-6.1.0.79-cp36-cp36m-macosx_10_15_x86_64.whl cp37m
        or 
        cli.py casatools-6.1.0.79-cp36-cp36m-macosx_10_15_x86_64.whl cp38
    """

    description = """

casatools_repack will modify the Py36 casatools .whl and repack it for installation under Py37/38

"""

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('whlname',type=str,
                        help=""".whl file name, e.g,:
    casatools-6.1.0.79-cp36-cp36m-macosx_10_15_x86_64.whl""")                                     

    parser.add_argument('abi',type=str,
                        help="""abi name of your platform, e.g, cp37m or cp38""")      

    args = parser.parse_args()

    whlname = args.whlname
    abi = args.abi
    pyver = args.abi.replace('m','')

    # whlname = sys.argv[1]
    # abi = sys.argv[2]
    # pyver = sys.argv[2].replace('m','')

    dest = '.'

    # Step 1:	wheel unpack .whl 
    #	https://github.com/pypa/wheel/blob/master/src/wheel/cli/unpack.py

    whl_unpack(whlname,dest=dest)
    wf = WheelFile(whlname)
    namever = wf.parsed_filename.group('namever')
    dirname = os.path.join(dest, namever)

    # Step 2:	modify the casacore library file (.so) names

    flist=glob.glob(dirname+'/casatools/__casac__/*-36m-*',recursive=True)

    for filename in flist:
        newfilename=filename.replace('-36m-','-'+abi.replace('cp','')+'-')
        print('Rename {} to {}'.format(filename, newfilename))
        shutil.move(filename, newfilename)
        
    # Step 3: rename the function keyword "async" to "isasync"

    pyfile=dirname+'/casatools/imager.py'
    print('rename the kwarg "async" in {}'.format(pyfile))
    with fileinput.FileInput(pyfile, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(', async=', ', isasync=').replace(': async', ': isasync'), end='')

    # Step 4: modify the .whl tag within .dist-info/WHEEL

    pyfile=namever+'/'+namever+'.dist-info/WHEEL'
    dict_oldname=wf.parsed_filename.groupdict()
    dict_newname=copy.deepcopy(dict_oldname)

    dict_newname['pyver']=pyver
    dict_newname['abi']=abi

    print('change "tag" in {}'.format(pyfile))
    with fileinput.FileInput(pyfile, inplace=True, backup='.bak') as file:
        oldtag = '{pyver}-{abi}-{plat}'.format(**dict_oldname)
        newtag = '{pyver}-{abi}-{plat}'.format(**dict_newname)
        for line in file:
            print(line.replace(oldtag, newtag), end='')

    # Step 5: repack: whl: wheel pack *
    #	https://github.com/pypa/wheel/blob/master/src/wheel/cli/pack.py

    whl_pack(dirname,'',None)


if  __name__ == '__main__':
    
    casatools_repack()