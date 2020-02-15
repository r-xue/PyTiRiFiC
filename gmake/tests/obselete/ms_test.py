
"""
from pyuvdata import UVData
import shutil
import os


repo='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/bx610/ms/'
UV=UVData()
ms_file=repo+'bb4.ms'
UV.read(ms_file)
print(UV.get_ants())

data=UV.get_data(0,1)
times = UV.get_times(0,1)
print(times.shape)
print(data.shape)


import numpy as np
import matplotlib.pyplot as plt

plt.clf()

fig=plt.figure(figsize=(12,8))
nx=2
ny=1 
ax1 = fig.add_subplot(ny,nx,1)
ax1.imshow(np.abs(UV.get_data((1,3, UV.polarization_array[0])))) 


bl = UV.antnums_to_baseline(1, 3)
bl_ind = np.where(UV.baseline_array == bl)[0]
ax2 = fig.add_subplot(ny,nx,2)
ax2.imshow(np.abs(UV.data_array[bl_ind, 0, :, 0]))

fig.tight_layout()


fig.savefig('test.pdf')


# record ? chan pol
print(UV.data_array.shape)

# tiem stamps
print(UV.Ntimes)

# freq number
print(UV.Nfreqs)
"""


execfile('gmake_init.py')


msname='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/bx610/alma/band6/bx610_band6.bb1.mfs.ms'
imname='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/bx610/models/xyb46dm128rc_ab/p_fits/imodel_b6_bb1.fits'

t=ctb.table(msname)
vis_data=t.getcol('DATA')
vis_data=vis_data[:,0,:]
print(vis_data.shape)
uvw=t.getcol('UVW')
weight=t.getcol('WEIGHT')

ts=ctb.table(msname+'/SPECTRAL_WINDOW')
chan_freq=ts.getcol('CHAN_FREQ')
chan_wave=const.c.value/chan_freq
#print(chan_wave)

uvw_wv=uvw/chan_wave
#print(uvw_wv.shape)


nxy, dxy = get_image_size(uvw_wv[:,0], uvw_wv[:,1], verbose=True)
#print(nxy,dxy)


imodel,header=fits.getdata(imname,header=True)
w=WCS(header)

#imodel=np.squeeze(imodel)
imodel=imodel[0,0,:,:].astype('float64')
#print(imodel.flags)
#print(type(imodel[0,0]))
dxy=np.deg2rad(np.mean(proj_plane_pixel_scales(w.celestial)))
#print(dxy)


sz=imodel.shape
wxy=w.celestial.wcs_pix2world(sz[1]/2,sz[0]/2,0)
print(wxy)

tf=ctb.table(msname+'/FIELD') 
phase_dir=tf.getcol('PHASE_DIR')
phase_dir=phase_dir[-1][0]
phase_dir=np.rad2deg(phase_dir)
phase_dir[0]+=360.0
print(phase_dir) 

dra=+(wxy[0]-phase_dir[0])
ddec=+(wxy[1]-phase_dir[1])

#dra=0
#ddec=0
print(dra*3600.0,ddec*3600.0)

#imodel=np.require(imodel.copy(),requirements='C')
#print(imodel.flags)


#imodel.copy(order='C') #byteswap().newbyteorder()
#print(np.zeros((100,100)))


#imodel=np.require(np.zeros((100,100)),requirements='C')
#print(imodel.flags)
#print(type(imodel[0,0]))

#print(uvw_wv[:,0].copy(order='C').flags)

#imodel needs to be <class 'numpy.float64'> and C-contigous

dRA=np.deg2rad(dra)
dDec=np.deg2rad(ddec)

# plotting  phase is bad


#imodel_pad=np.zeros((512,512))
#imodel_pad[(256-64):(256+64),(256-64):(256+64)]=imodel.copy()
#imodel=imodel_pad.copy()

vis_model = sampleImage(imodel, dxy, 
                  uvw_wv[:,0].copy(order='C'), 
                  uvw_wv[:,1].copy(order='C'), dRA=dRA, dDec=dDec, PA=0, check=False)

vis_model=np.repeat(vis_model[:, np.newaxis], 2, axis=1)


tmp=np.abs(vis_model[:,0]-vis_data[:,0])
chi2=np.sum(tmp**2*weight[:,0])

chi2=chi2Image(imodel,dxy,
          uvw_wv[:,0].copy(order='C'), 
          uvw_wv[:,1].copy(order='C'), 
          np.real(vis_data[:,0].astype('float64')).copy(order='C'),
          np.imag(vis_data[:,0].astype('float64')).copy(order='C'),
          weight[:,0].astype('float64').copy(order='C'),
          dRA=dRA, dDec=dDec, PA=0, check=False)


uvdist=np.sqrt(uvw_wv[:,0]**2+uvw_wv[:,1]**2)
#gmake_uvamp(uvdist/1e3,vis_data[:,0]*1e3,vis_model[:,0]*1e3)
gmake_uvamp_average(uvdist/1e3,vis_data[:,0]*1e3,plot=True)



plt.clf()
fig=plt.figure(figsize=(10,12))
nx=1
ny=1 
ax1 = fig.add_subplot(ny,nx,1)
ax1.plot(uvw_wv[:,0],uvw_wv[:,1],color='g',marker='o',linestyle='none')
figname='gmake_uvamp_plot.png'
fig.savefig(figname)
plt.close() 
    
