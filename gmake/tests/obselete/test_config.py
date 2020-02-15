#   https://docs.python.org/3/library/configparser.html

import configparser
config = configparser.ConfigParser()
config.read('test_config.cfg')

#print(config['bitbucket.org']['ServerAliveInterval'])
#print(config['DEFAULT']['ServerAliveInterval.test'])
print(type(config['DEFAULT']['ServerAliveInterval.test']))
print((config['DEFAULT']['ServerAliveInterval.test']))
#print(type(config['DEFAULT']['Test']))
#print((config['DEFAULT']['Test']))

with open('test_config_out.cfg', 'w') as configfile:
    config.write(configfile)


import configparser
config = configparser.ConfigParser()
config.read('/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/bx610/xysf_k_ab.cfg')
cfg_dct=config._sections

with open('test_config_example.cfg', 'w') as configfile:
    config.write(configfile)
    
    
