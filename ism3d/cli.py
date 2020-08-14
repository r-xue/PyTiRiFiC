"""

    usage:
        
        >ism3d_cli -a bx610/uvb6_ab.inp -d -l uvb6_ab.log
        >ism3d_cli --fit uv11_mc.inp --debug

    Here we include:
        workflow for CLI
        workflow for routine tasks
        
    check mkl

import ism3d
from ism3d.utils import rng_seeded 
print(ism3d.fft_use)
print(rng_seeded(None))
"""

import os
import argparse
import glob
import sys

#from ism3d import read_inp
#from ism3d import read_data
#from ism3d import __version__
#from ism3d import opt_setup
#from ism3d import opt_iterate
#from ism3d import opt_analyze


#from .plts import plt_spec1d
#from .plts import plt_mom0xy
#from .plts import plt_makeslice
#from .plts import plt_slice
#from .plts import plt_radprof
from types import SimpleNamespace

from .utils import *
from .logger import *

import astropy.units as u
import logging
logger=logging.getLogger(__name__)

from pprint import pformat

def main():
    
    """
    Parse options and launch the workflow
    """    
    
    description="""

The ISM3d CL entry point: 
    ism3d path/example.inp

    model fitting:
        ism3d -f path/example.inp
    analyze fitting results (saved in FITS tables / HDFs?) and export model/data for diagnostic plotting  
        ism3d -a path/example.inp 
    generate diagnostic plots
        ism3d -p path/example.inp 

Note:
    for more complicated / customized user cases, one should build a workflow by
    calling modules/functions directly (e.g. hz_examples.py) 
        
    """

    parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--fit',
                        dest="fit", action="store_true",
                        help="perform parameter optimization")
    parser.add_argument('-a', '--analyze',
                        dest="analyze", action="store_true",
                        help="analyze the fitting results / exporting data+model")
    parser.add_argument('-p', '--plot',
                        dest="plot", action="store_true",
                        help="generate diagnotisc plots")    
    parser.add_argument('-d', '--debug',
                        dest="debug", action="store_true",
                        help="Debug mode; prints extra statements") 
    parser.add_argument('-t', '--test',
                        dest="test", action="store_true",
                        help="test mode; run benchmarking scripts")        
    parser.add_argument('inpfile',type=str,
                        help="""A parameter input file""")
    parser.add_argument('-l','--logfile',type=str,
                        dest='logfile',action='store',default='',
                        help="path to log file")
    
    args = parser.parse_args()
    if  args.fit==False and args.analyze==False and args.plot==False:
        args.fit=True
       
    logger_config(loglevel='INFO')

    if  not os.path.isfile(args.inpfile):
        logger.info("The inpfile '"+args.inpfile+"' doesn't exist. Aborted!")
        return

    inp_dct=read_inp(args.inpfile)
    outdir=inp_dct['general']['outdir']    
    if  args.logfile=='':
        args.logfile=outdir+'/ism3d.log'  
    loglevel='DEBUG' if args.debug==True else 'INFO'

    logger_config(logfile=args.logfile,loglevel=loglevel,logfilelevel=loglevel)

    # start comments
    logger.info(" ")
    logger.info("#"*80+"\n"+"#"*80)
    logger.info("GMaKE "+__version__+" -- Start")
    check_setup()
    logger.info("#"*80+"\n"+"#"*80)
    logger.info(" ")      
    
    # show the CLI options
    logger.debug("\nism3d_cli process options:")
    for arg in vars(args):
        arg, getattr(args, arg)
        logger.debug("{:<10} :  {:}".format(arg,getattr(args,arg)) )    
    logger.debug("\nism3d_cli process paths:")
    logger.debug("{:<10} :  {:}".format('outdir',outdir) )
    logger.debug("{:<10} :  {:}\n".format('currentdir',os.getcwd()) )
    
    proc_inpfile(args)
    
    # end comments
    logger.info(" ")
    logger.info("#"*80+"\n"+"#"*80)
    logger.info("GMaKE "+__version__+" -- End")
    logger.info("#"*80+"\n"+"#"*80)
    logger.info(" ")

    return

def proc_inpfile(args=None):
    
    if  args is None:
        args.inpfile='example.inp'
        args.fit=False
        args.analyze=True
        args.plot=False
        
    inp_dct=read_inp(args.inpfile)
    
    if  args.fit==True:
        
        dat_dct=read_data(inp_dct)
        fit_dct,models=opt_setup(inp_dct,dat_dct)
        opt_iterate(fit_dct,inp_dct,dat_dct,models,resume=False)
        
    if  args.analyze==True:
        
        opt_analyze(args.inpfile)
        
        """
        casa_script_dir=os.path.dirname(os.path.abspath(__file__))+'/casa/'
        ms2im=casa_script_dir+'/ms2im_script.py'
        loglevel='DEBUG' if args.debug==True else 'INFO'
        casa_proc.logger_config(logfile=args.logfile,loglevel=loglevel,logfilelevel=loglevel)         
        casa_proc.casa_init(reset=True)
        
        ms_names=inp_dct['general']['outdir']+'/model_1/data*.ms'
        logger.debug("\nlooking up ms: "+ms_names+'\n')
        mslist=glob.glob(ms_names)        
        logger.debug(pformat(mslist))
        
        print(ms2im)
        for vis in mslist:
            logger.debug(" ")
            logger.debug('imaging: '+str(vis))
            casa_proc.casa_task('ms2im',
                        vis=vis.replace('data_','model_'),
                        imagename=vis.replace('.ms','').replace('data_','cmodel_'),
                        cell=0.04,imsize=64,
                        datacolumn='data',preload=ms2im)
            casa_proc.casa_task('ms2im',
                        vis=vis,
                        imagename=vis.replace('.ms','').replace('data_','data_'),
                        cell=0.04,imsize=64,
                        datacolumn='data',preload=ms2im)         

        ms_names=inp_dct['general']['outdir']+'/p_*/*.ms.contsub'
        logger.debug("\nlooking up ms: "+ms_names+'\n')
        mslist=glob.glob(ms_names)        
        logger.debug(pformat(mslist))
        for vis in mslist:
            logger.debug(" ")
            logger.debug('imaging: '+str(vis))
            casa_proc.casa_task('ms2im',
                        vis=vis,
                        imagename=vis.replace('.ms.contsub','').replace('data_','cmod2d_'),
                        cell=0.04,imsize=64,
                        datacolumn='data',preload=ms2im)
            casa_proc.casa_task('ms2im',
                        vis=vis,
                        imagename=vis.replace('.ms.contsub','').replace('data_','cmod3d_'),
                        cell=0.04,imsize=64,
                        datacolumn='corrected',preload=ms2im)
        #"""   
            
    if  args.plot==True:
        
        fn_pattern=inp_dct['general']['outdir']+'/p_*/data_b?_bb?.fits'
        fn_names=sorted(glob.glob(fn_pattern))
        logger.debug("\n"+fn_pattern)
        logger.debug('plotting list:')
        for fn_name in fn_names:
            logger.debug(fn_name)
        logger.debug("\n")

        # tmp
        source='bx610'
        
        for fn_name in fn_names:

            logger.info('#### processing the image set: {} \n'.format(fn_name))
            linechan=None
            
            if  source=='bx610':
                
                pa=-52
                radec=[356.5393256478768,12.82201783168984]
                width=0.5
                length=2.5
                cen1='icrs; circle( 356.5393256478768,12.82201783168984,1.00") # text={cen1}'
                cen2='icrs; circle( 356.5393256478768,12.82201783168984,0.20") # text={cen2}'
                slice1='icrs; box( 356.5393256478768,12.82201783168984,0.20",0.75",128) # text={slice1}'
                slice2='icrs; box( 356.5393256478768,12.82201783168984,0.20",0.75",38)  # text={slice2}'
                rois=[cen1,cen2,slice1,slice2]
                                
                if  'b6_bb2' in fn_name:
                    linechan=[(250.964*u.GHz,251.448*u.GHz),(251.847*u.GHz,252.246*u.GHz)]
                if  'b6_bb3' in fn_name:
                    linechan=(233.918*u.GHz,234.379*u.GHz)
                if  'b4_bb1' in fn_name:
                    linechan=(153.069*u.GHz,153.522*u.GHz)
                if  'b4_bb3' in fn_name:
                    linechan=(143.359*u.GHz,143.835*u.GHz)
                    
            for roi in rois:
                plt_spec1d(fn_name,roi=roi)

            plt_mom0xy(fn_name,linechan=linechan)
            plt_makeslice(fn_name,radec=radec,
                          width=width,length=length,pa=pa,linechan=linechan)
            
            plt_slice(fn_name,i=1)
            plt_slice(fn_name,i=2)
            
            plt_radprof(fn_name)        
        