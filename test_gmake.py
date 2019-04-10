import time
import importlib 

import gmake
importlib.reload(gmake)

#import builtins
#from IPython.lib import deepreload
#builtins.reload = deepreload.reload
#deepreload.reload(gmake)

if  __name__=="__main__":

    inp_dct=None
    dat_dct=None
    inp_dct=gmake.gmake_read_inp('examples/bx610/xysf_k_ab.inp',verbose=False)
    dat_dct=gmake.gmake_read_data(inp_dct,verbose=True)
    
    mod_dct=gmake.gmake_inp2mod(inp_dct)
    gmake.gmake_gravity_galpy(mod_dct,plotrc=False)
    
    tic0=time.time()
    models=gmake.gmake_model_api(mod_dct,dat_dct,verbose=True)
    print('Took {0} second on one API run'.format(float(time.time()-tic0))) 

    fit_dct,sampler=gmake.gmake_fit_setup(inp_dct,dat_dct)
    gmake.gmake_fit_iterate(fit_dct,sampler,nstep=300)
