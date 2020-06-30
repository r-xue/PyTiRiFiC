import numpy as np
import scipy.integrate
from scipy import interpolate
from scipy import integrate
from scipy import stats
from scipy import special as sc

# https://docs.scipy.org/doc/scipy/reference/tutorial/stats/continuous.html
from scipy.stats import rv_continuous
from scipy.stats import hypsecant
from scipy.stats import logistic
from scipy.stats import norm
import time

from numpy.random import Generator,SFC64,PCG64

"""
Note
    + see the rv_continous base class explaination here:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html
    + see subclassing template here:
        scipy/stats/_continuous_distns.py
    + to avoid the sub-class wrapper, one can calculate ppf by directly calling special function
    + performance of ufunc
        https://stackoverflow.com/questions/3985619/how-to-calculate-a-logistic-sigmoid-function-in-python

One np.random performance:

    np.random.RandomState is using the legacy MT generator, which is slower than the new implemnation:
        https://docs.scipy.org/doc/numpy/reference/random/legacy.html#numpy.random.mtrand.RandomState
        
    mordern "generator"
        https://docs.scipy.org/doc/numpy/reference/random/generator.html#numpy.random.Generator
        https://docs.scipy.org/doc/numpy/reference/random/index.html
        https://docs.scipy.org/doc/numpy/reference/random/new-or-different.html
        https://numpy.org/neps/nep-0019-rng-policy.html
    
    performance:
        https://docs.scipy.org/doc/numpy/reference/random/performance.html
     from numpy.random import Generator,SFC64,PCG64
     seed=1      
     rg_default=Generator(PCG64(seed))
     rg_fast=Generator(SFC64(seed))
     %time rg_default.standard_normal(150*100000)    # PCG64 
     %time rg_fast.standard_normal(150*100000)       # SFC64
     %time np.random.standard_normal(150*100000)     # Legacy (MT)
     
    rng_old = np.random.RandomState(seeds[1])
    rng_new = Generator(SFC64(seed))

"""

##############################

class sersic2d_gen(rv_continuous):
    """
    rho Distribution of a axisymatteric 2D distribution with a Sersic radial profile
    template from: 
    
    """
    def _pdf(self,r,n):
        
        bn=sc.gammaincinv(2*n, 0.5)
        fpdf=np.exp(-bn*(r**(1/n)-1))*r
        fint=n*np.exp(bn)/(bn**(2*n))*sc.gamma(2*n)
        
        return fpdf/fint

    def _ppf(self,p,n):
        # a direct call will vectize n while .rvs doesn't do it
        if  np.allclose(n,1):    
            # lambertw will be slightly faster than gammainvinv in this application
            b1=sc.gammaincinv(2, 0.5)
            return (-1-(sc.lambertw((p-1)/np.exp(1),k=-1)).real)/b1
        else:
            bn=sc.gammaincinv(2*n, 0.5)
            return (sc.gammaincinv(2*n, p)/bn)**n
    
sersic2d = sersic2d_gen(a=0.0,name='sersic2d')

class expon2d_gen(rv_continuous):
    """
    rho Distribution of a axisymatteric 2D distribution with a Exponential radial profile
    
    
    """
#     def _pdf(self,r):
#         """not done
#         """
#         fpdf=np.exp(-r)*r
#         fint=1
#         
#         return fpdf/fint

    def _ppf(self,p):
        
        return -1-(sc.lambertw((p-1)/np.exp(1),k=-1)).real 
    
expon2d = expon2d_gen(a=0.0,name='expon2d')

class norm2d_gen(rv_continuous):
    """
    rho Distribution of a axisymatteric 2D distribution with a Gaussian radial profile
    
    
    """
#     def _pdf(self,r):
#         """not done
#         """
#         bn=sc.gammaincinv(2*n, 0.5)
#         fpdf=np.exp(-bn*(r**(1/n)-1))*r
#         fint=n*np.exp(bn)/(bn**(2*n))*sc.gamma(2*n)
#         
#         return fpdf/fint

    def _ppf(self,p):

        return np.sqrt(-2*np.log(1-p))
    
norm2d = norm2d_gen(a=0.0,name='norm2d')

##############################

norm  = norm(scale=1.0)
#   https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypsecant.html
sech  = hypsecant(scale=1.0)
"""
logistic = exp(-x)/(1+exp(-x))^2 = 1/(2+exp(-x)+exp(x))
norm(sech) = 2 / (2+exp(-2*x)+exp(2*x))
"""
sech2 = logistic(scale=0.5)

class sechsq_gen(rv_continuous):
    """
    rho Distribution of a axisymatteric 2D distribution with a Exponential radial profile
    this is a direct implementation for testing, one should use sech2 instead
    """
#     def _pdf(self,r):
#         """not done
#         """
#         fpdf=np.exp(-r)*r
#         fint=1
#         
#         return fpdf/fint

    def _ppf(self,p):
        # = np.arctanh(2*p-1)           
        # = 0.5*sc.logit(p)             
        # = 0.5*np.log(p/(1-p)) = 0.5*np.log(-1+1/(1-p))
        """
        p=np.random.rand(int(1e7))
        %timeit -r 1 p=np.random.rand(int(1e8))
        %timeit -r 1 ne.evaluate('0.5*log(p/(1-p))')  # 0.25s threading
        %timeit -r 1 0.5*sc.logit(p)                  # 1s (one C-level)
        %timeit -r 1 np.arctanh(2*p-1)                # 2s 50% slower
        %timeit -r 1 0.5*np.log(p/(1-p))              # 1.7s
        %timeit -r 1 (-0.5)*np.log(1/p-1)             # 1.4s (>one C-level operation) 
        """

        return 0.5*sc.logit(p)

sechsq = sechsq_gen(name='sechsq')

class laplace_gen(rv_continuous):
    """
    rho Distribution of a axisymatteric 2D distribution with a Exponential radial profile
    
    """
    def _pdf(self,r):
        """not done
        """
        fpdf=np.exp(-r)*r
        fint=1
        
        return fpdf/fint

    def _ppf(self,p):
        
        up=1-2*p
        return np.sign(up)*np.log(1-np.abs(up))
    
laplace = laplace_gen(name='laplace')

#############################################################


def custom_rvs(func,
               size=100000,
               scale=1.0,
               interp=(0.02,20),    # only for slow sersic2d expon2d cases
               sersic_n=1,          # only for sersic2d
               seed=None):

    """
    https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.random.RandomState.html#numpy.random.RandomState
    use_nprng==True:
        use np built-in random generator rather than the hardcoded uniform+its formula 
    more ppf rvs can be found here:
        https://github.com/scipy/scipy/blob/master/scipy/stats/_continuous_distns.py
        scipy try to use special.fun as much as possible due to performance gain
        
    performance:
        scipy.stats.rvs is generally slowest as the wrapper
        A Good in-line ITS is usually fast and comparable to rng.dist (which still use C underhood)
        
        rvs=
        
    When size is large, the ppf calculation can slow down the ITS (ur->x);
    If interp is specificed as a two-element tuple, we will use the pre-calculated ur->x table to performance the transform
    interp=(a,b) ; (a,b) determined the random variable PDF accuracy, in units of "scale" 
        a: resolution (so the uncernraiy in x should be smaller than a*scale
        b: beyond b*scale, the transform is truncated and we lost the PDF accuracy in the random variable.
    smaller a or large b will increase the computation time.
    
    if interp is None then, the custom_ppf method is used and the compulation time will incrase with size=1.0
    if interp is set as default, the computing time will flatten at some point as size increase. 
    
    When using interp for inverse transformation, the better accurate in x within a limit dynamical range setting
    is determined by which part of sampling table is usable for interpolation.
    For oneside or twoside function, this is typically x-SF as saving numerican value SF can catpture
    x change at large x (with close to zero SF) with good enough precsion.
    
    note: np.interp(x,xp,xf) works faster if x is sorted; however, there is cost of sorting random number
          the bottleneck is here is still np.interp()  
          https://github.com/numpy/numpy/issues/10937
          
    func:    string / built-in function formula
             dict / {'x':x,'cdf':cdf} cdf-x is the CDF function
                    {'y':y,'sf':sf}   sf-x  is the surveve function
             this feature is used for the case where the PPF is not analytical for the distribution
    """
    
    size=int(size)
    rng=Generator(SFC64(seed))
    
    if  isinstance(func,dict): 
        if 'x' in func:
            x=func['x']
        if 'cdf' in func:
            q=func['cdf']
        if 'sf' in func:
            q=func['sf']
        # one must make sure cdf & sf is spanning between (0,1)
        rv =rng.random(size)
        ind=q.argsort()
        rv =np.interp(rv,q[ind],x[ind])
        if scale!=1: rv*=scale 
          
    if  func=='uniform2d':
        #
        # \prop~r/scale (r<scale)   this is for simulating rho-random variable 
        #                           of a 2D pan-cake distribution 
        #
        rv =np.sqrt(rng.random(size))
        if scale!=1: rv*=scale 
          
    if  func=='expon2d':
        #
        # \prop~r*exp(-r/scale): r>0
        #
        # no implementation in scipy.stats & numpy.random, we use an in-line formula 
        #see rv=custom_ppf('expon2d',rng.rand(size))
        if  interp is None:
            rv=custom_ppf('expon2d',rng.random(size))
        else:
            x_sampling=np.linspace(0,interp[1],int(interp[1]/interp[0]))
            sf_sampling=custom_sf('expon2d',x_sampling)
            rv=np.interp(rng.random(size),sf_sampling[::-1],x_sampling[::-1])
        if scale!=1: rv*=scale 

    if  func=='sersic2d':
        # \prop~r*sersic(r/scale,n,re=1) r>0
        # scale=1 ==> re=1
        #
        # no implementation in scipy.stats & numpy.random, we use an in-line formula 
        if  interp is None:
            rv=custom_ppf('sersic2d',rng.random(size),sersic_n=sersic_n)
        else:
            x_sampling=np.linspace(0,interp[1],int(interp[1]/interp[0]))
            sf_sampling=custom_sf('sersic2d',x_sampling,sersic_n=sersic_n)
            rv=np.interp((rng.random(size)),sf_sampling[::-1],x_sampling[::-1])
        if scale!=1: rv*=scale 
    
    if  func=='norm2d':
        # \prop~r*exp(-(r/scale)^2/2) r>0
        #
        # no implementation in scipy.stats, we use an in-line formula
        # the more general formula is not any faster
        #
        # technically should be rv=np.sqrt(2)*np.sqrt(-np.log(1-u))
        # see: rv=custom_ppf('norm2d',rng.rand(size)) 
        # but we reduce the math operation by replace 1-u with u
        rv=np.sqrt(2)*np.sqrt(-np.log(rng.random(size))) 
        if scale!=1: rv*=scale
        #rv=rng.weibull(2,size=int(size)) # slow due to overhead
        #rv=rng.rayleigh(scale=1.0,size=int(size)) # slow due to overhead
    
    if  func=='sech':
        # \prop~sech(z/scale) -inf<z<+inf
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypsecant.html#scipy.stats.hypsecant
        #
        # no implementation in scipy.stats & numpy.random, we use an in-line formula
        rv=custom_ppf('sech',rng.random(size)) 
        if scale!=1: rv*=scale
        #rv=hypsecant.rvs(size=int(size),random_state=seed)    # give the same results
        
    if  func=='sech2':
        # \prop~sech^2(z/scale) -inf<z<+inf
        #
        #rv=np.arctanh(1-2*u)
        rv=custom_ppf('sech2',rng.random(size))  # comparable to rng.logistic
        if scale!=1: rv*=scale       
        #rv=rng.logistic(loc=0.0,scale=0.5*scale,size=int(size))
        
    if  func=='laplace':
        # \prop~exp(-|z|) -inf<z<+inf
        #
        #rv=custom_ppf('laplace',rng.rand(size))
        rv=rng.laplace(loc=0.0,scale=scale,size=size) # faster since it's calculated at C-level
        #
        #ur=rng.rand(size)
        #rv=np.where(ur>0.5,-np.log(2*(1-ur)), np.log(2*ur))
        
        #ur=rng.uniform(low=-1,high=1,size=size)
        #rv=-np.sign(ur)*sc.log1p(np.abs(ur))
        
    if  func=='norm':
        #rv=custom_ppf('norm',rng.rand(size))
        rv=rng.normal(loc=0.0,scale=scale,size=size) # faster since it's calculated at C-level
    
    if  func=='uniform':
        rv=rng.uniform(-scale,scale,size=size)
        
    return rv

def custom_sf(func,x,sersic_n=1):
    """
    The relation between x and q (i.e. CDF) is used to transfer uniform standard random variables to the desired sampling
    for a specified PDF. If .ppf can be writtten in analytical forms, we can call funtions to directly calculate.
    However, if special functions are involved, the computation cost can be high and an pre-calculated transform table
    can be used. 
    
    To Keep numerical precision and meet the sampling gridding error requirementaion (that is the sampling transfer error 
    in X_{i} is smaller than pixel size / bin size. It's easier to build the table from a regular oversamped grid in x,
    then calculate the crosspoding p value (within 0~1). Of course the regular oversamped x value can not go to +finity,
    and an upper limit should be given:
        e.g. x_grid=np.linspace(0,100,10000) may be good enought for "expon2d",
            this means the transfered x from interpolated should have error(x)<=0.01Re (as we use linear interp to 
            replace the actual curve), withinin 100Re (more than 
            enought for our modeling accuray)
            
    However, another numerical problem may occare as large x may lead to very close to 1 in this case, and numercial 
            accurcy may degrade lead to 1: see:
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html
            note on _logsf
            and the test_custom_ppf_learn(): x=100 will lead to q=1 rather than something cose to zero.
    The solution is calculate sf=1-q=1-CDF or logsf=log(1-q)=log(1-CDF); 
    then the small deviation from 1 can still be acturrately represented numerically. And we can use x vs. logsf table to transfer ur to x-domain acurrate enought for gridding purpose
    
    The computer is good at saving small number close to zero rather than a number very close to one.
        https://scicomp.stackexchange.com/questions/20629/when-should-log1p-and-expm1-be-used
        
    note: the interplation method is only used for the transform in which the calculatione becomes to expensive
    
    
    The inverse function x=isf(sf):
        if sf is a uniform (0-1) random variable, then x should follow the desired distribution
    
    use sf instead of CDF is for numerical precsion purpose.
    
    We only use this to build interpolation table for expensive case; so only func='expon2d' & 'sersic2d'
    are implemented.
    """

    if  func=='expon2d':
        # \prop~r*exp(-r): r>0
        # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.sc.lambertw.html
        sf=(1+x)*np.exp(-x)
        
    if  func=='sersic2d':
        # \prop~r*sersic(r,n,re=1) r>0
        bn=sc.gammaincinv(2*sersic_n, 0.5)
        sf=sc.gammaincc(2*sersic_n,bn*x**(1/sersic_n)) 

    return sf

def custom_pdf(func,x,sersic_n=1):
    """
    note:
        the pdf values is not normalized: int(pdf*dx) is not one!
    Although we can use scipy.stats, we write a customized code here to improve performance.
    """
    if  func=='sersic':
        bn=sc.gammaincinv(2*sersic_n, 0.5)
        pdf=np.exp( -bn * ( (x)**(1/sersic_n)-1 ) )
    
    if  func=='expon':
        pdf=np.exp(-x)
        
    if  func=='norm':
        pdf=np.exp(-x**2/2)
        
    if  func=='sech':
        pdf=1.0/np.cosh(x)
        
    if  func=='sech2':
        tmp=np.exp(-x)
        pdf=tmp/(1+tmp)**2
    
    return pdf
    
def custom_ppf(func,q,sersic_n=1):

    """
    *** we also wrap the random generator into rv_continous class ***
    *** but this inline function may have better performance without the error checking overhead in rv_continous class
    
    To build a fast persodu-random genenrator for an analytical function, the key is calculate the inverse cumlutative 
    diftributon function or Percent Point Function  (PPF) in high precisiom:
    This is the parameter reliazation values as a function of CDF (Percent point function):
        https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.stats.norm.html
        https://docs.scipy.org/doc/scipy/reference/tutorial/stats/continuous.html
        https://github.com/scipy/scipy/blob/master/scipy/stats/_continuous_distns.py
        https://docs.scipy.org/doc/scipy/reference/special.html
        
    Sometimes this function will have an analytical form, which will be good in terms of performance and precision.
    
    should support vector
    Although this is 1D, any fancy function can be further manupilated
    
    https://reference.wolfram.com/language/ref/InverseCDF.html
    
    calculate ppf from percent cutoff for common (regularized/normalized) PDF 
    this can be used for inverse transform sampling
    
    *****
    If "u" is an uniform random number from (0,1), then the output would be 
    a sample following the desired distribution 
    *****
    
    see also the appendix Xue+2020
    
    see also: inverseCDF.nb in MM12
    
    If "-ss" is in the function name, we will use scipy.stats build-in RV class
    
    + typicall using scipy.special will be faster
    
    to use this function as inverse survive function (ISF)
    try:
        sp=1-q
        x=custom_ppf(func,sp)
    
    sersic_n only works for func="sersic2d"
    
    The interpolation sample should stay in:
        x <-> SF or x <->log(SF) space
    As it's difficult to keep the numerical accuracy and x <-> CDF for large x + close to one CDF table
    : when you set up a x grid, for large x, the corrspoding CDF will one due to numerical precision
    
    """
    
    
    
    if  func=='expon2d':
        # \prop~r*exp(-r): r>0
        # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.sc.lambertw.html
        rv=-1-(sc.lambertw((q-1)/np.e,k=-1)).real
          
    if  func=='sersic2d':
        # \prop~r*sersic(r,n,re=1) r>0
        if  np.allclose(sersic_n,1):    
            # lambertw will be slightly faster than gammainvinv in this application
            b1=sc.gammaincinv(2, 0.5)
            rv = (-1-(sc.lambertw((q-1)/np.e,k=-1)).real )/b1
        else:
            bn=sc.gammaincinv(2*sersic_n, 0.5)
            rv=(sc.gammaincinv(2*sersic_n, q)/bn)**sersic_n        
    
    if  func=='norm2d':
        # \prop~r*exp(-r^2/2) r>0
        rv=np.sqrt(2)*np.sqrt(-np.log(1-q))
    
    
    if  func=='sech':
        # \prop~sech(z) -inf<z<+inf
        rv=np.log(np.tan(np.pi*q/2.0))
        #also see:
        #    scipy/stats/_continuous_distns.py
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypsecant.html#scipy.stats.hypsecant
        # rv=stats.hypersecant.ppf(x)    # give the same results
        
    if  func=='sech2':
        # \prop~sech^2(z) -inf<z<+inf
        #rv=np.arctanh(1-2*u)
        rv=0.5*sc.logit(q) # faster
        
    if  func=='laplace':
        # \prop~exp(-|z|) -inf<z<+inf
        up=1-2*q
        rv=np.sign(up)*sc.log1p(-np.abs(up))
        
    if  func=='norm':
        #rv=np.sqrt(2)*sc.erfinv(2*u-1)
        rv=sc.ndtri(q) # faster
        
    return rv
    
def pdf2rv_nd(pdf,size=100000,
              sort=False,interp=True,seed=None):
    """
    Generate a pseudo-random sample (approximately) following a target PDF specified by a n-dimension array
    The inverse transform sampling approach is used without expensive MC.
    see more details here:
        https://stackoverflow.com/questions/21100716/fast-arbitrary-distribution-random-sampling/21101584#21101584
    
    Note:
        + A over-sampled PDF grid (with pdf_sort/pdf_interp=True) is preferred for accuracy.
        + For a input PDF with a shape of (ny,nx), the output will be
            xpos=sample[0,0]
            ypos=sample[1,:]
            xpos and ypos will be in 0-based pixel index units (i.a.xypos=[0,0] means the first pixel center.)
            This convention follow the FITS image format layout.
    """

    pdf_shape=pdf.shape
    pdf_flat=pdf.ravel()
    
    if  sort==True:
        sortindex=np.argsort(pdf, axis=None)
        pdf_flat=pdf_flat[sortindex]
    cdf=np.cumsum(pdf_flat)

    choice = np.random.uniform(high=cdf[-1],size=size)
    index = np.searchsorted(cdf, choice)

    if  sort==True:
        index=sortindex[index]
    index = np.vstack(np.unravel_index(index,pdf_shape))

    if  interp==True:
        sample=np.flip(index,axis=0)-0.5+np.random.uniform(size=index.shape)
    else:
        sample=np.flip(index,axis=0)

    return sample

def cdf2rv(x,cdf,size=100000,seed=None):
    """
    
    **** only here for backward compaibility *****
    
    Generate a pseudo-random random variable set following a target distribution described by the CDF,
    using the inverse transform / pesudo-random number sampling method
    
    The input CDF is presumed to be sorted already with mono increasing trend. 
    
    The result should stay within the range of cdf_x
    
    this is for backward compaibility
    make sure
        x[0] cdf=0
        x[-1] cdf=1
    
    icdf=interpolate.interp1d(y_cdf,x,kind='linear')
    # icdf: inverse cumulative distribution function
    # a.k.a Percent point function (inverse of `cdf`)
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html#scipy.stats.rv_continuous
    # It seems that scipy.interpolate mess up units when x.type is QUANTITY
    return icdf(pick) 
    """
    return custom_rvs({'x':x,'cdf':cdf},size=size,seed=seed) 


def pdf2rv(x,pdf,size=100000,seed=None):
    """
    Generate a pseudo-random random variable set following a target distribution described by the PDF
    using the inverse transform / pesudo-random number sampling method
    
    The result should stay within the range of pdf_x
    """

    cdf=integrate.cumtrapz(pdf,x,initial=0.)
    cdf/=np.max(cdf)
    
    return custom_rvs({'x':x,'cdf':cdf},size=size,seed=seed)



        