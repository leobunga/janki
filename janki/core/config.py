import traceback
import os, sys
from os.path import join    as opj
from os.path import dirname as opd
from ..common.exceptions import ConfigError

def readconfig(fpath=None):
    # Return the locals() of the executed code from `fpath`, thanks to Robert

    if not fpath:
        fpath = opj( opd(opd(opd(__file__))), 'config' )
    if not os.path.isfile(fpath):
        raise ConfigError(f'\n\nNo config found in: `{fpath}`')

    with open(fpath, 'r') as f:
        try:
            exec_locals = {} # Store and return these locals
            code        = compile(f.read(), fpath, 'exec')
            exec(code, {}, exec_locals)
        except Exception:
            print('An exception occurred while reading the config:')
            print('===============================================')
            traceback.print_exc()
            print('=====================================================')
            print('This probably indicates an error in your config file.')
            raise ConfigError

    for key in ['ANKIPATH', 'COLPATH']:
        if key not in exec_locals:
            raise ConfigError(f'\n\nVariable {key} not found in {fpath}\nCheck your config or run the configuration helper again.')

    for path in ['ANKIPATH', 'COLPATH']:
        if not os.path.exists(exec_locals[path]):
            raise ConfigError(f'\n\nThe path {path}=\'{exec_locals[path]}\' does not exist.\nCheck your config ({fpath}) or run the configuration helper again.')

    return exec_locals


def checkconfig(fpath):
    try:
        readconfig(fpath)
        return True
    except:
        return False
