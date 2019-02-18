
execfile('gmake_model_func.py')
execfile('gmake_model.py')
execfile('gmake_utils.py')
execfile('gmake_emcee.py')




if  __name__=="__main__":
    
    pass

    inp_dct=gmake_readinp('examples/bx610/bx610xy_dm_all.inp',verbose=False)
    dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
    fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
#gmake_emcee_iterate(sampler,fit_dct,nstep=500)

#outfolder='bx610xy_cont_dm_emcee'
#fit_tab=gmake_emcee_analyze(outfolder,plotsub=None,burnin=250,plotcorner=True,
#                    verbose=True)

#fit_dct=np.load(outfolder+'/fit_dct.npy').item()
#inp_dct=np.load(outfolder+'/inp_dct.npy').item()
#fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
#theta=fit_tab['p_median'].data[0]
#lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_median')
#print(lnl,blobs) 


"""
inp_dct=gmake_readinp('examples/bx610/bx610xy_cm_cont.inp',verbose=False)
dat_dct=gmake_read_data(inp_dct,verbose=False,fill_mask=True,fill_error=True)
fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
gmake_emcee_iterate(sampler,fit_dct,nstep=500)

outfolder='bx610xy_cont_cm_emcee'
fit_tab=gmake_emcee_analyze(outfolder,plotsub=None,burnin=250,plotcorner=True,
                    verbose=True)
fit_dct=np.load(outfolder+'/fit_dct.npy').item()
inp_dct=np.load(outfolder+'/inp_dct.npy').item()
fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
theta=fit_tab['p_median'].data[0]
lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_median')
print(lnl,blobs)
"""

"""
inp_dct=gmake_readinp('examples/bx610/bx610xy_dm_cont.inp',verbose=False)
dat_dct=gmake_read_data(inp_dct,verbose=False,fill_mask=True,fill_error=True)
fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
gmake_emcee_iterate(sampler,fit_dct,nstep=500)

outfolder='bx610xy_cont_dm_emcee'
fit_tab=gmake_emcee_analyze(outfolder,plotsub=None,burnin=250,plotcorner=True,
                    verbose=True)

fit_dct=np.load(outfolder+'/fit_dct.npy').item()
inp_dct=np.load(outfolder+'/inp_dct.npy').item()
fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
theta=fit_tab['p_median'].data[0]
lnl,blobs=gmake_model_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel=outfolder+'/p_median')
print(lnl,blobs)    
#"""






"""
#   build a dict holding input config
inp_dct=gmake_readinp('examples/bx610/bx610xy.inp',verbose=False)
#   build a dict holding data
dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
#   build the sampler and a dict holding sampler metadata
fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
#   iterate
gmake_emcee_iterate(sampler,fit_dct,nstep=500)
"""


#   build a dict holding input config
#inp_dct=gmake_readinp('examples/bx610/bx610xy_cont.inp',verbose=False)
#   build a dict holding data
#dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
#   build the sampler and a dict holding sampler metadata
#fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
#   iterate
#gmake_emcee_iterate(sampler,fit_dct,nstep=500)



"""
outfolder='bx610xy_emcee/'
fit_tab=gmake_emcee_analyze(outfolder,plotsub=None,burnin=250,plotcorner=True,
                    verbose=True)
fit_dct=np.load(outfolder+'/fit_dct.npy').item()
inp_dct=np.load(outfolder+'/inp_dct.npy').item()

dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
#inp_dct=gmake_readinp('examples/bx610/bx610xy.inp',verbose=False)

fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
print(fit_tab['p_name'].data[0])
theta=fit_tab['p_median'].data[0]
print(theta)
"""

#theta[0]=theta[0]*100.
#theta[2]=theta[2]*100.

#print('-->',theta)
#print(fit_dct['p_up'])  
#fit_dct['p_up'][0]=fit_dct['p_up'][0]*100.
#fit_dct['p_up'][2]=fit_dct['p_up'][2]*100.
#print(fit_dct['p_up'])

#lnl,blobs=gmake_kinmspy_lnprob(theta,fit_dct,inp_dct,dat_dct,savemodel='bx610xy_emcee/p_median')
#print(lnl,blobs)





"""
opt_dct=inp_dct['optimize']

for par_name in opt_dct.keys():
    po_str=key.split("@")
    pi_str=re.findall("\[(.*?)\]", po_str[0])
    #print(pi_str,po_str)
    if  len(pi_str)==0:
        par_str=po_str[0]
        obj_str=po_str[1]
        print(key,input[obj_str][par_str])
    else:
        par_str=(po_str[0].split("["))[0]
        obj_str=po_str[1]
        ind_str=pi_str[0]
        print(key,input[obj_str][par_str][make_slice(ind_str)])
        #print(input[po_str[1]][po_str[0]][make_slice(pi_str[0])])
"""        
"""
x=range(20)
print(x)
print(x[make_slice('0:1')])
print(x[make_slice('10:2:-1')])
print(x[make_slice('1')])
x[make_slice('0:1')]=[2]
x[make_slice('1:4')]=[3,2,1]
print(x)
"""
#mcpars['mode']='emcee'
#mcpars['nthreads']=multiprocessing.cpu_count()


#"""
#"""

#print(fit_dct['p_name'])

#print(fit_dct['p_start'])
#gmake_model_lnprob(fit_dct['p_start'],fit_dct,inp_dct,data_dct,savemodel='test',verbose=True)

#pprint.pprint(models)
#print(models.keys())


        
             #   for the 2D "common-beam" case
        #   broadcasting to 4D (broadcast_to just create a "view"; .copy needed)
        
#         model2d=convolve_fft(model2d,kernel)
#         model=np.broadcast_to(model2d,(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])).copy()
#     else:
#         #   for the varying-PSF case
#         model=np.broadcast_to(model2d,(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])).copy()
     
#     model=np.zeros('')
#     if  not cleanout:
#         # end up with Jy/beam
#         #print(model.shape,psf_beam.shape)
#         model=convolve_fft(model,kernel)
#         model *= ( intflux_model*kernel.sum()/model.sum() )
#     else: 
#         # end up with Jy/pix
#         model *= ( intflux_model/model.sum() )
    
    #   the same as the center method
    #psf=makekernel(15,15,[6.0,3.0],pa=20)
    #fits.writeto('makekernel_psf.fits',psf,overwrite=True)
#     psf1=makekernel(11,11,[3.0,3.0],pa=0,cent=0)
#     fits.writeto('makekernel_psf1.fits',psf1,overwrite=True)
#     psf2=makekernel(13,13,[3.0,3.0],pa=0,cent=0)
#     fits.writeto('makekernel_psf2.fits',psf2,overwrite=True)
    #cm=convolve_fft(im,psf)
    #fits.writeto('makekernel_convol.fits',cm,overwrite=True)
    
