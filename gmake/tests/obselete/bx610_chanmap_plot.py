import numpy as np
import warnings
from spectral_cube.utils import SpectralCubeWarning
warnings.filterwarnings(action='ignore', category=SpectralCubeWarning,append=True)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore")
from spectral_cube import SpectralCube


import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use("Agg")
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"


def bx610_chanmap_plot():
    """
    plot dirty map mom0 from one plane for data / model 
    """
    
    datadir='bx610_uvb6_ab/p_fits/'
    
    chs=np.arange(12)*2+8
    
    data=SpectralCube.read(datadir+'data_b6_bb2.fits',mode='readonly')
    data_line=SpectralCube.read(datadir+'data_line_b6_bb2.fits',mode='readonly')
    #data_cont=SpectralCube.read(datadir+'data_cont_b6_bb2.fits',mode='readonly')
    
    imodel=SpectralCube.read(datadir+'imodel_b6_bb2.fits',mode='readonly')
    imod3d=SpectralCube.read(datadir+'imod3d_b6_bb2.fits',mode='readonly')
    imod2d=SpectralCube.read(datadir+'imod2d_b6_bb2.fits',mode='readonly')
    
    cmodel=SpectralCube.read(datadir+'cmodel_b6_bb2.fits',mode='readonly')
    cmod3d=SpectralCube.read(datadir+'cmod3d_b6_bb2.fits',mode='readonly')
    cmod2d=SpectralCube.read(datadir+'cmod2d_b6_bb2.fits',mode='readonly')    
    
    
    data_val=data.unmasked_data[:].value
    cmodel_val=cmodel.unmasked_data[:].value
    cmod3d_val=cmod3d.unmasked_data[:].value
    cmod2d_val=cmod2d.unmasked_data[:].value
    
    imodel_val=imodel.unmasked_data[:].value
    imod3d_val=imod3d.unmasked_data[:].value
    imod2d_val=imod2d.unmasked_data[:].value    
     
    fig=plt.figure(figsize=(1*6,1.*12))
    
    ncol=6
    for ich in range(len(chs)):
        ind=chs[ich]
        print(ind,ich)
        
        #ax=fig.add_subplot(12,7,7*ich+1)
        #ax.set_xlabel('$uv$ distance (k$\lambda$)')
        #ax.set_ylabel('Real [mJy]')
        
        #ax=fig.add_subplot(12,7,7*ich+2)
        #ax.set_xlabel('$uv$ distance (k$\lambda$)')
        #ax.set_ylabel('Image [mJy]')
        
        
        vmax=np.nanmax(data_val[:,48:80,48:80])
        vmin=np.nanmin(data_val[:,48:80,48:80])        
        
        ax=fig.add_subplot(12,ncol,ncol*ich+1)
        ax.imshow(data_val[ind,48:80,48:80],vmax=vmax,vmin=vmin)
        ax.plot([8,12],[16,16],color='white', alpha=0.8)
        ax.plot([16,16],[8,12],color='white', alpha=0.8)
        
        ax=fig.add_subplot(12,ncol,ncol*ich+2)
        ax.imshow(cmodel_val[ind,48:80,48:80],vmax=vmax,vmin=vmin)
        ax.plot([8,12],[16,16],color='white', alpha=0.8)
        ax.plot([16,16],[8,12],color='white', alpha=0.8)        
        
        ax=fig.add_subplot(12,ncol,ncol*ich+3)
        ax.imshow(data_val[ind,48:80,48:80]-cmodel_val[ind,48:80,48:80],vmax=vmax,vmin=vmin)
        ax.plot([8,12],[16,16],color='white', alpha=0.8)
        ax.plot([16,16],[8,12],color='white', alpha=0.8) 
        
        #ax=fig.add_subplot(12,7,7*ich+4)
        #ax.imshow(cmod2d_val[ind,48:80,48:80],vmax=0.004,vmin=-0.001)
        #ax.plot([8,12],[16,16],color='white', alpha=0.8)
        #ax.plot([16,16],[8,12],color='white', alpha=0.8)             
        vmax=np.nanmax(imodel_val[:,48:80,48:80])
        vmin=np.nanmin(imodel_val[:,48:80,48:80])
        
        ax=fig.add_subplot(12,ncol,ncol*ich+4)
        ax.imshow(imodel_val[ind,48:80,48:80],vmax=vmax,vmin=vmin)
        ax.plot([8,12],[16,16],color='white', alpha=0.8)
        ax.plot([16,16],[8,12],color='white', alpha=0.8)                        

        ax=fig.add_subplot(12,ncol,ncol*ich+5)
        ax.imshow(imod3d_val[ind,48:80,48:80],vmax=vmax,vmin=vmin)
        ax.plot([8,12],[16,16],color='white', alpha=0.8)
        ax.plot([16,16],[8,12],color='white', alpha=0.8)  
        
        ax=fig.add_subplot(12,ncol,ncol*ich+6)
        ax.imshow(imod2d_val[ind,48:80,48:80],vmax=vmax,vmin=vmin)
        ax.plot([8,12],[16,16],color='white', alpha=0.8)
        ax.plot([16,16],[8,12],color='white', alpha=0.8)          


    fig.subplots_adjust(left=0.07,bottom=0.07,right=0.98,top=0.95)
    #fig.tight_layout()
    fig.savefig('bx610_chanmap.pdf')
    plt.close()

if  __name__=="__main__":
    
    bx610_chanmap_plot()