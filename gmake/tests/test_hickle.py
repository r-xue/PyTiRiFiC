import hickle as hkl
import astropy.units as u
from astropy.coordinates import Angle

radec=[1.0*u.deg,1.0*u.deg]
dct={'radec':radec}

h5file='test_hickle.h5'
hkl.dump(radec, h5file, mode='w')
dct_return=hkl.load(h5file)
x=Angle(dct_return[0]).to_string(unit=u.degree)
print(x,type(x))  
 
# pickle can serlias custom class if the class name is registered

# https://docs.astropy.org/en/stable/coordinates/angles.html


from astropy.table import Table

t=Table.read('test.csv')

t.write('test.tex',format='latex')


hkl.dump(radec, h5file, mode='w')
print()
dct_return=hkl.load(h5file)
print(dct_return,type(dct_return))
