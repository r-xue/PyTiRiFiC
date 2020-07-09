"""
functions translating object keywords to numerical model
"""
import numpy as np
import astropy.units as u

def fluxscale_from_contflux(contflux,w):
    """
    obatin the fluxscaling vector from the object keyword contflux:
        contflux is a tuple of one-element or three element
    """
    wspec=w.sub(['spectral'])
    sz=wspec.pixel_to_world(np.arange(w._naxis[2])).to(u.Hz,equivalencies=u.spectral())

    try:
        fluxscale=contflux[0]*((sz/contflux[1])**contflux[2]).decompose()
    except:
        fluxscale=contflux*sz/sz
    
    return fluxscale