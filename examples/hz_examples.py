#
#   Exampels of Fitting Gas Dynamics within High-redshift Galaxies 
#

# sys.path.insert(1,home+'/Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake/')
# 
# execfile('../gmake/gmake_init.py')
# 
# execfile('../gmake/gmake_model_func_kinms.py')
# execfile('../gmake/gmake_model_func.py')
# execfile('../gmake/gmake_model.py')
# execfile('../gmake/gmake_utils.py')
# execfile('../gmake/gmake_emcee.py')
# execfile('../gmake/gmake_amoeba.py')
# execfile('../gmake/gmake_lmfit.py')
# execfile('../gmake/gmake_gravity.py')
# execfile('../gmake/gmake_plots.py')
# execfile('../gmake/gmake_fit.py')
# execfile('../gmake/gmake_uvamp.py')

import os
import inspect

example_script = inspect.getframeinfo(inspect.currentframe()).filename
example_dir = os.path.dirname(os.path.abspath(example_script))

from gmake import gmake_read_inp
from gmake import gmake_read_data
from gmake import gmake_fit_setup

def hz_example(source,inpfile,
                  run_setup=True,
                  run_fit=True,
                  run_analysis=True,
                  run_plots=True,
                  dataset='alma'):
    
    if  run_setup==True:
        inp_dct=gmake_read_inp(example_dir+'/'+source+'/'+inpfile+'.inp',verbose=True)
        dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
        fit_dct,sampler=gmake_fit_setup(inp_dct,dat_dct)

    if  run_fit==True:
        gmake_fit_iterate(fit_dct,sampler,nstep=500)


    if  run_analysis==True:
        #inp_dct=gmake_read_inp('examples/bx610/'+inpfile+'.inp',verbose=False)
        outfolder='examples/'+source+'/models/'+inpfile
        gmake_fit_analyze(outfolder)

    if  run_plots==True:

        #fn_name_tmp='examples/bx610/models/'+inpfile+'/p_fits/data_bbx.fits'

        if  dataset=='alma':

            fn_pattern=example_dir+'/'+source+'/models/'+inpfile+'/p_fits/data_b?_bb?.fits'
            fn_names=sorted(glob.glob(fn_pattern))
            print("\n")
            print(fn_pattern)
            print('plotting list:')
            for fn_name in fn_names:
                print(fn_name)
            print("\n")

            for fn_name in fn_names:

                print('#### processing the image set:',fn_name,'\n')
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


                gmake_plots_mom0xy(fn_name,linechan=linechan)
                pa=-52
                #gmake_plots_makeslice(fn_name,
                #                      radec=[356.5393256478768,12.82201783168984],
                #                      width=0.5,length=2.5,pa=-52,linechan=linechan)
                #gmake_plots_slice(fn_name,i=1)
                #gmake_plots_slice(fn_name,i=2)
                gmake_plots_radprof(fn_name)

        if  dataset=='sinfoni' and source=='bx610':

            fn_name=example_dir+'/bx610/models/xysf_k_ab/p_fits/data_sf.fits'

            cen1='icrs; circle( 356.5393256478768,12.82201783168984,1.00") # text={cen1}'
            cen2='icrs; circle( 356.5393256478768,12.82201783168984,0.20") # text={cen2}'
            slice1='icrs; box( 356.5393256478768,12.82201783168984,0.20",0.75",128) # text={slice1}'
            slice2='icrs; box( 356.5393256478768,12.82201783168984,0.20",0.75",38)  # text={slice2}'
            rois=[cen1,cen2,slice1,slice2]
            for roi in rois:
                gmake_plots_spec1d(fn_name,roi=roi)
                continue

            linechan=None
            linechan=(20951*u.angstrom,21220*u.angstrom)
            gmake_plots_mom0xy(fn_name,linechan=linechan)

            pa=-52
            gmake_plots_makeslice(fn_name,
                                  radec=[356.5391952,12.8219583],
                                  width=0.5,length=2.5,pa=-52,linechan=linechan,
                                  slicechan=(20900*u.angstrom,21300*u.angstrom))
            gmake_plots_slice(fn_name,i=1)
            gmake_plots_slice(fn_name,i=2)
            gmake_plots_radprof(fn_name)


if  __name__=="__main__":


    ####################################
    #   EXAMPLES
    ####################################

    inpfile='xyb4dm128ab'
    #inpfile='xyb4dm128ab_rc'
    #inpfile='xyb6dm128ab'
    #inpfile='xyb6dm128ab_rc'
    #inpfile='xyb4dm128lm'
    inpfiles=[#'xyb4dm128_ab',
              #'xyb4dm128_lmnd',
              #'xyb4dm128_lmbt',
              'xyb4dm128rc_ab',
              #'xyb6dm128_ab',
              #'xyb6dm128_lmnd',
              'xyb6dm128rc_ab']
    inpfiles=['xyb46dm128rc_ab']
    inpfiles=['uvb6_ab']
    inpfiles=['xysf_ab']
    inpfiles=['xysf_k_ab']
    
    source='w0533'
    inpfiles=['uvb3_ab']
    
    
    source='bx610'
    inpfiles=['uvb6_ab']
    
    for inpfile in inpfiles:
        result=hz_example(source,inpfile,
                             run_setup=True,
                             run_fit=False,
                             run_analysis=False,
                             dataset='alma',
                             #dataset='sinfoni',
                             run_plots=False)

    ####################################
    #   EMCEE
    ####################################

    """
    #   build a dict holding input config
    #   build a dict holding data
    #   build the sampler and a dict holding sampler metadata
    #inp_dct=gmake_read_inp('examples/bx610/bx610xy_dm64_all.inp',verbose=False)
    #inp_dct=gmake_read_inp('examples/bx610/bx610xy_cm64_all.inp',verbose=False)
    #inp_dct=gmake_read_inp('examples/bx610/bx610xy_band4_cm64_all.inp',verbose=False)
    inp_dct=gmake_read_inp('examples/bx610/bx610xy_nas_cm64_all.inp',verbose=False)
    #inp_dct=gmake_read_inp('examples/bx610/bx610xy_cm_cont.inp',verbose=False)
    #inp_dct=gmake_read_inp('examples/bx610/bx610xy_dm_cont.inp',verbose=False)
    dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
    fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
    gmake_emcee_iterate(sampler,fit_dct,nstep=1000)

    outfolder='bx610xy_nas_cm64_all_emcee'
    fit_tab=gmake_emcee_analyze(outfolder,plotsub=None,burnin=600,plotcorner=True,
                    verbose=True)
    fit_dct=np.load(outfolder+'/fit_dct.npy').item()
    inp_dct=np.load(outfolder+'/inp_dct.npy').item()
    dat_dct=np.load(outfolder+'/dat_dct.npy').item()
    fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
    theta=fit_tab['p_start'].data[0]
    lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_start')
    print('pstart:    ',lnl,blobs)
    theta=fit_tab['p_median'].data[0]
    lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_median')
    print('p_median: ',lnl,blobs)
    """
