import os,sys
from os.path import join as opj, dirname as opd, abspath

DIR = abspath(opj(opd(__file__), os.pardir, os.pardir))

def clear():
    os.system('clear') if 'linux' in sys.platform or 'darwin' in sys.platform else os.system('cls')
