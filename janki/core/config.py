import traceback
import os, sys
from os.path import join    as opj
from os.path import dirname as opd
from ..common.exceptions import ConfigError

def readconfig(fpath=None, verbose=True):
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
            exec_locals['__file__'] = fpath

            for key in ['ANKIPATH', 'COLPATH', 'FIELDS']:
                if key not in exec_locals:
                    raise ConfigError(f'\n\nVariable {key} not found in config.')

            for path in ['ANKIPATH', 'COLPATH']:
                if not os.path.exists(exec_locals[path]):
                    raise ConfigError(f'\n\nThe path {path}=\'{exec_locals[path]}\' does not exist.')

        except Exception:
            if verbose:
                s = f'An exception occurred while reading the config in {fpath}:'
                print(s)
                print(len(s)*'=')
                traceback.print_exc()
                print(len(s)*'=')
                print('This probably indicates an error in your config file.')
            raise ConfigError

    return exec_locals


def checkconfig(fpath, verbose=True):
    try:
        readconfig(fpath, verbose)
        return True
    except:
        return False
