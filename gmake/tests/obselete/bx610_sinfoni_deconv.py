

execfile('gmake_init.py')



repo='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/bx610/sinfoni/'
fn=repo+'bx610_data.fits'

slicechan=(21000*u.angstrom,21200*u.angstrom)

data=SpectralCube.read(fn,mode='readonly')
noise=SpectralCube.read(fn.replace('_data','_noise'),mode='readonly')
data=data.with_mask(data.unitless_filled_data[:,:,:]>2.0*noise.unitless_filled_data[:,:,:])
data=data.spectral_slab(slicechan[0],slicechan[1])

data_m0=data.moment(order=0)
data_m0.write(fn.replace('_data.fits','_data.mom0.fits'),overwrite=True)  

from skimage import color, data, restoration

header=fits.getheader(fn)
psf=fits.getdata(fn.replace('_data.fits','_psf.fits'))
psf=psf[(32-23):(32+22),(32-23):(32+22)]
mom0=np.nan_to_num(data_m0.value)


data_m0_dc = restoration.richardson_lucy(mom0, psf, iterations=20,clip=False)
tmp=data_m0_dc[(22-16):(22+16),(24-14):(24+14)]
data_m0_dc=data_m0_dc*0.0
data_m0_dc[(22-16):(22+16),(24-14):(24+14)]=tmp
data_m0_dc[np.where(data_m0_dc<0.2)]=0.0



fits.writeto(fn.replace('_data.fits','_data.mom0.deconv.fits'),data_m0_dc,header,overwrite=True)
fits.writeto(fn.replace('_data.fits','_data.mom0.before.fits'),mom0,overwrite=True)
fits.writeto(fn.replace('_data.fits','_data.mom0.psf.fits'),psf,overwrite=True)

data_m0_dc2, _ = restoration.unsupervised_wiener(mom0, psf,clip=False)
fits.writeto(fn.replace('_data.fits','_data.mom0.deconv2.fits'),data_m0_dc2,overwrite=True)

data_m0_dc3 = restoration.wiener(mom0, psf,1e-3,clip=False)
fits.writeto(fn.replace('_data.fits','_data.mom0.deconv3.fits'),data_m0_dc3,overwrite=True)