from .term import C

class JankiError(Exception):
    def __str__(self):
        r = super().__str__()
        return C.str(r, 'FAIL', 'BOLD')

class DeckError(JankiError):
    pass

class NoteError(JankiError):
    pass

class ConfigError(JankiError):
    pass
