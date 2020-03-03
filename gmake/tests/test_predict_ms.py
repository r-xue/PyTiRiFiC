
from gmake.vis_utils import cpredict_ms
from gmake.vis_utils import gpredict_ms
from rxutils.casa.proc import setLogfile
from astropy.io import fits
from gmake.model import makepb
setLogfile('casa.log')
cpredict_ms('test1.ms',fitsimage='../../data/mockup_basic/00.ms/im.fits',\
            inputvis='../../data/mockup_basic/00.ms',pbcor=True)
#
# 0.0003 or 0.03 off
gpredict_ms('test2.ms',fitsimage='../../data/mockup_basic/00.ms/im.fits',\
            inputvis='../../data/mockup_basic/00.ms',pb='../../data/mockup_basic/00.ms/dm.pb.fits')

# 0.98  or 2% off
#gpredict_ms('test2.ms',fitsimage='../../data/mockup_basic/00.ms/im.fits',\
#            inputvis='../../data/mockup_basic/00.ms',antsize=25*u.m)

"""
# this is eqauivelent with the antsize=? 
header=fits.getheader('../../data/mockup_basic/00.ms/im.fits')
ms1=read_ms(vis='../../data/mockup_basic/00.ms')
pb=makepb(header,phasecenter=ms1['phasecenter@../../data/mockup_basic/00.ms'],antsize=25*u.m)
fits.writeto('pb.fits',pb,header,overwrite=True)
gpredict_ms('test2.ms',fitsimage='../../data/mockup_basic/00.ms/im.fits',\
            inputvis='../../data/mockup_basic/00.ms',pb='pb.fits')
"""

from gmake.test import test_predict_ms_plot

test_predict_ms_plot('test1.ms','test2.ms')


