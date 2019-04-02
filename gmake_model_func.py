
def gmake_model_disk2d(header,ra,dec,
                       r_eff=1.0,n=1.0,posang=0.,ellip=0.0,
                       pintflux=0.0,pra=None,pdec=None,
                       intflux=1.,restfreq=235.0,alpha=3.0):
    """
    
        insert a continuum model into a 2D image or 3D cube
        
        header:    data header including WCS
        
        ra,dec:    object center ra/dec
        ellip:     1-b/a
        posang:    in the astronomical convention
        r_eff:     in arcsec
        n:         sersic index
        
        intflux:   Jy
        restfreq:  GHz
        alpha:     
        
        co-centeral point souce: pintflux=0.0
        
        the header is assumed to be ra-dec-freq-stokes
    
        note:
            since the convolution is the bottom-neck, a plane-by-plane processing should
            be avoided.
            avoid too many header->wcs / wcs-header calls
            1D use inverse transsforming
            
    """

    #   build objects
    #   use np.meshgrid and don't worry about transposing

    w=WCS(header)
    cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0
    #px,py=skycoord_to_pixel(SkyCoord(ra,dec,unit="deg"),w,origin=0) # default to IRCS
    px,py,pz,ps=(w.wcs_world2pix(ra,dec,0,0,0))
    vz=np.arange(header['NAXIS3'])
    wz=(w.wcs_pix2world(0,0,vz,0,0))[2]

    #   get 2D disk model
    #start_time = time.time()
    x,y = np.meshgrid(np.arange(header['NAXIS1']), np.arange(header['NAXIS2']))
    mod = Sersic2D(amplitude=1.0,r_eff=r_eff/cell,n=n,x_0=px,y_0=py,
               ellip=ellip,theta=np.deg2rad(posang+90.0))
    #   since the intrinsic model is likley undersampled... we'd be careful on this one.
    #   use discretize_model(mode='oversample') rather than discretize_model(mode='center')
    #model2d=mod(x,y)
    model2d=discretize_model(mod,
                            (0,header['NAXIS1']),
                            (0,header['NAXIS2']),
                            mode='oversample',factor=10)
                            #mode='center')
    
    
    model2d=model2d/model2d.sum()
    #print("--- %s seconds ---" % (time.time() - start_time))
    
    #   intflux at different planes / broadcasting to the data dimension
    #   return model in units of Jy/pix
    
    #start_time = time.time()
    intflux_z=(wz/1e9/restfreq)**alpha*intflux
    if  pintflux!=0.0:
        pintflux_z=(wz/1e9/restfreq)**alpha*pintflux
    #start_time = time.time()
    model=np.empty((header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1']))
    #model=np.broadcast_to(model2d,(header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1'])).copy()
    for i in range(header['NAXIS3']):
        model[0,i,:,:]=intflux_z[i]*model2d
        #print(int(np.round(py)))
        #print(int(np.round(px)))
        #print(round(py),round(px[0]))
        if  pintflux!=0.0:
            model[0,i,int(np.round(py)),int(np.round(px))]+=pintflux_z[i]
    #print("--- %s seconds ---" % (time.time() - start_time))    
    #model_test=np.array([ map(lambda v : v*model2d, range(header['NAXIS3'])) ])
    #print("--- %s seconds ---" % (time.time() - start_time))
    #print(model.shape)

    return model



    
def gmake_model_kinmspy_inclouds(obj,seed,nSamps=100000,returnprof=True):
    """
    replace the cloudlet generator in KinMSpy(); replacement for kinms_sampleFromArbDist_oneSided()
    
    Note from KinMSpy()
        inclouds : np.ndarray of double, optional
         (Default value = [])
        If your required gas distribution is not symmetric you
        may input vectors containing the position of the
        clouds you wish to simulate. This 3-vector should
        contain the X, Y and Z positions, in units of arcseconds
        from the phase centre. If this variable is used, then
        `diskthick`, `sbrad` and `sbprof` are ignored.
        Example: INCLOUDS=[[0,0,0],[10,-10,2],...,[xpos,ypos,zpos]]

    This function takes the input radial distribution and generates the positions of
    `nsamps` cloudlets from under it. It also accounts for disk thickness
    if requested. Returns 
    
    Parameters
    ----------
    sbRad : np.ndarray of double
            Radius vector (in units of pixels).
    
    sbProf : np.ndarray of double
            Surface brightness profile (arbitrarily scaled).
    
    nSamps : int
            Number of samples to draw from the distribution.
    
    seed : list of int
            List of length 4 containing the seeds for random number generation.
    
    diskThick : double or np.ndarray of double
         (Default value = 0.0)
            The disc scaleheight. If a single value then this is used at all radii.
            If a ndarray then it should have the same length as sbrad, and will be 
            the disc thickness as a function of sbrad. 

    Returns
    -------
    inClouds : np.ndarray of double
            Returns an ndarray of `nsamps` by 3 in size. Each row corresponds to
            the x, y, z position of a cloudlet. 
    """

    # get sersic profile
    
    mod = Sersic1D(amplitude=1.0,r_eff=obj['sbser'][0],n=obj['sbser'][1])
    
    sbRad=np.arange(0.,obj['sbser'][0]*7.0,obj['sbser'][0]/25.0)
    sbProf=mod(sbRad)
    diskThick=0.0
    if  'diskthick' in obj:
        diskThick=obj['diskthick']
    
    # truncate the sb profile
    if  'sbrad_min' in obj:
        sbProf[np.where(sbRad<obj['sbrad_min'])]=0.0
    if  'sbrad_max' in obj:
        sbProf[np.where(sbRad>obj['sbrad_max'])]=0.0        

    
    # Randomly generate the radii of clouds based on the distribution given by the brightness profile
    pdf_x=abs(sbRad)
    pdf_y=sbProf*2.*np.pi*abs(sbRad)
    r_flat=pdf2rv(pdf_x,pdf_y,seed=seed[0],size=int(nSamps))

    # Generates a random phase around the galaxy's axis for each cloud 
    # with the Fourier Models (not the same as the xy-transform in galfit)
    fm_m=2. if ('fm_m' not in obj) else obj['fm_m']
    fm_frac=0. if ('fm_frac' not in obj) else obj['fm_frac']
    fm_pa=0. if ('fm_pa' not in obj) else obj['fm_pa']
    # in this case, cdf can be analystically written out easily
    if  fm_frac!=0.0:
        nres=10000.   # good enough
        cdf_x=np.arange(nres+1)/nres*2.0*np.pi-np.pi
        cdf_y=fm_frac*np.sin(fm_m*cdf_x)/fm_m+cdf_x
        phi=cdf2rv(cdf_x,cdf_y,size=nSamps,seed=seed[1])+np.deg2rad(fm_pa)
    else:
        rng2=np.random.RandomState(seed[1])
        phi = rng2.random_sample(nSamps) * 2 * np.pi
        
    # Generate the GE effect
    # GE: q=maj/min
    ge_pa=0. if ('ge_pa' not in obj) else obj['ge_pa']
    ge_q=1. if ('ge_q' not in obj) else obj['ge_q']

    if  ge_q>1.:
        phi=phi-np.deg2rad(ge_pa)
        r_flat=r_flat*np.sqrt((np.cos(phi)**2.+np.sin(phi)**2.0/ge_q**2.0))
        phi=np.arctan2(np.sin(phi)/ge_q,np.cos(phi))+np.deg2rad(ge_pa)
    
    """
    # CoordRot - Hyperbolic
    #phi_out=1.0
    #phi=
    #cr_alpha=0.0
    #r_in=1.0
    #r_out=2.0
    #theta_out=200.0
    
    #phi_offset=theta_out*cr_tanh(r_flat,r_in=r_in,r_out=r_out,theta_out=theta_out)\
    #           *(0.5*(r_flat/r_out+1.))**cr_alpha
    #phi=np.deg2rad(phi_offset)+phi
    """

        
    # Find the thickness of the disk at the radius of each cloud
    if  isinstance(diskThick, (list, tuple, np.ndarray)):
        interpfunc2 = interpolate.interp1d(sbRad,diskThick,kind='linear')
        diskThick_here = interpfunc2(r_flat)
    else:
        diskThick_here = diskThick    
    
    #Generates a random (uniform) z-position satisfying |z|<disk_here 
    rng3 = np.random.RandomState(seed[2])       
    zPos = diskThick_here * rng3.uniform(-1,1,nSamps)
    
    #Calculate the x & y position of the clouds in the x-y plane of the disk
    r_3d = np.sqrt((r_flat**2) + (zPos**2))                                                               
    theta = np.arccos(zPos / r_3d)                                                              
    xPos = ((r_3d * np.cos(phi) * np.sin(theta)))                                                        
    yPos = ((r_3d * np.sin(phi) * np.sin(theta)))
    
    
    #transform transform
 
    
    #Generates the output array
    inClouds = np.empty((nSamps,3))
    inClouds[:,0] = xPos
    inClouds[:,1] = yPos
    inClouds[:,2] = zPos
    
                                                              
    
    
    #return something could be useful
    profile={}
    profile['sbrad']=sbRad
    profile['sbprof']=sbProf
    
    if  returnprof==True:
        return inClouds,profile
    else:
        return inClouds


def gmake_model_kinmspy(header,obj,
                        nsamps=100000,
                        decomp=False,
                        fixseed=False,
                        verbose=False):
    """
    handle modeling parameters to kinmspy and generate the model cubes embeded into 
    a dictionary nest
    
    note:
        kinmspy can only construct a spectral cube in the ra-dec-vel space. We use kinmspy
        to construct a xyv cube with the size sufficient to cover the model object. Then 
        we insert it into the data using the WCS/dimension info. 
    """    

    #######################################################################
    #   WORLD ----      DATA        ----    MODEL
    #######################################################################
    #   ra    ----      xi_data     ----    xSize/2.+phasecen[0]/cell
    #   dec   ----      yi_data     ----    ySize/2.+phasecen[1]/cell
    #   vsys  ----      vi_data     ----    vSize/2.+voffset/dv
    #
    # collect the world coordinates of the disk center (ra,dec,freq/wave)
    # note: vsys is defined in the radio(freq)/optical(wave) convention, 
    #       within the rest frame set at obj['z']/
    #       the convention doesn't really matter, as long as vsys << c
    #######################################################################
    #   vector description of the z-axis (data in Hz or m/s; model in km/s)
    #   rfreq=obj['restfreq']/(1.0+obj['z'])            # GHz (obs-frame)
    #   fsys=(1.0-obj['vsys']/(const.c/1000.0))*rfreq   # line systematic frequency (obs-frame)
        
    w=WCS(header)
    if  'Hz' in header['CUNIT3']:
        wz=obj['restfreq']*1e9/(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
        dv=-const.c*header['CDELT3']/(1.0e9*obj['restfreq']/(1.0+obj['z']))/1000.
    if  'Angstrom' in header['CUNIT3']:
        wz=obj['restwave']*(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
        dv=const.c*header['CDELT3']/(obj['restwave']*(1.0+obj['z']))/1000.
    if  'm/s' in header['CUNIT3']:
        wz=obj['vsys']/1000.
        dv=header['CDELT3']/1000.        

    #   get 0-based pix-index
    
    px,py,pz,ps=w.wcs_world2pix(obj['xypos'][0],obj['xypos'][1],wz,1,0)
    
    ####
    #   About KinMS:
    #       + cube needs to be transposed to match the fits.data dimension 
    #       + the WCS/FITSIO in KINMSPY is buggy/offseted: don't use it
    #       + turn off convolution in kinmspy
    #       + KinMS only works in the RA/DEC/VELO domain.
    #       + KinMS is not preicse for undersampling SBPROFILE/VROT (linear interp -> integral)
    #           - we feed an oversampling vector to kinMS here.
    ####
    
    #####################
    
    #   build an oversampled SB vector.
    
    #mod = Sersic1D(amplitude=1.0,r_eff=obj['sbser'][0],n=obj['sbser'][1])
    #sbprof=mod(sbrad)
    
    #print(sbrad)
    #print(np.array(obj['radi']))
    #velrad=obj['radi']
    #velprof=obj['vrot']
    #gassigma=np.array(obj['vdis'])
    
    #   only extend to this range in vrot/sbprof
    #   this is the fine radii vector fed to kinmspy
    rad=np.arange(0.,obj['sbser'][0]*7.0,obj['sbser'][0]/25.0)
    
    ikind='cubic'  # bad for extraplate but okay for interplate 'linear'/'quadratic'

    if_vrot=interp1d(np.array(obj['vrad']),np.array(obj['vrot']),kind=ikind,bounds_error=False,fill_value=(obj['vrot'][0],obj['vrot'][-1]))
    velprof=if_vrot(rad)
    
    if  isinstance(obj['vdis'], (list, tuple, np.ndarray)):
        #print(obj['vrad'])
        #print(obj['vdis'])
        if_vdis=interp1d(np.array(obj['vrad']),np.array(obj['vdis']),kind=ikind,bounds_error=False,fill_value=(obj['vdis'][0],obj['vdis'][-1]))
        gassigma=if_vdis(rad)
    else:
        gassigma=rad*0.0+obj['vdis']
        obj['vdis']=np.array(obj['vrad'])*0.0+obj['vdis']
    """
    #   same as above
    if_vrot=interpolate.UnivariateSpline(np.array(obj['radi']),np.array(obj['vrot']),s=1.0,ext=3)
    velprof=if_vrot(velrad)
    #   not good for RC
    if_vrot=interp1d(np.array(obj['radi']),np.array(obj['vrot']),kind=ikind,bounds_error=False,fill_value='extrapolate')
    if_vdis=interp1d(np.array(obj['radi']),np.array(obj['vdis']),kind=ikind,bounds_error=False,fill_value='extrapolate')
    velprof=if_vrot(velrad)
    gassigma=if_vdis(velrad)    
    """

    
    ####################
    
    xs=np.max(rad)*1.0*2.0
    ys=np.max(rad)*1.0*2.0
    vs=np.max(velprof*np.abs(np.sin(np.deg2rad(obj['inc'])))+3.0*gassigma)
    vs=vs*1.0*2.

    cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0
    
    # this transformation follows the whatever defination of "cubecenter" in kinmspy
    px_o=px-float(round(xs/cell))/2.
    py_o=py-float(round(ys/cell))/2.
    pz_o=pz-float(round(vs/abs(dv)))/2.
    if  dv<0: pz_o=pz_o+1.0 # count offset backwards if the z-axis is decreasing in velocity
    px_o_int=round(px_o) ; px_o_frac=px_o-px_o_int
    py_o_int=round(py_o) ; py_o_frac=py_o-py_o_int
    pz_o_int=round(pz_o) ; pz_o_frac=pz_o-pz_o_int
    phasecen=np.array([px_o_frac,py_o_frac])*cell
    voffset=(pz_o_frac)*dv

    #start_time = time.time()

    if  fixseed==True:
        seeds=[100,101,102,103]
    else:
        seeds=np.random.randint(0,100,4)
        # seeds[0] -> rad
        # seeds[1] -> phi
        # seeds[2] -> z
        # seeds[3] -> v_sigma
        
    inclouds,prof1d=gmake_model_kinmspy_inclouds(obj,seeds,nSamps=nsamps)
    
    cube=KinMS(xs,ys,vs,
               cellSize=cell,dv=abs(dv),
               beamSize=1.0,cleanOut=True,
               inc=obj['inc'],
               #sbProf=sbprof,sbRad=sbrad,
               inClouds=inclouds,
               velRad=rad,velProf=velprof,gasSigma=gassigma,
               #ra=obj['xypos'][0],dec=obj['xypos'][1],
               restFreq=obj['restfreq'],vSys=obj['vsys'],
               phaseCen=phasecen,vOffset=voffset,
               #phaseCen=[0,0],vOffset=0,
               fixSeed=fixseed,
               #nSamps=nsamps,fileName=outname+'_'+tag,
               posAng=obj['pa'],
               intFlux=obj['intflux'])
    #print("--- %s seconds ---" % (time.time() - start_time))
    #   KinMS provide the cube in (x,y,v) shape, but not in the Numpy fasion. transpose required
    #   flip z-axis if dv<0
    #print(cube.shape)
    cube=cube.T
    if  dv<0: cube=np.flip(cube,axis=0)
    #print('sub:',cube.shape)
    model=np.zeros((header['NAXIS4'],header['NAXIS3'],header['NAXIS2'],header['NAXIS1']))
    model=paste_array(model,cube[np.newaxis,:,:,:],(0,int(pz_o_int),int(py_o_int),int(px_o_int)))
    
    model_prof={}
    model_prof['sbrad']=prof1d['sbrad'].copy()
    model_prof['sbprof']=prof1d['sbprof'].copy()
    
    model_prof['vrad']=rad.copy()
    model_prof['vrot']=velprof.copy()
    model_prof['vdis']=gassigma
    
    #model_prof['sbrad_node']=obj['radi'].copy()
    #model_prof['sbprof_node']=obj['radi'].copy()
    model_prof['vrad_node']=np.array(obj['vrad'])
    model_prof['vrot_node']=np.array(obj['vrot'])
    model_prof['vdis_node']=np.array(obj['vdis'])
    if  'vrot_halo' in obj:
        model_prof['vrot_halo_node']=np.array(obj['vrot_halo'])
    if  'vrot_disk' in obj:
        model_prof['vrot_disk_node']=np.array(obj['vrot_disk'])
            
    return model,model_prof


def gmake_model_simobs(data,header,beam=None,psf=None,returnkernel=False,verbose=True,average=False):
    """
        simulate the observation in the image-domain
        input is expected in units of Jy/pix
        output will in the Jy/cbeam or Jy/dbeam if kernel is peaked at unity.
        
        average=True:
        
            the data is assumed to a continuum image even it's a 3D cube.
            we will take the middle plane of 2D data and PSF for one-time convolution, and broadcast the
            results back into 3D with channel-wise flux changes corrected.
            in this way, we can save the plane-by-plane convolution loop.
            
            It should be only used for narrow-band imaging without near galaxy morphology/PSF changes.
            *DO NOT* turn this one for a model including spectral line emission 
        
        the adopted kernel can be returned
        
        note: + we only use cellsize/bmaj/bmin/bpa info from the header.
                so the header doesn't need to match the data "dimension"
              + the function will skip any plane with 0-flux
              + no clear advantage from 3D-FFT vs. 2D-FFT+loop
              + In 2D-FFT+loop, we can selectively choose the usefull planes
              
        TestLog (numpy vs. mkl):
        
            (62, 48, 48)
            (62, 48, 48)
            (58, 48, 48)
            imodel@examples/bx610/bx610.bb2.cube.iter0.image.fits
            data   dim: (1, 238, 105, 105)
            kernel dim: (1, 238, 105, 105)
            ---  simobs   : 1.12489  seconds ---
            convolved plane counts:  96
            imodel@examples/bx610/bx610.bb3.cube.iter0.image.fits
            data   dim: (1, 238, 105, 105)
            kernel dim: (1, 238, 105, 105)
            ---  simobs   : 0.53417  seconds ---
            convolved plane counts:  45
            --- apicall   : 1.96320  seconds ---
            ---  export   : 0.98041  seconds ---
            
            In [43]: execfile('/Users/Rui/Dropbox/Worklib/projects/GMaKE/gmake_test.py')
            (62, 48, 48)
            (62, 48, 48)
            (58, 48, 48)
            imodel@examples/bx610/bx610.bb2.cube.iter0.image.fits
            data   dim: (1, 238, 105, 105)
            kernel dim: (1, 238, 105, 105)
            ---  simobs   : 0.30933  seconds ---
            convolved plane counts:  98
            imodel@examples/bx610/bx610.bb3.cube.iter0.image.fits
            data   dim: (1, 238, 105, 105)
            kernel dim: (1, 238, 105, 105)
            ---  simobs   : 0.12595  seconds ---
            convolved plane counts:  44
            --- apicall   : 0.75084  seconds ---
            ---  export   : 1.02895  seconds ---
              
              
    """

    # the default setting in convolve_fft is optimzed for the precision rather than speed..
    # https://software.intel.com/en-us/articles/mkl-ipp-choosing-an-fft
    # https://software.intel.com/en-us/articles/fft-length-and-layout-advisor
    # http://www.fftw.org/fftw2_doc/fftw_3.html
    convol_fft_pad=False # we don't care about 2^n since the fancy MKL or FFTW is used: 
                         # the optimized radices are 2, 3, 5, 7, and 11.
                         # we will control the imsize when extracting subregion
    convol_complex_dtype=np.complex64   #np.complex128
    #convol_complex_dtype=np.complex256   #np.complex128
    convol_psf_pad=False # psf_pad=True can avoild edge wrap by padding the original image to naxis1+naxis2 (or twice if square)
                         # since our sampling/masking cube already restrict the inner quarter for chi^2, we don't need to pad further.
    
    #w=WCS(header)
    #cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0
    cell=np.sqrt(abs(header['CDELT1']*header['CDELT2']))*3600.0


    #   get the convolution Kernel normalized to 1 at PEAK
    #   turn on normalization in convolve() will force the Jy/Pix->Jy/beam conversion
    #   priority: psf>beam>header(2D or 3D KERNEL) 
    
    dshape=data.shape
    
    #   we didn't turn on mode='oversample' since the data pixelization 
    #   is generally oversampling the beam
     
    if  psf is not None:
        kernel=psf.copy()
    elif beam is not None:
        if  not isinstance(beam, (list, tuple, np.ndarray)):
            gbeam = [beam,beam,0]
        else:
            gbeam = beam
        kernel=makekernel(dshape[-1],dshape[-2],
                        [gbeam[0]/cell,gbeam[1]/cell],pa=gbeam[2],
                        mode=None)
    else:
        kernel=makekernel(dshape[-1],dshape[-2],
                        [header['BMAJ']*3600./cell,header['BMIN']*3600./cell],pa=header['BPA'],
                        mode=None)

    if  verbose==True:
        print('data   dim:',data.shape)
        print('kernel dim:',kernel.shape)
        start_time = time.time()

    model=np.zeros(data.shape)
    cc=0
    for i in range(dshape[-3]):

        #   skip blank planes
        if  np.sum(data[0,i,:,:])==0.0:
            continue
        #   skip all-but-one planes if average==True
        if  average==True and i!=int(dshape[-3]/2.0):
            continue
                
        if  kernel.ndim==2:
            kernel_used=kernel
        else:
            kernel_used=kernel[0,i,:,:]
        
        model[0,i,:,:]=convolve_fft(data[0,i,:,:],kernel_used,
                                    fft_pad=convol_fft_pad,psf_pad=convol_psf_pad,
                                    complex_dtype=convol_complex_dtype,
                                    #fftn=np.fft.fftn, ifftn=np.fft.ifftn,
                                    fftn=mkl_fft.fftn, ifftn=mkl_fft.ifftn,
                                    #fftn=scipy.fftpack.fftn, ifftn=scipy.fftpack.ifftn,
                                    #fftn=pyfftw.interfaces.numpy_fft.fftn, ifftn=pyfftw.interfaces.numpy_fft.ifftn,
                                    normalize_kernel=False)
        cc=cc+1
    
    if  average==True:
        
        i0=int(dshape[-3]/2.0)
        model0=model[0,i0,:,:]
        data0sum=data[0,i0,:,:].sum()
        
        for i in range(dshape[-3]):
            model[0,i,:,:]=model0*(data[0,i,:,:]).sum()/data0sum
    

    if  verbose==True:
        
        print("convolved plane counts: ",cc)
        print("---{0:^10} : {1:<8.5f} seconds ---".format('simobs',time.time()-start_time))
        #start_time = time.time()
        #test1=(data[0,:,:,:])
        #test2=(kernel[np.newaxis,0,100,(52-10):(52+10),(52-10):(52+10)])
        #print(test1.shape,test2.shape)
        #test=convolve(test1,test2)
        #print("---{0:^10} : {1:<8.5f} seconds ---".format('simobs-beta',time.time()-start_time))
        

    if  returnkernel==True:
        return model,kernel
    else:
        return model

#@profile
def gmake_model_uvsample(xymodel,header,uvdata,uvw,phasecenter,
                         uvmodel_in=None,
                         average=False,
                         verbose=True):
    """
    simulate the observation in the UV-domain
    input is expected in units of Jy/pix
    
    uvdata shape:        nrecord x nchan (less likely: nrecord x nchan x ncorr)
    xymodel shape:       nstokes x nchan x ny x nx
    
    note: when uvmodel_in is provided, a new model will be added into the array without additional memory usage 
          the return variable is just a reference of mutable uvmodel_in 
    """

    cell=np.sqrt(abs(header['CDELT1']*header['CDELT2']))
    
    #   
    # + set order='F' as we want to have quick access to each column.
    #   i.a. first dimension is consequential in memory 
    #   this make a big difference in effeciency of fetching each channel
    # + zeros_like vs. zeros()
    #   the memory of an array created by zeros() can allocated on-the-fly
    #   the creation will appear to be faster but the looping+plan initialization may be slightly slower (or comparable?) 
    #start_time1 = time.time()
    if  uvmodel_in is not None:
        uvmodel=uvmodel_in
    else:
        uvmodel=np.zeros((uvdata.shape)[0:2],dtype=uvdata.dtype,order='F')
    
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('create',time.time()-start_time1))
    #start_time1 = time.time()
    
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('create',time.time()-start_time1))    
    
    uvdata_shape=uvdata.shape
    
    if  verbose==True:
        #print('uvdata  dim:',uvdata.shape)
        #print('xymodel dim:',xymodel.shape)
        #print('uvmodel dim:',uvmodel.shape)
        start_time = time.time()    
            
    # assume that CRPIX1/CRPIX2 is at model image "center" floor(naxis/2);
    # which is true for the mock-up image header 
    dRA=np.deg2rad(+(header['CRVAL1']-phasecenter[0]))
    dDec=np.deg2rad(+(header['CRVAL2']-phasecenter[1]))
    
    #start_time1 = time.time()
    
    if  average==False:
        
        cc=0
        # create the array before looping
        if  uvmodel_in is None:
            uvmodel=np.zeros_like(uvdata,dtype=uvdata.dtype,order='F')
        for i in range(uvdata_shape[1]):
            if  np.sum(xymodel[0,i,:,:])==0.0:
                continue
            wv=const.c/(header['CDELT3']*i+header['CRVAL3'])
            # just like the convolution in the image domain but only fft once vs. fft/iff in convolve_fft
            #print((uvw[:,0]/wv).flags)            
            uvmodel[:,i]+=sampleImage(xymodel[0,i,:,:],np.deg2rad(cell),
                                       #(uvw[:,0]/wv).copy(order='C'),
                                       #(uvw[:,1]/wv).copy(order='C'),
                                       (uvw[:,0]/wv),
                                       (uvw[:,1]/wv),                                   
                                       dRA=dRA,dDec=dDec,PA=0,check=False)
            cc=cc+1
    
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('fft',time.time()-start_time1))
    
    #start_time1 = time.time()
    
    if  average==True:
        
        cc=1
        if  uvmodel_in is None:
            uvmodel=np.zeros_like(uvdata,dtype=uvdata.dtype,order='F')
        i0=int(uvdata_shape[1]/2.0)
        xymodelsum=xymodel.sum(axis=(0,2,3))
        xymodel_zscale=xymodelsum/xymodelsum[i0]        
        wv=const.c/(header['CDELT3']*i0+header['CRVAL3'])
        uvmodel0=sampleImage(xymodel[0,i0,:,:],np.deg2rad(cell),
                                   #(uvw[:,0]/wv).copy(order='C'),
                                   #(uvw[:,1]/wv).copy(order='C'),
                                   (uvw[:,0]/wv),
                                   (uvw[:,1]/wv),                                   
                                   dRA=dRA,dDec=dDec,PA=0,check=False)
        #print(uvmodel0.dtype)
        for i in range(uvdata_shape[1]):
            uvmodel[:,i]+=uvmodel0*xymodel_zscale[i]
        #print(uvmodel.dtype)
        
        # this is x2 fasfter for an array of (489423, 238)
        #np.multiply(uvmodel0,xymodel_zscale[i],out=uvmodel[:,i])
        #np.add(uvmodel[:,i],uvmodel0*xymodel_zscale[i],out=uvmodel[:,i])    
        #slow: uvmodel_test=np.einsum('i,j->ij',uvmodel0,xymodel_zscale,optimize='greedy',order='C')
        #slow: uvmodel_test=uvmodel*xymodel_zscale
        #uvmodel+=np.einsum('i,j->ij',uvmodel0,xymodel_zscale,order='F')
        #print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>loop-fancy',time.time()-start_time1))
        
        #print(uvmodel.shape)
        #"""
        
        #"""
        #start_time1 = time.time()
        #print(uvmodel.dtype)
        #print(uvmodel0.dtype)
        #np.einsum('i,j->ij',uvmodel0.astype(np.complex64),xymodel_zscale.astype(np.float32),order='F',out=uvmodel)
        #slow: uvmodel_test=uvmodel*xymodel_zscale            
        #print("---{0:^10} : {1:<8.5f} seconds ---".format('>>>>matrix',time.time()-start_time1))
        #print(uvmodel.shape)        
        #"""
        
    if  verbose==True:
        
        print("uvsampling plane counts: ",cc)
        print("---{0:^10} : {1:<8.5f} seconds ---".format('simobs',time.time()-start_time))
        
        #print("--")
    
    return uvmodel


    
def makekernel(xpixels,ypixels,beam,pa=0.,cent=None,
               mode=None,
               verbose=True):
    """
    mode: 'center','linear_interp','oversample','integrate'

    beam=[bmaj,bmin] FWHM
    pa=east from north (ccw)deli
    
    in pixel-size units
    
    by default: the resulted kernel is always centered around a single pixel, and the application of
        the kernel will lead to zero offset,
    
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
            cent=floor(ks/2.) or int(ks/2) #  int() try to truncate towards zero.
        
        note:
            
            Python "rounding half to even" rule vs. traditional IDL:
                https://docs.scipy.org/doc/numpy/reference/generated/numpy.around.html
                https://realpython.com/python-rounding/
                Python>round(1.5)    # 2
                Python>round(0.5)    # 0
                IDL>round(1.5)       # 2 
                IDL>round(0.5)       # 1
 
            "forget about how the np.array is stored, just use the array as it is IDL;
             when it comes down to shape/index, reverse the sequence"
             
            About Undersampling Images:
            http://docs.astropy.org/en/stable/api/astropy.convolution.discretize_model.html
            
    """
    
    if  cent is None:
        cent=[np.floor(xpixels/2.),np.floor(ypixels/2.)]
    sigma2fwhm=np.sqrt(2.*np.log(2.))*2.
    mod=Gaussian2D(amplitude=1.,x_mean=cent[0],y_mean=cent[1],
               x_stddev=beam[1]/sigma2fwhm,y_stddev=beam[0]/sigma2fwhm,
               theta=np.deg2rad(pa))
    if  mode==None:
        x,y=np.meshgrid(np.arange(xpixels),np.arange(ypixels))
        psf=mod(x,y)
    else:
        psf=discretize_model(mod,(0,int(xpixels)),(0,int(ypixels)),
                             mode=mode)
    
    return psf
    

    
if  __name__=="__main__":

    """
    examples
    """
    pass


