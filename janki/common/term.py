import os,sys
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
