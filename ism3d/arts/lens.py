"""
Lionel got a lens, Janet got a lens
Matthew got a lens on me right now, yeah
Cleve got a lens, Kevin got a lens
"""

import numpy as np
import astropy.units as u
from lenstronomy.LensModel.lens_model import LensModel

def sie_rt(x,y,
           theta_e=1,xc=0,yc=0,pa=0,q=1.0,
           method='ls'):
    """
    performe ray-tracing for a SIE potential
    two methods:    abs, using sie_grad_abs()
                    ls, using lenstronomy
    theta_e:  Einstein radius
    xc,yc:    x/y position of center
    pa:    P.A. (degree)
    q:        axiasratio b/a
    
    """
    
    if  method.lower()=='ls':
        # see e1/e2 def:
        #   https://github.com/sibirrer/lenstronomy_extensions
        #       enstronomy_extensions/Notebooks/units_coordinates_parameters.ipynb
        # we only used the "ray_shotting" api here but a higher-level module:
        #   lenstronomy.ImSim.image_model import ImageModel 
        # can be used:
        # see: lenstronomy_extensions/Notebooks/lenstronomy_numerics.ipynb
        e1=(1-q)/(1+q)*np.cos(2*pa/180*np.pi)
        e2=(1-q)/(1+q)*np.sin(2*pa/180*np.pi)
        lensModel = LensModel(lens_model_list=['SIE'])
        kwargs_lens = [{'theta_E': theta_e, 'e1': e1, 'e2': e2, 
                        'center_x': xc, 'center_y': yc}]        
        xs, ys = lensModel.ray_shooting(x,y, kwargs_lens)
    
    if  method.lower()=='asb':
        
        #l_amp = 200   # Einstein radius
        #l_xcen = 0.0  # x position of center
        #l_ycen = 0.0  # y position of center
        #l_axrat = 0.5 # minor-to-major axis ratio
        #l_pa = 30.    # major-axis position angle (degrees) c.c.w. from x axis
        # pa may need to rotated by 90degree due to different convention
        lpar = np.asarray([theta_e, xc, yc, q, pa])
        
        xg,yg=sie_grad_abs(x,y,lpar)
        xs=x-xg ; ys=y-yg
        # xx-xg,yy-yg source plane coordins
        # xx,yy lens plane
        
    return xs,ys

def sie_grad_abs(x, y, par):
    """
    source:
        http://www.physics.utah.edu/~bolton/python_lens_demo/
        
    NAME: sie_grad

    PURPOSE: compute the deflection of an SIE potential

    USAGE: (xg, yg) = sie_grad(x, y, par)

    ARGUMENTS:
      x, y: vectors or images of coordinates;
            should be matching numpy ndarrays
      par: vector of parameters with 1 to 5 elements, defined as follows:
        par[0]: lens strength, or 'Einstein radius'
        par[1]: (optional) x-center (default = 0.0)
        par[2]: (optional) y-center (default = 0.0)
        par[3]: (optional) axis ratio (default=1.0)
        par[4]: (optional) major axis Position Angle
                in degrees c.c.w. of x axis. (default = 0.0)

    RETURNS: tuple (xg, yg) of gradients at the positions (x, y)

    NOTES: This routine implements an 'intermediate-axis' conventionp.
      Analytic forms for the SIE potential can be found in:
        Kassiola & Kovner 1993, ApJ, 417, 450
        Kormann et al. 1994, A&A, 284, 285
        Keeton & Kochanek 1998, ApJ, 495, 157
      The parameter-order convention in this routine differs from that
      of a previous IDL routine of the same name by ASB.

    WRITTEN: Adam S. Bolton, U of Utah, 2009
    """
    # Set parameters:
    b = np.abs(par[0]) # can't be negative!!!
    xzero = 0. if (len(par) < 2) else par[1]
    yzero = 0. if (len(par) < 3) else par[2]
    q = 1. if (len(par) < 4) else np.abs(par[3])
    phiq = 0. if (len(par) < 5) else par[4]
    eps = 0.001 # for sqrt(1/q - q) < eps, a limit expression is used.
    # Handle q > 1 gracefully:
    if (q > 1.):
        q = 1.0 / q
        phiq = phiq + 90.0
    # Go into shifted coordinats of the potential:
    phirad = np.deg2rad(phiq)
    xsie = (x-xzero) * np.cos(phirad) + (y-yzero) * np.sin(phirad)
    ysie = (y-yzero) * np.cos(phirad) - (x-xzero) * np.sin(phirad)
    # Compute potential gradient in the transformed system:
    r_ell = np.sqrt(q * xsie**2 + ysie**2 / q)
    qfact = np.sqrt(1./q - q)
    # (r_ell == 0) terms prevent divide-by-zero problems
    if (qfact >= eps):
        xtg = (b/qfact) * np.arctan(qfact * xsie / (r_ell + (r_ell == 0)))
        ytg = (b/qfact) * np.arctanh(qfact * ysie / (r_ell + (r_ell == 0)))
    else:
        xtg = b * xsie / (r_ell + (r_ell == 0))
        ytg = b * ysie / (r_ell + (r_ell == 0))
    # Transform back to un-rotated system:
    xg = xtg * np.cos(phirad) - ytg * np.sin(phirad)
    yg = ytg * np.cos(phirad) + xtg * np.sin(phirad)
    # Return value:
    return (xg, yg)
