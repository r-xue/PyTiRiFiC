execfile('gmake_init.py')


vis='/Users/Rui/Downloads/test.ms'
"""

t=ctb.table(vis,ack=False,readonly=True)
coldmi = t.getdminfo('DATA')
print(coldmi)

coldmi["NAME"] = 'tsm2'
t.close

"""







    
    
    #np.save(fit_dct['outfolder']+'/dat_dct.npy',dat_dct)
    #np.save(fit_dct['outfolder']+'/fit_dct.npy',fit_dct)   #   fitting metadata
    #np.save(fit_dct['outfolder']+'/inp_dct.npy',inp_dct)   #   input metadata
    
    
#"""
 
t=ctb.table(vis,ack=False,readonly=True)
data=t.getcol('DATA')
t.unlock()

uvmodel=np.sum(data,axis=-1)
print(data.shape,uvmodel.shape)
add_uvmodel(vis,uvmodel)

