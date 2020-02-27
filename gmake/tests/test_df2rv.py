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

import matplotlib.pyplot as plt



def test_df2rv():
    
    sample_sort=False
    sample_interp=True
    
    nxy=[1001,2001]
    pdf=makekernel(nxy[0],nxy[1],[10,0.2],pa=0,cent=[501,501])
    
    start_time = time.time()
    sample=pdf2rv_nd(pdf)
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('approx random sample ND',time.time()-start_time)) 

    xpos=sample[0,:]
    ypos=sample[1,:]

    fig=plt.figure(figsize=(24,11))
    ax= fig.add_subplot(1,2,1)
    ax.plot(xpos,ypos,linestyle='None',marker='.')
    ax.set_xlim([501-2,501+2])
    ax.set_ylim([501-20,501+20])
    ax.set_title('verify offset')
    
    
    nxy=[1001,2001]
    pdf=makekernel(nxy[0],nxy[1],[200,100],pa=10,cent=[501,501])
    pdf=pdf+makekernel(nxy[0],nxy[1],[100,20],pa=10,cent=[501+300,501])
    #print(pdf.shape)
    #pdf (c_row,n_column)
    
    start_time = time.time()
    sample=pdf2rv_nd(pdf)
    #print("---{0:^10} : {1:<8.5f} seconds ---".format('approx random sample ND',time.time()-start_time)) 

    xpos=sample[0,:]
    ypos=sample[1,:]

    #fig=plt.figure(figsize=(24,11))
    ax= fig.add_subplot(1,2,2)
    ax.plot(xpos,ypos,linestyle='None',marker='.')
    ax.set_xlim([0,2001])
    ax.set_ylim([0,2001])
    ax.set_title('verify axis')    
    
    fig.savefig('test_df2rv.png')
    
def test_pdf2rv():
    
    from scipy.stats import expon
    from scipy.stats import halfnorm
    
    fig, ax = plt.subplots(2, 1)
    
    
    
    x = np.linspace(expon.ppf(0.01),expon.ppf(0.99), 100)
    ax[0].plot(x, expon.pdf(x),'r-', lw=5, alpha=0.6, label='expon pdf')
    rv = expon()
    ax[0].plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
    
    r = expon.rvs(size=10000)
    ax[0].hist(r, density=True, histtype='stepfilled', alpha=0.2,label='from rvs',
            bins=30,range=[0,10])
    
    x = np.linspace(expon.ppf(0.01),expon.ppf(0.99), 100)
    r_local=pdf2rv(x,rv.pdf(x),size=10000)
    
    ax[0].hist(r_local, density=True, histtype='stepfilled', alpha=0.2,label='from pdf2rv',
            bins=30,range=[0,10])
    
    ax[0].legend(loc='best', frameon=False)
    
    
    
    x = np.linspace(halfnorm.ppf(0.01),halfnorm.ppf(0.99), 100)
    ax[1].plot(x, halfnorm.pdf(x),'r-', lw=5, alpha=0.6, label='halfnorm pdf')
    rv = halfnorm()
    ax[1].plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
    
    r = halfnorm.rvs(size=10000)
    ax[1].hist(r, density=True, histtype='stepfilled', alpha=0.2,label='from rvs',
            bins=30,range=[0,10])
    
    x = np.linspace(halfnorm.ppf(0.01),halfnorm.ppf(0.99), 100)
    r_local=pdf2rv(x,rv.pdf(x),size=10000)
    
    ax[1].hist(r_local, density=True, histtype='stepfilled', alpha=0.2,label='from pdf2rv',
            bins=30,range=[0,10])
    
    ax[1].legend(loc='best', frameon=False)    
    
    
    fig.savefig('test_pdf2rv.png')
    plt.close()
    

    
if  __name__ == '__main__':
    
    """
    #test_df2rv()
    test_pdf2rv()
    
    from scipy.stats import rv_continuous
    class gaussian_gen(rv_continuous):
        "Gaussian distribution"
        def _pdf(self, x):
            return np.exp(-x**2 / 2.) / np.sqrt(2.0 * np.pi)
        
        def _ppf(self,x):
            xsample=np.linspace(-10.0,10.0, 100)
            icdf=interpolate.interp1d(integrate.cumtrapz(self._pdf(xsample),xsample,initial=0.),
                                 xsample,kind='linear')
            return icdf(x)
        
    gaussian = gaussian_gen(name='gaussian')
    p0=gaussian.pdf(0.0)
    r0=gaussian.rvs(size=1000)
    #print(p0)
    print(r0)
    """
    