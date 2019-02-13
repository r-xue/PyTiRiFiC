from __future__ import print_function
from KinMS import KinMS
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
import scipy.constants as const
import time
from astropy.modeling.models import Sersic2D
from astropy.modeling.models import Gaussian2D

def makebeam(xpixels,ypixels,beam,pa=0.,cent=0):
    """

    beam=[bmaj,bmin] FWHM
    pa=east from north (ccw)
    
    make a "centered" Gaussian PSF kernel:
        e.g. npixel=7, centered at px=3
             npixel=8, centered at px=4
             so the single peak is always at a pixel center (not physical center)
             and the function is symmetric around that pixel
             the purpose of doing this is to avoid offset when the specified kernel size is
             even number and you build a function peaked at a pixel edge. 
             
        is x ks (peak pixel index)
        10 x 7(3) okay
        10 x 8(4) okay
        10 x 8(3.5) offset
        for convolve (non-fft), odd ks is required (the center pixel is undoubtely index=3)
                                even ks is not allowed
        for convolve_fft, you need to use cent=ks/2:
                                technically it's not the pixel index of image center
                                but the center pixel is "considers"as index=4
        the rule of thumb-up:
            cent=np.round((ks-1.)/2.)
        
        note:
            
            be careful about rounding:
                NumPy rounds to the nearest even value. Thus 1.5 and 2.5 round to 2.0, -0.5 and 0.5 round to 0.0,
                https://docs.scipy.org/doc/numpy/reference/generated/numpy.around.html
            
            "forget about how the np.array is stored, just use the array as it is IDL;
             when it comes down to shape/index, reverse the sequence"
            
    """
    
    if not cent: cent=[round((xpixels-1.)/2.)*1.,round((ypixels-1.)/2.)*1.]
    sigma2fwhm=np.sqrt(2.*np.log(2.))*2.
    mod=Gaussian2D(amplitude=1.,x_mean=cent[0],y_mean=cent[1],
               x_stddev=beam[1]/sigma2fwhm,y_stddev=beam[0]/sigma2fwhm,
               theta=np.deg2rad(pa))
    x,y=np.meshgrid(np.arange(xpixels),np.arange(ypixels))
    psf=mod(x,y)
    #print(psf.shape)
    #print(cent)
    return psf

def gmake_model_kinmspy(mod_dct,dat_dct={},
                      outname='',
                      decomp=False,
                      verbose=False):
    """
    handle modeling parameters to kinmspy and generate the model cubes embeded into 
    a dictionary nest
    
    """
    
    models={}
    
    for tag in mod_dct.keys():
        
        obj=mod_dct[tag]
        if  'method' not in obj.keys():
            continue
        elif 'kinmspy' not in obj['method'].lower():
            continue
        
        if  verbose==True:
            print("+"*40)
            print('@',tag)
            print("-"*40)
        
        #tic=time.time()
        if  'data@'+obj['image'] not in dat_dct:
            data,hd=fits.getdata(obj['image'],header=True,memmap=False)
        else:
            data=dat_dct['data@'+obj['image']]
            hd=dat_dct['header@'+obj['image']]
        if  'error@'+obj['image'] not in dat_dct:
            error=fits.getdata(obj['error'],memmap=False)
        else:
            error=dat_dct['error@'+obj['image']]
        if  'mask@'+obj['image'] not in dat_dct:
            mask=fits.getdata(obj['mask'],memmap=False)
        else:
            mask=dat_dct['mask@'+obj['image']]
        if  'sample@'+obj['image'] not in dat_dct:
            sample=fits.getdata(obj['sample'],memmap=False)
            sample=sample['sp_index']
        else:
            sample=dat_dct['sample@'+obj['image']]       
                                                           
        #print('Took {0} seconds to read FITS'.format(float(time.time()-tic)/float(1)))
        
        if  verbose==True:
            print(hd['NAXIS1'],hd['NAXIS2'],hd['NAXIS3'])
        
        psize=np.sqrt(np.abs(hd['CDELT1']*hd['CDELT2']))*3600.0         #   arcsec
        
        cdelt3=hd['CDELT3']     # hz or m/s
        crval3=hd['CRVAL3']     # hz or m/s
        crpix3=hd['CRPIX3']     # pix
        
        #   vector description of the z-axis: 
        #       vdelt3/vrval3/crpix3
        rfreq=obj['restfreq']/(1.0+obj['z'])                            #   GHz
        if  'Hz' in hd['CUNIT3']:   # by freq
            vdelt3=-const.c*cdelt3/(1.0e9*rfreq)/1000.                  #   km/s
            vrval3=const.c*((1.0e9*rfreq)-crval3)/(1.0e9*rfreq)/1000.0  #   km/s
        else:                       # by velo
            vdelt3=cdelt3/1000.0
            vrval3=crval3/1000.0
        
        if  verbose==True:
            print(psize,vdelt3,vrval3,crpix3)
        
        xs=psize*hd['NAXIS1']
        ys=psize*hd['NAXIS2']
        vs=abs(vdelt3)*hd['NAXIS3']
        cell=psize
        dv=abs(vdelt3)
        
        beamsize=[0.2,0.2,0.]
        
        if  'BMAJ' in hd.keys():
            beamsize[0]=hd['BMAJ']*3600.
        if  'BMIN' in hd.keys():
            beamsize[1]=hd['BMIN']*3600.
        if  'BPA' in hd.keys():
            beamsize[2]=hd['BPA']                        
        if  verbose==True:
            print('beamsize->',beamsize)
        
        inc=obj['inc']
        gassigma=np.array(obj['vdis'])
        
        sbrad=np.array(obj['radi'])
        
        sbprof=1.*np.exp(-sbrad/obj['sbexp'])
        
        velrad=obj['radi']
        velprof=obj['vrot']
        posang=obj['pa']
        intflux=obj['intflux']
        filename='test'
        
        xypos=obj['xypos']
        restfreq=115.271e9
        restfreq=obj['restfreq']
        
        vsys=obj['vsys']
        
        fsys=(1.0-vsys/(const.c/1000.0))*rfreq # line systematic frequency in the observer frame
        
        
        #   ra    ----      xi_data     ----    (xSize-1.)/2.+phasecen[0]/cell
        #   dec   ----      yi_data     ----    (ySize-1.)/2.+phasecen[1]/cell
        #   vsys  ----      vi_data     ----    (vSize-1.)/2.+voffset/dv
       
        #
        # collect the world coordinates of the disk center (ra,dec,freq/wave)
        # note: vsys is defined in the radio(freq)/optical(wave) convention, 
        #       within the rest frame set at obj['z']/
        #       the convention doesn't really matter, as long as vsys << c
        #
        w=WCS(hd)
        wx=xypos[0]
        wy=xypos[1]
        ws=1    # stokes
        wo=0    # 0-based or 1-based index
        if  'Hz' in hd['CUNIT3']:
            wz=obj['restfreq']*1e9/(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
            dv=-const.c*cdelt3/(1.0e9*obj['restfreq']/(1.0+obj['z']))/1000.
        if  'Angstrom' in hd['CUNIT3']:
            wz=obj['restwave']*(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
            dv=const.c*cdelt3/(obj['restwave']*(1.0+obj['z']))/1000.
        if  'm/s' in hd['CUNIT3']:
            wz=obj['vsys']/1000.
            dv=cdelt3/1000.        

        px,py,pz,ps=w.wcs_world2pix(wx,wy,wz,ws,wo)
        
        px_int=round(px)
        py_int=round(py)
        pz_int=round(pz)
        phasecen=np.array([px-px_int,py-py_int])*cell
        voffset=(pz-pz_int)*dv
        
        #print(phasecen,voffset)
        #print('<-->',tag,px_int,py_int,pz_int,ps)
        #print('hz:',int(xs/cell*0.5))
        phasecen=[0.,0.]
        
        
        
        xs=np.max(sbrad)*2.0*2.0
        ys=np.max(sbrad)*2.0*2.0
        vs=np.max(velprof)*1.5*2.0
        
        px_o=px_int-int(xs/cell*0.5)
        py_o=py_int-int(ys/cell*0.5)
        pz_o=pz_int-int(vs/abs(dv)*0.5)

        #tic=time.time()
        # cube needs to be transposed to match the fits.data dimension 
        cube=KinMS(xs,ys,vs,
                   cellSize=cell,dv=abs(dv),
                   beamSize=beamsize,cleanOut=False,
                   inc=inc,gasSigma=gassigma,sbProf=sbprof,
                   sbRad=sbrad,velRad=velrad,velProf=velprof,
                   #nSamps=nsamps,
                   ra=xypos[0],dec=xypos[1],
                   restFreq=restfreq,vSys=vsys,phaseCen=phasecen,vOffset=voffset,
                   #fileName=outname+'_'+tag,
                   posAng=posang,
                   intFlux=intflux)
        #print('Took {0} seconds to execute KinMSpy'.format(float(time.time()-tic)/float(1)))
        
        if  dv<0:
            cube=np.flip(cube,axis=2)
        
        model=data.T*0.0
        #print('shape:',model.shape)
        #print('shape:',cube.shape)
        #print('-->',px_int,py_int,pz_int)
        #print('-->',[px_o,py_o,pz_o])
        model=gmake_insertmodel(model,cube,offset=[px_o,py_o,pz_o])
        #fits.writeto(tag+'.fits',model.T,overwrite=True)
        if  decomp==True:
            models[tag+'@'+obj['image']]=model.T
        
        if  'model@'+obj['image'] in models.keys():
            models['model@'+obj['image']]+=model.T
        else:
            models['model@'+obj['image']]=model.T.copy()
            models['header@'+obj['image']]=hd
            models['data@'+obj['image']]=data
            models['error@'+obj['image']]=error     
            models['mask@'+obj['image']]=mask
            models['sample@'+obj['image']]=sample
            
    return models


def gmake_model_disk2d(header,ra,dec,
                       beam=None,psf=None,
                       r_eff=20.0,      # r_eff in arcsec
                       n=1.0,           # sersic index
                       intflux=1.,      # Jy
                       restfreq=100.0,  # GHz
                       alpha=3.0,       # alpha
                       posang=0.,       # degree
                       ellip=0.0,       # 
                       cleanout=False):
    """
        insert a continuum model into a 2D image or 3D cube
            ellip:     1-b/a
            posang:    in the astronomical convention
    """

    #   build objects
    #   use np.meshgrid and don't worry about transposing
    w=WCS(header).celestial
    cell=np.mean(proj_plane_pixel_scales(w))*3600.0
    pos=w.wcs_world2pix(np.array([[ra],[dec]]).T,0)
    px=pos[:,0]
    py=pos[:,1]
    x,y = np.meshgrid(np.arange(header['NAXIS1']), np.arange(header['NAXIS2']))
    mod = Sersic2D(amplitude=1.0,r_eff=r_eff/cell,n=n,x_0=px,y_0=py,
               ellip=ellip,theta=np.deg2rad(posang+90.0))
    model=mod(x,y)
    
    #   get Kernel normalized to 1 at PEAK
    #   priority: psf>beam>header
    if  psf is not None:
        kernel=np.squeeze(psf)
    elif beam is not None:
        if  not isinstance(beam, (list, tuple, np.ndarray)):
            gbeam = [beam,beam,0]
        else:
            gbeam = beam
        kernel=makebeam(header['NAXIS1'],header['NAXIS2'],
                        [gbeam[0]/cell,gbeam[1]/cell],pa=gbeam[2])
    else:
        kernel=makebeam(header['NAXIS1'],header['NAXIS2'],
                        [hd['BMAJ']*3600./cell,hd['BMIN']*3600./cell],pa=hd['BPA'])


    intflux_model=intflux*(header['CRVAL3']/1e9/restfreq)**alpha
    
    if  not cleanout:
        # end up with Jy/beam
        #print(model.shape,psf_beam.shape)
        model=convolve_fft(model,kernel)
        model *= ( intflux_model*kernel.sum()/model.sum() )
    else: 
        # end up with Jy/pix
        model *= ( intflux_model/model.sum() )

    return kernel
    
if  __name__=="__main__":

    """
    examples
    """
    pass
    #im=makebeam(29,21,[6.0,6.0],pa=0)
    #fits.writeto('makebeam_im.fits',im,overwrite=True)
    
    #psf=makebeam(15,15,[6.0,3.0],pa=20)
    #fits.writeto('makebeam_psf.fits',psf,overwrite=True)
#     psf1=makebeam(11,11,[3.0,3.0],pa=0,cent=0)
#     fits.writeto('makebeam_psf1.fits',psf1,overwrite=True)
#     psf2=makebeam(13,13,[3.0,3.0],pa=0,cent=0)
#     fits.writeto('makebeam_psf2.fits',psf2,overwrite=True)
    #cm=convolve_fft(im,psf)
    #fits.writeto('makebeam_convol.fits',cm,overwrite=True)