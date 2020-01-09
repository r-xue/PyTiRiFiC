import numpy as np
import scipy.integrate
from scipy import interpolate
from scipy import integrate

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
    Generate a pseudo-random random variable set following a target distribution described by the CDF,
    using the inverse transform / pesudo-random number sampling method
    
    The input CDF is presumed to be sorted already with mono increasing trend. 
    
    The result should stay within the range of cdf_x
    """

    y_cdf=cdf-cdf[0]
    y_cdf/=np.max(y_cdf)
    rng = np.random.RandomState(seed=seed)  
    pick =rng.random_sample(size)
    
    
    """
    icdf=interpolate.interp1d(y_cdf,x,kind='linear')
    # icdf: inverse cumulative distribution function
    # a.k.a Percent point function (inverse of `cdf`)
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html#scipy.stats.rv_continuous
    # It seems that scipy.interpolate mess up units when x.type is QUANTITY
    return icdf(pick) 
    """
    return np.interp(pick,y_cdf,x)


def pdf2rv(x,pdf,size=100000,seed=None):
    """
    Generate a pseudo-random random variable set following a target distribution described by the PDF
    using the inverse transform / pesudo-random number sampling method
    
    The result should stay within the range of pdf_x
    """

    cdf=integrate.cumtrapz(pdf,x,initial=0.)
    
    return cdf2rv(x,cdf,size=size,seed=seed)