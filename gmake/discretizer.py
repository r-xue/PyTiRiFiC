import numpy as np
from .model import clouds_discretize_2d

import astropy.units as u
from astropy.wcs import WCS
from astropy import constants as const
from astropy.cosmology import Planck13
from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
from astropy.io import fits 
from astropy.coordinates import SkyCoord
import numexpr as ne
from galario.single import sampleImage
from astropy.convolution import convolve_fft
import pyfftw
from scipy.sparse import csr_matrix

def pix2sky(obj,header,px=None,py=None,pz=None):
    """
    convert pixel index (zero-based to a "relative" "sky" frame (centered around the object xypos)
        "sky-frame" could be (angular,angular,velocity) or (distance,distance,velocity)
        while typically the sky-frame is defined in angular units;
        if the sky frame is defined in length the angular seperation will be converted to physical angular size.
        the object redshift is required
        
        We assume:
            inverse-RA (and pixel-x) aligns along with x
            DEC (and pixel-y) aligns along with y 
        The functin dosn't consider pixel rotation at this moment
    """
    
    #   gather some information about the object
    
    w=WCS(header)
    
    #   wz  : galaxy zero systematic velocity in the hz or wavelength 
    
    if  'Hz' in header['CUNIT3']:
        wz=(obj['restfreq']/(1.0+obj['z'])*(1.-obj['vsys']/const.c)).to(u.Hz)
        dv=(-const.c*header['CDELT3']*u.Hz/(obj['restfreq']/(1.0+obj['z']))).to(u.km/u.s)
    if  'angstrom' in header['CUNIT3']:
        wz=(obj['restwave']*(1.0+obj['z'])*(1.+obj['vsys']/const.c)).to(u.m)
        dv=(const.c*header['CDELT3']*u.angstrom/(obj['restwave']*(1.0+obj['z']))).to(u.km/u.s)
    if  'm/s' in header['CUNIT3']:
        wz=obj['vsys']
        dv=(header['CDELT3']*u.m/u.s).to(u.km/u.s)    
    
    #   get 0-based pix-index of galactic center in the spectral cube
    
    if  w.naxis==4:
        fpx,fpy,fpz,fps=w.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,wz,1,0)
    if  w.naxis==3:
        fpx,fpy,fpz=w.wcs_world2pix(obj['xypos'].ra,obj['xypos'].dec,wz.si,0)    


    cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0*u.arcsec
    kps=Planck13.kpc_proper_per_arcmin(obj['z']).to(u.kpc/u.arcsec)
    dp=cell*kps
    
    if  px is None:
        # if px/py/pz is not specified, will be 1d vector from 0 to naxiy
        # the sx will tell you the sky-value for px=0/px=1/px=2...
        px=np.arange(header['NAXIS1'])
        py=np.arange(header['NAXIS2'])
        pz=np.arange(header['NAXIS3'])
        
    sx=(px-fpx)*dp
    sy=(py-fpy)*dp
    sz=(pz-fpz)*dv
    
    return sx,sy,sz

def chi2uv(objs,header,
           uvdata,uvw,phasecenter,uvweight,uvflag):
    """
    map mutiple component into one header and calculate chisq
    
    models:    a list of model to be mapped into the visibility model for the chisq calculation
    header:    pesudo fits header
    uv...:     visibility data 
    
    """
    
    cc=0
    chi2=0
    
    phasecenter_sc = SkyCoord(phasecenter[0], phasecenter[1], frame='icrs')
    refimcenter_sc = SkyCoord(header['CRVAL1']*u.deg,header['CRVAL2']*u.deg, frame='icrs')
    dra, ddec = phasecenter_sc.spherical_offsets_to(refimcenter_sc)    
    dRA=dra.to_value(u.rad)
    dDec=ddec.to_value(u.rad)
        
    cube=np.zeros((header['NAXIS3'],header['NAXIS2'],header['NAXIS1']),dtype=np.float32)
    cell=np.sqrt(abs(header['CDELT1']*header['CDELT2']))
    wv=const.c.to_value('m/s')/(header['CDELT3']*(np.arange(header['NAXIS3'])-header['CRPIX3'])+header['CRVAL3'])
    #   gather information per object before going into the channel loop,
    #   so it won't need to reapt for each chanel
     
    sxyv_list=[]
    fluxscale_list=[]
    for i in range(len(objs)):
        
        # return coordinate transform info
        sx,sy,sv=pix2sky(objs[i],header)
        sxyv_list.append((sx,sy,sv))
        fluxscale=objs[i]['lineflux']/objs[i]['clouds_loc'].size/np.abs(sv[1]-sv[0])
        fluxscale_list.append(fluxscale.to_value('Jy'))
        
    
    for iz in range(header['NAXIS3']):
        
        blank=True
                    
        for i in range(len(objs)):
            
            obj=objs[i]
            sx,sy,sv=sxyv_list[i]
            locflat=objs[i]['clouds_loc']
            if  objs[i]['clouds_wt'] is None:
                weights=None
            else:
                weights=objs[i]['clouds_wt']
            fluxscale=fluxscale_list[i]
            
            dx=sx[1]-sx[0]
            xrange=[sx[0].value-dx.value/2,sx[-1].value+dx.value/2]
            dy=sy[1]-sy[0]
            yrange=[sy[0].value-dy.value/2,sy[-1].value+dy.value/2]
            dv=np.abs(sv[1]-sv[0])
            vrange=[sv[iz]-dv/2,sv[iz]+dv/2]
            
            select=np.where( (locflat.differentials['s'].d_z > -vrange[1]) & 
                             (locflat.differentials['s'].d_z < -vrange[0]) )
            if  select[0].size>0:
                blank=False
                if  weights is not None:
                    weights_select=weights[select]
                else:
                    weights_select=None
                cube[iz,:,:]+=clouds_discretize_2d(locflat[select],axes=['y','x'],
                                                     range=[yrange,xrange],
                                                     bins=(header['NAXIS2'],header['NAXIS1']),
                                                     weights=weights_select)*fluxscale
        plane=cube[iz,:,:]
        if  blank==False:
            uvdiff=ne.evaluate('a-b',
                     local_dict={'a':sampleImage(plane,
                                            (np.deg2rad(cell)).astype(np.float32),
                                            (uvw[:,0]/wv[iz]),
                                            (uvw[:,1]/wv[iz]),                                   
                                            dRA=dRA,dDec=dDec,
                                            PA=0.,check=False,origin='lower'),
                                 'b':uvdata[:,iz]})
            cc+=1
        else:
            uvdiff=uvdata[:,iz]
            
        chi2+=ne.evaluate('sum( ( (a.real)**2+(a.imag)**2 ) * (~b*c) )', #'sum( abs(a)**2*c)'
                         local_dict={'a':uvdiff,
                                     'b':uvflag[:,iz],
                                     'c':uvweight})        
    
    
    return chi2

def chi2im(objs,header,
           imdata,psf,error):
    """
    map mutiple component into one header and calculate chisq
    
    models:    a list of model to be mapped into the visibility model for the chisq calculation
    header:    pesudo fits header
    uv...:     visibility data 
    
    """
    
    cc=0
    chi2=0
    

        
    cube=np.zeros((header['NAXIS3'],header['NAXIS2'],header['NAXIS1']),dtype=np.float32)
    cell=np.sqrt(abs(header['CDELT1']*header['CDELT2']))
    wv=const.c.to_value('m/s')/(header['CDELT3']*(np.arange(header['NAXIS3'])-header['CRPIX3'])+header['CRVAL3'])
    
    #   gather information per object before going into the channel loop,
    #   so it won't need to reapt for each chanel
     
    sxyv_list=[]
    fluxscale_list=[]
    select_list=[]
    for i in range(len(objs)):
        # return coordinate transform info
        sx,sy,sv=pix2sky(objs[i],header)
        sxyv_list.append((sx,sy,sv))
        # calculate eqavelent flux density contribution per cloud within one channel
        dv=sv[1]-sv[0] 
        fluxscale=objs[i]['lineflux']/objs[i]['clouds_loc'].size/np.abs(dv)
        fluxscale_list.append(fluxscale.to_value('Jy'))
        """
        vrange=[sv[0]-dv/2,sv[-1]+dv/2]
        nbins=sv.size
        digitized = (float(nbins)/(vrange[1] - vrange[0])*\
                     (objs[i]['clouds_loc'].differentials['s'].d_z - vrange[0]))\
                     .astype(int)
        N=objs[i]['clouds_loc'].size
        S = csr_matrix((np.arange(N), [digitized, np.arange(N)]), shape=(nbins, N))
        select_list=np.split(S.data, S.indptr[1:-1])
        """
        
    for iz in range(header['NAXIS3']):
        
        blank=True
                    
        for i in range(len(objs)):
            
            obj=objs[i]
            sx,sy,sv=sxyv_list[i]
            locflat=objs[i]['clouds_loc']
            if  objs[i]['clouds_wt'] is None:
                weights=None
            else:
                weights=objs[i]['clouds_wt']
            fluxscale=fluxscale_list[i]
            
            dx=sx[1]-sx[0]
            xrange=[sx[0].value-dx.value/2,sx[-1].value+dx.value/2]
            dy=sy[1]-sy[0]
            yrange=[sy[0].value-dy.value/2,sy[-1].value+dy.value/2]
            dv=np.abs(sv[1]-sv[0])
            vrange=[sv[iz]-dv/2,sv[iz]+dv/2]
            
            select=np.where( (locflat.differentials['s'].d_z > -vrange[1]) & 
                             (locflat.differentials['s'].d_z < -vrange[0]) )
            """
            print('old',select.size)
            select=select_list[i]
            print('new',select.size)
            """
            if  select[0].size>0:
                blank=False
                if  weights is not None:
                    weights_select=weights[select]
                else:
                    weights_select=None
                cube[iz,:,:]+=clouds_discretize_2d(locflat[select],axes=['y','x'],
                                                     range=[yrange,xrange],
                                                     bins=(header['NAXIS2'],header['NAXIS1']),
                                                     weights=weights_select)*fluxscale
        plane=cube[iz,:,:]
        if  blank==False:
            convol_fft_pad=False
            convol_psf_pad=False
            convol_complex_dtype=np.complex64
            imdiff=ne.evaluate('a-b',
                     local_dict={'a':convolve_fft(plane,psf[:,:],
                                                    fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
                                                    complex_dtype=convol_complex_dtype,
                                                    #fftn=np.fft.fftn, ifftn=np.fft.ifftn,
                                                    #fftn=mkl_fft.fftn, ifftn=mkl_fft.ifftn,
                                                    #nan_treatment='fill',fill_value=0.0,
                                                    #fftn=scipy.fftpack.fftn, ifftn=scipy.fftpack.ifftn,
                                                    fftn=pyfftw.interfaces.numpy_fft.fftn, ifftn=pyfftw.interfaces.numpy_fft.ifftn,
                                                    normalize_kernel=False),
                                 'b':imdata[iz,:,:]})
            cc+=1
        else:
            imdiff=imdata[iz,:,:]
            
        chi2+=ne.evaluate('sum( ( a**2 ) * (1/c)**2 )', #'sum( abs(a)**2*c)'
                         local_dict={'a':imdiff,
                                     'c':error[iz,:,:]})        
    
    
    return chi2

def mapper(objs,header,psf=None):
           
    """
    map a cloudlets-based model into a gridd data model (i.a FITS image-like for exporting or XY->UV tranform)
    
    obj:        target metadata (galactic center position (ra,dec), redshift, vsys, etc.)
                whatever information nesscarity to convert WCS units to physical units
    header:     data frame
    loc:        cloudlet position and velocity in the physical car on-sky frame
    weights:    cloudlet weights 
    
    convert pixel index wthin a WCS to a position in the on-sky galactic coordinates defined in the cloudlet model (ppv)
    
    
    #   get the coordinate of tl tr pix in the galactic frame
    
    #   x/y_sky is along x/y_pix
    #   here we directly map x/y_gal into x/y_pix without considering RA/DEC
        
    """
    
    cc=0
    chi2=0

    
    cube=np.zeros((header['NAXIS3'],header['NAXIS2'],header['NAXIS1']),dtype=np.float32)
    if  psf is not None:
        scube=np.zeros((header['NAXIS3'],header['NAXIS2'],header['NAXIS1']),dtype=np.float32)
        
    sxyv_list=[]
    fluxscale_list=[]
    for i in range(len(objs)):
        # return coordinate transform info
        sx,sy,sv=pix2sky(objs[i],header)
        sxyv_list.append((sx,sy,sv))
        fluxscale=objs[i]['lineflux']/objs[i]['clouds_loc'].size/np.abs(sv[1]-sv[0])
        fluxscale_list.append(fluxscale.to_value('Jy'))
        
    
    for iz in range(header['NAXIS3']):
        
        blank=True
        
        for i in range(len(objs)):
            
            obj=objs[i]
            sx,sy,sv=sxyv_list[i]
            locflat=objs[i]['clouds_loc']
            if  objs[i]['clouds_wt'] is None:
                weights=None
            else:
                weights=objs[i]['clouds_wt']
            fluxscale=fluxscale_list[i]
            
            dx=sx[1]-sx[0]
            xrange=[sx[0].value-dx.value/2,sx[-1].value+dx.value/2]
            dy=sy[1]-sy[0]
            yrange=[sy[0].value-dy.value/2,sy[-1].value+dy.value/2]
            dv=np.abs(sv[1]-sv[0])
            vrange=[sv[iz]-dv/2,sv[iz]+dv/2]
            
            select=np.where( (locflat.differentials['s'].d_z > -vrange[1]) & 
                             (locflat.differentials['s'].d_z < -vrange[0]) )
            if  select[0].size>0:
                blank=False
                if  weights is not None:
                    weights_select=weights[select]
                else:
                    weights_select=None
                cube[iz,:,:]+=clouds_discretize_2d(locflat[select],axes=['y','x'],
                                                     range=[yrange,xrange],
                                                     bins=(header['NAXIS2'],header['NAXIS1']),
                                                     weights=weights_select)*fluxscale
        if  psf is not None:
            plane=cube[iz,:,:]
            if  blank==False:
                convol_fft_pad=False
                convol_psf_pad=False
                convol_complex_dtype=np.complex64
                scube[iz,:,:]=convolve_fft(plane,psf,
                                          fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
                                          complex_dtype=convol_complex_dtype,
                                          #fftn=np.fft.fftn, ifftn=np.fft.ifftn,
                                          #fftn=mkl_fft.fftn, ifftn=mkl_fft.ifftn,
                                          #nan_treatment='fill',fill_value=0.0,
                                          #fftn=scipy.fftpack.fftn, ifftn=scipy.fftpack.ifftn,
                                          fftn=pyfftw.interfaces.numpy_fft.fftn, ifftn=pyfftw.interfaces.numpy_fft.ifftn,
                                          normalize_kernel=False)
            cc+=1       
    if  psf is None:
        return cube
    else:
        return cube,scube