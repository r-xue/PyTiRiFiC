
from gmake import gmake_casa

import subprocess
import sys

try:
    casa_version=cu.version_string()
except:
    casa_version=None
    
if  casa_version is None:

    script_name='../casa/ms2im.py'
    script_para='./test_casa_ms2im.last'
    script_log='./test_casa_ms2im.log'
    
    """
    print("\n test1: \n")
    gmake_casa(script_name,input=script_para,logs=script_log)
    
    print("\n test2: \n")
    gmake_casa(script_name,input=script_para,verbose=True)    
    
    print("\n test3: \n")
    gmake_casa("print('try something inline within CASA') ; print(cu.version_string())",verbose=True)
    """
    
    vis        =    '../../examples/bx610/models/uvb6_ab/p_fits/data_b6_bb2.ms'
    imagename  =  vis.replace('.ms','').replace('/data_','/cmodel_')

    
    # these works 
    gmake_casa("print('try something inline within CASA') ; print(a) ; print(b) ",'a=1 b=2',verbose=True)
    gmake_casa("print('try something inline within CASA') ; print(a) ; print(b) ",'a=1 ; b =2',verbose=True)
    # this doesn't work by design
    #gmake_casa("print('try something inline within CASA') ; print(a) ; print(b) ",'a=1 b =2',verbose=True)
    # this works
    
else:
    
    cu.getrc()
    cu.hostinfo()
    print("please run this script in Python/IPython, not under CASA")