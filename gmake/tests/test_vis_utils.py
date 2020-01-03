# test CASA6-related function
#   note: CASA6 replaced casacore & galario  

#import matplotlib as mpl
from gmake.vis_utils import read_ms
from gmake.vis_utils import write_ms
from gmake.ms import read_ms0

import gmake
srcdir=gmake.__demo__

gmake.logger_config(logfile='gmake.tests.log',loglevel='DEBUG',logfilelevel='DEBUG')
gmake.logger_status()

def test_read_ms():
    """
    based on casa6.casatools
    """
    
    repo='/Volumes/S1/projects/GMaKE/examples/data/gn20/vla/'
    dat_dct={}
    read_ms(vis=repo+'AC974.110212.ms',dat_dct=dat_dct)
          
def test_read_ms0():
    """
    based on casacore
    """
    
    repo='/Volumes/S1/projects/GMaKE/examples/data/gn20/vla/'
    dat_dct={}
    read_ms0(vis=repo+'AC974.110212.ms',dat_dct=dat_dct)
    
def test_write_ms():
    """
    base on casa6.casatools
    """
    repo='/Volumes/S1/projects/GMaKE/examples/data/gn20/vla/'
    visfile='AC974.110212.ms'
    
    os.system('rm -rf '+visfile)
    os.system('cp -rf '+repo+visfile+' '+visfile)
    
    dat_dct={}
    read_ms(vis=repo+'AC974.110212.ms',dat_dct=dat_dct)
    #print((dat_dct['data@/Volumes/S1/projects/GMaKE/examples/data/gn20/vla/AC974.110212.ms']).flags)
    write_ms(visfile,dat_dct['data@/Volumes/S1/projects/GMaKE/examples/data/gn20/vla/AC974.110212.ms'])
    
if  __name__ == '__main__':
    
    #test_read_ms()
    #test_read_ms0()
    test_write_uvmodel()