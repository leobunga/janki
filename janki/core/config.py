import traceback
import os, sys
from os.path import join    as opj
from os.path import dirname as opd

def readconfig(fpath=None):
    # Return the locals() of the executed code from `fpath`, thanks to Robert

    if not fpath:
        fpath = opj( opd(opd(opd(__file__))), 'config' )
    if not os.path.isfile(fpath):
        print(f'No config found in: `{fpath}`')
        sys.exit(1)

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
            sys.exit(1)

    for key in ['ANKIPATH', 'COLPATH']:
        if key not in exec_locals:
            print(f'Variable {key} not found in {fpath}')
            print('Check your config or run the configuration helper again.')
            sys.exit(1)

    for path in ['ANKIPATH', 'COLPATH']:
        if not os.path.exists(exec_locals[path]):
            print(f'The path {path}=\'{exec_locals[path]}\' does not exist.')
            print(f'Check your config ({fpath}) or run the configuration helper again.')
            sys.exit(1)

    return exec_locals
