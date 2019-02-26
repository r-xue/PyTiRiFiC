import glob
from astropy.wcs import WCS
from reproject import reproject_interp
from astropy.io import fits
import pprint
import numpy as np
from drizzle import drizzle
from drizzlepac import astrodrizzle
import pyfits

def bx610_drizzle(infiles='',outname=''):
    """
    
    Data Quality:
    
        flc+AstroDrizzle (drc_sci) > flt+AstroDrizzle (drz_sci) > Drizzle > a "house" solution
    
    """
    flist=glob.glob(infiles)
    print("*"*100)
    print(flist,'-->',outname)
    print("*"*100)
    
    #   quick solution
    
    if  not ('flt.fits' in infiles or 'flc.fits' in infiles) :
        
        #   reproject+meanstack
        
        stack=[]
        data,header=fits.getdata(flist[0],header=True,memmap=False)
        stack=[data]
        for i in range(1,len(flist)):
            olddata,oldheader=fits.getdata(flist[i],header=True,memmap=False)
            newdata,footprint=reproject_interp((olddata,oldheader), header)
            #fits.writeto(flist[i].replace('.fits','_reproj.fits'),newdata,header,overwrite=True)
            stack+=[newdata.copy()]
        #pprint.pprint(stack)
        stack=np.array(stack)
        stack=np.mean(stack,axis=0)
        fits.writeto(outname+'_stack_quickmean.fits',stack,header,overwrite=True)

        #   direct drizzle solution
        
        hdulist=fits.open(flist[0])
        reference_wcs = WCS(hdulist[1].header)
        driz=drizzle.Drizzle(outwcs=reference_wcs)
        for flist0 in flist:
            driz.add_fits_file(flist0)
        driz.write(outname+'_stack_drizzle.fits')

    
    #   the pipeline solution: astrodrizzle
    #   Note:
    #       ext: http://www.stsci.edu/hst/wfc3/documents/handbooks/currentDHB/Chapter2_data_structure2.html
    #       flc-fix: http://www.stsci.edu/hst/wfc3/documents/newsletters/STAN_10_11_2013
    if  'flt.fits' in infiles or 'flc.fits' in infiles:
        if  'flc.fits' in infiles:
            for flist0 in flist:
                flc = pyfits.open(flist0,mode='update')
                del flc['sci',1].header['d2imdis*']
                flc.close()
        astrodrizzle.AstroDrizzle(infiles,output=outname+'_stack',updatewcs=True,coeffs=True) 
        
    
if  __name__=="__main__":
    
    #bx610_comb(infiles='n9nh06*mos.fits',outname='p10924')
    #bx610_comb(infiles='icjl08*drc.fits',outname='p13669')
    bx610_drizzle(infiles='icjl08*flc.fits',outname='p13669')
    
    """
    F160W->p10924_stack_drizzle.fits / p10924_stack_drc_sci.fits p10924_stack_mean.fits
    F140W->id7l04010_drz.fits
    F110W->ibra20010_drz
    F814W->jcjla8010_drc.fits
    F438W->p13669_stack_drizzle.fits / p13669_stack_drc_sci.fits p13669_stack_mean.fits
    """