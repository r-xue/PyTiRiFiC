import time
import importlib 

import gmake
importlib.reload(gmake)

#import builtins
#from IPython.lib import deepreload
#builtins.reload = deepreload.reload
#deepreload.reload(gmake)

import pprint

import matplotlib.pyplot as plt

if  __name__=="__main__":

    #par_dct=gmake.gmake_read_inp('gmake/parameters.inp',verbose=True)
    #pprint.pprint(par_dct)

   
    #"""
    inp_dct=None
    dat_dct=None
    #inp_dct=gmake.gmake_read_inp('examples/bx610/xysf_k_ab.1.inp',verbose=True)
    #inp_dct=gmake.gmake_read_inp('examples/bx610/test_rc.inp',verbose=True)
    inp_dct=gmake.gmake_read_inp('examples/w0533/uvb3_ab.inp',verbose=True)
    
    pprint.pprint(inp_dct)
    mod_dct=gmake.gmake_inp2mod(inp_dct)
    pprint.pprint(mod_dct)
    
    #"""
    dat_dct=gmake.gmake_read_data(inp_dct,verbose=True)
    
    mod_dct=gmake.gmake_inp2mod(inp_dct)
    #gmake.gmake_model_func_dynamics(mod_dct,plotrc=False)
    
    tic0=time.time()
    models=gmake.gmake_model_api(mod_dct,dat_dct,verbose=True)
    #print('Took {0} second on one API run'.format(float(time.time()-tic0))) 

    #fit_dct,sampler=gmake.gmake_fit_setup(inp_dct,dat_dct)
    
    #gmake.gmake_fit_iterate(fit_dct,sampler,nstep=300)
    #"""
    
    """
    gmake.gmake_fit_analyze('examples/bx610/models/xysf_k_ab.2')
    
    """
    
    
    """
    x=models['imod3d_prof@co43@examples/bx610/alma/band4/bx610.bb3.cube128x128.iter0.image.fits']['vrad'] 
    y=models['imod3d_prof@co43@examples/bx610/alma/band4/bx610.bb3.cube128x128.iter0.image.fits']['vrot']
    
     
    plt.clf()
    fig,ax1=plt.subplots(1,1,figsize=(5,3))
    ax1.plot(x,y,color='red')
    #ax1.loglog(rad,vcirc_tp)
    #ax1.loglog(rad,vcirc_tp,color='black')
    #ax2.loglog(rad,cmass_tp)
    fig.savefig('pot2rc.pdf')
    plt.close()
    """