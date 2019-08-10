
from gmake import gmake_casa

import subprocess
import sys

try:
    casa_version=cu.version_string()
except:
    casa_version=None
    
if  casa_version is None:
    

    
    task="print('try something inline within CASA') ; print(a) ; print(b) "
    
    print("\n"+"#"*30+"\ntest_gmake_casa: example1\n"+"#"*30)
    gmake_casa(task,is_expr=True,input='a=1 ; b =2',verbose=True)
    
    print("\n"+"#"*30+"\ntest_gmake_casa: example2\n"+"#"*30)
    gmake_casa(task,is_expr=True,input={'a':1,'b':3},verbose=True)
    
    print("\n"+"#"*30+"\ntest_gmake_casa: example3\n"+"#"*30)
    gmake_casa('test_gmake_casa_task',is_expr=False,input={'a':1,'b':3,'vis':'xyz.ms'},verbose=True)
    
    vis        = '../../examples/bx610/models/uvb6_ab/p_fits/data_b6_bb2.ms'
    imagename  =  vis.replace('.ms','').replace('/data_','/cmodel_')
    datacolumn = 'corrected'
    
    print("\n"+"#"*30+"\ntest_gmake_casa: example4\n"+"#"*30)
    gmake_casa('ms2im',input={'vis':vis,'imagename':imagename,'datacolumn':datacolumn},verbose=True)    

    
    print("\n"+"#"*30+"\ntest_gmake_casa: example5\n"+"#"*30)
    script_name='../casa/ms2im.py'
    script_para='./test_casa_ms2im.last'
    script_log='./test_casa_ms2im.log'
    
    gmake_casa(script_name,input=script_para,verbose=True,logs=script_log) 
    
else:
    
    cu.getrc()
    cu.hostinfo()
    print("please run this script in Python/IPython, not under CASA")