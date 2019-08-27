
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

from gmake import gmake_read_inp
from gmake import gmake_read_data
from gmake import gmake_fit_setup
from gmake import gmake_fit_iterate
from gmake import gmake_fit_analyze
from gmake import gmake_plots_spec1d
from gmake import gmake_casa
from gmake import gmake_plots_mom0xy
from gmake import gmake_plots_makeslice
from gmake import gmake_plots_slice
from gmake import gmake_plots_radprof

from .gmake_utils import *

from .__version__ import __version__

import astropy.units as u

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
        
    if  not os.path.isfile(args.inpfile):
        print("The inpfile '"+args.inpfile+"' doesn't exist. Aborted!")
        return
    
    #logging.basicConfig(level=logging.DEBUG,
    #                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    #                    filename=args.logfile)
    
    logfile_formatter=MultilineFormatter('%(asctime)s %(name)-6s %(levelname)-6s -- %(message)s')
    #logfile_formatter=logging.Formatter('%(asctime)s %(name)-6s %(levelname)-6s -- %(message)s')
    logfile_handler=logging.FileHandler(args.logfile)  
    logfile_handler.setFormatter(logfile_formatter)
    
    logger=logging.getLogger('gmake')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logfile_handler)
    
    """
    logger.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        filename=args.logfile)
    """    
    if  args.debug==False:
        logger.setLevel(logging.INFO)
    
    
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.DEBUG)
    #logger.addHandler(ch)
    
    #ch
    
    
    """
    logging levels:
        logging.debug('This is a debug message')
        logging.info('This is an info message')
        logging.warning('This is a warning message')
        logging.error('This is an error message')
        logging.critical('This is a critical message')    
    """
    
    logger.info("+"*60)
    logger.info("GMaKE -- Start")
    logger.debug("Software version {}".format(__version__))
    logger.debug("Python version: {}".format(sys.version))
    logger.info("-"*60)      
    
    process_inpfile(args)
    
    logger.info("+"*60)
    logger.info("GMaKE -- End")
    logger.info("-"*60)

    return


def process_inpfile(args):
    
    logging.debug("process options:")
    logging.debug("fit:    "+str(args.fit))
    logging.debug("analyze:"+str(args.analyze))
    logging.debug("plot:   "+str(args.plot))
    logging.debug("debug:  "+str(args.debug))
    
    inp_dct=gmake_read_inp(args.inpfile,verbose=args.debug)
    
    if  args.fit==True:

        dat_dct=gmake_read_data(inp_dct,verbose=args.debug,fill_mask=True,fill_error=True)
        fit_dct,sampler=gmake_fit_setup(inp_dct,dat_dct)
        gmake_fit_iterate(fit_dct,sampler,nstep=inp_dct['optimize']['niter'])
        
        
    if  args.analyze==True:

        gmake_fit_analyze(inp_dct['optimize']['outdir'])
        #"""
        mslist=glob.glob(inp_dct['optimize']['outdir']+'/p_fits/*bb?*.ms')
        for vis in mslist:
            
            logging.debug('imaging: '+str(vis))
            
            input={}
            
            input['vis']=vis
            input['imagename']=vis.replace('.ms','').replace('/data_','/cmodel_')
            input['datacolumn']='corrected'
            logging.info('{} --> {}'.format(input['vis'],input['imagename']))
            gmake_casa('ms2im',input=input,verbose=False)

            input['vis']=vis+'.contsub'
            input['imagename']=vis.replace('.ms','').replace('/data_','/cmod3d_')
            input['datacolumn']='corrected'
            logging.info('{} --> {}'.format(input['vis'],input['imagename']))
            gmake_casa('ms2im',input=input,verbose=False)
                        
            input['vis']=vis+'.cont'
            input['imagename']=vis.replace('.ms','').replace('/data_','/cmod2d_')
            input['datacolumn']='corrected'
            logging.info('{} --> {}'.format(input['vis'],input['imagename']))
            gmake_casa('ms2im',input=input,verbose=False)            
            
            input['imagename']=vis.replace('.ms','').replace('/data_','/data_')
            input['datacolumn']='data'
            logging.info('{} --> {}'.format(input['vis'],input['imagename']))
            gmake_casa('ms2im',input=input,verbose=False)  
        #"""      
        
    if  args.plot==True:
        
        fn_pattern=inp_dct['optimize']['outdir']+'/p_fits/data_b?_bb?.fits'
        fn_names=sorted(glob.glob(fn_pattern))
        logging.info("\n")
        logging.info(fn_pattern)
        logging.info('plotting list:')
        for fn_name in fn_names:
            logging.info(fn_name)
        logging.info("\n")

        # tmp
        source='bx610'
        for fn_name in fn_names:

            logging.info('#### processing the image set: {} \n'.format(fn_name))
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
                gmake_plots_spec1d(fn_name,roi=roi)

            """
            gmake_plots_mom0xy(fn_name,linechan=linechan)
            pa=-52
            gmake_plots_makeslice(fn_name,
                                  radec=[356.5393256478768,12.82201783168984],
                                  width=0.5,length=2.5,pa=-52,linechan=linechan)
            gmake_plots_slice(fn_name,i=1)
            gmake_plots_slice(fn_name,i=2)
            """
            gmake_plots_radprof(fn_name)        
        