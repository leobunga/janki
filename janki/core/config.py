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
            _checks(exec_locals)
        except:
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


def _checks(exec_locals):
    for key in ['ANKIPATH', 'COLPATH', 'DECK', 'FIELDS',]:
        if key not in exec_locals:
            raise ConfigError(f'\n\nVariable {key} not found in config.')

    for path in ['ANKIPATH', 'COLPATH']:
        if not os.path.exists(exec_locals[path]):
            raise ConfigError(f'\n\nThe path {path}=\'{exec_locals[path]}\' does not exist.')

    if not os.path.exists(exec_locals['COLPATH']+'.jankibak'):
        from shutil import copyfile
        copyfile(exec_locals['COLPATH'], exec_locals['COLPATH']+'.jankibak')
        print(f'A backup of your collection has been created at \'{exec_locals["COLPATH"]}.jankibak\'')

    if exec_locals['ANKIPATH'] not in sys.path:
        sys.path.append(cfg['ANKIPATH'])
    import anki
    col = anki.Collection(exec_locals['COLPATH'])
    names = col.decks.allNames()
    col.close()
    if exec_locals['DECK'] not in names:
        raise ConfigError(f'\n\nThe deck `{exec_locals["DECK"]}` does not exist.\nAvailable decks are: {", ".join(names)}')

    col = anki.Collection(exec_locals['COLPATH'])
    col.decks.select(col.decks.id(exec_locals["DECK"]))
    fields = [i['name'] for i in col.models.current()['flds']]
    col.close()
    for k in exec_locals['FIELDS'].keys():
        if k not in fields:
            jstr = '\n'.join(fields)
            raise ConfigError(f"The FIELD '{k}' is unknown to your selected deck. Available FIELDs with this deck are:\n\n{jstr}\n")
