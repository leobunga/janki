import os
from os.path import join as opj, abspath
from  .userinput   import dinput
from ..core.config import checkconfig
from ..common.vars import DIR

TEMPLATE = """## Path to your anki folder (https://github.com/dae/anki):
#  Note: An `anki` directory should be present at `ANKIPATH/anki`
ANKIPATH = '/path/to/anki'

## Path to the .anki2 collection you would like to edit
COLPATH  = '/path/to/collection.anki2'
"""

def setup(configpath):
    if os.path.exists(configpath):
        _ = checkconfig(configpath)
        if _:
            print(f'Config file found at {configpath} and is working fine.')
        else:
            print(f'\nConfig file found at {configpath} bit it seems to be corrupted.')
            print('Check the above message and make sure all variables are making sense.')
            print('You can also choose to overwrite the file with a template if you are lost.')
            action = dinput('Do you want to overwrite the existing config with the template?', default='n', choices=['y','n'])
            if action == 'y':
                make_config()
    else:
        make_config()

def make_config():
    cfgpath = opj(DIR,'config')
    with open(cfgpath, 'w') as f:
        print(TEMPLATE, file=f)
    print(f'Config template successfully written to {cfgpath}.')
    print('Make sure the variables are making sense before proceeding!')
