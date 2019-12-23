from .utils import *
from .model_func_kinms import *
from .model_func import *

from galario.single import sampleImage

from io import StringIO
from asteval import Interpreter
import astropy.units as u
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
aeval = Interpreter(err_writer=StringIO())
aeval.symtable['u']=u
aeval.symtable['SkyCoord']=SkyCoord

from sys import getsizeof
from .utils import human_unit
from .utils import human_to_string

import scipy.constants as const
from astropy.modeling.models import Gaussian2D
from astropy.modeling.models import Sersic1D
from astropy.modeling.models import Sersic2D
from astropy.convolution import discretize_model
from astropy.wcs import WCS

from copy import deepcopy

from scipy.interpolate import interp1d

from astropy.wcs.utils import proj_plane_pixel_area, proj_plane_pixel_scales
import numexpr as ne
import fast_histogram
import time
#import gc

from memory_profiler import profile

    
@profile    
def model_disk2d2(header,objp,
                  model=[],
                  factor=5):
    """
    insert a continuum model (frequency-independent) into a 2D image or 3D cube
    
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
    
    return model in units of Jy/pix  
    
    note:    now we return model in the native forms rather than gridded cubes (which can be large)
    return form (componnet_name,im2d,scaling_vector,ox,oy mapping to fudicual grid)
    
    """

    obj=obj_defunit(objp)
    
    #   translate to dimensionless numerical value in default units

    ra=obj['xypos'][0]
    dec=obj['xypos'][1]
    r_eff=obj['sbser'][0]
    n=obj['sbser'][1]
    posang=obj['pa']
    ellip=1.-np.cos(np.deg2rad(obj['inc']))
    pintflux=0.0
    if  'pcontflux' in obj:
        pintflux=obj['pcontflux']    
    intflux=obj['contflux']
    restfreq=obj['restfreq']
    alpha=3.0
    if  'alpha' in obj:
        alpha=obj['alpha']
    
    #   build objects
    #   use np.meshgrid and don't worry about transposing
    w=WCS(header)
    cell=np.mean(proj_plane_pixel_scales(w.celestial))*3600.0
    #px,py=skycoord_to_pixel(SkyCoord(ra,dec,unit="deg"),w,origin=0) # default to IRCS
    px,py,pz,ps=(w.wcs_world2pix(ra,dec,0,0,0))
    vz=np.arange(header['NAXIS3'])
    wz=(w.wcs_pix2world(0,0,vz,0,0))[2]

    #   get 2D disk model
    mod = Sersic2D(amplitude=1.0,r_eff=r_eff/cell,n=n,x_0=px,y_0=py,
               ellip=ellip,theta=np.deg2rad(posang+90.0))
    xs_hz=int(r_eff/cell*7.0)
    ys_hz=int(r_eff/cell*7.0)
    #   use discretize_model(mode='oversample') 
    #       discretize_model(mode='center') or model2d=mod(x,y) may lead worse precision
    
    #   x,y = np.meshgrid(np.arange(header['NAXIS1']), np.arange(header['NAXIS2']))
    #   model2d=mod(x,y)

    #   intflux at different planes / broadcasting to the data dimension
    intflux_z=(wz/1e9/restfreq)**alpha*intflux    
    
    #option 1
    
    px_o_int=round(px-xs_hz)
    py_o_int=round(py-ys_hz)
    model2d=discretize_model(mod,
                             (px_o_int,px_o_int+2*xs_hz+1),
                             (py_o_int,py_o_int+2*ys_hz+1),
                             mode='oversample',factor=factor)
    model2d/=model2d.sum()
    print('2d',get_obj_size(model2d,to_string=True))
    #model2d=model2d[np.newaxis,np.newaxis,:,:]*intflux_z[np.newaxis,:,np.newaxis,np.newaxis]
    
    #component=
    model.append(('disk2d',model2d,intflux_z,int(px_o_int),int(py_o_int)))
    if  pintflux!=0.0:        
        model.append(('disk2d',np.ones((1,1)),(wz/1e9/restfreq)**alpha*pintflux,int(np.round(px)),int(np.round(py))))
    
    return 

def model_disk3d2(header,objp,
                 model=[],
                 nsamps=100000,decomp=False,fixseed=False,
                 verbose=False,
                 mod_dct=None):
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
    #   follow the convention / units defined in WCS:
    #   https://arxiv.org/pdf/astro-ph/0207407.pdf
    #   http://dx.doi.org/10.1051/0004-6361/201015362
    #   https://www.atnf.csiro.au/people/mcalabre/WCS/wcslib/wcsunits_8h.html#a25ba0f0129e88c6e7c74d4562cf796cd
    
    
    
    obj=obj_defunit(objp)
    #pprint(obj)
    
    w=WCS(header)
    if  'Hz' in header['CUNIT3']:
        wz=obj['restfreq']*1e9/(1.0+obj['z'])*(1.-obj['vsys']*1e3/const.c)
        dv=-const.c*header['CDELT3']/(1.0e9*obj['restfreq']/(1.0+obj['z']))/1000.
    if  'angstrom' in header['CUNIT3']:
        wz=obj['restwave']*(1.0+obj['z'])*(1.+obj['vsys']*1e3/const.c)/1e10
        dv=const.c*header['CDELT3']/(obj['restwave']*(1.0+obj['z']))/1000.
    if  'm/s' in header['CUNIT3']:
        wz=obj['vsys']*1000.
        dv=header['CDELT3']/1000.        
    #   wz: in hz / m or m.s
    #   dv: km/s
    
    #   get 0-based pix-index
    if  w.naxis==4:
        px,py,pz,ps=w.wcs_world2pix(obj['xypos'][0],obj['xypos'][1],wz,1,0)
    if  w.naxis==3:
        px,py,pz=w.wcs_world2pix(obj['xypos'][0],obj['xypos'][1],wz,0)
    #print(wz)
    #print(">>>>>>",(0,px,py,pz))
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

    nsamps=int(nsamps)
    if  fixseed==True:
        seeds=[100,101,102,103]
    else:
        seeds=np.random.randint(0,100,4)
        # seeds[0] -> rad
        # seeds[1] -> phi
        # seeds[2] -> z
        # seeds[3] -> v_sigma    
    
    if  obj['pmodel'] is None:
        inclouds,prof1d=model_disk3d_inclouds(obj,seeds,nSamps=nsamps)
        rad=np.arange(0.,obj['sbser'][0]*7.0,obj['sbser'][0]/25.0)
    else:
        inclouds,prof1d=model_disk3d_inclouds_pmodel(obj,seeds,nSamps=nsamps)
        rad=np.arange(0.,np.nanmax(np.sqrt(inclouds[:,0]**2+inclouds[:,1]**2))+obj['sbser'][0]/25.0,obj['sbser'][0]/25.0)
    
    ikind='cubic'  # bad for extraplate but okay for interplate 'linear'/'quadratic'

    if  isinstance(obj['vrot'], (list, np.ndarray)):
        if_vrot=interp1d(np.array(obj['vrad']),np.array(obj['vrot']),kind=ikind,bounds_error=False,fill_value=(obj['vrot'][0],obj['vrot'][-1]))
        velprof=if_vrot(rad)
    if  isinstance(obj['vrot'], tuple):
        if  obj['vrot'][0].lower()=='dynamics':
            velprof=model_dynamics(obj,mod_dct[obj['vrot'][1]],rad)
        elif  obj['vrot'][0].lower()=='arctan':
            velprof=obj['vrot'][1]*2.0/np.pi*np.arctan(rad/obj['vrot'][2])
        elif  obj['vrot'][0].lower()=='exp':
            velprof=obj['vrot'][1]*(1-np.exp(-rad/obj['vrot'][2]))
        elif  obj['vrot'][0].lower()=='tanh':
            velprof=obj['vrot'][1]*np.tanh(rad/obj['vrot'][2])
        else:
            for ind in range(1,len(obj['vrot'])):
                aeval.symtable["p"+str(ind)]=obj['vrot'][ind]
                aeval.symtable["vrad"]=rad
            velprof=aeval(obj['vrot'][0])
    
    if  isinstance(obj['vdis'], (list, tuple, np.ndarray)):
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
    #print(obj)
    #print(cell,xs,ys,vs)
    clouds=KinMS2(xs,ys,vs,
               cellSize=cell,dv=abs(dv),
               beamSize=1.0,cleanOut=True,
               inc=obj['inc'],
               #sbProf=sbprof,sbRad=sbrad,
               inClouds=inclouds,
               velRad=rad,velProf=velprof,gasSigma=gassigma,
               #ra=obj['xypos'][0],dec=obj['xypos'][1],restFreq=obj['restfreq'],
               vSys=obj['vsys'],
               phaseCen=phasecen,vOffset=voffset,
               #phaseCen=[0,0],vOffset=0,
               fixSeed=fixseed,
               #nSamps=nsamps,fileName=outname+'_'+tag,
               posAng=obj['pa'],
               intFlux=obj['lineflux'])
    
    int(pz_o_int),int(py_o_int),int(px_o_int)
    
    model.append(('disk3d',)+clouds+(int(px_o_int),int(py_o_int),int(pz_o_int)))

    
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

    return model_prof
                             

#@profile
def model_uvchi2(imodel,xyheader,
                    uvdata,uvw,phasecenter,uvweight,
                    average=True,verbose=True):
    """
    simulate the observation in the UV-domain
    The input reference 2D / 3D model (e.g. continuume+line) is expected in units of Jy/pix
    
    uvw shape:           nrecord x 3  
    uvmodel shape:       nrecord x nchan (less likely: nrecord x nchan x ncorr)
    xymodel shape:       nstokes x nchan x ny x nx
    
    note1:
        Because sampleImaging() can be only applied to single-wavelength dataset, we have to loop over
        all channels for multi-frequency dataset (e.g. spectral cubes). This loop operations is typically
        the bottle-neck. To reduce the number of operation, we can only do uvsampling for frequency-plane
        with varying morphology and process frequency-inpdent emission using one operation:  
        the minimal number of operations required  is:
                nplane(with varying morphology) + 1 x sampleImage()
          we already trim any else overhead (e.g. creating new array) and reach close to this limit.
    
    note2:
        when <uvmodel> is provided as input, a new model will be added into the array without additional memory usage 
          the return variable is just a reference of mutable <uvmodel>

    """

    #print('3d:',imodel is not None)
    #print('2d:',xymod2d is not None)
    
    cell=np.sqrt(abs(xyheader['CDELT1']*xyheader['CDELT2']))
    nchan=xyheader['NAXIS3']
    nrecord=(uvw.shape)[0]
    
    # + zeros_like vs. zeros()
    #   the memory of an array created by zeros() can allocated on-the-fly
    #   the creation will appear to be faster but the looping+plantu initialization may be slightly slower (or comparable?) 
    # + set order='F' as we want to have quick access to each column:
    #   i.a. first dimension is consequential in memory 
    #   this will improve on the performance of picking uvdata from each channel  
    # we force order='F', so the first dimension is continiuous and we can quicky fetch each channel
    # as the information in a single channel is saved in a block  


    if  verbose==True:
        start_time = time.time()
        print('nchan,nrecord:',nchan,nrecord)    
            
    # assume that CRPIX1/CRPIX2 is at model image "center" floor(naxis/2);
    # which is true for the mock-up/reference model image xyheader 
    # more information on the pixel index /ra-dec mapping, see:
    #       https://mtazzari.github.io/galario/tech-specs.html     
    #dRA=np.deg2rad(+(xyheader['CRVAL1']-phasecenter[0].to_value(u.deg)))
    #dDec=np.deg2rad(+(xyheader['CRVAL2']-phasecenter[1].to_value(u.deg)))
    
    dRA=np.deg2rad(+(xyheader['CRVAL1']-phasecenter[0].to_value(u.deg)))
    dDec=np.deg2rad(+(xyheader['CRVAL2']-phasecenter[1].to_value(u.deg)))
    #print('<--',dRA,dDec)
    
    phasecenter_sc = SkyCoord(phasecenter[0], phasecenter[1], frame='icrs')
    refimcenter_sc = SkyCoord(xyheader['CRVAL1']*u.deg,xyheader['CRVAL2']*u.deg, frame='icrs')
    dra, ddec = phasecenter_sc.spherical_offsets_to(refimcenter_sc)    
    dRA=dra.to_value(u.rad)
    dDec=ddec.to_value(u.rad)
    #print('-->',dRA,dDec)
    
    cc=0
    chi2=0

    for i in range(nchan):
        
        wv=const.c/(xyheader['CDELT3']*i+xyheader['CRVAL3'])
        cc+=1
        plane=np.zeros((xyheader['NAXIS2'],xyheader['NAXIS1']),dtype=np.float32)
        
        for j in range(len(imodel)):
            if  imodel[j][0]=='disk3d':
                model_type,clouds2do,xSize,ySize,vSize,scale,px_o_int,py_o_int,pz_o_int=imodel[j]
                #plane0,edges=np.histogramdd(clouds2do[subs,:],bins=(xSize,ySize,1),range=((0,xSize),(0,ySize),(j,j+1)))
                #subs=np.where( ne.evaluate('(a>=i) & (a<i+1)',local_dict={'a':clouds2do[:,2],'i':i}) )
                subs=np.where( (clouds2do[:,2]>=i) & (clouds2do[:,2]<i+1) )
                if  len(subs[0])>0:
                    #plane0,xedges,yedges=np.histogram2d(clouds2do[subs[0],0],clouds2do[subs[0],1],
                    #                                bins=[xSize,ySize],range=[[0,xSize],[0,ySize]])
                    plane0=fast_histogram.histogram2d(clouds2do[subs[0],0],clouds2do[subs[0],1],
                                                      bins=[int(xSize),int(ySize)],
                                                      range=[[0,xSize],[0,ySize]])
                    #print(plane.shape,plane0.shape,py_o_int,px_o_int)                            
                    plane=paste_array(plane,plane0*scale,(py_o_int,px_o_int),method='add')
            if  imodel[j][0]=='disk2d':
                model_type,model2d,intflux_z,px_o_int,py_o_int=imodel[j]
                model2d*=intflux_z[j]
                plane=paste_array(plane,model2d,(py_o_int,px_o_int),method='add') 
        if  np.sum(plane)!=0:        
            delta_uv=ne.evaluate('a-b',
                             local_dict={'a':sampleImage(plane,
                                                    (np.deg2rad(cell)).astype(np.float32),
                                                    (uvw[:,0]/wv),
                                                    (uvw[:,1]/wv),                                   
                                                    dRA=dRA,dDec=dDec,
                                                    PA=0.,check=False,origin='lower'),
                                         'b':uvdata[:,i]})
            chi2+=ne.evaluate('sum( ( (a.real)**2+(a.imag)**2 ) *c)', #'sum( abs(a)**2*c)'
                             local_dict={'a':delta_uv,
                                         'c':uvweight})
                
    return chi2


    
if  __name__=="__main__":

    """
    examples
    """
    pass
