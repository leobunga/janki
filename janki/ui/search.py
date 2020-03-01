import os,sys
from os.path import join as opj, abspath
from  .userinput    import dinput
from ..common.clear import clear
from ..core.jisho   import *
from ..core.deck    import DECK


def search():
    def cp(req,id):
        clear()
        print(f'Search result {id+1:02d}/10')
        jprint(req[id])
        print('Actions: (a)dd, (n)ext, (p)revious, new (s)earch, (q)uit')
        return dinput('Enter action', choices=['a','n','p', 's'])

    req = dinput('Enter search string (q to quit)')
    if not req:
        clear()
        sys.exit()
    ret = jsearch(req)
    if not ret:
        clear()
        print(f'No search results for: {req}')
        search()
    id  = 0
    action = cp(ret, id)
    while action == 'n' or action == 'p': # Next / Previous
        if action == 'n':
            id += 1 if id < 9 else 0
            action = cp(ret, id)
        else:
            id -= 1 if id != 0 else 0
            action = cp(ret, id)
    if action == 's':
        clear()
        search()
    elif action == 'a':
        DECK.add(ret[id])
        clear()
        print('Added')
        search()
    elif action == None:
        clear()
