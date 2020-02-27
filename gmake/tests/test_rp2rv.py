"""

"""

from gmake.stats import pdf2rv_nd
from gmake.stats import cdf2rv
from gmake.stats import pdf2rv
from gmake.model_func import makekernel

import time
import numpy as np

from scipy import interpolate
from scipy import integrate


import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# mpl.rcParams['xtick.direction'] = 'in'
# mpl.rcParams['ytick.direction'] = 'in'
# mpl.rcParams.update({'font.size': 12})
# mpl.rcParams["font.family"] = "serif"
# mpl.rcParams["image.origin"]="lower"
# mpl.rc('text', usetex=True)

mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams.update({'font.size': 12})
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["image.origin"]="lower"
mpl.rcParams['agg.path.chunksize'] = 10000


from astropy.modeling.models import Sersic1D
from astropy.modeling.models import Gaussian1D
import astropy.units as u
from scipy.stats import norm
from astropy.convolution import discretize_model
from fast_histogram import histogram1d, histogram2d

def test_sersic1d_sample():
    
    print('test')
    rp1=('sersic',0.2*u.arcsec,1.0)

    plt.clf()
    #fig,ax=plt.figure(figsize=(8,8)) 
    
    fig,ax=plt.subplots(1,1,figsize=(16,8))
    #s1 = Sersic1D(amplitude=1, r_eff=10)
    s1=Gaussian1d(amplitude=1,mean=0,stddev=2)
    r=np.arange(-0.72, 0.72, .04)*u.arcsec
    r_fine=np.arange(-1.0, 1.0, .0001)*u.arcsec
    r_test=np.arange(-1-1./30, 1-1./30, 2./30)*u.arcsec
    
    x=r_fine
    y=s1(x)
    
    ftotal=np.trapz(y,x)
    print(ftotal)
    
    for n in np.arange(1, 2):
         s1.n = n
         ax.plot(r, s1(r),color='blue')
         ax.plot(r_test, s1(r_test),drawstyle='steps-mid',color='blue')
         ax.plot(r_test, s1(r_test),color='red',drawstyle='steps-mid')
        
        #model2d=discretize_model(s1,(0,
        #                     (py_o_int,py_o_int+2*ys_hz+1),
        #                     mode='oversample',factor=factor)
             
             
         ax.plot(r_fine, s1(np.abs(r_fine)),color='gray')
         
    #plt.axis([1e-1, 30, 1e-2, 1e3])
    ax.set_xlabel('radius')
    ax.set_ylabel('Surface Brightness')
    ax.text(.25, 1.5, 'n=1')
    ax.text(.25, 300, 'n=10')
    
    
    rr=pdf2rv(r_fine,s1(np.abs(r_fine)))
    print(rr)
    ax.hist(rr,density=True,histtype='stepfilled', alpha=0.2,label='from pdf2rv',
            bins=30,range=[-1.,1.])

    fig.savefig('test_sersic1d_sample.pdf')
    plt.close()
    
def test_sersic1d_sample_dl():
    

    plt.clf()
    
    fig,ax=plt.subplots(1,1,figsize=(16,8))
    s1=Gaussian1D(amplitude=1,mean=0,stddev=1.0)

    r=np.arange(-20, 20, .1)
    
    r_fine=np.arange(-20, 20, .0001)
    r_coarse=np.arange(-20, 20, 1)

    ftotal=np.trapz(s1(r_fine),r_fine)
    ax.plot(r_fine, s1(r_fine)/ftotal,color='black',drawstyle='steps-mid',label='fine center sampling')
    #ax.plot(r_coarse, s1(r_coarse)/ftotal,color='blue',drawstyle='steps-mid',label='coarse center sampling')
    #ax.plot(r_test, s1(np.abs(r_test))/ftotal,color='gray')
    
    #for n in np.arange(1, 2):
    #     s1.n = n
         #ax.plot(r, s1(np.abs(r))/ftotal,color='blue')
         #ax.plot(r_test, s1(np.abs(r_test))/ftotal,drawstyle='steps-mid',color='blue')
         #ax.plot(r_test, s1(np.abs(r_test))/ftotal,color='red',drawstyle='steps-mid')
    
    
        #model2d=discretize_model(s1,(0,
        #                     (py_o_int,py_o_int+2*ys_hz+1),
        #                     mode='oversample',factor=factor)
    """
    note: although astropy.modeling can work with quantity, discretize_model() is designed to work with a pixel coordinate
    and the grid is specified with a pixel range (xrange[1]-xrange[0] is number.int)
    """
    x=np.arange(-20, 20, 1)
    # this is a little bit off due to the "center" sampling mode (not good on flux conservation)
    y=discretize_model(s1,(-20,20),mode='oversample',factor=1)
    ax.plot(x, y/ftotal,color='yellow',drawstyle='steps-mid',alpha=0.4,label='disc_model,coarse')
    # the oversampling method is closer to random sampling method
    y=discretize_model(s1,(-20,20),mode='oversample',factor=100)
    ax.plot(x, y/ftotal,color='green',drawstyle='steps-mid',alpha=0.4,label='disc_model,oversampling')    
    
    r_fine=np.arange(-10, 10, .01)
    rr0=pdf2rv(r_fine,s1(np.abs(r_fine)),size=100000)
    #hist,bin_edge=np.histogram(rr0,bins=20,range=[-10.5,9.5],density=True)
    #bin_center=(bin_edge[:-1]+bin_edge[1:])/2.0
    hist=histogram1d(rr0,20,(-10.5,9.5))
    hist/=100000.
    bin_center=np.arange(-10,10)
    ax.fill_between(bin_center,hist,step='mid',label='from pdf2rv with a numerical PDF shape',alpha=0.2)    
    #ax.hist(rr0,density=True,histtype='stepfilled', alpha=0.2,label='from pdf2rv with a numerical PDF shape',
    #        bins=20,range=[-10.5,9.5])

    rr1=norm.rvs(size=100000)
    #hist,bin_edge=np.histogram(rr1,bins=20,range=[-10.5,9.5],density=True)
    #bin_center=(bin_edge[:-1]+bin_edge[1:])/2.0
    hist=histogram1d(rr0,20,(-10.5,9.5))
    hist/=100000.
    bin_center=np.arange(-10,10)    
    ax.fill_between(bin_center,hist,step='mid',label='from norm.rvs from an analytical ppf',alpha=0.2)
    #ax.hist(rr1,density=True,histtype='stepfilled', alpha=0.2,label='from norm.rvs from an analytical ppf',
    #        bins=20,range=[-10.5,9.5])    
        
    ax.set_xlim(-10,10)
    ax.legend(loc='best', frameon=False)    
    
    fig.savefig('test_sersic1d_sample_dl.png')
    plt.close()    
        
if  __name__ == '__main__':    
    
    #test_sersic1d_sample()
    test_sersic1d_sample_dl()
    pass

    #lprun -f test_sersic1d_sample_dl test_sersic1d_sample_dl()