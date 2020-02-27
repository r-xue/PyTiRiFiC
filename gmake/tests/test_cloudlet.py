from gmake.model import clouds_morph
from gmake.model import clouds_kin
from gmake.model import cr_tanh
from astropy.modeling.models import Sersic1D
import yt
import yt.units as unyt
from matplotlib import cm
from fast_histogram import histogram1d, histogram2d
import fast_histogram as fh
import adaptive
from gmake.stats import pdf2rv
from gmake.stats import custom_rvs
from gmake.stats import custom_pdf
from gmake.model import clouds_tosky
from gmake.model import cloudlet_moms
from gmake.model import clouds_discretize_2d
import time
from astropy.coordinates.matrix_utilities import rotation_matrix, matrix_product
import astropy.units as u
from astropy.coordinates.matrix_utilities import rotation_matrix,matrix_product,matrix_transpose
from astropy.coordinates.representation import SphericalRepresentation, CylindricalRepresentation, CartesianRepresentation
from astropy.coordinates.representation import SphericalDifferential, CylindricalDifferential, CartesianDifferential
import numpy as np
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.ticker as plticker
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.colors as colors
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"
mpl.rcParams['agg.path.chunksize'] = 10000
plt.rc('text', usetex=True)


def test_cloudlet_disk2d_plt3d(cloudlet_car,cloudlet_car_sky):
    
    #fig=plt.figure(figsize=(10,10))
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(cloudlet_car.x.to(u.kpc),cloudlet_car.y.to(u.kpc),cloudlet_car.z.to(u.kpc),
    #           alpha=0.5,marker='.',
    #           c=np.sqrt(cloudlet_car.differentials['s'].d_x**2+cloudlet_car.differentials['s'].d_y**2).value,
    #           cmap = cm.coolwarm)
    plt.clf()
    fig = plt.figure(figsize=(8,8))
    ax = fig.gca(projection='3d')
    ax.quiver(cloudlet_car.x.value,cloudlet_car.y.value,cloudlet_car.z.value,
          cloudlet_car.differentials['s'].d_x.value/50,
          cloudlet_car.differentials['s'].d_y.value/50,
          cloudlet_car.differentials['s'].d_z.value/50,
          arrow_length_ratio=0.3,color='r',
          linewidths=0.5,alpha=0.2)
    uu=cloudlet_car.differentials['s'].d_x.value
    vv=cloudlet_car.differentials['s'].d_y.value
    xx=cloudlet_car.x.value
    yy=cloudlet_car.y.value
    ax.set_xlabel('X [kpc]')
    ax.set_ylabel('Y [kpc]')
    ax.set_zlabel('Z [kpc]')
    ax.set_xlim(-50,50)
    ax.set_ylim(-50,50)
    ax.set_zlim(-1,+1)
    
    # azim and elev of camera location in respect to the original. 
    ax.view_init(azim=-90,elev=90)
    fig.tight_layout()
    fig.savefig('test_cloudlet_disk2d_plt3d_fig1.png')
    plt.close()
    
    #plt.clf()
    #fig=plt.figure(figsize=(10,10))
    #ax = fig.add_subplot(111, projection='3d')
    plt.clf()
    fig = plt.figure(figsize=(8,8))
    ax = fig.gca(projection='3d')
    
    ax.scatter(cloudlet_car_sky.x.to(u.kpc),
               cloudlet_car_sky.y.to(u.kpc),
               cloudlet_car_sky.z.to(u.kpc),
               alpha=0.5,marker='.',
               c=cloudlet_car_sky.differentials['s'].d_z.value,
               cmap = cm.coolwarm)
    
    ax.set_xlabel('X [kpc]')
    ax.set_ylabel('Y [kpc]')
    ax.set_zlabel('Z [kpc]')
    ax.set_xlim(-50,50)
    ax.set_ylim(-50,50)
    
    ax.view_init(azim=-90,elev=90)
    fig.tight_layout()
    fig.savefig('test_cloudlet_disk2d_plt3d_fig2.png') 
    plt.close()   
    
    #ax.view_init(45,90)
    #fig.savefig('test_cloudlet_v2.png')
    #ax.view_init(0,-90)
    #fig.savefig('test_cloudlet_v3.png')
    
    plt.close()
    
    return 




def test_clouds_morph():
    
    #r_eff=10*u.kpc
    #rmax=10*u.kpc
    #vmax=300*u.km/u.s
    #rcProf_r=np.arange(0.0,r_eff.value*10.0,r_eff.value/25.0)*r_eff.unit
    #rcProf_v=np.minimum(rcProf_r/rmax,1.)*vmax


    sbProf=('sersic2d',5*u.kpc,2)
    vbProf=('sech',1*u.kpc)
    rcProf=('rho : minimum(rho/p2,1.0)*p1',200*u.km/u.s,5*u.kpc)
        
    start_time = time.time()

    rotAz=('alpha',0*u.kpc,20*u.kpc,270*u.deg,-2.5)
    rotAz=('alpha',0*u.kpc,20*u.kpc,270*u.deg,0)
    rotAz=('log',0*u.kpc,20*u.kpc,270*u.deg,5*u.kpc)
    #bendY
    cloudlet_car,cloudlet_weights=clouds_morph(
                                    sbProf=sbProf,
                                    #fmPhi=(4,0.4,0*u.deg),
                                    rotPhi=rotAz,
                                    #bm=(2,1),
                                    sbQ=0.4,
                                    vbProf=vbProf,
                                    rcProf=rcProf,
                                    vSigma=None,vRadial=-80*u.km/u.s,subsize=1,
                                    seeds=[None,None,None,None],size=1000000)
    
    plt.clf()
    fig = plt.figure(figsize=(12,6)) 
    
    ###### Panel 1

    ax = fig.add_subplot(121)
    
    xx=cloudlet_car.x.value
    yy=cloudlet_car.y.value

    
    cloudlet_sb=custom_pdf(sbProf[0].replace('2d',''),
                           cloudlet_car.represent_as(CylindricalRepresentation).rho/sbProf[1],
                           sersic_n=sbProf[-1])    
    
    arr_scale=0.5

    ax.scatter(xx,yy,c=cloudlet_sb,cmap=cm.coolwarm,s=1.0,alpha=0.2)
    ax.set_xlabel(r'$x_{\rm gal}$ [kpc]')
    ax.set_ylabel(r'$y_{\rm gal}$ [kpc]')
    ax.set_xlim(-40,40)
    ax.set_ylim(-40,40) 
    
    ###### panel 2
    
    ax = fig.add_subplot(122)
    
    im_i=clouds_discretize_2d(cloudlet_car,
                                  axes=['y','x'],
                                  range=[[-40, 40], [-40, 40]], bins=[80-1,80-1],
                                  weights=None)
    
    ax.imshow(im_i,extent=([-40,40,-40,40]),
              norm=colors.SymLogNorm(linthresh=0.03, linscale=0.03,
                                     vmin=1, vmax=im_i.max()))
    ax.contour(im_i, colors='k', origin='image', extent=([-40,40,-40,40]))
    ax.set_xlim(-40,40)
    ax.set_ylim(-40,40)
    ax.set_xlabel(r'$x_{\rm gal}$ [kpc]')
    ax.set_ylabel(r'$y_{\rm gal}$ [kpc]')
    #ax.set_xlim(-30,30)
    #ax.set_ylim(-30,30)     

    
    fig.tight_layout()
    fig.savefig('test_clouds_morph.png') 
    plt.close(fig)     

def test_models():
    
    sbProf=('sersic2d',10*u.kpc,1)
    c0=0.0
    q=1.0
    
    x=np.linspace(-40,40,1000)*u.kpc
    y=np.linspace(-40,40,1000)*u.kpc
    xx,yy=np.meshgrid(x,y)
    
    re=1*u.kpc
    am=1.0
    m=3
    
    yy-=am*re*(xx/re)**m
    
    #yy+=am*(xx/r_e)**m
    
    
    #rho=(np.abs(xx)**(c0+2)+np.abs(yy/q)**(c0+2))**(1/(c0+2))
    rho=np.sqrt(xx**2+yy**2)
    
    
    #am=0.5
    #m=4
    #phim=10*u.deg
    #phi=np.arctan2(yy,xx/q)
    #rho*=(1+am*np.cos(m*(phi+phim)))
    
    sersic_n=1
    
    from scipy import special as sc
    bn=sc.gammaincinv(2*sersic_n, 0.5)
    #pdf=np.exp( -bn * ( (rho/r_e)**(1/sersic_n)-1 ) )    
    pdf=rho.value
    #pdf=np.minimum(rho.value,10)
    
    plt.clf()
    fig = plt.figure(figsize=(6,6)) 
    ax = fig.add_subplot(111)
    
    ax.imshow(pdf,extent=([-40,40,-40,40]))
    levels=np.linspace(1,40,40)
    ax.contour(pdf, levels, colors='k', extent=([-40,40,-40,40]))
    fig.tight_layout()
    fig.savefig('test_models.png') 
    plt.close() 
    
def test_clouds_morphi_cr_tanh():
    
    fig, ax = plt.subplots(1,1,figsize=(5,5))
    
    r=np.linspace(-100,200,300)*u.kpc
    theta_out=100*u.deg
    tanh_v=cr_tanh(r,r_in=-10*u.kpc,r_out=100*u.kpc,theta_out=theta_out)    
    ax.plot(r,tanh_v*theta_out)
    ax.plot([-100,200],[20,20])
    y0=20*u.deg
    r0=np.interp(y0,tanh_v*theta_out,r)
    print(r0)
    
    r=np.linspace(-100,200,300)*u.kpc
    theta_out=100*u.deg
    tanh_v=cr_tanh(r,r_in=-20*u.kpc,r_out=100*u.kpc,theta_out=theta_out)    
    ax.plot(r,tanh_v*theta_out)
    ax.plot([-100,200],[20,20])
    y0=20*u.deg
    r0=np.interp(y0,tanh_v*theta_out,r)
    print(r0)
    
    r=np.linspace(-100,200,300)*u.kpc
    theta_out=100*u.deg
    tanh_v=cr_tanh(r,r_in=30*u.kpc,r_out=100*u.kpc,theta_out=theta_out)    
    ax.plot(r,tanh_v*theta_out)
    ax.plot([-100,200],[20,20])
    y0=20*u.deg
    r0=np.interp(y0,tanh_v*theta_out,r)
    print(r0)    
    
    r=np.linspace(-100,200,300)*u.kpc
    theta_out=200*u.deg
    tanh_v=cr_tanh(r,r_in=30*u.kpc,r_out=150*u.kpc,theta_out=theta_out)    
    ax.plot(r,tanh_v*theta_out)
    ax.plot([-100,200],[20,20])
    y0=20*u.deg
    r0=np.interp(y0,tanh_v*theta_out,r)
    print(r0)     
    
    r=np.linspace(-100,200,300)*u.kpc
    theta_out=720*u.deg
    tanh_v=cr_tanh(r,r_in=30*u.kpc,r_out=150*u.kpc,theta_out=theta_out)    
    ax.plot(r,tanh_v*theta_out)
    ax.plot([-100,200],[20,20])
    y0=20*u.deg
    r0=np.interp(y0,tanh_v*theta_out,r)
    print(r0)     
    
    fig.savefig('test_clouds_morphi_cr_tanh.pdf')






def test_clouds_morph_kin_tosky_performance(size=10000):

    """
    test clouds_morph / clouds_kin / clouds_tosky and plot the results
    
    kernprof -l -v /Users/Rui/Resilio/Workspace/projects/GMaKE/gmake/tests/test_cloudlet.py
    with @profile dec for the testing function
    
    @ the header
    https://jakevdp.github.io/PythonDataScienceHandbook/01.07-timing-and-profiling.html
    """
    
    """
    generate the cloud set
    """
    
    sbProf=('sersic2d',10*u.kpc,2)
    vbProf=('sech',1*u.kpc)
    rotAz=('log',0*u.kpc,20*u.kpc,270*u.deg,5*u.kpc)
    sbQ=0.3
    
    start_time = time.time()    
    car,meta=clouds_morph(sbProf=sbProf,rotPhi=rotAz,sbQ=sbQ,
                        vbProf=vbProf,
                        seeds=[1,2,3],size=size)    
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_morph',time.time()-start_time))
    print(car.shape)
    
    
    """
    TEST clouds_kin()
    """    
    
    print("\n"*2)
    sbProf=('sersic2d',5*u.kpc,1)
    vbProf=('sech',1*u.kpc)
    rcProf=('rho : minimum(rho/p2,1.0)*p1',400*u.km/u.s,5*u.kpc)
    rcProf=('tanh',400*u.km/u.s,10*u.kpc)    
    

    print("\n"*2)
    start_time = time.time()
    car_k=clouds_kin(car,rcProf=rcProf,vRadial=-60*u.km/u.s,
                     vSigma=60*u.km/u.s,
                     seed=4,nV=30)    
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_kin',time.time()-start_time))
    print(car_k.shape)
    
    """
    TEST clouds_tosky()
    """
    
    print("\n"*2)
    pa=30*u.deg
    inc=45*u.deg

    car_nk=car_k.without_differentials()
    
    start_time = time.time()
    car_sky1=clouds_tosky(car_k,inc,pa,inplace=False)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_tosky',time.time()-start_time))
    print(car_k.xyz[:,0,0])
    print(car_sky1.xyz[:,0,0])
    print(car_k.differentials['s'].d_xyz[:,0,0])
    print(car_sky1.differentials['s'].d_xyz[:,0,0])
        
    
    start_time = time.time()
    car_sky2=clouds_tosky(car_nk,inc,pa,inplace=False)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_tosky',time.time()-start_time))    
    print(car_nk.xyz[:,0,0])
    print(car_sky2.xyz[:,0,0])
        
    start_time = time.time()
    clouds_tosky(car_k,inc,pa,inplace=True)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_tosky_inplace',time.time()-start_time))
    print(car_k.xyz[:,0,0])
    print(car_k.differentials['s'].d_xyz[:,0,0])
    
    start_time = time.time()
    clouds_tosky(car_nk,inc,pa,inplace=True)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_tosky_inplace',time.time()-start_time))     
    print(car_nk.xyz[:,0,0])


    return


def test_clouds_morph_kin_tosky_plt2d(size=10000):

    """
    test clouds_morph / clouds_kin / clouds_tosky and plot the results
    """
    
    """
    generate the cloud set
    """
    
    sbProf=('sersic2d',10*u.kpc,2)
    vbProf=('sech',1*u.kpc)
    rotAz=('log',0*u.kpc,20*u.kpc,270*u.deg,5*u.kpc)
    sbQ=0.3
    
    start_time = time.time()    
    car,meta=clouds_morph(sbProf=sbProf,rotPhi=rotAz,sbQ=sbQ,
                        vbProf=vbProf,
                        seeds=[None,None,None],size=size)    
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_morph',time.time()-start_time))
    print(car.shape)
    
    """
    attach kinmeatics info
    """    
    
    sbProf=('sersic2d',5*u.kpc,1)
    vbProf=('sech',1*u.kpc)
    rcProf=('rho : minimum(rho/p2,1.0)*p1',400*u.km/u.s,5*u.kpc)
    rcProf=('tanh',300*u.km/u.s,10*u.kpc)    
    
    start_time = time.time()
    car_k,meta_k=clouds_kin(car,return_meta=True,
                            rcProf=rcProf,vRadial=-100*u.km/u.s,
                            vSigma=60*u.km/u.s,
                            seed=None,nV=30)    
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_kin',time.time()-start_time))
    print(car_k.shape)
    
    
#             if  meta is not None:
#             meta_out={}
#             meta_out['weight']=np.broadcast_to(meta['weight'],(nV,size),subok=True)
#             meta_out['localSB']=np.broadcast_to(meta['localSB'],(nV,size),subok=True)
#             meta_out['v_ordered']=car_diff_ordered
#             meta_out['v_random']=car_diff_vdisp    
    
    start_time = time.time()
    pa=30*u.deg
    car_sky=clouds_tosky(car_k,45*u.deg,pa,inplace=False)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('clouds_tosky',time.time()-start_time))

    """
    plotting
    """
    plt.clf()
    fig = plt.figure(figsize=(12,4)) 
    
    ###### Panel 1
    
    ax = fig.add_subplot(131)
    arr_scale=0.5
    #(3,nv,nc)      
    ax.quiver(car_k.x.value,car_k.y.value,
              meta_k['v_random'].d_x.value/50,
              meta_k['v_random'].d_y.value/50 ,
              linewidths=0.3,alpha=0.5,
              units='x',scale=1/arr_scale,color='gray')
    #(3,nc)
    ax.quiver(car.x.value,car.y.value,
              meta_k['v_ordered'].d_x.value/50,
              meta_k['v_ordered'].d_y.value/50,
              meta['localSB'],
              linewidths=0.5,alpha=0.2,
              units='x',scale=1/arr_scale,
              cmap = cm.coolwarm)

    ax.scatter(car.x.value,car.y.value,c=meta['localSB'],cmap=cm.coolwarm,s=1.0,alpha=0.2)
    ax.set_xlabel(r'$x_{\rm gal}$ [kpc]')
    ax.set_ylabel(r'$y_{\rm gal}$ [kpc]')
    ax.set_xlim(-30,30)
    ax.set_ylim(-30,30) 

    
    ###### Panel 2

    ax = fig.add_subplot(132)
    axis_r=[-30,60] 
    ax.arrow(axis_r[0]*np.cos(90*u.deg+pa),axis_r[0]*np.sin(90*u.deg+pa),
             axis_r[1]*np.cos(90*u.deg+pa),axis_r[1]*np.sin(90*u.deg+pa),
             head_width=1, head_length=3,
             color='k',alpha=0.2)

    arr_scale=0.5
    ax.quiver(car_sky.x.value,car_sky.y.value,
              car_sky.differentials['s'].d_x.value/50,
              car_sky.differentials['s'].d_y.value/50,
              meta['localSB'][np.newaxis,:],    # broadcasted to (nv,nc)
              linewidths=0.5,alpha=0.2,
              units='x',scale=1/arr_scale,
              cmap = cm.coolwarm)
    ax.scatter(car_sky.x.value,car_sky.y.value,
               c=np.broadcast_to(meta['localSB'][np.newaxis,:],car_sky.shape),
               cmap=cm.coolwarm,s=1.0,alpha=0.2)
    ax.set_xlabel(r'$x_{\rm sky}$ [kpc]')
    ax.set_ylabel(r'$y_{\rm sky}$ [kpc]')
    ax.set_xlim(-30,30)
    ax.set_ylim(-30,30)

    
    ####### Panel 3
    
    ax = fig.add_subplot(133)
    
    ax.scatter(car_sky.x.to(u.kpc),
               car_sky.y.to(u.kpc),
               alpha=0.5,marker='.',
               c=car_sky.differentials['s'].d_z.value,
               cmap = cm.coolwarm)
    ax.set_xlabel(r'$x_{\rm pix}$ [kpc]')
    ax.set_ylabel(r'$y_{\rm pix}$ [kpc]')
    ax.set_xlim(-30,30)
    ax.set_ylim(-30,30) 
    
    print('saving....')
    fig.tight_layout()
    fig.savefig('test_clouds_morph_kin_tosky_plt2d.png') 
    plt.close()   
        
    
    return car,meta,car_k,meta_k,car_sky

def test_cloudlet_moms_plt2d(cloudlet,weights=None):   
    """
    """
    im_i,im_v,im_vsigma,im_ierr=cloudlet_moms(cloudlet,
                                              range=[[-40, 40], [-40, 40]], bins=[40-1,40-1],
                                              weights=weights)
        
    plt.clf()
    fig=plt.figure(figsize=(15,3))
    
    ax1 = fig.add_subplot(151)
    ax1.scatter(cloudlet.x,cloudlet.y,marker='.',alpha=0.2,s=0.5)
    ax1.set_xlim(-40,40)
    ax1.set_ylim(-40,40)
    
    ax2 = fig.add_subplot(152)
    ax2.imshow(im_i,extent=([-40,40,-40,40]))
    ax2.set_xlim(-40,40)
    ax2.set_ylim(-40,40)
    
    ax3 = fig.add_subplot(153)
    ax3.imshow(im_ierr,extent=([-40,40,-40,40]))    

    ax4 = fig.add_subplot(154)
    ax4.imshow(im_v,cmap=cm.coolwarm,extent=([-40,40,-40,40]))
    pt=np.nanpercentile(im_v,[0,25,50,75,100])
    print('im_v:pt',pt) 

    ax5 = fig.add_subplot(155)
    ax5.imshow(im_vsigma,extent=([-40,40,-40,40]))
    pt=np.nanpercentile(im_vsigma,[0,25,50,75,100])
    print('im_vsigma:pt',pt)  
    
    #im_sky_i[np.where(im_sky_i==0)]=1
    #np.seterr(divide='ignore')
    #im_sky=im_sky_iv/im_sky_i
    #np.seterr(divide=None)
    #np.seterr(invalid='ignore')
    #im_sky=im_sky_iv/im_sky_i
    #im_sky=im_sky_i
    #np.seterr(invalid=None)
    #xx=np.ravel(cloudlet.x.value)
    #yy=np.ravel(cloudlet.y.value)
    #if  weights is None:
    #    zz=None
    #else:
    #    zz=np.ravel(weights)
        
    #im_sky=fh.histogram2d(xx,yy,
    #                      weights=zz,
    #                      range=[[-40, 40], [-40, 40]], bins=[80,80])
    #im_sky,xedges,yedges=np.histogram2d(np.ravel(xx),np.ravel(yy), 
    #                                    weights=np.ravel(zz),
    #                                    range=[[-40, 40], [-40, 40]], bins=[9,9])
    
    
    fig.tight_layout()
    fig.savefig('test_cloudlet_moms_plt2d.png')
    plt.close()

    return


if  __name__=="__main__":
    
    #test_models() # ibsolete
    #test_cloudlet_disk2d_plt3d(cloudlet_car,cloudlet_car_sky)    # obselete
    #test_clouds_morph()
    #test_cr_tanh()
    #test_clouds_morph_kin_tosky_performance(size=100000)
    car,meta,car_k,meta_k,car_sky=test_clouds_morph_kin_tosky_plt2d(size=100000)
    if  meta['weight'] is None:
        im_sky=test_cloudlet_moms_plt2d(car_sky)
    else:
        im_sky=test_cloudlet_moms_plt2d(car_sky,
                                    weights=np.broadcast_to(meta['weight'][np.newaxis,:],car_sky.shape))












###############################################################################################

    """>>>>> Carterian Grid
    #require careful setup of grid
    
    r_eff=5*u.kpc
    n=1
    diskThick=0.1*u.kpc
    sbModel=Sersic1D(amplitude=1.0,r_eff=r_eff,n=n)
    
    sbRad=np.arange(0.0,r_eff.value*10.0,r_eff.value/3.0)*r_eff.unit
    #sbRad=np.arange(0.0,r_eff.value*10.0,r_eff.value/1.0)*r_eff.unit
    #sbProf=sbModel(sbRad)

    #0,5kpc resolution
    x_vec=np.linspace(-50,50,endpoint=False,num=600)*u.kpc
    y_vec=np.linspace(-50,50,endpoint=False,num=600)*u.kpc
    z_vec=np.linspace(-10,10,endpoint=False,num=10)*u.kpc
    z_vec=0*u.kpc
    xx,yy,zz=np.meshgrid(x_vec,y_vec,z_vec)
    rho=np.sqrt(xx**2+yy**2)

    sb=sbModel(rho)
    #print(xx.shape)
    mesh_car=CartesianRepresentation(xx,yy,zz)
    mesh_car_sky=clouds_tosky(mesh_car,45*u.deg,45*u.deg)

    test_cloudlet_gridding_plt2d(mesh_car_sky,weights=sb)
    """    
        
        
            
    """>>>>> Polar Grid
    
    r_eff=5*u.kpc
    n=1
    diskThick=0.1*u.kpc
    sbModel=Sersic1D(amplitude=1.0,r_eff=r_eff,n=n)
    
    sbRad=np.arange(0.0,r_eff.value*10.0,r_eff.value/10.0)*r_eff.unit
    #sbRad=np.arange(0.0,r_eff.value*10.0,r_eff.value/1.0)*r_eff.unit
    #sbProf=sbModel(sbRad)
    rho_vec=sbRad+(sbRad[1]-sbRad[0])/2.0
    phi_vec=np.linspace(0,360,endpoint=False,num=360)*u.deg
    rho,phi=np.meshgrid(rho_vec,phi_vec)

    sb=sbModel(rho)*sbRad
    z=rho*0.
    
    mesh_cyl=CylindricalRepresentation(rho,phi,z)
    mesh_car=mesh_cyl.represent_as(CartesianRepresentation)
    mesh_car_sky=clouds_tosky(mesh_car,45*u.deg,45*u.deg)

    test_cloudlet_gridding_plt2d(mesh_car_sky,weights=sb)
    
    """
    
    """>>>>> AMR Grid
    
    

    
    def sbModel_sampler(xy):
        
        r_eff=5*u.kpc
        n=1
        diskThick=0.1*u.kpc
        sbModel=Sersic1D(amplitude=1.0,r_eff=r_eff,n=n)
        x,y=xy
        rho=np.sqrt(x**2+yy**2)
        
        return sbModel(rho)
    
    
    #def complete_when(learner):
    #    return learner.npoints >= 600
    
    learner2d = adaptive.Learner2D(sbModel_sampler, [(-50, 50), (-50, 50)])
    #adaptive.runner.simple(learner, complete_when)
    #runner2d = adaptive.Runner(learner2d, goal=lambda l: l.npoints > 1000)
    
    #plot = learner.plot(tri_alpha=0.2)
    #runner.live_info()
    """

def test_cloudlet_disk2d_render():
    
    
    plt.clf()
    fig=plt.figure(figsize=(10,10))
    
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(cloudlet_car.x.to(u.kpc),cloudlet_car.y.to(u.kpc),cloudlet_car.z.to(u.kpc))
    ax.set_xlabel('X [kpc]')
    ax.set_ylabel('Y [kpc]')
    ax.set_zlabel('Z [kpc]')
    ax.set_xlim(-50,50)
    ax.set_ylim(-50,50)
    
    ax.view_init(90,90)
    fig.savefig('test_cloudlet_v1.png')
    
    ax.view_init(45,90)
    fig.savefig('test_cloudlet_v2.png')
    
    ax.view_init(0,90)
    fig.savefig('test_cloudlet_v3.png')
    
    plt.close()
    

    cloudlet_car=test_cloudlet_disk2d_gen()
    #"""
    ppx=cloudlet_car.x.to(u.kpc).value
    ppy=cloudlet_car.y.to(u.kpc).value
    ppz=cloudlet_car.z.to(u.kpc).value
    bbox = 1.1*np.array([[-100, 100],
                         [-100, 100],
                         [-100, 100]])
    #bbox = 1.1*[[np.min(ppx), np.max(ppx)], [np.min(ppy), np.max(ppy)], [np.min(ppz), np.max(ppz)]]
    data = dict(
            particle_position_x=ppx,
            particle_position_y=ppy,
            particle_position_z=ppz,
            particle_mass=np.ones(ppx.size))
    ds = yt.load_particles(data,length_unit=unyt.kpc,mass_unit=1*unyt.Msun,bbox=bbox)
    p=yt.ParticlePlot(ds, 'particle_position_x', 'particle_position_y', color='b')
    p.set_width(80, 'kpc')
    p.set_axes_unit('kpc')
    p.save('test_cloudlet_disk3d_faceon.png')
    
    obj = ds.arbitrary_grid([-50, -50, -5], [50, 50, 5],
                       dims=[256, 256, 25])
    tmp=obj["deposit", "all_density"]
    
    data=dict(density=(tmp.value,str(tmp.units)))
    print(tmp.value.shape)
    bbox = np.array([[-50, 50], [-50, 50], [-50, 50]])
    ds_grid=yt.load_uniform_grid(data,tmp.value.shape,length_unit='kpc',bbox=bbox)
    slc = yt.SlicePlot(ds_grid, "z", ["density"])
    slc.set_cmap("density", "Blues")
    slc.annotate_grids(cmap=None)
    slc.save('test_cloudlet_disk3d_faceon_slice.png')
    
    #im, sc = yt.volume_render(ds_grid, 'density', fname='rendering.png')
    
    # im is the image array generated. it is also saved to 'rendering.png'.
    # sc is an instance of a Scene object, which allows you to further refine
    # your renderings and later save them.
    
    # Let's zoom in and take a closer look
    #sc.camera.width = (50, 'kpc')
    #sc.camera.switch_orientation()
    
    # Save the zoomed in rendering
    #sc.save('zoomed_rendering.png')    
    
    
    sc = yt.create_scene(ds_grid, lens_type='perspective')
    
    # Get a reference to the VolumeSource associated with this scene
    # It is the first source associated with the scene, so we can refer to it
    # using index 0.
    source = sc[0]
    #source.set_log(True)
    # Set the bounds of the transfer function
    #source.set_log(True)
    
    vmax=np.max(tmp.value)
    vmin=vmax/1000.0
    #source.tfh.set_bounds((vmin, vmax))
    
    # set that the transfer function should be evaluated in log space
    source.tfh.set_log(True)
    
    # Make underdense regions appear opaque
    source.tfh.grey_opacity = True

    tf = yt.ColorTransferFunction((vmin, vmax),grey_opacity=True)

    def linramp(vals, minval, maxval):
        return (vals - vals.min())/(vals.max() - vals.min())

    #tf=transfer.add_layers(n_v, dv, colormap='RdBu_r')
    tf.map_to_colormap(vmin,vmax, colormap='arbre',scale_func=linramp)
    source.tfh.tf=tf
    source.tfh.bounds=(vmin,vmax)
    #sc.background_color = 'red'
    
    # save the image, flooring especially bright pixels for better contrast
    source.tfh.plot('transfer_function.png', profile_field='density')
    
    
    sc.camera.width = (30, 'kpc')
    #sc.camera.switch_orientation()
    sc.camera.position=np.array([0,0,20])
    sc.save('rendering.png', sigma_clip=6.0)    
    
    
    
    """
    sc = yt.create_scene(ds_grid,'density')
    #source = sc[0]
    n_v=10
    dv=0.2
    vmin=np.min(tmp.value)
    vmax=np.max(tmp.value)
    transfer = yt.ColorTransferFunction((vmin, vmax))
    transfer.add_layers(n_v, dv, colormap='RdBu_r')
         
    center=[0,0,0]
    direction = np.array([1.0, 0.0, 0.0])
    width=100
    size=1024
    camera = sc.camera
    camera.width=
    
    (center, direction, width, size, transfer,
                   fields=['density'])
    snapshot = camera.snapshot()
    write_bitmap(snapshot, 'cube_rendering.png', transpose=True) 
    """   
    
    # Set the bounds of the transfer function
    #source.tfh.set_bounds((3e-31, 5e-27))
    
    # set that the transfer function should be evaluated in log space
    #source.tfh.set_log(True)
    
    # Make underdense regions appear opaque
    #source.tfh.grey_opacity = True
    
    # Plot the transfer function, along with the CDF of the density field to
    # see how the transfer function corresponds to structure in the CDF
    #source.tfh.plot('transfer_function.png', profile_field='density')
    
    # save the image, flooring especially bright pixels for better contrast
    #sc.save('rendering.png')


    #sc = yt.create_scene(ds)
    
    #print(obj["deposit"])
    #p=yt.ParticlePlot(ds, 'particle_position_z', 'particle_position_x', color='b')
    #p.set_width(80, 'kpc')
    #p.set_axes_unit('kpc')
    #p.save('test_cloudlet_disk3d_edgeon.png')
    
    """
    ad = ds.all_data()
    # This is generated with "cloud-in-cell" interpolation.
    cic_density = ad["deposit", "all_cic"]
    
    # These three are based on nearest-neighbor cell deposition
    nn_density = ad["deposit", "all_density"]
    nn_deposited_mass = ad["deposit", "all_mass"]
    particle_count_per_cell = ad["deposit", "all_count"]    
    
    slc = yt.SlicePlot(ds, 2, ('deposit', 'all_cic'))
    slc.set_width((80, 'kpc'))
    slc.save('test_cloudlet_disk3d_faceon_slc.png')
    """
    
    #"""
    
#     import numpy as np
#     n_particles = 5000000
#     ppx, ppy, ppz = 1e6*np.random.normal(size=[3, n_particles])
#     ppm = np.ones(n_particles)
#     data = {'particle_position_x': ppx,
#         'particle_position_y': ppy,
#         'particle_position_z': ppz,
#         'particle_mass': ppm}
#     from yt.units import parsec, Msun
#     bbox = 1.1*np.array([[min(ppx), max(ppx)], [min(ppy), max(ppy)], [min(ppz), max(ppz)]])
#     ds = yt.load_particles(data, length_unit=parsec, mass_unit=1e8*Msun, n_ref=256, bbox=bbox)
#     p=yt.ParticlePlot(ds, 'particle_position_x', 'particle_position_y', color='b')
#     p.save()



    
    
        #print(cloudlet_car_sky)
    #print(cloudlet_car_sky.differentials)
    
    #test_cloudlet_disk2d_mplot3d(cloudlet_car_sky)
    
    
    #cloudlet_cyl=cloudlet_car.represent_as(CylindricalRepresentation)
    
    #d_phi=(200*u.km/u.s/cloudlet_cyl.rho*u.rad).to(u.rad/u.s)
    #cloudlet_cyldiff=CylindricalDifferential(np.zeros(100000)*u.km/u.s,
                                             #d_phi,
                                             #np.zeros(100000)*u.km/u.s)
    
    
    
    #print(cloudlet_cyl)
    #cloudlet_car=cloudlet_cyl_withdiff.represent_as(CartesianRepresentation,differential_class=CartesianDifferential)
    #
    #cloudlet_cardiff=cloudlet_cyldiff.to_cartesian(base=cloudlet_cyl) 
    

    
    