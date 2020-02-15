import gmake

#"""
inpfile='../inpfile/bx610_band6_uv_ab.inp'
inp_dct=gmake.read_inp(inpfile)
dat_dct=gmake.read_data(inp_dct,fill_mask=True,fill_error=True)        
print(dat_dct)
#"""

%time gmake.dct2fits(dat_dct,outname='data')
%time gmake.dct2hdf(dat_dct,outname='data')
%time np.save('data.npy',dat_dct)

%time dct0=gmake.fits2dct('data.fits')
%time dct1=gmake.hdf2dct('data.h5')



"""
import hickle as hkl

dat_dct0=dat_dct.copy()
keys=list(dat_dct0.keys())
print(keys)
for key in keys:
    dat_dct0[key.replace('/','|')]=dat_dct0.pop(key)
    
hkl.dump(dat_dct0, 'dat_dct0.hkl', mode='w')
dat_dct1=hkl.load('dat_dct0.hkl')


test_dct0={'a':{'a1':1,'a2':2},'b':'b'}
hkl.dump(test_dct0, 'test_dct0.hkl', mode='w')
test_dct1=hkl.load('test_dct0.hkl')
print(test_dct0)
"""