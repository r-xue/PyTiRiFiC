
execfile('gmake_model_func.py')
execfile('gmake_model.py')
execfile('gmake_utils.py')
execfile('gmake_emcee.py')

def gmake_insertmodel(data,model,offset=[0,0,0],verbose=False):
    """
    insert a model into the data
        data/model is supposed to be transposed already,
        therefore follows the IDL indexing convention.
    offset is define from the left-bottom corner of data.
        so    model        -->    data
            [0,0,0]-pix    -->    offset-pix
    """
    d_nd=data.shape
    m_nd=model.shape

    
    mx_range=[0,m_nd[0]]
    my_range=[0,m_nd[1]]
    mz_range=[0,m_nd[2]]
    dx_range=[0+int(offset[0]),m_nd[0]+int(offset[0])]
    dy_range=[0+int(offset[1]),m_nd[1]+int(offset[1])]
    dz_range=[0+int(offset[2]),m_nd[2]+int(offset[2])]
    
    if  dx_range[0]<0:
        mx_range[0]+=-dx_range[0]
        dx_range[0]=0
    if  dx_range[1]>d_nd[0]:
        mx_range[1]+=-(dx_range[1]-d_nd[0])
        dx_range[1]+=-(dx_range[1]-d_nd[0])
    
    if  dy_range[0]<0:
        my_range[0]+=-dy_range[0]
        dy_range[0]=0
    if  dy_range[1]>d_nd[1]:
        my_range[1]+=-(dy_range[1]-d_nd[1])
        dy_range[1]+=-(dy_range[1]-d_nd[1])
    
    if  dz_range[0]<0:
        mz_range[0]+=-dz_range[0]
        dz_range[0]=0
    if  dz_range[1]>d_nd[2]:
        mz_range[1]+=-(dz_range[1]-d_nd[2])
        dz_range[1]+=-(dz_range[1]-d_nd[2])
    
    if  verbose==True:
        print("+"*20)
        print(offset)
        print(d_nd)
        print(dx_range[0],dx_range[1])
        print(dy_range[0],dy_range[1])
        print(dz_range[0],dz_range[1])
        print(m_nd)
        print(mx_range[0],mx_range[1])
        print(my_range[0],my_range[1])
        print(mz_range[0],mz_range[1])    
    
    if  data.ndim==3 and model.ndim==3:
        data[dx_range[0]:dx_range[1],
             dy_range[0]:dy_range[1],
             dz_range[0]:dz_range[1]]=model[mx_range[0]:mx_range[1],
                                            my_range[0]:my_range[1],
                                            mz_range[0]:mz_range[1]]
    if  data.ndim==4 and model.ndim==3:
        data[0,
             dx_range[0]:dx_range[1],
             dy_range[0]:dy_range[1],
             dz_range[0]:dz_range[1]]=model[mx_range[0]:mx_range[1],
                                            my_range[0]:my_range[1],
                                            mz_range[0]:mz_range[1]]    
    
    return data

def test_gmake_model_disk2d():
    
    data,hd=fits.getdata('examples/bx610/bx610_spw25.mfs.fits',header=True,memmap=False)
    data,hd=fits.getdata('examples/bx610/bx610.bb4.cube.iter0.image.fits',header=True,memmap=False)
    psf,phd=fits.getdata('examples/bx610/bx610.bb4.cube.iter0.psf.fits',header=True,memmap=False)
    #psf=psf[0,100,:,:]
    model=gmake_model_disk2d(hd,356.539321,12.8220179445,
                             beam=[0.1,0.2,10.0],
                             psf=psf,
                             r_eff=0.2,n=1.0,posang=20,ellip=0.5,
                             cleanout=False)
    
    
    #fits.writeto('test/test_model_disk2d.fits',model,hd,overwrite=True)
    """
    log_model=np.log(model)
    plt.figure()
    plt.imshow(np.log(model), origin='lower', interpolation='nearest',
           vmin=np.min(log_model), vmax=np.max(log_model))
    plt.xlabel('x')
    plt.ylabel('y')
    cbar = plt.colorbar()
    cbar.set_label('Log Brightness', rotation=270, labelpad=25)
    cbar.set_ticks([np.min(log_model),np.max(log_model)], update_ticks=True)
    plt.savefig('test/test_model_disk2d.eps')
    """

if  __name__=="__main__":
    
    pass

#inp_dct=gmake_readinp('examples/bx610/bx610xy_dm_all.inp',verbose=False)
#dat_dct=gmake_read_data(inp_dct,verbose=True,fill_mask=True,fill_error=True)
#fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
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
    
