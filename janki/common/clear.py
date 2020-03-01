import os,sys
def clear():
    os.system('clear') if 'linux' in sys.platform or 'darwin' in sys.platform else os.system('cls')
