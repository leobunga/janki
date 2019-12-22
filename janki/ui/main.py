import os
from os.path import join as opj, abspath
from  .userinput   import dinput
from ..common.vars import DIR, clear
from ..core.jisho  import *


def cp(req,id):
    clear()
    print(f'Search result {id+1:02d}/10')
    jprint(req[id])
    print('Actions: (a)dd, (n)ext, (p)revious, (q)uit')
    return dinput('Enter action', choices=['a','n','p'])

def main():
    req = dinput('Enter search string')
    ret = jsearch(req)
    if not ret:
        print(f'No search results for: {req}')
        return
    id  = 0
    action = cp(ret, id)
    while action == 'n' or action == 'p': # Next / Previous
        if action == 'n':
            id += 1 if id < 9 else 0
            action = cp(ret, id)
        else:
            id -= 1 if id != 0 else 0
            action = cp(ret, id)
    if action == 'a':
        print('Add')
    elif action == None:
        print('Quit')
