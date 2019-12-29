import sys
from typing import *
from  .config            import readconfig
from ..common.exceptions import *

cfg = readconfig()
import anki


__all__ = ['Deck', 'get_deck_names']


def copen(col=None):
    if col:
        if col.open:
            return
        else:
            col.open = True
            col.reopen()
    else:
        ret = anki.Collection(cfg['COLPATH'])
        ret.open = True
        return ret

def cclose(col):
    if col.open:
        col.close()
        col.open = False

def get_deck_names(ids=False):
    ret = (COL.decks.allNames(), COL.decks.allIds()) if ids else COL.decks.allNames()
    return ret

COL  = copen()

class Deck:
    def __init__(self,deck_name_or_id:Union[str, int]=None):
        copen(COL)
        self.decks  = COL.decks
        self.change_deck(deck_name_or_id)

    def fields(self) -> List:
        ''' Return the fields associated with this deck's model '''
        copen(COL)
        ret = [(i['ord'],i['name']) for i in self._model()['flds']]
        return [i[1] for i in sorted(ret)]

    def change_deck(self, name_or_id=None):
        copen(COL)
        names, ids  = get_deck_names(True)
        if not name_or_id:
            name_or_id = names[0]
            print(f'No deck specified, will select "{names[0]}".')
            print( 'Use `get_deck_names()` to list all available. Use `change_deck()` to change the selection')

        self.id = name_or_id if str(name_or_id) in ids else self.decks.id(name_or_id)
        self._strid = str(self.id)
        self.decks.select(self.id)
        self.name   = COL.decks.decks[self._strid]['name']
        self._model = COL.models.current

    def add_note(self, *fargs, tags:Sequence=None):
        copen(COL)
        f = self.fields()
        if len(fargs) != len(f):
            strf = ', '.join(f'"{i}"' for i in f)
            raise NoteError(f'The number of passed arguments must be the same as the number of fields: {len(f)}, where each argument is the value of the respective field -- {strf}.')
        note = COL.newNote()
        note.fields = [str(i) for i in fargs]
        if tags:
            note.tags += [str(i) for i in tags]
        note.model()['did'] = self.id
        COL.addNote(note)
        cclose(COL)

    @staticmethod
    def close():
        cclose(COL)

    @property
    def config(self):
        copen(COL)
        return self.decks.confForDid(self._strid)

    @config.setter
    def config(self, value):
        copen(COL)
        conf = self.config
        conf.update(value)
        self.decks.setConf(conf, self._strid)
        COL.save()
# %%
# Testing
# deck = Deck('Yomichan')
# deck.fields()
# deck.add_note('three', 'is', 'note', 'nr', 'one', 'for', 'japanese')
#
#
# n.fields = [str(i) for i in range(7)]
# deck._col.findTemplates(n)
# deck._col.addNote(n)
# deck._col._newCard(n, deck.model()['tmpls'][0], 1)
# deck._col.save()
#
# deck._col.close()
