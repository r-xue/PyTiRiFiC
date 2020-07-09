from astropy.wcs import WCS
from astropy.wcs.utils import skycoord_to_pixel, proj_plane_pixel_scales


def linear_offset_coords(wcs, center):
    """
    Returns a locally linear offset coordinate system.
    
    Given a 2-d celestial WCS object and a central coordinate, return a WCS
    that describes an 'offset' coordinate system, assuming that the
    coordinates are locally linear (that is, the grid lines of this offset
    coordinate system are always aligned with the pixel coordinates, and
    distortions from spherical projections and distortion terms are not taken
    into account)
    
    Parameters
    ----------
    wcs : `~astropy.wcs.WCS`
        The original WCS, which should be a 2-d celestial WCS
    center : `~astropy.coordinates.SkyCoord`
        The coordinates on which the offset coordinate system should be
        centered.
    """

    # Convert center to pixel coordinates
    xp, yp = skycoord_to_pixel(center, wcs)
        
    # Set up new WCS
    new_wcs = WCS(naxis=2)
    new_wcs.wcs.crpix = xp + 1, yp + 1
    new_wcs.wcs.crval = 0., 0.
    cell=proj_plane_pixel_scales(wcs)*3600.
    new_wcs.wcs.cdelt = -cell[0], cell[1]
    new_wcs.wcs.ctype = 'XOFFSET', 'YOFFSET'
    new_wcs.wcs.cunit = 'arcsec', 'arcsec'

    return new_wcs

def calc_ppbeam(header):
    """
    For Radio Cubes:        ppbeam=npix/beam
    For optical/IR Cubes:   ppbeam=1.0
    """
    if  'BMAJ' in header.keys() and 'BMIN' in header.keys():
        beam_area = np.abs(header['BMAJ']*header['BMIN']*3600.**2.0)*2.*np.pi/(8.*np.log(2.))
        pixel_area=np.abs(header['CDELT1']*header['CDELT2']*3600.**2.0)
        ppbeam=beam_area/pixel_area
    else:
        ppbeam=1.
    
    return ppbeam