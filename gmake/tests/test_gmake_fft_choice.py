import gmake
import socket
if  'hypersion' or 'mini' in socket.gethostname() :
    os.chdir(gmake.__demo__+'/../gmake/tests/results/mockup/uv_nelder')
    os.chdir(gmake.__demo__+'/../gmake/tests/results/mockup/sbrci')
print(sys.version)

print(socket.gethostname())
print(os.getcwd())
print(gmake.__version__)
print(gmake.__email__)
print(gmake.__demo__)
inpfile=gmake.__demo__+'/../gmake/tests/data/mockup_basic_opt_ab.inp'
inpfile='xy00_mc.inp'
#pprint(np.sum(dat_dct['weight@../../../data/mockup_basic_withnoise.ms']==0))
import gmake
inp_dct=gmake.read_inp(inpfile)
dat_dct=gmake.read_data(inp_dct)
#inp_dct=gmake.inp_validate(inp_dct)
#mod_dct=gmake.inp2mod(inp_dct)
#gmake.clouds_fill(mod_dct)
#print(mod_dct)
#models=gmake.model_setup(gmake.inp2mod(inp_dct),dat_dct)

fit_dct,models=gmake.opt_setup(inp_dct,dat_dct,initial_model=True)
#pprint(models)
#models['error@../../data/mockup_basic_withnoise.ms/dm.image.fits']
#pprint(fit_dct)
#pprint(models)
#%lprun -f gmake.evaluate.calc_wdev gmake.opt_iterate(fit_dct,inp_dct,dat_dct,models,resume=False)
#gmake.opt_iterate(fit_dct,inp_dct,dat_dct,models)
p0=[q.value for q in fit_dct['p_start']]
gmake.utils.set_threads(1)
%timeit gmake.evaluate.calc_wdev(p0,fit_dct=fit_dct,inp_dct=inp_dct,models=models)
