



   
x=[] 
x+=[  1.0*u.m/u.s ]
x+=[ [1.0,2.0]*u.m/u.s ]
x+=[ SkyCoord('02h20m16.653s','-06d01m41.92s',frame='icrs') ]
for x0 in x:
    print('x0:',x0,type(x0))
    y0=repr_parameter(x0)
    print('repr:',y0)
    x0_back=aeval(y0)
    print('x0_back:',x0_back)
    print(x0==x0_back)
    if  isinstance(x0,SkyCoord):
        print(x0_back.separation(x0).to(u.arcsec)*10000.)
