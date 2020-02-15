#execfile('/Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake/gmake_init.py')
#execfile('/Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake/msplot.py')

#from gmake import msplot
from gmake import *
logger_config(logfile='gmake_test.log')


"""
msname='bx610_uvb6_ab/p_fits/data_b6_bb2.ms'

ind=20
t=ctb.table(msname)
#vis_data=t.getcol('DATA')
vis_data=t.getcol('DATA')
vis_model=t.getcol('CORRECTED_DATA')
print(vis_data.shape)
vis_data=vis_data[:,ind,:]
vis_model=vis_model[:,ind,:]
print(vis_data.shape)


uvw=t.getcol('UVW')
weight=t.getcol('WEIGHT')

ts=ctb.table(msname+'/SPECTRAL_WINDOW')
chan_freq=ts.getcol('CHAN_FREQ')
print(chan_freq)
chan_freq=chan_freq[0][ind]
print(chan_freq)
chan_wave=const.c/chan_freq

uvw_wv=uvw/chan_wave



uvdist=np.sqrt(uvw_wv[:,0]**2+uvw_wv[:,1]**2)

#msplot2.uvamp_average(uvdist/1e3,vis_data[:,0]*1e3,plot=True)

#msplot2.uvamp(uvdist/1e3,vis_data[:,0]*1e3,vis_model[:,0]*1e3)
"""


uvw_kl,uvdata=ms_utils.ms_read('bx610_band6_uv_ab/p_fits/data_b6_bb2.ms',datacolumn='data')
uvw_kl,uvmodel=ms_utils.ms_read('bx610_band6_uv_ab/p_fits/data_b6_bb2.ms',datacolumn='corrected')

print("---")
print(uvw_kl.shape) #(515942, 79, 3)
print(uvdata.shape) #(515942, 79, 2)



"""
for i in range(nchan):
    for j in range(ncorr):
        uvdata[:,i,j]=apply_phase_vis(-0.03/3600*np.pi/180,-0.03/3600*np.pi/180,
                                      (uvw_kl[:,i,0].astype(np.float32))*1e3,(uvw_kl[:,i,1].astype(np.float32))*1e3,np.ascontiguousarray(uvdata[:,i,j])
"""

nrecord=uvw_kl.shape[0]
ncorr=uvdata.shape[2]
print(nrecord)
print(ncorr)
chs=np.arange(12)*2+8
chs=[8,18]
chs=[18]


figname='bx610_uvamp_plot.png'
nch=len(chs)
ncol=2

plt.clf()
fig=plt.figure(figsize=(4.5*ncol,3.*nch))

for ich in range(len(chs)):
    
    ind=chs[ich]
    print(ind,ich)

    ax = fig.add_subplot(nch,ncol,ncol*ich+1)
    
    uvdist_select=np.sqrt(uvw_kl[:,ind,0]**2+uvw_kl[:,ind,1]**2)
    uvdist_select=np.broadcast_to(uvdist_select[:,np.newaxis],(nrecord,ncorr))
    uvdata_select=uvmodel[:,ind,:]

    bins=20
    count, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),uvdata_select.flatten(), statistic='count', bins=bins)
    dist=(bin_edges[:-1]+bin_edges[1:])/2.0
    real, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.real(uvdata_select.flatten()), statistic='mean', bins=bins)
    imag, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.imag(uvdata_select.flatten()), statistic='mean', bins=bins)
    ap=np.sqrt(real**2+imag**2)
    ph=np.angle(real+imag*1j,deg=True)
    print(count)
    
    real_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.real(uvdata_select.flatten()), statistic=stats.tstd, bins=bins)
    imag_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.imag(uvdata_select.flatten()), statistic=stats.tstd, bins=bins)
    real_std=real_std/np.sqrt(count/2.0)
    imag_std=imag_std/np.sqrt(count/2.0)
    
    ph_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.angle(uvdata_select.flatten(),deg=False), statistic=stats.circstd, bins=bins)
    
    ph_std=ph_std*np.rad2deg(1.)
    print(ph_std)
    
    ph_std=np.array([])
    ph_el=np.array([])
    ph_eu=np.array([])
    ph_mean=np.array([])
    ph_median=np.array([])
    for ind in range(real_std.size):
        ph_samp=np.arctan2(np.random.normal(imag[ind],imag_std[ind],size=1024),
                           np.random.normal(real[ind],real_std[ind],size=1024))
        ph_samp=ph_samp*np.rad2deg(1.0)
        ph_mean=np.append(ph_mean,np.mean(ph_samp))
        ph_std=np.append(ph_std,np.std(ph_samp))
        ph_pc=np.percentile(ph_samp,[34.1,50.0,100-34.1])
        ph_el=np.append(ph_el,np.abs(ph_pc[0]-ph_mean[-1]))
        ph_eu=np.append(ph_eu,np.abs(ph_pc[2]-ph_mean[-1]))
        ph_median=np.append(ph_median,ph_pc[1])
        print(ind,ph_pc)

    ax.plot(uvdist_select.flat,np.absolute(uvdata_select.flat)*1e3,color='g',marker='o',linestyle='none')
    ax.plot(dist,ap*1e3,color='r',marker='o',linestyle='none')
    
    
    
    
    uvdist_select=np.sqrt(uvw_kl[:,ind,0]**2+uvw_kl[:,ind,1]**2)
    uvdist_select=np.broadcast_to(uvdist_select[:,np.newaxis],(nrecord,ncorr))
    uvdata_select=uvdata[:,ind,:]

    bins=20
    count, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),uvdata_select.flatten(), statistic='count', bins=bins)
    dist=(bin_edges[:-1]+bin_edges[1:])/2.0
    real, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.real(uvdata_select.flatten()), statistic='mean', bins=bins)
    imag, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.imag(uvdata_select.flatten()), statistic='mean', bins=bins)
    ap=np.sqrt(real**2+imag**2)
    ph=np.angle(real+imag*1j,deg=True)
    print(count)
    
    real_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.real(uvdata_select.flatten()), statistic=stats.tstd, bins=bins)
    imag_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.imag(uvdata_select.flatten()), statistic=stats.tstd, bins=bins)
    real_std=real_std/np.sqrt(count/2.0)
    imag_std=imag_std/np.sqrt(count/2.0)
    
    ph_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.angle(uvdata_select.flatten(),deg=False), statistic=stats.circstd, bins=bins)
    
    ph_std=ph_std*np.rad2deg(1.)
    print(ph_std)
    
    ph_std=np.array([])
    ph_el=np.array([])
    ph_eu=np.array([])
    ph_mean=np.array([])
    ph_median=np.array([])
    for ind in range(real_std.size):
        ph_samp=np.arctan2(np.random.normal(imag[ind],imag_std[ind],size=1024),
                           np.random.normal(real[ind],real_std[ind],size=1024))
        ph_samp=ph_samp*np.rad2deg(1.0)
        ph_mean=np.append(ph_mean,np.mean(ph_samp))
        ph_std=np.append(ph_std,np.std(ph_samp))
        ph_pc=np.percentile(ph_samp,[34.1,50.0,100-34.1])
        ph_el=np.append(ph_el,np.abs(ph_pc[0]-ph_mean[-1]))
        ph_eu=np.append(ph_eu,np.abs(ph_pc[2]-ph_mean[-1]))
        ph_median=np.append(ph_median,ph_pc[1])
        print(ind,ph_pc)

    #ax.plot(uvdist_select.flat,np.absolute(uvdata_select.flat)*1e3,color='g',marker='o',linestyle='none')
    ax.plot(dist,ap*1e3,color='b',marker='o',linestyle='none')    
    
    
    ax.set_ylim(bottom=0.0)
    ax.set_ylim(0,8)
    amp_lim=ax.get_ylim()   
    
    
     
    #ax.errorbar(dist,real*1e3,real_std*1e3,color='r',marker='o',linestyle='none')
    
    
    
    
    
    if  ich==len(chs)-1:
        ax.set_xlabel('$uv$ distance (k$\lambda$)')
        ax.set_ylabel('Amp [mJy]')
    
    
    
    
    ax = fig.add_subplot(nch,ncol,ncol*ich+2)
    
    uvdist_select=np.sqrt(uvw_kl[:,ind,0]**2+uvw_kl[:,ind,1]**2)
    uvdist_select=np.broadcast_to(uvdist_select[:,np.newaxis],(nrecord,ncorr))
    uvdata_select=uvdata[:,ind,:]-uvmodel[:,ind,:]

    bins=20
    count, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),uvdata_select.flatten(), statistic='count', bins=bins)
    dist=(bin_edges[:-1]+bin_edges[1:])/2.0
    real, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.real(uvdata_select.flatten()), statistic='mean', bins=bins)
    imag, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.imag(uvdata_select.flatten()), statistic='mean', bins=bins)
    ap=np.sqrt(real**2+imag**2)
    ph=np.angle(real+imag*1j,deg=True)
    print(count)
    
    real_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.real(uvdata_select.flatten()), statistic=stats.tstd, bins=bins)
    imag_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.imag(uvdata_select.flatten()), statistic=stats.tstd, bins=bins)
    real_std=real_std/np.sqrt(count/2.0)
    imag_std=imag_std/np.sqrt(count/2.0)
    
    ph_std, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.angle(uvdata_select.flatten(),deg=False), statistic=stats.circstd, bins=bins)
    
    ph_std=ph_std*np.rad2deg(1.)
    print(ph_std)
    
    ph_std=np.array([])
    ph_el=np.array([])
    ph_eu=np.array([])
    ph_mean=np.array([])
    ph_median=np.array([])
    for ind in range(real_std.size):
        ph_samp=np.arctan2(np.random.normal(imag[ind],imag_std[ind],size=1024),
                           np.random.normal(real[ind],real_std[ind],size=1024))
        ph_samp=ph_samp*np.rad2deg(1.0)
        ph_mean=np.append(ph_mean,np.mean(ph_samp))
        ph_std=np.append(ph_std,np.std(ph_samp))
        ph_pc=np.percentile(ph_samp,[34.1,50.0,100-34.1])
        ph_el=np.append(ph_el,np.abs(ph_pc[0]-ph_mean[-1]))
        ph_eu=np.append(ph_eu,np.abs(ph_pc[2]-ph_mean[-1]))
        ph_median=np.append(ph_median,ph_pc[1])
        print(ind,ph_pc)

    #ax.plot(uvdist_select.flat,np.absolute(uvdata_select.flat)*1e3,color='g',marker='o',linestyle='none')
    ax.plot(dist,ap*1e3*np.cos(np.deg2rad(ph)),color='r',marker='o',linestyle='none')
    ax.set_ylabel('Real [mJy]')
    ax.axhline(0.0,color='gray',lw=0.8,ls='--')
    ax.set_ylim(bottom=0.0)
    ax.set_ylim(-2,2)
    #amp_lim=ax.get_ylim()       
    
    """

    ax1 = fig.add_subplot(nch,ncol,ncol*ich+2)
    ax1.plot(uvdist_select.flat,np.angle(uvdata_select.flat,deg=True),color='g',marker='o',linestyle='none')
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--')
    ax1.set_ylim(-180,180)
    if  ich==len(chs)-1:
        ax1.set_xlabel('$uv$ distance (k$\lambda$)')
        ax1.set_ylabel('Phase [deg]')    
    
    ax1 = fig.add_subplot(nch,ncol,ncol*ich+3)
    ax1.plot(uvdist_select.flat,np.real(uvdata_select.flat)*1e3,color='g',marker='o',linestyle='none')
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--')
    ax1.set_ylim(-amp_lim[1],amp_lim[1])
    ax1.set_ylim(-2,8)
    if  ich==len(chs)-1:
        ax1.set_xlabel('$uv$ distance (k$\lambda$)')
        ax1.set_ylabel('Real [mJy]')    
    
    ax1 = fig.add_subplot(nch,ncol,ncol*ich+4)
    ax1.plot(uvdist_select.flat,np.imag(uvdata_select.flat)*1e3,color='g',marker='o',linestyle='none')
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--')
    ax1.set_ylim(-amp_lim[1],amp_lim[1])
    ax1.set_ylim(-2,2)
    if  ich==len(chs)-1:
        ax1.set_xlabel('$uv$ distance (k$\lambda$)')
        ax1.set_ylabel('Imag [mJy]')    
    
    uvdata_select=uvdata[:,ind,:]
    
    
    bins=20
    count, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),uvdata_select.flatten(), statistic='count', bins=bins)
    dist=(bin_edges[:-1]+bin_edges[1:])/2.0
    real, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.real(uvdata_select.flatten()), statistic='mean', bins=bins)
    imag, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.imag(uvdata_select.flatten()), statistic='mean', bins=bins)
    ap=np.sqrt(real**2+imag**2)
    ph=np.angle(real+imag*1j,deg=True)
    print(count)    
    
    ax1 = fig.add_subplot(nch,ncol,ncol*ich+5)
    ax1.plot(uvdist_select.flat,np.absolute(uvdata_select.flat)*1e3,color='g',marker='o',linestyle='none')
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--')
    ax1.plot(dist,ap*1e3,color='k',marker='o',linestyle='none')
    ax1.set_ylim(-amp_lim[1],amp_lim[1])
    ax1.set_ylim(0,6)
    if  ich==len(chs)-1:
        ax1.set_xlabel('$uv$ distance (k$\lambda$)')
        ax1.set_ylabel('Imag [mJy]')    


    uvdata_select=uvdata[:,ind,:]-uvmodel[:,ind,:]
    
    
    bins=20
    count, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),uvdata_select.flatten(), statistic='count', bins=bins)
    dist=(bin_edges[:-1]+bin_edges[1:])/2.0
    real, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.real(uvdata_select.flatten()), statistic='mean', bins=bins)
    imag, bin_edges, binnumber = stats.binned_statistic(uvdist_select.flatten(),np.imag(uvdata_select.flatten()), statistic='mean', bins=bins)
    ap=np.sqrt(real**2+imag**2)
    ph=np.angle(real+imag*1j,deg=True)
    print(count)    
    
    ax1 = fig.add_subplot(nch,ncol,ncol*ich+6)
    ax1.plot(uvdist_select.flat,np.absolute(uvdata_select.flat)*1e3,color='g',marker='o',linestyle='none')
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--')
    ax1.plot(dist,ap*1e3,color='k',marker='o',linestyle='none')
    ax1.set_ylim(-amp_lim[1],amp_lim[1])
    ax1.set_ylim(0,6)
    if  ich==len(chs)-1:
        ax1.set_xlabel('$uv$ distance (k$\lambda$)')
        ax1.set_ylabel('Imag [mJy]')           

    #ax1.plot(uvdist_kl.flat,np.real(uvdata.flat)*1e3,color='g',marker='o',linestyle='none')

    #ax1.errorbar(dist,real,real_std,color='g',marker='o',linestyle='none')
    #ax1.set_ylim(ymin,ymax)
    
    
    #ax1 = fig.add_subplot(ny,nx,2)
    #ax1.plot(dist,imag,color='g',marker='o',linestyle='none')
    #ax1.errorbar(dist,imag,imag_std,color='g',marker='o',linestyle='none')
    #ax1.set_ylim(ymin,ymax)
    #ax1.axhline(0.0,color='gray',lw=0.8,ls='--')    
    
    #ax1 = fig.add_subplot(ny,nx,3)
    #ax1.plot(dist,ap,color='g',marker='o',linestyle='none')
    #ax1.errorbar(dist,,imag_std,color='g',marker='o',linestyle='none')
    #ax1.set_ylim(ymin,ymax)
    #ax1.axhline(0.0,color='gray',lw=0.8,ls='--') 
    
    #ax1 = fig.add_subplot(ny,nx,4)
    #ax1.plot(dist,ph,color='g',marker='o',linestyle='none')
    #ax1.errorbar(dist,ph_median,np.array([ph_el,ph_eu]),color='g',marker='o',linestyle='none')
    #ax1.set_ylim(-180,180)
    #ax1.axhline(0.0,color='gray',lw=0.8,ls='--') 
    
    
    """
    
plt.tight_layout()
fig.savefig(figname)
plt.close()       





















#msplot.uvamp('bx610_uvb6_ab/p_fits/data_b6_bb1.ms',
#             datacolumn='corrected',
#             figname='bx610_uvamp_plot.png')

"""
plt.clf()
fig=plt.figure(figsize=(10,12))
nx=1
ny=1 
ax1 = fig.add_subplot(ny,nx,1)
ax1.plot(uvw_wv[:,0],uvw_wv[:,1],color='g',marker='o',linestyle='none')
figname='gmake_uvamp_plot.png'
fig.savefig(figname)
plt.close()
""" 