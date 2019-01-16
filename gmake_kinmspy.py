from __future__ import print_function
from KinMS import KinMS
import numpy as np
from astropy.io import fits
import scipy.constants as const
import time

def gmake_kinmspy_api(objs,
                      outname=False,
                      verbose=False):
    """
    handle modeling parameters to kinmspy and generate the model cubes embeded into 
    a dictionary nest
    
    """
    
    models={}
    for tag in objs.keys():
        
        if  verbose==True:
            print("+"*40)
            print('@',tag)
            print("-"*40)
        
        obj=objs[tag]
        im,hd=fits.getdata(obj['image'],header=True)
        if  verbose==True:
            print(hd['NAXIS1'],hd['NAXIS2'],hd['NAXIS3'])
        psize=np.sqrt(np.abs(hd['CDELT1']*hd['CDELT2']))*3600.0         #   arcsec
        cdelt3=hd['CDELT3']     # hz or m/s
        crval3=hd['CRVAL3']     # hz or m/s
        crpix3=hd['CRPIX3']     # pix
        
        rfreq=obj['restfreq']/(1.0+obj['z'])                            #   GHz
        
        
        #   vector description of the z-axis: 
        #       vdelt3/vrval3/crpix3
        
        if  'Hz' in hd['CUNIT3']:   # by freq
            vdelt3=const.c*cdelt3/(1.0e9*rfreq)  #   m/s
            vdelt3=vdelt3/1000.0                                        #   km/s
            vrval3=const.c*((1.0e9*rfreq)-crval3)/(1.0e9*rfreq)
        else:                       # by velo
            vdelt3=cdelt3/1000.0
            vrval3=crval3
        
        if  verbose==True:
            print(psize,vdelt3,vrval3)
        
        xs=psize*hd['NAXIS1']
        ys=psize*hd['NAXIS2']
        vs=vsize*hd['NAXIS3']
        cellsize=psize
        dv=vdelt3
        
        beamsize=[0.2,0.2,0.]
        if  'BMAJ' in hd.keys():
            beamsize[0]=hd['BMAJ']
        if  'BMIN' in hd.keys():
            beamsize[0]=hd['BMIN']
        if  'BPA' in hd.keys():
            beamsize[0]=hd['BPA']                        
        if  verbose==True:
            print(beamsize)
        
        inc=obj['inc']
        gassigma=np.array(obj['vdis'])
        
        #print,hd['BMAJ']
        #print,hd['BMIN']
        #print,hd['BPA']
        
        sbrad=np.array(obj['radi'])
        sbprof=obj['sbexp'][0]*np.exp(-sbrad/obj['sbexp'][1])
        
        velrad=obj['radi']
        velprof=obj['vrot']
        posang=obj['pa']
        intflux=0.01
        filename='test'
        
        xypos=obj['xypos']
        restfreq=115.271e9
        restfreq=obj['restfreq']
        
        vsys=obj['vsys']
        
        fsys=(1.0-vsys/(const.c/1000.0))*rfreq # line systematic frequency in the observer frame
        
        
        #   ra    ----      xi_data     ----    (xSize-1.)/2.+phasecen[0]/cellsize
        #   dec   ----      yi_data     ----    (ySize-1.)/2.+phasecen[1]/cellsize
        #   vsys  ----      vi_data     ----    (vSize-1.)/2.+voffset/dv
        
        
        
        phasecen=[0.,0.]
        
        tic=time.time()
        
        xs=np.max(sbrad)*2.0*2.0
        ys=np.max(sbrad)*2.0*2.0
        vs=np.max(velprof)*1.5*2.0
        
        
        
        
        model=KinMS(xs,ys,vs,
                   cellSize=cellsize,dv=dv,
                   beamSize=beamsize,cleanOut=False,
                   inc=inc,gasSigma=gassigma,sbProf=sbprof,
                   sbRad=sbrad,velRad=velrad,velProf=velprof,
                   #nSamps=nsamps,
                   ra=xypos[0],dec=xypos[1],
                   restFreq=restfreq,vSys=vsys,phaseCen=phasecen,
                   fileName=outname+'_'+tag,
                   posAng=posang,
                   intFlux=intflux)
        print('Took {0} seconds to execute KinMSpy'.format(float(time.time()-tic)/float(1)))
        
        models[tag+'@'+obj['image']]=model
        
    return models
    
if  __name__=="__main__":

    objs=gmake_readpars('examples/bx610/bx610xy.inp',verbose=False)
    #gmake_listpars(objs)
    objs=gmake_fillpars(objs)
    gmake_listpars(objs)
    
    #tic=time.time()
    models=gmake_kinmspy_api(objs,outname='testexample')
    #print(models.keys())
    #print('Took {0} seconds to execute KinMSpy'.format(float(time.time()-tic)/float(1)))
          