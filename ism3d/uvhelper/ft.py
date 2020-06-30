
import finufftpy  as nufft
import astropy.units as u
import numpy as np

def invert_ft(uu,vv,wv,vis,cell,imsize,wt=None,bychannel=True):
    """
    use nufft to create dirty cube from visibility
    uu: in meter (vector, nrecord
    vv: in meter (vector, nrecord)
    wv: in meter (vector, nchannel)
    psize: Quality
    wt:         apply wt when doing invert (essentialy nature weighting)
                only works when bychannle=true
    bychannel:  False ignore the wavelength changing effect on uvw
                True: uu/vv will be calculated channel by channel
                
    output (nx,ny,nz)
    """
    
    if  bychannel==False:
        uuu=-uu/np.mean(wv)*2*np.pi*(cell.to(u.rad).value)
        vvv=vv/np.mean(wv)*2*np.pi*(cell.to(u.rad).value)
        cube=np.zeros((imsize,imsize,len(wv)),dtype=np.complex128,order='F')
        nufft.nufft2d1many(uuu,vvv,vis,
                           -1,1e-15,imsize,imsize,cube,debug=1)
        cube/=uu.shape[0]         
    else:
        cube=np.zeros((imsize,imsize,len(wv)),dtype=np.complex128,order='F')
        
        #im0=np.zeros((imsize,imsize),dtype=np.complex128,order='F')
        for i in range(len(wv)):
            uuu=-uu/wv[i]*2*np.pi*(cell.to(u.rad).value)
            vvv=vv/wv[i]*2*np.pi*(cell.to(u.rad).value)
            if  wt is None:
                nufft.nufft2d1(uuu,vvv,vis[:,i],
                            -1,1e-15,imsize,imsize,cube[:,:,i],debug=0)
            else:
                nufft.nufft2d1(uuu,vvv,vis[:,i]*wt,
                            -1,1e-15,imsize,imsize,cube[:,:,i],debug=0)                
        #cube[:,:,i]=im0
        if  wt is None:
            cube/=uu.shape[0]
        else:
            cube/=np.sum(wt)
    
    return cube.real

def make_psf(uu,vv,wv,cell,imsize,wt=None,bychannel=True):
    
    vis=np.ones((uu.shape[0],len(wv)),dtype=np.complex128,order='F')
    cube=invert_ft(uu,vv,wv,vis,cell,imsize,wt=wt,bychannel=bychannel)

    return cube