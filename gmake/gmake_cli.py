import os
import argparse
import glob
from configparser import ConfigParser, ExtendedInterpolation

# gmake -a bx610/uvb6_ab.inp

from gmake import gmake_read_inp
from gmake import gmake_read_data
from gmake import gmake_fit_setup
from gmake import gmake_fit_iterate
from gmake import gmake_fit_analyze
from gmake import gmake_plots_spec1d
from gmake import gmake_casa


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

    args = parser.parse_args()
    
    if  args.fit==False and args.analyze==False and args.plot==False:
        args.fit=True
        
    if  not os.path.isfile(args.inpfile):
        print("The inpfile '"+args.inpfile+"' doesn't exist. Aborted!")
        return
    
    process_inpfile(args)
    
    return


def process_inpfile(args):
    
    if  args.debug==True:
        print(args.fit)
        print(args.analyze)
        print(args.plot)    
        print(args.debug)
    
    inp_dct=gmake_read_inp(args.inpfile,verbose=args.debug)
    
    if  args.fit==True:
        #inp_dct=gmake_read_inp(args.inpfile,verbose=args.debug)
        dat_dct=gmake_read_data(inp_dct,verbose=args.debug,fill_mask=True,fill_error=True)
        fit_dct,sampler=gmake_fit_setup(inp_dct,dat_dct)
        gmake_fit_iterate(fit_dct,sampler,nstep=inp_dct['optimize']['niter'])
        
        
    if  args.analyze==True:
        #inp_dct=gmake_read_inp(args.inpfile,verbose=args.debug)
        gmake_fit_analyze(inp_dct['optimize']['outdir'])
        #"""
        mslist=glob.glob(inp_dct['optimize']['outdir']+'/p_*/*.ms')
        for vis in mslist:
            print('imaging: ',vis)
            input={}
            input['vis']=vis
            input['imagename']=vis.replace('.ms','').replace('/data_','/cmodel_')
            input['datacolumn']='corrected'
            gmake_casa('ms2im',input=input,verbose=False)
            input['imagename']=vis.replace('.ms','').replace('/data_','/data_')
            input['datacolumn']='data'
            gmake_casa('ms2im',input=input,verbose=False)  
        #"""      