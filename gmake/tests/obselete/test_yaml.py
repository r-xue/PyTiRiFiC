#import yaml
#import ruamel.yaml as yaml
import yaml
#from astropy.io.misc import yaml
import numpy as np
dic={}

dictionary = {
    "a": [1, 2],
    "b": [4, 5]}
    

dic['test']=[1,2,3]
dic['hello']='test'

configfile = open('config.yaml', 'w')
yaml.dump(dic,configfile)
print(yaml.dump(dictionary))

dic_back=yaml.load('config.yaml', Loader=yaml.FullLoader)


"""

import sys
import ruamel.yaml as yaml
from ruamel.yaml.comments import CommentedSeq, CommentedMap
import pprint

cm = CommentedMap()
cm['a'] = 5
cm['b'] = 6
cm['c'] = 7
cm['d'] = cl = CommentedSeq([1, 2, 3])
cl.append(4)
cl.fa.set_flow_style()
yaml.dump(cm, sys.stdout, Dumper=yaml.RoundTripDumper)

with open("test.yaml", 'r') as stream:
    data=yaml.safe_load(stream)

with open('test_out.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data,outfile,Dumper=yaml.RoundTripDumper)
    
    
# ruamle.yaml is slightly better formatted than pyyaml

"""
