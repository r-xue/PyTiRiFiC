



    #fig,ax=plt.subplots(1,1,sharex=True,figsize=(8,8))
     

    #ax.projection=wcs
    #cbar = fig.colorbar(cs1,ax=(ax1,ax2,ax3),orientation='vertical',fraction=.1)
    #cbar.set_label('Log Brightness', rotation=270, labelpad=25)
    #cbar.set_ticks([vmin,vmax])
    
    #model_m0.write('model_mom0.fits',overwrite=True)
    
#     fig = plt.figure(figsize=(14, 7))
#     
#     f1 = aplpy.FITSFigure(model_m0.array,hdu=model_m0.hdu, figure=fig,
#                           subplot=[0.13, 0.1, 0.35, 0.7])
#     
#     f1.tick_labels.set_font(size='x-small')
#     f1.axis_labels.set_font(size='small')
#     f1.show_grayscale()
#     
#     f2 = aplpy.FITSFigure('model_mom0.fits', figure=fig,
#                           subplot=[0.5, 0.1, 0.35, 0.7])
#     
#     f2.tick_labels.set_font(size='x-small')
#     f2.axis_labels.set_font(size='small')
#     f2.show_grayscale()
#     
#     f2.axis_labels.hide_y()
#     f2.tick_labels.hide_y()
#     
#     fig.savefig('subplots.png', bbox_inches='tight')    
    
    #"""
    #log_model=np.log(model)

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

    
#     fit_tab=Table.read(outfolder+'/'+'emcee_chain_analyzed.fits')
#     print(fit_tab['p_name'].data[0])
#     theta=fit_tab['p_median'].data[0]
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