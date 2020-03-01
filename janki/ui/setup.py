import os
from os.path import join as opj, abspath
from  .userinput   import dinput
from ..core.config import checkconfig
from ..            import __path__ as jpath

TEMPLATE = """
## Path to your anki folder (https://github.com/dae/anki):
# Try `find / -name anki 2> /dev/null` if you do not know your anki path
# Note: An `anki` directory should be present at `ANKIPATH/anki`
ANKIPATH = '/path/to/anki'

## Path to the .anki2 collection you would like to edit
COLPATH  = '/path/to/collection.anki2'

## Name or ID of the Anki deck you would like to edit
DECK = 'Yomichan'

## Mapping of the four Janki search esult fields fields in your Anki DECK.
# Replace each 'ANKIFIELD' with the actual field name.
# If you dont know your DECKS field names, run `janki setup`, if the paths above are properly defined,
#  the script will give a hint about the names you can use.
# Note: Unassigned fields will be left blank.
FIELDS = {
'ANKIFIELD' : 'Kanji'      ,
'ANKIFIELD' : 'Reading'    ,
'ANKIFIELD' : 'Translation',
'ANKIFIELD' : 'Info'       ,
}

## Miscellaneous settings
MISC = {
'Add parts of speech' : True,
'Add tags'            : True,
'Enumerate entries'   : True,
'Entry separator'     : '<br>',
}

"""

def setup(configpath):
    if os.path.exists(configpath):
        _ = checkconfig(configpath)
        if _:
            print(f'Config file found at {configpath} and is working fine.')
        else:
            print(f'\nConfig file found at {configpath} but it seems to be corrupted.')
            print('Check the above message and make sure all variables are making sense.')
            print('You can also choose to overwrite the file with a template if you are very lost.')
            action = dinput('\nDo you want to overwrite the existing config with the template?', default='n', choices=['y','n'])
            if action == 'y':
                make_config()
    else:
        make_config()

def make_config():
    cfgpath = opj(jpath[0],'config')
    with open(cfgpath, 'w') as f:
        print(TEMPLATE, file=f)
    print(f'Config template successfully written to {cfgpath}.')
    print('Make sure the variables are making sense before proceeding!')
