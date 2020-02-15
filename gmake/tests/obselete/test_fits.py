from astropy.table import Table
from astropy.table import Column
from astropy.io import fits
import numpy as np

t=Table()

data=np.array([1.2])
t.add_column(Column(name='col1',data=[data],shape=(1,)))

data=np.array([[1.1,2.2],[1,2]])
t.add_column(Column(name='col2',data=[data]))
t.write('test.fits',overwrite=True)  

print(t['col1'][0].shape)
hdu=fits.table_to_hdu(t)
hdu.writeto('test2.fits',overwrite=True)


c1 = fits.Column(name='a', array=[[1.2]],format='')
c2 = fits.Column(name='b', array=[[1,2,3]],format='')
t = fits.BinTableHDU.from_columns([c1, c2])
t.writeto('test3.fits')


import sys
print(sys.sys.byteorder)

x=np.array([1,2])
dt=x.dtype
dt.byteorder
