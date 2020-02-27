
def test_makepsf():
    """
    obselete
    """
    header=gmake.meta.create_header()
    header['NAXIS3']=128
    header['NAXIS1']=64
    
    header['CRVAL1']=189.2995416666666 
    header['CDELT1']=-6.0596976551930E-05 
    header['CRPIX1']=65.0
    
    header['CRVAL2']=62.36994444444444
    header['CDELT2']=6.05969765519303E-05   
    header['CRPIX2']=65.0
    
    header['CRVAL3']=45535299115.90349
    header['CDELT3']=2000013.13785553
    header['CRPIX3']=1.0   
    
    beam=(0.1*u.arcsec,0.5*u.arcsec,10*u.deg)
    cell=np.sqrt(abs(header['CDELT1']*header['CDELT2']))
    print(cell*3600)
    
    cc_psf=gmake.model.makepsf(header,beam=beam,size=(31,31),mode='center')
    os_psf=gmake.model.makepsf(header,beam=beam,size=(31,31),mode='oversample')    
    true_psf=gmake.model.makepsf(header,beam=beam,size=(31,31),mode='oversample',factor=50)    