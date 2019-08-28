
"""

    usage:
        
        >gmake_cli -a bx610/uvb6_ab.inp -d -l uvb6_ab.log

"""

import os
import argparse
import glob
import logging
import sys

from configparser import ConfigParser, ExtendedInterpolation

from gmake import read_inp
from gmake import read_data
from gmake import gmake_fit_setup
from gmake import gmake_fit_iterate
from gmake import fit_analyze
from gmake import gmake_casa

from gmake import plt_spec1d
from gmake import plt_mom0xy
from gmake import plt_makeslice
from gmake import plt_slice
from gmake import plt_radprof

from .gmake_utils import *
from .__version__ import __version__

import astropy.units as u

logger=logging.getLogger(__name__)

def main():
    
    """
    Parse options and launch the workflow
    """    
    
    description="""

The GMAKE CL entry point: 
    gmake path/example.inp

    model fitting:
        gmake -f path/example.inp
    analyze fitting results (saved in FITS tables / HDFs?) and export model/data for diagnostic plotting  
        gmake -a path/example.inp 
    generate diagnostic plots
        gmake -p path/example.inp 

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
                        dest='logfile',action='store',default='gmake.log',
                        help="path to log file")
    
    args = parser.parse_args()
    if  args.fit==False and args.analyze==False and args.plot==False:
        args.fit=True
       
     
    """
    logging levels:
        logging.debug('This is a debug message')
        logging.info('This is an info message')
        logging.warning('This is a warning message')
        logging.error('This is an error message')
        logging.critical('This is a critical message')
    default level is "warning"    
    """
    logging.getLogger().setLevel(logging.DEBUG)
    """
    file logging handler 
       + customize logfile formatter
       + add logfile to the RootLogger (messages from all loggers will be propagated to the master logfile)
    """
    logfile_handler=logging.FileHandler(args.logfile)
    #format="%(asctime)s "+"{:<40}".format("%(name)s.%(funcName)s")+" [%(levelname)s] ::: %(message)s"
    #logfile_formatter=MultilineFormatter(format)
    logfile_formatter=CustomFormatter()
    logfile_handler.setFormatter(logfile_formatter)
    logfile_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(logfile_handler)
    """
    console logging handler
    """
    consol_handler = logging.StreamHandler()
    if  args.debug==False:
        consol_handler.setLevel(logging.INFO)
    else:
        consol_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(consol_handler)        
        
    if  not os.path.isfile(args.inpfile):
        logger.info("The inpfile '"+args.inpfile+"' doesn't exist. Aborted!")
        return
    
    
    
    logger.info("\n"*2+"#"*80)
    logger.info("GMaKE "+__version__+" -- Start")
    logger.debug("Python version: {}".format(sys.version))
    logger.info("#"*80+'\n')      
    
    proc_inpfile(args)
    
    logger.info('\n'+"#"*80)
    logger.info("GMaKE "+__version__+" -- End")
    logger.info("#"*80+'\n'*2)

    return


def proc_inpfile(args):
    
    logger.debug("gmake_cli process options:")
    for arg in vars(args):
        arg, getattr(args, arg)
        logger.debug("{:<10} :  {:}".format(arg,getattr(args,arg)) )
    
    inp_dct=read_inp(args.inpfile)
    
    if  args.fit==True:
        
        dat_dct=read_data(inp_dct,fill_mask=True,fill_error=True)
        fit_dct,sampler=gmake_fit_setup(inp_dct,dat_dct)
        gmake_fit_iterate(fit_dct,sampler,nstep=inp_dct['optimize']['niter'])
        
    if  args.analyze==True:

        #fit_analyze(inp_dct['optimize']['outdir'])
        #"""
        mslist=glob.glob(inp_dct['optimize']['outdir']+'/p_fits/*bb?*.ms')
        for vis in mslist:
            
            logger.debug(" ")
            logger.debug('imaging: '+str(vis))
            
            input={}
            
            input['vis']=vis
            input['imagename']=vis.replace('.ms','').replace('/data_','/cmodel_')
            input['datacolumn']='corrected'
            logger.debug('{} --> {}'.format(input['vis'],input['imagename']))
            gmake_casa('ms2im',input=input)

            input['vis']=vis+'.contsub'
            input['imagename']=vis.replace('.ms','').replace('/data_','/cmod3d_')
            input['datacolumn']='corrected'
            logger.debug('{} --> {}'.format(input['vis'],input['imagename']))
            gmake_casa('ms2im',input=input)
                        
            input['vis']=vis+'.cont'
            input['imagename']=vis.replace('.ms','').replace('/data_','/cmod2d_')
            input['datacolumn']='corrected'
            logger.debug('{} --> {}'.format(input['vis'],input['imagename']))
            gmake_casa('ms2im',input=input)            
            
            input['imagename']=vis.replace('.ms','').replace('/data_','/data_')
            input['datacolumn']='data'
            logger.debug('{} --> {}'.format(input['vis'],input['imagename']))
            gmake_casa('ms2im',input=input)  
        #"""      
        
    if  args.plot==True:
        
        fn_pattern=inp_dct['optimize']['outdir']+'/p_fits/data_b?_bb?.fits'
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
            if  'b6_bb2' in fn_name and source=='bx610':
                linechan=[(250.964*u.GHz,251.448*u.GHz),(251.847*u.GHz,252.246*u.GHz)]
            if  'b6_bb3' in fn_name and source=='bx610':
                linechan=(233.918*u.GHz,234.379*u.GHz)
            if  'b4_bb1' in fn_name and source=='bx610':
                linechan=(153.069*u.GHz,153.522*u.GHz)
            if  'b4_bb3' in fn_name and source=='bx610':
                linechan=(143.359*u.GHz,143.835*u.GHz)

            cen1='icrs; circle( 356.5393256478768,12.82201783168984,1.00") # text={cen1}'
            cen2='icrs; circle( 356.5393256478768,12.82201783168984,0.20") # text={cen2}'
            slice1='icrs; box( 356.5393256478768,12.82201783168984,0.20",0.75",128) # text={slice1}'
            slice2='icrs; box( 356.5393256478768,12.82201783168984,0.20",0.75",38)  # text={slice2}'
            rois=[cen1,cen2,slice1,slice2]
            for roi in rois:
                plt_spec1d(fn_name,roi=roi)

            """
            plt_mom0xy(fn_name,linechan=linechan)
            pa=-52
            plt_makeslice(fn_name,
                                  radec=[356.5393256478768,12.82201783168984],
                                  width=0.5,length=2.5,pa=-52,linechan=linechan)
            plt_slice(fn_name,i=1)
            plt_slice(fn_name,i=2)
            """
            plt_radprof(fn_name)        
        