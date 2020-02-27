from gmake import stats as gm_stats
import numpy as np
from scipy import special as sc
from scipy import special
from scipy import integrate
from scipy import stats

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import fast_histogram as fh
import timeit
import numexpr as ne
import time
import adaptive
import pprint

from functools import partial
import random  

from gmake.stats import sersic2d,expon2d,norm2d,sech,sech2,sechsq,laplace,norm


def test_custom_ppf_learn_fun(q):
    """
    """
    return gm_stats.custom_ppf('sersic2d',q,sersic_n=2)
    
def test_custom_invtransform_interp():
    
    # https://github.com/python-adaptive/adaptive/pull/218
    # https://github.com/python-adaptive/adaptive/issues/1
    
    from gmake import stats as gm_stats
    import adaptive
    #adaptive.notebook_extension(_inline_js=False)

    sersic_n=2
    
    q=np.linspace(0,1,1000000)
    #q=q[1:-2]
    start_time = time.time()
    x=gm_stats.custom_ppf('sersic2d',q,sersic_n=sersic_n)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_sersic2d',time.time()-start_time))
    
    #adaptive.notebook_extension(_inline_js=False)
    start_time = time.time()
    learner=adaptive.Learner1D(test_custom_ppf_learn_fun,bounds=(0,1))
    runner = adaptive.runner.simple(learner, goal=lambda l: l.loss() < 0.01)    
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_sersic2d',time.time()-start_time))
    
    q_lr=[]
    x_lr=[]
    for key in learner.data.keys():
        q_lr.append(key)
        x_lr.append(learner.data[key])
    q_lr=np.array(q_lr)
    x_lr=np.array(x_lr)
    
    ind=q_lr.argsort()
    q_lr=q_lr[ind]
    x_lr=x_lr[ind]

    fig=plt.figure(figsize=(10,6))
    
    
    ax=fig.add_subplot(231)
    ax.plot(q_lr,x_lr,label='Learner1D-interp',alpha=0.5)
    ax.scatter(q_lr,x_lr,label='Leaner1D-sampling',alpha=0.5)
    print('npoints',len(q_lr))
    qx=gm_stats.custom_ppf('sersic2d',q,sersic_n=sersic_n)
    ax.plot(q,x,lw=10,alpha=0.5,label='True')
    ax.set_ylim(0,20)
    
    ax.set_xlabel('CDF')
    ax.set_ylabel('R/Re')
    ax.legend()
    #ax.set_yscale('log')

    ax=fig.add_subplot(234)    
    x_lr_interp=np.interp(q,q_lr,x_lr)
    ax.plot(x,x_lr_interp-x,alpha=0.5)
    ax.set_ylim(-0.2,0.2)
    ax.set_xlim(0,100)
    #ax.set_yscale('log')    
    ax.set_xlabel("R/Re")
    ax.set_ylabel("error(R/Re)")
    
    
    
    ##########################################
        
    sersic_n=1
    
    bn=sc.gammaincinv(2*sersic_n,0.5)
    # true value
    x_true=np.linspace(0,100,1000000)
    q_true=sc.gammainc(2*sersic_n,bn*x_true**(1/sersic_n))
    if  sersic_n==1:
        b1=sc.gammaincinv(2, 0.5)
        q_true=1-(1+x_true*b1)*np.exp(-x_true*b1)
    # coarse true value
    x_grid_true=np.linspace(0,100,1000) 
    q_grid_true=sc.gammainc(2*sersic_n,bn*x_grid_true**(1/sersic_n))
    if  sersic_n==1:
        b1=sc.gammaincinv(2, 0.5)
        q_grid_true=1-(1+x_grid_true*b1)*np.exp(-x_grid_true*b1)    

    
    ax=fig.add_subplot(232)    
    ax.scatter(q_grid_true,x_grid_true,label='Truth-coarse-sampling',alpha=0.5)
    ax.plot(q_true,x_true,lw=5,label='True',alpha=0.5)
    ax.set_ylim(0,100)
    ax.legend()
    ax.set_xlabel("CDF")
    ax.set_title("Interp-Table in X->CDF")
    #ax.set_yscale('log') 
    
    ax=fig.add_subplot(235)
    #we get interp(x) for each real(x):
    #   for each real(x) get real(q) -> get interp (x) from real(x,p) pair
    x_interp=np.interp(q_true,q_grid_true,x_grid_true)
    #pprint.pprint(q_sp)
    #pprint.pprint()
    
    ax.plot(x_true,x_interp-x_true)
    ax.set_ylim(-0.1,0.1)    
    ax.set_xlim(0,30)
    ax.set_xlabel("R/Re")
    ax.set_ylabel("error(R/Re)_predict")
    
    # this is problematica since the interpolation table is hard to keep precision near
    # large x where CDF is close to one
    
    ##########################################
    
    ax=fig.add_subplot(233)
        
    # we present sf_true vs x_true
    # the accuracy is preserved for large x as SF near 0 can be kept for high precsion
    # for interpolation or presentation purpose
    
    x_true=np.linspace(0,100,1000000)
    sf_true=gm_stats.custom_sf('expon2d',x_true,sersic_n=2)
    ax.plot(sf_true,x_true,alpha=0.5,lw=2,label='trueth')

    start_time = time.time()
    x_grid_true=np.linspace(0,100,100000)
    sf_grid_true=gm_stats.custom_sf('expon2d',x_grid_true,sersic_n=2)
    ind=sf_grid_true.argsort()
    x_interp=np.interp(sf_true,sf_grid_true[ind],x_grid_true[ind])
    print("---{0:^10} : {1:<8.5f} seconds ---".format('ITS (SF interp) cost',time.time()-start_time)) 
    
    start_time = time.time()
    tmp=gm_stats.custom_ppf('expon2d',sf_true)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('ITS (custom_ppf) cost',time.time()-start_time)) 
    
    ax.scatter(sf_grid_true,x_grid_true,alpha=0.5,lw=2,label='Truth-coarse-sampling')
    ax.set_xlabel('Survive function')
    ax.set_ylabel('R/Re')
    ax.legend()    
    ax.set_title("Interp-Table in X->SF")

    ax=fig.add_subplot(236)
    ax.plot(x_true,x_interp-x_true)
    ax.set_xlabel("R/Re")
    ax.set_ylabel("error(R/Re)_predict")
    print('max(error)',np.max(np.abs(x_interp-x_true)))
    fig.tight_layout()
    fig.savefig('test_custom_invtransform_interp.pdf')
    plt.close()        
    
    return


def test_ppf_sech2_performance():
    """
    We check ppf performance here:
    stats.ppf performance is generally worst due to wrapping
    we can call ._ppf to slightly reduce overhead
     
    https://stackoverflow.com/questions/3985619/how-to-calculate-a-logistic-sigmoid-function-in-python
    
    """
    p=np.random.rand(int(1e7))
    
    setup_code="""
import numpy as np
import numexpr as ne
from scipy import special as sc 
p=np.random.rand(int(1e7))
from scipy.stats import logistic
sech2 = logistic(scale=0.5)
    """
    main_code1="""
ne.evaluate('0.5*log(p/(1-p))')
    """
    main_code2="""
0.5*sc.logit(p)
    """
    main_code3="""
np.arctanh(2*p-1)
    """
    main_code4="""
0.5*np.log(p/(1-p))
    """        
    main_code5="""
(-0.5)*np.log(1/p-1)
    """            
    main_code5="""
sech2.ppf(p)
    """ 
        
    #time ne.evaluate('0.5*log(p/(1-p))')
    print("test_ppf_sech2_performance")
    print(timeit.timeit(stmt=main_code1,setup=setup_code,number=10))
    print(timeit.timeit(stmt=main_code2,setup=setup_code,number=10))
    print(timeit.timeit(stmt=main_code3,setup=setup_code,number=10))
    print(timeit.timeit(stmt=main_code4,setup=setup_code,number=10))
    print(timeit.timeit(stmt=main_code5,setup=setup_code,number=10))
    """
0.213603361999958
0.9265875829999004
1.6657896990000154
1.0486936380000316
6.520332013999905    # the class-wrapping appraoch in stats.logistics is slowing thing done.
    """

    

def test_rvs_sech2_performance():

    """
    stats.ppf leads to large overhead but, stats.rvs seems to be comparable with a explicit code.
    https://github.com/scipy/scipy/issues/1914
    https://github.com/edeno/Jadhav-2016-Data-Analysis/issues/82
    looks like: .ppf spend a large overhead for generic parameter checking
    
        import numpy as np
        import numexpr as ne
        import os
        from scipy import special as sc
        np.__config__.show()
        os.environ['OPENBLAS_NUM_THREADS'] = '1'
        os.environ["OMP_NUM_THREADS"] = "1"
        os.environ['MKL_NUM_THREADS'] = '1'
        os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
        os.environ["NUMEXPR_NUM_THREADS"] = "1"
    """    
    setup_code="""
import numpy as np
import numexpr as ne
from scipy import special as sc 
p=np.random.rand(int(1e7))
from scipy.stats import logistic
sech2 = logistic(scale=0.5)
from gmake.stats import sersic2d,expon2d,norm2d,sech,sech2,sechsq,laplace,norm
    """
        
    mc1="""    
sech2.rvs(size=int(1e7))
"""        
    mc1p="""
sechsq.rvs(size=int(1e7))
"""
    mc2p="""
rv=np.random.rand(int(1e7))
"""  

# this is pretty bad...
    mc2="""
rv=sech2.ppf(np.random.rand(int(1e7)))
"""    
    mc3="""
rv=sechsq.ppf(np.random.rand(int(1e7)))
"""    
# ._ppf performanced better than .ppf
    mc3p="""
rv=sechsq._ppf(np.random.rand(int(1e7))) 
"""    
    mc4="""
rv=0.5*sc.logit(np.random.rand(int(1e7)))        
"""
    mc5="""    
rv=(-0.5)*np.log(1/np.random.rand(int(1e7))-1)
"""
# ne.out (*chunk*)
#   https://code.google.com/archive/p/numexpr/#Why_It_Works
#   python -c"import numexpr; numexpr.print_versions()"
    mc6="""    
rv=np.random.rand(int(1e7))
ne.evaluate("(-0.5)*log(1/rv-1)",out=rv)
"""
    print("test_ppf_sech2_performance")
    print(timeit.timeit(stmt=mc1,setup=setup_code,number=10))
    print(timeit.timeit(stmt=mc1p,setup=setup_code,number=10))
    print(timeit.timeit(stmt=mc2p,setup=setup_code,number=10))
    print(timeit.timeit(stmt=mc2,setup=setup_code,number=10))
    print(timeit.timeit(stmt=mc3,setup=setup_code,number=10))
    print(timeit.timeit(stmt=mc3p,setup=setup_code,number=10))
    print(timeit.timeit(stmt=mc4,setup=setup_code,number=10))
    print(timeit.timeit(stmt=mc5,setup=setup_code,number=10))
    print(timeit.timeit(stmt=mc6,setup=setup_code,number=10))

"""
2.0861017530000936
1.8044886980001138
0.6911269649999667
7.189131905999602
7.1829417060002925
1.5958998329997485
1.5997248590001618
0.8552806279999459
"""
    
def test_custom_rvs_performance():
    
    sc_code="""
import numpy as np
import numexpr as ne
from scipy import special as sc 
p=np.random.rand(int(1e7))
from scipy.stats import logistic
sech2 = logistic(scale=0.5)
from gmake.stats import custom_ppf
from gmake.stats import custom_rvs
    """
    
    mc1="""
rv=custom_rvs('norm',size=10000000,scale=2)
    """
    mc2="""
rv=custom_rvs('laplace',size=10000000,scale=2)
#rv=custom_rvs('uniform',size=10000000,scale=2)
    """    
    mc3="""
rv=custom_rvs('sech2',size=10000000,scale=2)
    """     
    mc4="""
rv=custom_rvs('sech',size=10000000,scale=2)
    """         
    mc5="""
rv=custom_rvs('norm2d',size=10000000,scale=2)
    """      
    mc6="""
rv=custom_rvs('sersic2d',size=10000000,scale=2,sersic_n=2,interp=(0.02,20))
    """    
    mc7="""
rv=custom_rvs('expon2d',size=10000000,scale=2,interp=(0.02,20))
    """
    mc6d="""
rv=custom_rvs('sersic2d',size=10000000,scale=2,sersic_n=2,interp=None)
    """
    mc7d="""
rv=custom_rvs('expon2d',size=10000000,scale=2,interp=None)
    """                 
    print('mc1:',timeit.timeit(stmt=mc1,setup=sc_code,number=1))
    print('mc2:',timeit.timeit(stmt=mc2,setup=sc_code,number=1))
    print('mc3:',timeit.timeit(stmt=mc3,setup=sc_code,number=1))
    print('mc4:',timeit.timeit(stmt=mc4,setup=sc_code,number=1))
    print('mc5:',timeit.timeit(stmt=mc5,setup=sc_code,number=1))
    print('mc6:',timeit.timeit(stmt=mc6,setup=sc_code,number=1))
    print('mc7:',timeit.timeit(stmt=mc7,setup=sc_code,number=1))
    print('mc6d:',timeit.timeit(stmt=mc6d,setup=sc_code,number=1))
    print('mc7d:',timeit.timeit(stmt=mc7d,setup=sc_code,number=1))
    
    mc1="""
rv=custom_rvs('norm',size=1000000,scale=2)
    """
    mc2="""
rv=custom_rvs('laplace',size=1000000,scale=2)
#rv=custom_rvs('uniform',size=1000000,scale=2)
    """    
    mc3="""
rv=custom_rvs('sech2',size=1000000,scale=2)
    """     
    mc4="""
rv=custom_rvs('sech',size=1000000,scale=2)
    """         
    mc5="""
rv=custom_rvs('norm2d',size=1000000,scale=2)
    """      
    mc6="""
rv=custom_rvs('sersic2d',size=1000000,scale=2,sersic_n=2,interp=(0.02,20))
    """    
    mc7="""
rv=custom_rvs('expon2d',size=1000000,scale=2,interp=(0.02,20))
    """
    mc6d="""
rv=custom_rvs('sersic2d',size=1000000,scale=2,sersic_n=2,interp=None)
    """
    mc7d="""
rv=custom_rvs('expon2d',size=1000000,scale=2,interp=None)
    """                 
    print('mc1:',timeit.timeit(stmt=mc1,setup=sc_code,number=1))
    print('mc2:',timeit.timeit(stmt=mc2,setup=sc_code,number=1))
    print('mc3:',timeit.timeit(stmt=mc3,setup=sc_code,number=1))
    print('mc4:',timeit.timeit(stmt=mc4,setup=sc_code,number=1))
    print('mc5:',timeit.timeit(stmt=mc5,setup=sc_code,number=1))
    print('mc6:',timeit.timeit(stmt=mc6,setup=sc_code,number=1))
    print('mc7:',timeit.timeit(stmt=mc7,setup=sc_code,number=1))
    print('mc6d:',timeit.timeit(stmt=mc6d,setup=sc_code,number=1))
    print('mc7d:',timeit.timeit(stmt=mc7d,setup=sc_code,number=1))    

def test_custom_ppf_performance():
    """
    mpmath/sympy performance is worse than scipy.special
    although its special function collection may be larger
    check the scipy build-in option here:
        https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html
    """
    sc_code="""
import numpy as np
import numexpr as ne
from scipy import special as sc 
p=np.random.rand(int(1e7))
from scipy.stats import logistic
sech2 = logistic(scale=0.5)
from gmake.stats import custom_ppf
    """
    
    mc1="""
rv=custom_ppf('expon2d',p)
    """
    mc2="""
rv=custom_ppf('sersic2d',p)
    """    
    mc3="""
rv=custom_ppf('norm2d',p)
    """  
    mc4="""
rv=custom_ppf('sech',p)
    """      
    mc5="""
rv=custom_ppf('sech2',p)
    """
    mc6="""
rv=custom_ppf('laplace',np.random.rand(int(1e7)))
    """      
    mc6p="""    
#rv=np.random.exponential(size=int(1e7))
rv=np.random.laplace(size=int(1e7)) # slightly faster
    """        
    mc7="""
rv=custom_ppf('norm',p)
    """      
    mc8="""
rv=np.random.randn(int(1e7))
    """      
    mc9="""
# slightly slower    
rv=custom_ppf('norm',np.random.rand(int(1e7)))
    """        
            
    print('mc1:',timeit.timeit(stmt=mc1,setup=sc_code,number=1))
    print('mc2:',timeit.timeit(stmt=mc2,setup=sc_code,number=1))
    print('mc3:',timeit.timeit(stmt=mc3,setup=sc_code,number=1))
    print('mc4:',timeit.timeit(stmt=mc4,setup=sc_code,number=1))
    print('mc5:',timeit.timeit(stmt=mc5,setup=sc_code,number=1))
    print('mc6:',timeit.timeit(stmt=mc6,setup=sc_code,number=1))
    print('mc6p:',timeit.timeit(stmt=mc6p,setup=sc_code,number=1))
    print('mc7:',timeit.timeit(stmt=mc7,setup=sc_code,number=1)) 
    print('mc8:',timeit.timeit(stmt=mc8,setup=sc_code,number=1)) 
    print('mc9:',timeit.timeit(stmt=mc9,setup=sc_code,number=1)) 
    
"""
1.9816010099998493
4.211996406000253
0.10972880700001042
0.20146700900022552
0.0871336519999204
0.1863947750002808
0.18302789199969993
0.24400783600003706
0.26482248399997843
"""  




    

def test_custom_ppf():
    """
    examine custom_ppf implementation vs. scipy/numpy built-in RVS results
    numpy has np.random implement rvs at C-level
    scipy has scipy.stats.dist with more distribution and related function, but may not have fastest implemnatation
    """
    
    
    q=np.linspace(0,1,1000000)
    q=q[1:-2]
    
    fig=plt.figure(figsize=(20,7))
    ax=fig.add_subplot(121)
    
    ##### laplace
    
    start_time = time.time()
    x=stats.laplace.ppf(q)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('stats.laplace.ppf',time.time()-start_time))    
    ax.plot(q,x,label='scipy.stats.laplace.pdf',alpha=0.5)
    
    start_time = time.time()
    x=gm_stats.custom_ppf('laplace',q)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_laplace',time.time()-start_time))    
    ax.plot(q,x,label='gmake.stats.custom_laplace',lw=10,alpha=0.5)
    
    ##### sech
    
    start_time = time.time()
    x=stats.hypsecant.ppf(q)
    # the arg check work around the -infinity +finity limit 
    print("---{0:^10} : {1:<8.5f} seconds ---".format('hypsecant.pdf',time.time()-start_time))    
    ax.plot(q,x,label='scipy.stats.hypsecant.pdf',alpha=0.5)
    
    start_time = time.time()
    x=gm_stats.custom_ppf('sech',q)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_sech',time.time()-start_time))    
    ax.plot(q,x,label='gmake.stats.custom_sech',lw=10,alpha=0.5)
    ##### norm
    
    start_time = time.time()
    x=stats.norm.ppf(q)
    # the arg check work around the -infinity +finity limit 
    print("---{0:^10} : {1:<8.5f} seconds ---".format('norm.ppf',time.time()-start_time))    
    ax.plot(q,x,label='scipy.stats.norm.ppf',alpha=0.5)
    
    start_time = time.time()
    x=gm_stats.custom_ppf('norm',q)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_norm',time.time()-start_time))    
    ax.plot(q,x,label='gmake.stats.custom_norm',lw=10,alpha=0.5)        
    
    ax.legend()
    ax.set_xlabel('q / PPF / Inverse-CDF or (1-SF)')
    ax.set_ylabel('x/x_scale')
    ax.set_ylim(-5,5)
    #ax.set_xlim(0,1) 
    
    
    ax1=fig.add_subplot(122)
    
    ##### expon2d

    start_time = time.time()
    x=gm_stats.custom_ppf('expon2d',q)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_ppf_expon2d',time.time()-start_time))    
    ax1.plot(q,x,label='custom_ppf_expon2d',lw=10,alpha=0.5)  
    q_recover=1-gm_stats.custom_sf('expon2d',x,sersic_n=2)       
    ax1.plot(q_recover,x,label='custom_sf_expond',lw=1,alpha=0.5)      
    
    start_time = time.time()
    x=gm_stats.custom_ppf('sersic2d',q)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_ppf_sersic2d n=1',time.time()-start_time))
    ax1.plot(q,x,label='custom_ppf_sersic2d n=1',lw=5,alpha=0.5)    
    #ax1.plot(q,x*sc.gammaincinv(2, 0.5),label='gmake.stats.custom_sersic2d',lw=5,alpha=0.5)
    q_recover=1-gm_stats.custom_sf('sersic2d',x,sersic_n=1)       
    ax1.plot(q_recover,x,label='custom_sf_sersic2d n=1',lw=1,alpha=0.5) 
    
    start_time = time.time()
    x=gm_stats.custom_ppf('sersic2d',q,sersic_n=2)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_sersic2d n=2',time.time()-start_time))
    ax1.plot(q,x,label='custom_ppf_sersic2d n=2)',lw=10,alpha=0.5) 
    q_recover=1-gm_stats.custom_sf('sersic2d',x,sersic_n=2)       
    ax1.plot(q_recover,x,label='custom_sf_sersic2d n=2',lw=1,alpha=0.5)
    
    start_time = time.time()
    x=gm_stats.custom_ppf('norm2d',q)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_norm2d',time.time()-start_time))
    ax1.plot(q,x,label='custom_ppf_norm2d',lw=2,alpha=0.5)    
        
    ax1.legend()
    ax1.set_xlabel('q / PPF / Inverse-CDF ')
    ax1.set_ylabel('x/x_scale')
    ax1.set_ylim(0.01,10)
    #ax1.set_xlim(0,1)    
    ax1.set_yscale('log')

    
    fig.tight_layout()
    fig.savefig('test_custom_ppf.pdf')
    plt.close()

def test_custom_rvs():
    """
    generate a random sampling set following the desired distribution 
    """
    num_bins = 100
    range=(0,8)
    x=np.linspace(0,8,1000)
    b1=special.gammaincinv(2*1, 0.5)
    
    fig=plt.figure(figsize=(15,8))
    ax1=fig.add_subplot(121)
    
    #"""
    name='norm2d'
    def fun1(x):
        return x*np.exp(-x*x/2.)
    int1,err1=integrate.quad(fun1,0,100)
    ax1.plot(x,fun1(x)/int1,label=name+'-True')
    ax1.hist(gm_stats.custom_rvs('norm2d',size=int(1e6)), num_bins,alpha=0.8,range=range,label=name+'-RVS',density=True)
    ax1.hist(norm2d.rvs(size=int(1e6)), num_bins,alpha=0.8,range=range,label=name+'-SubClass-RVS',density=True,histtype='step')
    start_time = time.time()
    tmp=gm_stats.custom_rvs('norm2d',size=int(1e6))
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_norm2d',time.time()-start_time))
    start_time = time.time()
    tmp=gm_stats.custom_rvs('norm2d',size=int(1e6),interp=None)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_norm2d',time.time()-start_time))    
    #"""
    
    #"""
    name='sersic2d-3.0'
    n_set=2.0
    def fun2(x,n):
        bn=special.gammaincinv(2*n, 0.5)
        return x*np.exp(-bn*((x**(1/n)-1)))
    int2,err2=integrate.quad(fun2,0,8,args=(n_set,))    
    ax1.plot(x,fun2(x,n_set)/int2,label=name+'-func')
    ax1.hist(gm_stats.custom_rvs('sersic2d',size=int(1e6),sersic_n=n_set), num_bins,alpha=0.2,range=range,label=name+'-RVS-default',density=True) 
    ax1.hist(gm_stats.custom_rvs('sersic2d',size=int(1e6),sersic_n=n_set,interp=None), num_bins,alpha=0.8,range=range,label=name+'-RVS-direct',density=True,histtype='step',lw=8)
    ax1.hist(sersic2d.rvs(n_set,size=int(1e6)), num_bins,alpha=0.5,range=range,label=name+'-SubClass-RVS',density=True,histtype='step',lw=4)
    start_time = time.time()
    tmp=gm_stats.custom_rvs('sersic2d',size=int(1e6),sersic_n=n_set)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_sersic2d_default',time.time()-start_time))
    start_time = time.time()
    tmp=gm_stats.custom_rvs('sersic2d',size=int(1e6),interp=None,sersic_n=n_set)
    print("---{0:^10} : {1:<8.5f} seconds ---".format('custom_sersic2d_direct',time.time()-start_time)) 
    #"""
    
    # if n_set=1, then rv2_its*b1 PDF should match "halfexpn1dx"
    #n, bins, patches = ax.hist(rv2_its*b1, num_bins,alpha=0.2,range=range,label='rv2_hack',density=True)
    
    name='expon2d'
    rv=np.random.rand(int(1e6))
    def fun3(x):
        return x*np.exp(-x)
    int3,err3=integrate.quad(fun3,0,8)
    ax1.plot(x,fun3(x)/int3,label=name+'-func')
    ax1.hist(gm_stats.custom_rvs('expon2d',size=int(1e6)), num_bins,alpha=0.2,range=range,label=name+'-RVS-default',density=True) 
    ax1.hist(gm_stats.custom_rvs('expon2d',size=int(1e6),interp=None), num_bins,alpha=0.8,range=range,label=name+'-RVS-direct',density=True,histtype='step',lw=8)
    ax1.hist(expon2d.rvs(size=int(1e6)), num_bins,alpha=0.5,range=range,label=name+'-SubClass-RVS',density=True,histtype='step',lw=4)
    
    ax1.set_xlabel('R')
    ax1.set_ylabel('PDF')
    ax1.set_title(r'Inverse Transform Sampling (R of 2D dist)')
    ax1.legend()


    range=(-7,7)
    x=np.linspace(-8,8,1000)
    ax2=fig.add_subplot(122)

    #"""
    name='sech'
    def fun1(x):
        return 1/np.cosh(x)
    int1,err1=integrate.quad(fun1,-100,100)
    ax2.plot(x,fun1(x)/int1,label=name+'-func',lw=3)    
    ax2.hist(gm_stats.custom_rvs('sech',size=int(1e6)), num_bins,alpha=0.2,range=range,label=name+'-RVS',density=True)
    ax2.hist(sech.rvs(size=int(1e6)), num_bins,alpha=0.8,range=range,label=name+'-SubClass-RVS',density=True,histtype='step')
    #"""
    
    #"""
    name='sech2'
    def fun2(x):
        return (1/np.cosh(x))**2
    int2,err1=integrate.quad(fun2,-100,100)
    ax2.plot(x,fun2(x)/int2,label=name+'-func',lw=3)      
    ax2.hist(gm_stats.custom_rvs('sech2',size=int(1e6)), num_bins,alpha=0.2,range=range,label=name+'-RVS',density=True)
    ax2.hist(sech2.rvs(size=int(1e6)), num_bins,alpha=0.8,range=range,label=name+'-SubClass1-RVS1',density=True,histtype='step',lw=10)
    ax2.hist(sechsq.rvs(size=int(1e6)), num_bins,alpha=0.8,range=range,label=name+'-SubClass2-RVS',density=True,histtype='step',lw=4)
    #"""
    
    #"""
    name='laplace'
    def fun3(x):
        return np.exp(-np.abs(x))
    int3,err1=integrate.quad(fun3,-100,100)
    ax2.plot(x,fun3(x)/int3,label=name+'-func',lw=3)     
    ax2.hist(gm_stats.custom_rvs('laplace',size=int(1e6)), num_bins,alpha=0.2,range=range,label=name+'-RVS',density=True)
    ax2.hist(laplace.rvs(size=int(1e6)), num_bins,alpha=0.8,range=range,label=name+'-SubClass-RVS',density=True,histtype='step')
    #"""
    
    name='norm'
    rv=np.random.rand(int(1e6))
    def fun4(x):
        return np.exp(-x**2/2)
    int4,err1=integrate.quad(fun4,-100,100)
    ax2.plot(x,fun4(x)/int4,label=name+'-func',lw=3)    
    ax2.hist(gm_stats.custom_ppf('norm',rv), num_bins,alpha=0.2,range=range,label=name+'-RVS',density=True)
    ax2.hist(norm.rvs(size=int(1e6),random_state=None), num_bins,alpha=0.8,range=range,label=name+'-SubClass-RVS',density=True,histtype='step')

    ax2.set_xlabel('z (height)')
    ax2.set_ylabel('PDF')
    ax2.set_title(r'Inverse Transform Sampling (fun)')
    ax2.set_yscale('log')
    ax2.set_ylim(1e-2,1)
    ax2.set_xlim(-3,5)
    ax2.legend()    

    
    fig.tight_layout()
    fig.savefig('test_custom_rvs.pdf')
    plt.close()



def test_rand_funweight():
    """
    generate a uniform sampling set with weight=fun for each sampling points
    """
    fig, ax = plt.subplots()
    
    num_bins = 30
    range=(0,8)
    x=np.linspace(0,8,1000)
    
    rv=np.random.rand(int(1e6))
    n_set=2
    rv2_its=gm_stats.custom_ppf('halfsersic1dx_n',rv,sersic_n=n_set)
    def fun2(x,n):
        bn=special.gammaincinv(2*n, 0.5)
        return x*np.exp(-bn*((x**(1/n)-1)))
    n, bins, patches = ax.hist(rv2_its, num_bins,alpha=0.2,range=range,label='rv2-sample',density=True) 
    int2,err2=integrate.quad(fun2,0,8,args=(n_set,))
    ax.plot(x,fun2(x,n_set)/int2,label='rv2-func')
    
    # drawback1: we have to specify the interested func range (0,8)
    rv=np.random.rand(int(1e6))*8
    wt=fun2(rv,n_set)
    hist=fh.histogram1d(rv,weights=wt,range=range,bins=num_bins)
    hist_x=np.linspace(range[0],range[1],num_bins)
    sumwt=(hist_x[1]-hist_x[0])*np.sum(wt)
    hist=hist/sumwt
    ax.plot(hist_x+(hist_x[1]-hist_x[0])*0.5,hist)

    fig.tight_layout()
    fig.savefig('test_rand_funweight.pdf')
    plt.close()
    

def test_custom_pdf_wt():
    """
    test different weighting for generating cloudlets
    """
    fig=plt.figure(figsize=(8,8))
    ax=fig.add_subplot(111)
    from gmake.stats import custom_pdf
    
    x=np.linspace(0,10,1000)
    def fun0(x):
        return x
    def fun1(x):
        return custom_pdf('sersic',x)*x
    def fun2(x):
        return custom_pdf('sersic',x)**2*x      
    int0,err0=integrate.quad(fun0,0,10)    
    int1,err1=integrate.quad(fun1,0,10)
    int2,err2=integrate.quad(fun2,0,10)
    ax.plot(x,fun0(x)/int0)
    ax.plot(x,fun1(x)/int1)
    ax.plot(x,fun2(x)/int2)
    #y0=r
    #y1=custom_pdf('sersic')*r
    #y2=custom_pdf('sersic')^2*r
    
    
    fig.tight_layout()
    fig.savefig('test_custom_pdf_wt.pdf')
    plt.close()    
        
if  __name__=="__main__":
    
    
    ###########################################
    # test invtransform interplation method
    #   note: use SF rather than CDF due to numercail precision loss near 1 for larger x
    ###########################################
    
    #test_custom_invtransform_interp()
    
    ###########################################
    # test different methods of ppf/rv calculations
    #   note: write your inline function rather than using scipy.stats.rv_ class
    ###########################################
    
    #test_ppf_sech2_performance()
    #test_rvs_sech2_performance()
    
    ###########################################
    # test custom_rvs performance (direct vs. interp)
    #   note: write your inline function rather than using scipy.stats.rv_ class
    ###########################################    
  
    #test_custom_rvs_performance()
    
    ###########################################
    # test custom_ppf performance (direct vs. interp)
    #   note: write your inline function rather than using scipy.stats.rv_ class
    ###########################################    
  
    #test_custom_ppf_performance()    
    
    ###########################################
    # test_custom_ppf
    ###########################################    
  
    #test_custom_ppf()            
    
    ###########################################
    # test_custom_rvs
    ###########################################    
  
    #test_custom_rvs()          
    
    ###########################################
    # test_custom_pdf_wt
    ########################################### 
        
    test_custom_pdf_wt()
    
    #test_rand_funweight()
