"""
functions for building:
    imsets,data,disks
"""
def py_tirific_mc_setup_hxmm01_disks(lines,objects):
    """
        return a list containing the disk geometry and kinematic properties
        the radii grid must be consistent among lines for each object
        but each object can have its own radii grid setup
    """
    disks=[]
    
    #'radi':np.array([0., 0.12, 0.24, 0.36, 0.54 ,0.72]),
    #'radi':np.array([0., 0.12, 0.24, 0.36, 0.48 ,0.60]),
    #'esbr':[24.72,5.16],
    #'lc0':np.zeros(8),
    #'ls0':np.zeros(8),
    #'ga1a':np.zeros(8),
    #'ga1p':np.zeros(8),
    #'ga1d':np.zeros(8),    
    #'edisp':[82.93,-1.00]}) 
          
    #############
    #   XMM01N
    #############
    disks.append({'object':'Core',
          'line':'CII',
          'xypos':[150.22704167,2.57669444],
          'vsys':0.0,
          'pa':140.0,
          'inc':60.0,
          'radi':np.arange(5)*0.15,
          'esbr':np.array([5.89,0.10]),
          #'sm1a':np.array([0.0,0.54,0.14,0.37,0.22,0.19,0.61,-0.4]),
          #'sm1p':np.zeros(8)-7.0,
          'vrot':np.array([0,463,461,341,482]),
          'vdisp':np.zeros(5)+157.0})      

    out_disks=[]
    for disk in disks:
        pick=False
        for ind in range(len(lines)):
            if  disk['line'] in lines[ind] and disk['object'] in objects[ind]:
                pick=True
        if  pick==True:
            out_disks.append(disk)
    
    return out_disks

def py_tirific_mc_setup_hxmm01_imsets(imlist,lines,objects):
    
    #<----image set tag; different from line name
    #<----imsets hold image metadata
    
    imsets={}
    data={}
    
    for ind in range(len(imlist)):
        
        imlist0=deepcopy(imlist[ind])
        if  imlist[ind]=='CICO76':
            imlist0='CO76' 
        
        #   this already done in IDL here.
        #tirific_imprep(infile='J1000+0234.'+imlist0+'.cm.fits',outfile='J1000+0234.'+imlist0+'.cm.tr.fits',delbeam=False)
        #tirific_imprep(infile='J1000+0234.'+imlist0+'.cm.fits',outfile='J1000+0234.'+imlist0+'.cm.nb.fits',delbeam=True)
    
        fitsfile='J1000+0234.'+imlist0+'.cm.fits'
        errfile='J1000+0234.'+imlist0+'.em.fits'
        blankfile='J1000+0234.'+imlist0+'.mk_blank.fits'    # 1 for useable region 
        detecfile='J1000+0234.'+imlist0+'.mk_detec.fits'    # 1 for detection
        hexfile='J1000+0234.'+imlist0+'.hex.fits'
        psffile='J1000+0234.'+imlist0+'.psf.fits'
        
        samp=fitsio.read('J1000+0234.'+imlist0+'.samp.fits')
        hex_ra=samp['HEX_RA'][0]
        hex_dec=samp['HEX_DEC'][0]
        hex_ind=samp['HEX_IND'][0]
        
        im,hd= fits.getdata(fitsfile,header=True)
        em = fits.getdata(errfile)
        hx = fits.getdata(hexfile)
        
        if  os.path.isfile(blankfile):
            bl = fits.getdata(blankfile)
        else:
            bl = im*0.0+1.0
        if  os.path.isfile(detecfile):
            dt = fits.getdata(detecfile)
        else:
            dt = im*0.0+1.0
        if  os.path.isfile(psffile):
            pf = fits.getdata(psffile)
        else:
            pf = im*0.0+1.0
        data0={ 'im':deepcopy(im),     #   spectral cube
                'em':deepcopy(em),      #   error cube
                'bl':deepcopy(bl),      #   blanking
                'dt':deepcopy(dt),      #   detection
                'hx':deepcopy(hx),      #   sampling
                'pf':deepcopy(pf)}      #   psf    
        data0['sp']=deepcopy(hx)
        if  imlist[ind]=='CI' or imlist[ind]=='CO76':
            data0['sp']=deepcopy(bl*hx)
        data0['hd']=hd
        
        data0['hex_ra']=deepcopy(hex_ra)
        data0['hex_dec']=deepcopy(hex_dec)
        data0['hex_ind']=deepcopy(hex_ind)
        
        
        if  os.path.isfile('J1000+0234.'+imlist0+'.cm_finexxxxx.fits'):
            im_fine,hd_fine=fits.getdata('J1000+0234.'+imlist0+'.cm_fine.fits',header=True)
            data0['im_fine']=im_fine
            data0['hd_fine']=hd_fine
            em_fine=fits.getdata('J1000+0234.'+imlist0+'.em_fine.fits')
            data0['em_fine']=em_fine
            hx_fine=fits.getdata('J1000+0234.'+imlist0+'.hex_fine.fits')
            data0['hx_fine']=deepcopy(hx_fine)             
            data0['sp_fine']=deepcopy(hx_fine) 
            
        fs=np.sum(np.squeeze(dt*hx*im*40.0),axis=0)
        nyx=np.shape(fs)
        iyx=np.where(fs!=0)
        data0['fs']=deepcopy(fs)            # 2D detection sampling point
        fits.writeto('J1000+0234.'+imlist0+'.fs0.fits',data0['fs'],overwrite=True)
        data0['iy']=deepcopy(iyx[0])        # sampling point index(y)
        data0['ix']=deepcopy(iyx[1])        # sampling point index(x)
        data0['is']=deepcopy(fs[iyx[0],iyx[1]])    # sampling point scaling factor
        xx,yy=np.meshgrid(np.arange(nyx[1]),np.arange(nyx[0]))
        data0['xx']=xx
        data0['yy']=yy
        data[imlist[ind]]=deepcopy(data0)       #<<<<<<<<<<<<<<<<<<
        
        #   UPPER CASE: tr parameters
        #   LOWER CASE: disk metadata
        imset={}
        
        imset['INSET']='J1000+0234.'+imlist0+'.cm.nb.fits'
        imset['BMAJ']=hd['BMAJ']*3600.0
        imset['BMIN']=hd['BMIN']*3600.0 
        imset['BPA']=hd['BPA']
        imset['CONDISP']=0.0 #FWHM=50km/s from Hanning smooth
        imset['INTY']=1
        imset['CLNR']=1

        
        imset['lnf']=0.05
        imset['cflux_scale']=0.03**2./10
        imset['cflux']=2e-6        
        if  imlist[ind]=='CICO76':
            imset['lnf']=0.00
            imset['cflux_scale']=0.06**2./10
            imset['cflux']=2e-6
        if  imlist[ind]=='water':
            imset['lnf']=0.00
            imset['cflux_scale']=0.06**2./10
            imset['cflux']=2e-6            
        if  imlist[ind]=='CO10':
            imset['lnf']=0.00
            imset['cflux_scale']=0.06**2./10
            imset['cflux']=2e-7                                          
        imset['lines']=deepcopy(lines[ind])
        imset['objects']=deepcopy(objects[ind])
        imset['outfolder']='J1000+0234.'+imlist[ind]
        imset['outname']='diskmod'
        imset['vshift_ci']=-997.17281
        imset['vshift_co76']=0.0
        imset['vshift_water']=0.0
        
        imsets[imlist[ind]]=deepcopy(imset)     #<<<<<<<<<<<<<<<<<<
        
        
    return  imsets,data


