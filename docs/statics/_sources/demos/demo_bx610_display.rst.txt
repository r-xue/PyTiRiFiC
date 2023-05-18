Example: BX610 (High-z SFG) : Examine Moment0 + 1D Spectrum
-----------------------------------------------------------

.. code:: ipython3

    from spectral_cube import SpectralCube, LazyMask
    from spectral_cube.utils import SpectralCubeWarning
    warnings.filterwarnings(action='ignore', category=SpectralCubeWarning,append=True)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore")
    
    import numpy as np
    from astropy.io import fits
    from astropy.wcs import WCS
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from astropy.stats import mad_std
    import regions
    import glob
    
    %matplotlib inline
    import matplotlib as mpl
    
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    mpl.rcParams.update({'font.size': 14})
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["image.origin"]="lower"
    mpl.rc('text', usetex=True)
    
    import matplotlib.pyplot as plt


Plot Mom0 + 1D Spectra from Dirty Maps: 2013 Band4 Cycle2 -> 2017 Band4 Cycle5 -> Band4 Cycle2+5 -> 2015 Band 6 Cycle3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
        
        
    cc=SkyCoord('23h46m09.4382s +12d49m19.2655s',unit=(u.hourangle, u.deg),frame='icrs')
    inc=0.*u.deg
    pa=0.*u.deg
    rad=1.2*u.arcsec
    skyreg=regions.EllipseSkyRegion(cc,rad,rad*np.cos(inc),\
                                    angle=pa+90.0*u.deg,meta={'label':'Aperture'})
    
    cubelist=[]
    cubelist.extend(glob.glob('2013*/*/*sci.fits'))
    cubelist.extend(glob.glob('2017*/*/*sci.fits'))
    cubelist.extend(glob.glob('band4*/*/*sci.fits'))
    cubelist.extend(glob.glob('2015*/*/*sci.fits'))
    for cubename in cubelist:
    
        if 'cont' in cubename:
            continue
            
        figname=cubename.replace('/sci.fits','_sci.pdf')
        
        cube=SpectralCube.read(cubename,mode='readonly')
        cube.beam_threshold=1.0
        cbeam=cube.beams.largest_beam()
        mom0=(cube.moment(order=0)).array
        #mom0=(cube.moment(order=1)).array
    
        #cube_sigma = mad_std(cube,ignore_nan=True)
        #cube_mask = LazyMask(lambda x: x>(6.0*cube_sigma),cube=cube)
        #cube_mskd=cube.with_mask(cube_mask)   
        #mom0=(cube_mskd.moment(order=0)).array
        #mom0=(cube_mskd.moment(order=1)).array
        
        
        header=fits.getheader(cubename)
        w=WCS(header).celestial
        skyreg_pix=skyreg.to_pixel(w)
        
        plt.clf()
        figsize=(10,5)
        fig=plt.figure(figsize=figsize)
    
        ax = fig.add_axes([0.1,0.1,0.5,0.9],projection=w)
    
        ax.imshow(mom0, interpolation='nearest', vmin=np.nanmin(mom0), vmax=np.nanmax(mom0))
        skyreg_pix.plot(ax=ax,facecolor='none', edgecolor='yellow', lw=0.5,label='test')
    
        sz=mom0.shape
        wx,wy=w.wcs_pix2world(sz[0]/8.0,sz[1]/8.0,0)
        bshape=mpl.patches.Ellipse((wx,wy),
                               (cbeam.minor).to_value(u.deg),(cbeam.major).to_value(u.deg),
                               angle=-(cbeam.pa).to_value(u.deg), 
                                edgecolor='cyan', facecolor='cyan',
                                transform=ax.get_transform('icrs'))
        ax.add_patch(bshape)
        ax.coords['ra'].set_axislabel('Right Ascension (ICRS)')
        ax.coords['dec'].set_axislabel('Declination (ICRS)')
    
        subcube=cube.subcube_from_regions([skyreg])
        subcube_1d=subcube.sum(axis=(1,2))
    
        ax_spec=fig.add_axes([0.7,0.1,0.9,0.9])
        freq=(cube.spectral_axis)
        freq=freq.to(u.GHz)
        ax_spec.plot(freq,subcube_1d.array,color='gray',label='Data') #,drawstyle='steps-mid'
        ax_spec.fill_between(freq,0,subcube_1d.array,facecolor='0.9',step='mid',alpha=1.0)
        ax_spec.set_xlabel('Freq [GHz]')
        ax_spec.set_ylabel('Jy/ppbeam')
        ax_spec.set_title(cubename+"     "+\
                          "{0.value:0.2f}{0.unit:latex} x {1.value:0.2f}{1.unit:latex} {2.value:0.2f}{2.unit:latex}".format(cbeam.major,cbeam.minor,cbeam.pa),
                         fontsize=15)
    
        plt.show()
        fig.savefig(figname) 
        plt.close()    
    
    #cubename='bb3.co43/sci.fits'
    #cubename='bb1.ci10/sci.fits'



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_3_1.png



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_3_3.png



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_3_5.png



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_3_7.png



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_3_9.png



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_3_11.png



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_3_13.png



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_3_15.png


Summary Figure of all spectral lines in 1D spectra form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    from spectral_cube import SpectralCube, LazyMask
    from spectral_cube.utils import SpectralCubeWarning
    warnings.filterwarnings(action='ignore', category=SpectralCubeWarning,append=True)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore")
    
    import numpy as np
    from astropy.io import fits
    from astropy.wcs import WCS
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from astropy.stats import mad_std
    import regions
    import glob
    
    %matplotlib inline
    import matplotlib as mpl
    
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    mpl.rcParams.update({'font.size': 14})
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["image.origin"]="lower"
    mpl.rc('text', usetex=True)
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    
    def bx610_1dspec(cubename):
        """
        generate a quickview of the data mom0 map & 1D model/data spectra
        """
        
        cc=SkyCoord('23h46m09.4382s +12d49m19.2655s',unit=(u.hourangle, u.deg),frame='icrs')
        inc=0.*u.deg
        pa=0.*u.deg
        rad=1.2*u.arcsec
        skyreg=regions.EllipseSkyRegion(cc,rad,rad*np.cos(inc),\
                                        angle=pa+90.0*u.deg,meta={'label':'Aperture'})
    
    
        cube=SpectralCube.read(cubename,mode='readonly')
        cube.beam_threshold=1.0
    
        subcube=cube.subcube_from_regions([skyreg])
        subcube_1d=subcube.sum(axis=(1,2))
    
        freq=(cube.spectral_axis)
        freq=freq.to(u.GHz)
        spec={'x':freq,'y':subcube_1d.array}
        
        return spec
    
    #cubename='bb3.co43/sci.fits'
    #cubename='bb1.ci10/sci.fits'
    
    
    
    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
        
    cubelist=[]
    cubelist.extend(glob.glob('band4*/*co43*/*sci.fits'))
    cubelist.extend(glob.glob('band4*/*ci10*/*sci.fits'))
    cubelist.extend(glob.glob('2015*/*h2o*/*sci.fits'))
    cubelist.extend(glob.glob('2015*/*co76ci21*/*sci.fits'))
    
    print(cubelist)
    plt.clf()
    # If you're not familiar with np.r_, don't worry too much about this. It's just 
    # a series with points from 0 to 1 spaced at 0.1, and 9 to 10 with the same spacing.
    #x = np.r_[100:104:0.1, 200:204:0.1]
    #y = np.sin(x)
    
    fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(10,6))
    
    # plot the same data on both axes
    #ax.plot(x, y, 'bo')
    #ax2.plot(x, y, 'bo')
    
    # zoom-in / limit the view to different portions of the data
    ax1.set_xlim(143,144) # most of the data
    ax2.set_xlim(153,154) # outliers only
    ax3.set_xlim(233.25,235.00)
    ax4.set_xlim(250.75,252.50)
    ax1.set_ylim(-0.4,2.0) # most of the data
    ax2.set_ylim(-0.4,2.0) # outliers only
    ax3.set_ylim(-0.1,0.50)
    ax4.set_ylim(-0.1,0.50)
    
    specs=[]
    specs+=[bx610_1dspec(cubelist[0])]
    specs+=[bx610_1dspec(cubelist[1])]
    specs+=[bx610_1dspec(cubelist[2])]
    specs+=[bx610_1dspec(cubelist[3])]
    ax_list=[ax1,ax2,ax3,ax4]
    for i in range(4):
        spec=specs[i]
        ax=ax_list[i]
        ax.plot(spec['x'],spec['y'],color='gray')
        ax.fill_between(spec['x'],0,spec['y'],facecolor='0.9',step='mid',alpha=1.0)
        if i==2 or i==3:
            ax.set_xlabel('Freq [GHz]')
        if i==0 or i==2:
            ax.set_ylabel('Jy/ppbeam')
    
    ax1.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.yaxis.tick_right()
    
    ax3.spines['right'].set_visible(False)
    ax4.spines['left'].set_visible(False)
    ax4.yaxis.tick_right()
    
    plt.subplots_adjust(wspace=0.15)
    
    #ax2.spines['right'].set_visible(False)
    #ax3.spines['left'].set_visible(False)
    #ax3.spines['right'].set_visible(False)
    #ax4.spines['left'].set_visible(False)
    
    d = .015 # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
    ax1.plot((1-d,1+d),(-d,+d), **kwargs) # top-left diagonal
    ax1.plot((1-d,1+d),(1-d,1+d), **kwargs) # bottom-left diagonal
    
    kwargs.update(transform=ax2.transAxes) # switch to the bottom axes
    ax2.plot((-d,d),(-d,+d), **kwargs) # top-right diagonal
    ax2.plot((-d,d),(1-d,1+d), **kwargs) # bottom-right diagonal
    
    kwargs = dict(transform=ax3.transAxes, color='k', clip_on=False)
    ax3.plot((1-d,1+d),(-d,+d), **kwargs) # top-left diagonal
    ax3.plot((1-d,1+d),(1-d,1+d), **kwargs) # bottom-left diagonal
    
    kwargs.update(transform=ax4.transAxes) # switch to the bottom axes
    ax4.plot((-d,d),(-d,+d), **kwargs) # top-right diagonal
    ax4.plot((-d,d),(1-d,1+d), **kwargs) # bottom-right diagonal
    
    ax2.tick_params(axis='y',which='both',left=False,right=False)
    
    ax1.plot([], [], ' ', label="CO 4-3")
    ax1.legend(frameon=False,loc='upper right')
    
    ax2.plot([], [], ' ', label="CI 1-0")
    ax2.legend(frameon=False,loc='upper right')
    
    ax3.plot([], [], ' ', label="H2O")
    ax3.legend(frameon=False,loc='upper right')
    
    ax4.plot([], [], ' ', label="CO 7-6")
    ax4.plot([], [], ' ', label="CI 2-1")
    ax4.legend(frameon=False,loc='upper right')
    
    plt.show()
    fig.savefig('bx610_1dspec.pdf') 
    plt.close()



.. parsed-literal::

    ['band4/co43/sci.fits', 'band4/ci10/sci.fits', '2015.1.00250.S/bb3.h2o/sci.fits', '2015.1.00250.S/bb2.co76ci21/sci.fits']



.. parsed-literal::

    <Figure size 432x288 with 0 Axes>



.. image:: demo_bx610_display_files/demo_bx610_display_5_2.png


