from .gmake_init import *

def uvamp(uvdist,
                uvdata,
                uvmodel,
                figname='gmake_uvamp.png'):
    """
    mimicking the old-fashion miriad/uvamp
        uvdist:        np.array    klambda
        uvdata:        np.array    Jy
        uvmodel:       np.array    Jy
    """
    

    ymin=-0.0005*1e3
    ymax=+0.0100*1e3

    plt.clf()
    fig=plt.figure(figsize=(10,8))
    nx=2
    ny=2 

    x=uvdist

    ax2 = fig.add_subplot(ny,nx,1)
    y=np.real(uvdata)
    #ax2.plot(x,y,marker='.',linestyle='none')
    bin_std, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='std', bins=20)
    bin_count, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='count', bins=20)
    bin_std=bin_std/np.sqrt(bin_count)
    bin_means, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='mean', bins=20)
    ax2.plot(bin_edges[:-1],bin_means,color='g',marker='o',linestyle='none')
    ax2.errorbar(bin_edges[:-1],bin_means,bin_std,color='g',marker='o',linestyle='none')
    x_real=bin_edges[:-1].copy()
    y_real=bin_means.copy()
    ye_real=bin_std.copy()
    ax2.set_xlabel('$uv$ distance (k$\lambda$)')
    ax2.set_ylabel('Real [mJy]')
    ax2.set_ylim(ymin,ymax)
    ax2.set_title('Data-BX610 \n (Caled. Vis.) ')
    
    ax4 = fig.add_subplot(ny,nx,3)
    y=np.imag(uvdata)
    #ax2.plot(x,y,marker='.',linestyle='none')
    bin_std, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='std', bins=20)
    bin_count, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='count', bins=20)
    bin_std=bin_std/np.sqrt(bin_count)
    bin_means, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='mean', bins=20)
    ax4.plot(bin_edges[:-1],bin_means,color='g',marker='o',linestyle='none')
    ax4.errorbar(bin_edges[:-1],bin_means,bin_std,color='g',marker='o',linestyle='none')
    x_imag=bin_edges[:-1].copy()
    y_imag=bin_means.copy()
    ye_imag=bin_std.copy()
    ax4.set_xlabel('$uv$ distance (k$\lambda$)')
    ax4.set_ylabel('Image [mJy]')
    ax4.set_ylim(ymin,ymax)
    
    ax1 = fig.add_subplot(ny,nx,2)

    y=np.real(uvmodel)
    ax1.plot(x,y,marker='.',linestyle='none',markersize=0.02,color='gray')
    bin_std, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='std', bins=20)
    bin_count, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='count', bins=20)
    bin_std=bin_std/np.sqrt(bin_count)
    bin_means, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='mean', bins=20)
    ax1.plot(bin_edges[:-1],bin_means,color='black',marker='o',linestyle='none')
    ax1.errorbar(bin_edges[:-1],bin_means,bin_std,color='black',marker='o',linestyle='none')
    ax1.errorbar(x_real,y_real,ye_real,color='g',marker='o',linestyle='none',fillstyle='none')
    
    ax1.set_xlabel('$uv$ distance [k$\lambda$]')
    ax1.set_ylabel('Real [mJy]')
    ax1.set_ylim(ymin,ymax)
    ax1.set_title('Model-BX610 \n (Vis. predicted from the image fit)')
    
    ax3 = fig.add_subplot(ny,nx,4)
    y=np.imag(uvmodel)
    ax3.plot(x,y,marker='.',linestyle='none',markersize=0.02,color='gray')
    bin_std, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='std', bins=20)
    bin_count, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='count', bins=20)
    bin_std=bin_std/np.sqrt(bin_count)
    bin_means, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='mean', bins=20)
    ax3.plot(bin_edges[:-1],bin_means,color='black',marker='o',linestyle='none')
    ax3.errorbar(bin_edges[:-1],bin_means,bin_std,color='black',marker='o',linestyle='none')    
    ax3.errorbar(x_imag,y_imag,ye_imag,color='g',marker='o',linestyle='none',fillstyle='none')
    ax3.set_xlabel('$uv$ distance (k$\lambda$)')
    ax3.set_ylabel('Image [mJy]')
    ax3.set_ylim(ymin,ymax)    

    fig.savefig(figname)
    plt.close() 


def uvamp_average(uvdist,uvdata,bins=20,plot=False):
    """
    vector vs. scalar:
        http://www.atnf.csiro.au/computing/software/miriad/doc/userguide/node69.html
        do not use scalar averging for low SNR data (postively biased due to noise, typical here)
        uvdist: 1d numpy.array (float)
        uvdata: 1d numpy.array (complex)
        
    """
    count, bin_edges, binnumber = stats.binned_statistic(uvdist,uvdata, statistic='count', bins=bins)
    dist=(bin_edges[:-1]+bin_edges[1:])/2.0
    real, bin_edges, binnumber = stats.binned_statistic(uvdist,np.real(uvdata), statistic='mean', bins=bins)
    imag, bin_edges, binnumber = stats.binned_statistic(uvdist,np.imag(uvdata), statistic='mean', bins=bins)
    ap=np.sqrt(real**2+imag**2)
    ph=np.angle(real+imag*1j,deg=True)
    print(count)
    
    real_std, bin_edges, binnumber = stats.binned_statistic(uvdist,np.real(uvdata), statistic=stats.tstd, bins=bins)
    imag_std, bin_edges, binnumber = stats.binned_statistic(uvdist,np.imag(uvdata), statistic=stats.tstd, bins=bins)
    real_std=real_std/np.sqrt(count/2.0)
    imag_std=imag_std/np.sqrt(count/2.0)
    
    ph_std, bin_edges, binnumber = stats.binned_statistic(uvdist,np.angle(uvdata,deg=False), statistic=stats.circstd, bins=bins)
    
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
    
    ymin=-0.0015*1e3
    ymax=+0.0135*1e3
    
    plt.clf()
    fig=plt.figure(figsize=(10,12))
    nx=2
    ny=3 
    
    x=dist
    y=real
    ye=real_std
    
    ax1 = fig.add_subplot(ny,nx,1)
    ax1.plot(dist,real,color='g',marker='o',linestyle='none')
    ax1.errorbar(dist,real,real_std,color='g',marker='o',linestyle='none')
    ax1.set_ylim(ymin,ymax)
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--')
    
    ax1 = fig.add_subplot(ny,nx,2)
    ax1.plot(dist,imag,color='g',marker='o',linestyle='none')
    ax1.errorbar(dist,imag,imag_std,color='g',marker='o',linestyle='none')
    ax1.set_ylim(ymin,ymax)
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--')    
    
    ax1 = fig.add_subplot(ny,nx,3)
    ax1.plot(dist,ap,color='g',marker='o',linestyle='none')
    #ax1.errorbar(dist,,imag_std,color='g',marker='o',linestyle='none')
    ax1.set_ylim(ymin,ymax)
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--') 
    
    
    
    
    ax1 = fig.add_subplot(ny,nx,4)
    #ax1.plot(dist,ph,color='g',marker='o',linestyle='none')
    ax1.errorbar(dist,ph_median,np.array([ph_el,ph_eu]),color='g',marker='o',linestyle='none')
    ax1.set_ylim(-180,180)
    ax1.axhline(0.0,color='gray',lw=0.8,ls='--')              
    
#     ax1.set_xlabel('$uv$ distance (k$\lambda$)')
#     ax1.set_ylabel('Real [mJy]')
#     ax1.set_ylim(ymin,ymax)
#     ax1.set_title('Data-BX610 \n (Caled. Vis.) ')
#     
#     y=np.imag(uvdata)
#     ax1 = fig.add_subplot(ny,nx,2)
#     #ax1.plot(x,y,marker='.',linestyle='none')
#     bin_std, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='std', bins=20)
#     bin_count, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='count', bins=20)
#     bin_std=bin_std/np.sqrt(bin_count)
#     bin_means, bin_edges, binnumber = stats.binned_statistic(x,y, statistic='mean', bins=20)
#     ax1.plot(bin_edges[:-1],bin_means,color='g',marker='o',linestyle='none')
#     ax1.errorbar(bin_edges[:-1],bin_means,bin_std,color='g',marker='o',linestyle='none')
#     x_real=bin_edges[:-1].copy()
#     y_real=bin_means.copy()
#     ye_real=bin_std.copy()
#     ax1.set_xlabel('$uv$ distance (k$\lambda$)')
#     ax1.set_ylabel('Real [mJy]')
#     ax1.set_ylim(ymin,ymax)
#     ax1.set_title('Data-BX610 \n (Caled. Vis.) ')    
#     
#     fig.savefig(figname)
#     plt.close() 
#     
#     
#     y=uvdata
#     ax1 = fig.add_subplot(ny,nx,3)
#     ym_real, bin_edges, binnumber = stats.binned_statistic(x,np.real(uvdata), statistic='mean', bins=20)
#     ym_imag, bin_edges, binnumber = stats.binned_statistic(x,np.imag(uvdata), statistic='mean', bins=20)
#     ax1.plot(bin_edges[:-1],np.abs(ym_real**2+ym_imag**2),color='g',marker='o',linestyle='none')
# 
#     ax1.set_xlabel('$uv$ distance (k$\lambda$)')
#     ax1.set_ylabel('Vec (ave) [mJy]')
#     ax1.set_ylim(ymin,ymax)
#     ax1.set_title('Data-BX610 \n (Caled. Vis.) ')    
#     
#     
#     
#     ym_phase=
#     ax1 = fig.add_subplot(ny,nx,4)
#     ax1.plot(bin_edges[:-1],ym_phase,color='g',marker='o',linestyle='none')
#     
#     """
#     ym_abs, bin_edges, binnumber = stats.binned_statistic(x,np.abs(uvdata), statistic='mean', bins=20)
#     ax1 = fig.add_subplot(ny,nx,5)
#     ax1.plot(x,np.abs(uvdata))
#     ax1.plot(bin_edges[:-1],ym_abs,color='g',marker='o',linestyle='none')
    #"""
    figname='gmake_uvamp_average.png'
    fig.savefig(figname)
    plt.close() 
    
    return
  

if  __name__=="__main__":

    pass