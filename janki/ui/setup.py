import os
from os.path import join as opj, abspath
from  .userinput   import dinput
from ..core.config import checkconfig
from ..common.vars import DIR

def setup(configpath):
    if os.path.exists(configpath):
        _ = checkconfig(configpath)
        if _:
            print(f'Config file already exists at {configpath} and appears to be fine.')
            return
        else:
            print(f'Config at {configpath} seems to be corrupted.')
            action = dinput('Do you want to set up a new one (doing so will overwrite the old file)', default='n', choices=['y','n'])
            if action == 'y':
                make_config()
    else:
        make_config()

def make_config():
    descr = {
    'ANKIPATH' : "## Path to your anki folder (https://github.com/dae/anki):\n# Note: An `anki` directory should be present at `ANKIPATH/anki`",
    'COLPATH'  : "## Path to the .anki2 collection you would like to edit:"""
    }
    anki = dinput('Enter the path to your anki installation', 'path/to/anki')
    while (not os.path.exists(anki)) or (os.path.exists(anki) and 'anki' not in os.listdir(anki)):
        print('The provided path does not exist or does not contain the \'anki\' directory.')
        anki = dinput('Enter the path to your anki installation', 'path/to/anki')
    anki = abspath(anki)

    col = dinput('Enter the path to the .anki2 collection file you would like to edit', 'path/to/collection.anki2')
    while not os.path.isfile(col):
        print('The file does not exist.')
        col = dinput('Enter the path to the .anki2 collection file you would like to edit', 'path/to/collection.anki2')
    col = abspath(col)

    cfgpath = opj(DIR,'config')
    with open(cfgpath, 'w') as f:
        print(descr['ANKIPATH'],    file=f)
        print(f'ANKIPATH = {anki}', file=f, end='\n\n')
        print(descr['COLPATH'],     file=f)
        print(f'COLPATH = {col}',   file=f)
    print(f'Config successfully written to {cfgpath}')
