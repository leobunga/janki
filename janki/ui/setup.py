import os
from os.path import join as opj, abspath
from  .userinput   import dinput
from ..core.config import checkconfig
from ..common.term import C
from ..            import __path__ as jpath

TEMPLATE = """# v0.1

## Path to your top level anki folder (https://github.com/dae/anki):
# Try `find / -name anki 2> /dev/null` if you do not know your anki path
# Note: An `anki` directory should be present at `ANKIPATH/anki`
ANKIPATH = '/path/to/anki'

## Path to the .anki2 collection you would like to edit
COLPATH  = '/path/to/collection.anki2'

## Name or ID of the Anki deck you would like to edit
DECK = 'MyDeckName'

## Mapping of the four Janki search result fields to the fields in your Anki DECK.
# Replace each 'ANKIFIELD' with the actual field name.
# If you dont know your DECKS field names, run `janki setup`: If all the paths above
# are properly defined, the script will give a hint about the names you can use.
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
            print(C.str(f'\nConfig file found at {configpath} but it seems to be corrupted.', 'WARNING'))
            print(C.str('Check the above message and make sure all variables are making sense.', 'WARNING'))
            print(C.str('\nIf you are very lost, you can choose to overwrite the existing file with a template by running `janki --reset` instead.', 'WARNING'))
    else:
        make_config(configpath)

def make_config(configpath):
    with open(configpath, 'w') as f:
        print(TEMPLATE, file=f)
    print(f'Config template successfully written to {configpath}.')
    print('Make sure the variables are making sense before proceeding (see the README for more help)!')
