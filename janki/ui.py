import os,sys
import readline
from os.path import join as opj, abspath
from .jisho  import *
from . import __path__ as __jpath, __version__

def clear():
    os.system('clear') if 'linux' in sys.platform or 'darwin' in sys.platform else os.system('cls')


class C:
    # Colour a string that will be printed to term
    # https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    END       = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    @staticmethod
    def str(string, *colors):
        for c in colors:
            assert hasattr(C, c), f"No such color: {c}"
        return f"{''.join(getattr(C,c) for c in colors)}{string}{C.END}"


def dinput(string, default=None, choices=None, quitbutton='q'):
    """
    Get user input with possible default values and choices (POSIX only?)

    Will preprint the `default` string, if provided.
    Will print the `choices` in brackets after the `string`, if provided.
    Will additionally check, if input matches the `choices` or is empty, and prompt
    until a valid value is provided or the `quitbutton` is pressed.
    """

    if choices:
        choices = [choices] if not isinstance(choices, (list,tuple)) else choices
        if default and (default not in choices):
            raise ValueError(f'Default {default} not in choices.')
        if len(choices) == 1:
            default = choices[0]
            choices = None
    msg = string
    if choices:
        msg += f' ({"/".join(str(i) for i in choices)})'
    msg += ': '

    readline.set_startup_hook(lambda: readline.insert_text(default)) # https://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible
    ret = input(msg)
    readline.set_startup_hook()

    if ret == quitbutton:
        return None
    if ret=='' or (choices and ret not in choices):
        print(f'Enter a valid value or press ({quitbutton}) to quit.')
        ret = dinput(string, default, choices, quitbutton)
    return ret


def header():
    clear()
    s = f'Janki v{__version__}'
    print(f"{len(s)*'*'}")
    print(C.str(s, 'BOLD'))
    print(f"{len(s)*'*'}")
    print(f"Install path: {__jpath[0]}\n")

def search(config):
    def cp(req,id):
        # clear and print
        # clear()
        print(f'Search result {id+1:02d}/10')
        jprint(req[id])
        print('Actions: (a)dd, (n)ext, (p)revious, new (s)earch, (q)uit')
        return dinput('Enter action', choices=['a','n','p','s'])

    header()
    req = dinput('Enter search string (q to quit)')
    if not req:
        clear()
        sys.exit()
    ret = jsearch(req)
    if not ret:
        header()
        print(f'No search results for: {req}')
        search(config)
    id  = 0
    action = cp(ret, id)
    while action == 'n' or action == 'p': # Next / Previous
        header()
        if action == 'n':
            id += 1 if id < 9 else 0
            action = cp(ret, id)
        else:
            id -= 1 if id != 0 else 0
            action = cp(ret, id)
    if action == 's':
        clear()
        header()
        search(config)
    elif action == 'a':
        print(ret[id])
        search(config)
    elif action == None:
        clear()
