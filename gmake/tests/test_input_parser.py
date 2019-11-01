from configparser import ConfigParser
config = ConfigParser()
config.read('test_inp.cfg')
config_dct=config._sections

from pprint import pprint
pprint(config_dct)


config1 = ConfigParser()
config1.read_dict(config_dct)

with open('test_out.cfg', 'w') as configfile:
    config1.write(configfile)