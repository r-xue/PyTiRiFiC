
from gmake.model import clouds_kin
from gmake.model import clouds_morph
from gmake.model import clouds_tosky
from gmake.model import cloudlet_moms
from gmake.model import clouds_discretize_2d
import time
from astropy.coordinates.matrix_utilities import rotation_matrix, matrix_product
import astropy.units as u

from astropy.coordinates.matrix_utilities import rotation_matrix,matrix_product,matrix_transpose
from astropy.coordinates.representation import SphericalRepresentation, CylindricalRepresentation, CartesianRepresentation
from astropy.coordinates.representation import SphericalDifferential, CylindricalDifferential, CartesianDifferential

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from mpl_toolkits.mplot3d import Axes3D

mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"
mpl.rcParams['agg.path.chunksize'] = 10000
plt.rc('text', usetex=True)

from matplotlib import cm

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

def cuboid_data(center, size):
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the (left, outside, bottom) point
    o = [a - b / 2 for a, b in zip(center, size)]
    # get the length, width, and height
    l, w, h = size
    x = np.array([[o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in bottom surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in upper surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in outside surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]])  # x coordinate of points in inside surface
    y = np.array([[o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in bottom surface
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in upper surface
         [o[1], o[1], o[1], o[1], o[1]],          # y coordinate of points in outside surface
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]])    # y coordinate of points in inside surface
    z = np.array([[o[2], o[2], o[2], o[2], o[2]],                        # z coordinate of points in bottom surface
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],    # z coordinate of points in upper surface
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],                # z coordinate of points in outside surface
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]])                # z coordinate of points in inside surface
    return x, y, z

if __name__ == '__main__':
    """
    Special Note:
        All plotting happens in the mplot3d coordinate system or x/y/z-canvas
        howerver, there are mutiple user-defined coordiante system here:
            x/y/z-gal
            x/y/z-sky
            x/y/z-celestial (RA/DEC/LOS)
            x/y/z-pixel
        select wisely!
    """
    
    fig = plt.figure(figsize=(10,10))
    #ax = fig.add_subplot(111, projection='3d')
    ax=fig.gca(projection='3d')
    
    bsize=1
    ax.set_xlabel(r'$x_{\rm canvas}$')
    ax.set_xlim3d(0, bsize*4)
    ax.set_ylabel(r'$y_{\rm canvas}$')
    ax.set_ylim3d(-bsize*2.0, bsize*2.0)
    ax.set_zlabel(r'r$z_{\rm canvas}$')
    ax.set_zlim3d(-bsize*2.0, bsize*2.0)
    #ax.auto_scale_xyz([0, bsize*5], [-bsize*2, bsize*2.0], [-bsize*1.0, -bsize*1.0])
    ax.view_init(20,-50)
    ax.dist=7.5
    
    arrow_prop_dict = dict(mutation_scale=20, arrowstyle='->', shrinkA=0, shrinkB=0)

    dim=0.75
    inc=-40*u.deg
    
    y_gal, z_gal = np.meshgrid([-dim*np.cos(inc), dim*np.cos(inc)], [-dim, dim])
    x_gal = -y_gal*np.tan(inc)
    y_sky, z_sky = y_gal, z_gal
    x_sky = x_gal*0.0
    y_sky_top=y_sky*1.0
    y_sky_top[y_sky_top>0]=0
    y_sky_bot=y_sky*1.0
    y_sky_bot[y_sky_bot<0]=0
   
    
    # for galactic plane
    # for skyplane (far/near) # align with the y-z plane
    ax.plot_surface(x_sky+0.0, y_sky_bot, z_sky, color='blue', alpha=.3, linewidth=0)
    #ax.plot_surface(x_sky+0.0, y_sky, z_sky, color='blue', alpha=.2, linewidth=0, zorder=-1)    
    ax.plot_surface(x_gal, y_gal, z_gal, color='red', alpha=.3, linewidth=0) 
    #ax.plot_surface(x_sky+0.0, y_sky, z_sky, color='blue', alpha=.5, linewidth=0, zorder=10)


    # intersection line between galactic and sky plane
    
    #ax.plot([0,0],[0,0],[-1.5*bsize,1.5*bsize],linestyle='--',color='blue',alpha=0.4)
    ax.plot([0,0],[0,0],[-1.5*bsize,1.5*bsize],linestyle='-',color='k',linewidth=0.5)    
    ax.plot([2.0,2.0],[0,0],[-1.5*bsize,1.5*bsize],linestyle='-',color='k',linewidth=0.5)
    ax.plot([4.0,4.0],[0,0],[-1.5*bsize,1.5*bsize],linestyle='-',color='k',linewidth=0.5,zorder=50)   
    
    #ax.plot([0,0],[-1.5*bsize,1.5*bsize],[0,0],linestyle='-',color='k',linewidth=0.5)    
    #ax.plot([2.0,2.0],[-1.5*bsize,1.5*bsize],[0,0],linestyle='-',color='k',linewidth=0.5)
    #ax.plot([4.0,4.0],[-1.5*bsize,1.5*bsize],[0,0],linestyle='-',color='k',linewidth=0.5,zorder=50)        
    
    # xyz-axes for galactic plane
    axis_len=1.10
    a = Arrow3D([0, 0], [0, 0], [0, axis_len], **arrow_prop_dict, color='red',linewidth=1.5)
    ax.add_artist(a)
    ax.scatter(0,0,0,color='red')
    ax.text(0, 0, axis_len*1.1, r'$y_{\rm gal}$',color='red')
    
    a = Arrow3D([0, axis_len*np.cos(inc)], [0, axis_len*np.sin(inc)], [0, 0], **arrow_prop_dict, color='red',linewidth=1.5)
    ax.add_artist(a)
    ax.scatter(0,0,0,color='red')
    ax.text(axis_len*1.2*np.cos(inc), axis_len*1.2*np.sin(inc), 0, r'$z_{\rm gal}$',color='red')
    
    inc_step=np.linspace(0,inc,100)
    ax.plot(axis_len*0.7*np.cos(inc_step),axis_len*0.7*np.sin(inc_step),np.zeros(100),color='red')
    ax.text(axis_len*0.7*np.cos(inc_step[50]),axis_len*0.7*np.sin(inc_step[50]),0.02,r'$i$',color='red')
              
    a = Arrow3D([0, -axis_len*np.sin(inc)], [0, +axis_len*np.cos(inc)], [0, 0], **arrow_prop_dict, color='red',linewidth=1.5)
    ax.add_artist(a)
    ax.scatter(0,0,0,color='red')
    ax.text(-axis_len*0.90*np.sin(inc), +axis_len*0.90*np.cos(inc), axis_len*0.05, r'$x_{\rm gal}$',color='red')     
    
    ax.plot_surface(x_sky+0.0, y_sky_top, z_sky, color='blue', alpha=0.3, linewidth=0,zorder=10)
    #ax.plot([2.0,2.0],[0,0],[-1.5*bsize,1.5*bsize],linestyle='--',color='red',alpha=0.4)      
    
    # LOS guideline
        
    ax.plot([0-dim*np.sin(inc)*0.0,4.0],[dim*np.cos(inc),dim*np.cos(inc)],[dim,dim],color='k',linestyle='--',zorder=50)
    #ax.plot([0,2.0],[dim*np.cos(inc),dim*np.cos(inc)],[0,0],color='k',linestyle=':')
    ax.plot([0-dim*np.sin(inc)*0.0,4.0],[dim*np.cos(inc),dim*np.cos(inc)],[-dim,-dim],color='k',linestyle='--',zorder=50)
    #ax.plot([0-dim*np.sin(inc)*1.0,0.0],[dim*np.cos(inc),dim*np.cos(inc)],[dim,dim],color='k',linestyle=':')
    #ax.plot([0,2.0],[dim*np.cos(inc),dim*np.cos(inc)],[0,0],color='k',linestyle=':')
    #ax.plot([0-dim*np.sin(inc)*1.0,0.0],[dim*np.cos(inc),dim*np.cos(inc)],[-dim,-dim],color='k',linestyle=':')
    
    ax.plot([0+dim*np.sin(inc)*0.0,4.0],[-dim*np.cos(inc),-dim*np.cos(inc)],[dim,dim],color='k',linestyle='--',zorder=50)
    #ax.plot([0+dim*np.sin(inc),2.0],[-dim*np.cos(inc),-dim*np.cos(inc)],[0,0],color='k',linestyle=':',zorder=10)  
    ax.plot([0+dim*np.sin(inc)*0.0,4.0],[-dim*np.cos(inc),-dim*np.cos(inc)],[-dim,-dim],color='k',linestyle='--',zorder=50)
    ax.plot([0+dim*np.sin(inc)*1.0,0],[-dim*np.cos(inc),-dim*np.cos(inc)],[dim,dim],color='k',linestyle=':',zorder=50)
    #ax.plot([0+dim*np.sin(inc),2.0],[-dim*np.cos(inc),-dim*np.cos(inc)],[0,0],color='k',linestyle=':',zorder=10)  
    ax.plot([0+dim*np.sin(inc)*1.0,0],[-dim*np.cos(inc),-dim*np.cos(inc)],[-dim,-dim],color='k',linestyle=':',zorder=50) 
    ax.plot([0,2.0],[0,0],[0,0],color='k',linestyle='-')  
    
    ax.plot_surface(x_sky+2.0, y_sky, z_sky, color='blue', alpha=.3, linewidth=0,zorder=10)
    
    # RA/DEC axes
 
    axis_len=1.10
    pa=0*u.deg
    a = Arrow3D([2, 2], [0,+axis_len*np.cos(pa)], [0, -axis_len*np.sin(pa)], **arrow_prop_dict, color='blue',linewidth=2)
    ax.add_artist(a)
    ax.scatter(2,0,0,color='blue')
    ax.text(2, +axis_len*np.cos(pa)*1.1, -axis_len*np.sin(pa)*1.1, r'$x_{\rm proj.}$',color='blue')
    
    a = Arrow3D([2, 2], [0,-axis_len*np.sin(pa)], [0, +axis_len*np.cos(pa)], **arrow_prop_dict, color='blue',linewidth=2)
    ax.add_artist(a)
    ax.scatter(2,0,0,color='blue')
    ax.text(2, -axis_len*np.sin(pa)*1.1, +axis_len*np.cos(pa)*1.1, r'$y_{\rm proj.}$',color='blue') 
    
    a = Arrow3D([2, 2+axis_len], [0,0], [0, 0], **arrow_prop_dict, color='blue',linewidth=2)
    ax.add_artist(a)
    ax.scatter(2,0,0,color='blue')
    ax.text(2+axis_len*0.85,0,axis_len*0.05, r'$z_{\rm proj./LOS}$',color='blue') 
    
    rho=np.array([1,0.5,1,0.5,1,0.5,1,0.5])*dim
    rho=np.array([1,1.0,1,1.0,1,1.0,1,1.0])*dim
    phi=np.linspace(0,360-45,8)*u.deg
    rho=np.array([1.0,1.0,1.0,1.0])*dim
    phi=np.linspace(0,360-90,4)*u.deg
    phi=np.array([0,90,180,270])*u.deg    
    z=0.0*rho
    v_rot=np.minimum(rho/0.25,1.)*1.0
    d_phi=(v_rot/rho*u.rad)
    d_z=rho*0.0
    d_rho=rho*0.0
    
    # CLOUDLET model
    
    cloudlet_cyl=CylindricalRepresentation(rho,phi,z)
    cloudlet_cyldiff=CylindricalDifferential(d_rho,d_phi,d_z)
    cloudlet_cyl=cloudlet_cyl.with_differentials(cloudlet_cyldiff)
    cloudlet_car=cloudlet_cyl.represent_as(CartesianRepresentation,differential_class=CartesianDifferential)
    rot=rotation_matrix(-90,'y')
    cloudlet_car=cloudlet_car.transform(rot)
    rot=rotation_matrix(40,'z')
    cloudlet_car=cloudlet_car.transform(rot)

    rho_cc=np.ones(100)*dim
    phi_cc=np.linspace(0,360,100)*u.deg
    z_cc=0.0*rho_cc    
    
    cloudlet_cyl_cc=CylindricalRepresentation(rho_cc,phi_cc,z_cc)
    cloudlet_car_cc=cloudlet_cyl_cc.represent_as(CartesianRepresentation)
    rot=rotation_matrix(-90,'y')
    cloudlet_car_cc_sky=cloudlet_car_cc.transform(rot)
    rot=rotation_matrix(40,'z')
    cloudlet_car_cc=cloudlet_car_cc_sky.transform(rot)
    
    rho_r=np.random.rand(5000)*dim
    phi_r=360*np.random.rand(5000)*u.deg
    z_r=0.0*rho_r    
    
    v_rot=np.minimum(rho_r/0.25,1.)*1.0
    d_phi_r=(v_rot/rho_r*u.rad)
    d_z_r=rho_r*0.0
    d_rho_r=rho_r*0.0    
    
    cloudlet_cyl_r=CylindricalRepresentation(rho_r,phi_r,z_r)
    cloudlet_cyldiff_r=CylindricalDifferential(d_rho_r,d_phi_r,d_z_r)
    cloudlet_cyl_r=cloudlet_cyl_r.with_differentials(cloudlet_cyldiff_r)
    cloudlet_car_r=cloudlet_cyl_r.represent_as(CartesianRepresentation,differential_class=CartesianDifferential)
    rot=rotation_matrix(-90,'y')
    cloudlet_car_r=cloudlet_car_r.transform(rot)
    rot=rotation_matrix(40,'z')
    cloudlet_car_r=cloudlet_car_r.transform(rot)   
    
    
    ax.quiver(cloudlet_car.x.value,cloudlet_car.y.value,cloudlet_car.z.value,
          cloudlet_car.differentials[''].d_x.value/2,
          cloudlet_car.differentials[''].d_y.value/2,
          cloudlet_car.differentials[''].d_z.value/2,
          arrow_length_ratio=0.3,color='r',
          linewidths=3.0,alpha=1.0)
    ax.scatter(cloudlet_car.x.value,cloudlet_car.y.value,cloudlet_car.z.value,color='red',s=500,marker='.')
    
    ax.plot(cloudlet_car_cc.x,cloudlet_car_cc.y,cloudlet_car_cc.z,color='red',linewidth=1) 
    ax.plot(cloudlet_car_cc_sky.x+2,cloudlet_car_cc_sky.y*np.cos(inc),cloudlet_car_cc_sky.z,color='blue',linewidth=1,zorder=-1) 
 
    
    ax.quiver(cloudlet_car.x.value*0.0+2,cloudlet_car.y.value,cloudlet_car.z.value,
          cloudlet_car.differentials[''].d_x.value/2,
          cloudlet_car.differentials[''].d_y.value/2*0.0,
          cloudlet_car.differentials[''].d_z.value/2*0.0,
          arrow_length_ratio=0.3,color='b',
          linewidths=3.0,alpha=0.9)            
    ax.quiver(cloudlet_car.x.value*0.0+2,cloudlet_car.y.value,cloudlet_car.z.value,
          cloudlet_car.differentials[''].d_x.value/2*0.0,
          cloudlet_car.differentials[''].d_y.value/2,
          cloudlet_car.differentials[''].d_z.value/2,
          arrow_length_ratio=0.3,color='b',
          linewidths=4.0,alpha=0.9)    
    ax.scatter(cloudlet_car.x.value*0.0+2,cloudlet_car.y.value,cloudlet_car.z.value,
               alpha=1.0,marker='.',
               c=-cloudlet_car.differentials[''].d_x.value/3,s=500,
               cmap=cm.coolwarm,zorder=3)
    
    #   sky-plane with RA/DEC
    
    pa=47*u.deg
    pa*=-1
    
    y_gal, z_gal = np.meshgrid([-dim*np.cos(inc), dim*np.cos(inc)], [-dim, dim])

    y_pix=np.linspace(-dim*1.28,+dim*1.28,30)
    z_pix=np.linspace(-dim*1.28,+dim*1.28,30)

    y_pix,z_pix=np.meshgrid(y_pix,z_pix)
    x_pix=y_pix*0+4.0
    
    #ax.plot_wireframe(y_pix*0+4, y_pix, z_pix, linewidth=1,rstride=1,cstride=1,color='gray')
    
    car_pix_align=CartesianRepresentation(x_pix,y_pix,z_pix)
    rot=rotation_matrix(-pa,'x')
    car_pix_align=car_pix_align.transform(rot)
    #ax.plot_wireframe(car_pix_align.x, car_pix_align.y, car_pix_align.z, linewidth=1,rstride=1,cstride=1,color='gray')
    
    from scipy.interpolate import griddata
    from matplotlib import cm

    zp=-griddata((cloudlet_car_r.y.value,cloudlet_car_r.z.value),
                cloudlet_car_r.differentials[''].d_x.value,
                (car_pix_align.y.value,car_pix_align.z.value),method='linear')
    zp=np.ma.masked_array(zp,zp!=zp)
#    ax.plot_surface(car_pix_align.x, car_pix_align.y, car_pix_align.z,
#                      linewidth=1,rstride=1,cstride=1,color='gray',
#                      #facecolors=zp,cmap=cm.coolwarm)
#                      facecolors=cm.coolwarm(zp))
    cmap=cm.coolwarm
    #cmap.set_bad('black',0.)
    cmap.set_bad('white')
    cmap.set_under('blue',alpha=0.2)

    norm = mpl.colors.Normalize(vmin=-np.abs(np.nanmax(zp)), vmax=+np.abs(np.nanmax(zp)))
    #print(np.nanmin(zp), np.nanmax(zp))
    ax.plot_surface(x_sky+4.0, y_sky, z_sky, color='blue', alpha=.5, linewidth=0,zorder=1)    
    
    # half pixel shift for cell-/sampling offset
    yy=(car_pix_align.y[:-1,:-1]+car_pix_align.y[1:,1:])/2.0
    zz=(car_pix_align.z[:-1,:-1]+car_pix_align.z[1:,1:])/2.0
    xx=(car_pix_align.x[:-1,:-1]+car_pix_align.x[1:,1:])/2.0 

    ax.plot_surface(xx,
                    yy,
                    zz,
                      #linewidth=1,rstride=1,cstride=1,
                    #cmap=cmap,vmin=-0.64,vmax=+0.64)
                    facecolors=cm.coolwarm((zp[1:,1:]*1.0/np.abs(np.sin(inc)))/2.0+0.5),alpha=0.8,linewidth=0,antialiased=False,shade=False,zorder=1)

    
    
    axis_len=1.10
    
    ax.add_artist(a)    
    a = Arrow3D([4, 4], [0,-axis_len*np.cos(pa)], [0, -axis_len*np.sin(pa)], **arrow_prop_dict, color='blue',linewidth=2)
    a.zorder=50
    ax.add_artist(a)    
    ax.scatter(2,0,0,color='blue')
    ax.text(4, -axis_len*np.cos(pa)*1.1, -axis_len*np.sin(pa)*1.1, r'$\alpha$',color='blue')
    
    a = Arrow3D([4, 4], [0,-axis_len*np.sin(pa)], [0, +axis_len*np.cos(pa)], **arrow_prop_dict, color='blue',linewidth=2)
    a.zorder=50
    ax.add_artist(a)
    ax.scatter(2,0,0,color='blue')
    ax.text(4, -axis_len*np.sin(pa)*1.1, +axis_len*np.cos(pa)*1.1, r'$\delta$',color='blue') 
    ax.plot([4, 4], [0,-axis_len*np.sin(pa)], [0, +axis_len*np.cos(pa)], color='blue',linewidth=2)
    
    pa_step=np.linspace(0,pa,100)
    ax.plot(4+np.zeros(100), -axis_len*0.5*np.sin(pa_step), +axis_len*0.5*np.cos(pa_step), color='blue',linewidth=2,zorder=50)
    ax.text(4,-axis_len*0.5*np.sin(pa_step[30]),+axis_len*0.5*np.cos(pa_step[30]),r'P.A.',zorder=50,color='blue')
    a = Arrow3D([4, 4+axis_len], [0,0], [0, 0], **arrow_prop_dict, color='blue',linewidth=2)
    
    a.zorder=50
    ax.add_artist(a)
    ax.scatter(2,0,0,color='blue')
    ax.text(4+axis_len, 0,0, r'LOS',color='blue')     

    ox=xx[0,0]*0.40
    oy=yy[0,0]*0.40
    oz=zz[0,0]*0.40
    
    a = Arrow3D([4, 4], [0+oy,+axis_len*np.cos(pa)*0.2+oy], [0+oz, +axis_len*np.sin(pa)*0.2+oz], **arrow_prop_dict, color='blue',linewidth=2)
    a.zorder=50
    ax.add_artist(a)    
    ax.scatter(2,0,0,color='blue')
    ax.text(4, +axis_len*np.cos(pa)*0.2+oy,+axis_len*np.sin(pa)*0.2+oz, r'$x_{\rm pix}$',color='blue',zorder=50)
    
    a = Arrow3D([4, 4], [0+oy,-axis_len*np.sin(pa)*0.2+oy], [0+oz, +axis_len*np.cos(pa)*0.2+oz], **arrow_prop_dict, color='blue',linewidth=2)
    a.zorder=50
    ax.add_artist(a)
    ax.scatter(2,0,0,color='blue')
    ax.text(4, -axis_len*np.sin(pa)*0.2+oy, +axis_len*np.cos(pa)*0.2+oz, r'$y_{\rm pix}$',color='blue',zorder=50) 
    ax.plot([4, 4], [0,-axis_len*np.sin(pa)], [0, +axis_len*np.cos(pa)], color='blue',linewidth=2)    
    
    ax.set_axis_off()
    #ax.set_axis_on()
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    ax.zaxis.set_major_locator(plt.NullLocator())
    
    fig.tight_layout()
    #fig.savefig('plt_coordsys.pdf',bbox_inches = 'tight',pad_inches = 0,transparent = True)
    fig.savefig('plt_coordsys.pdf',bbox_inches = 'tight')
    plt.close()        




