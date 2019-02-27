import glob
from astropy.wcs import WCS
from reproject import reproject_interp
from astropy.io import fits
import pprint
import numpy as np
from drizzle import drizzle
from drizzlepac import astrodrizzle
import pyfits
from drizzlepac import tweakreg

def bx610_drizzle(infiles='',outname='',fixheader=False,coeffs=True,
                  final_refimage='',
                  pipeline=True):
    """
    
    Data Quality:
    
        flc+AstroDrizzle (drc_sci) > flt+AstroDrizzle (drz_sci) > Drizzle > a "house" solution
    
    """
    flist=glob.glob(infiles)
    print("*"*100)
    print(flist,'-->',outname)
    print("*"*100)

    
    if  pipeline==False:
        
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
        fits.writeto(outname+'_quickmean.fits',stack,header,overwrite=True)

        #   direct drizzle solution
        
        hdulist=fits.open(flist[0])
        reference_wcs = WCS(hdulist[1].header)
        driz=drizzle.Drizzle(outwcs=reference_wcs)
        for flist0 in flist:
            driz.add_fits_file(flist0)
        driz.write(outname+'_drizzle.fits')

    
    #   the pipeline solution: astrodrizzle
    #   Note:
    #       ext: http://www.stsci.edu/hst/wfc3/documents/handbooks/currentDHB/Chapter2_data_structure2.html
    #       flc-fix: http://www.stsci.edu/hst/wfc3/documents/newsletters/STAN_10_11_2013
    #       http://www.stsci.edu/hst/HST_overview/drizzlepac/examples
    else:

        if  fixheader==True:
            if  'flc.fits' in infiles:
                for flist0 in flist:
                    flc = pyfits.open(flist0,mode='update')
                    del flc['sci',1].header['d2imdis*']
                    flc.close()
    
        astrodrizzle.AstroDrizzle(infiles,output=outname,coeffs=coeffs,
                                  static=True,skysub=True,driz_separate=True,
                                  #final_refimage=final_refimage,final_scale=0.06,
                                  final_wcs=True,final_rot=0)
        #updatewcs=True,coeffs=True
    
if  __name__=="__main__":
    
    ###bx610_drizzle(infiles='n9nh06*mos.fits',outname='p10924')
    ###bx610_drizzle(infiles='icjl08*drc.fits',outname='p13669')
    
    #"""
    #   p13669-f438w (WFC3/UVIS1)
    bx610_drizzle(infiles='p13669-f438w/icjl08*flc.fits',outname='stack_f438w')
    #   p13669-f814w (ACS/WFC)
    bx610_drizzle(infiles='p13669-f814w/jcjla8*flc.fits',outname='stack_f814w')
    #   p14620-f140w (WFC3/IR, no flt)
    bx610_drizzle(infiles='p14620-f140w/id7l04*flt.fits',outname='stack_f140w')
    #   p12578-f110w (WFC3/IR, no flt)
    bx610_drizzle(infiles='p12578-f110w/ibra20*flt.fits',outname='stack_f110w')
    #"""    
    
    #"""
    #   p10924-f160w 
    #bx610_drizzle(infiles='n9nh06*cal.fits',outname='stack_cal',coeffs=False) # okay
    bx610_drizzle(infiles='p10924-f160w/n9nh06*mos.fits',outname='stack_f160w',coeffs=False) # okay
    #bx610_drizzle(infiles='n9nh06*mos.fits',outname='stack_mos',pipeline=False) # okay
    #bx610_drizzle(infiles='n9nh06*cal.fits',outname='stack_cal',pipeline=False) # bad choice
    #"""
    
    """
    flist=['stack_f438w_drc_sci.fits','stack_f814w_drc_sci.fits']
    tweakreg.TweakReg(flist,
          imagefindcfg=     {'threshold':100, 'conv_width' : 3.5},
          refimagefindcfg=  {'threshold':100, 'conv_width' : 3.5},
          updatehdr=False, shiftfile=True, outshifts='shift.txt')    
    """
    
    
    
    """
    F160W->p10924_stack_drizzle.fits / p10924_stack_drc_sci.fits p10924_stack_mean.fits
    F140W->id7l04010_drz.fits
    F110W->ibra20010_drz
    F814W->jcjla8010_drc.fits
    F438W->p13669_stack_drizzle.fits / p13669_stack_drc_sci.fits p13669_stack_mean.fits
    """