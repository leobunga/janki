import traceback
import os, sys
from os.path import join as opj
from .exceptions import ConfigError
# from .common.term       import C
import yaml

def readconfig(path):
    with open(path) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    if config['outfile'].startswith('~'):
        config['outfile'] = os.path.expanduser(config['outfile'])
    return config
