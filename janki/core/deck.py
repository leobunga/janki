# %%
import sys
from typing import *
from ..common.exceptions import *
from .config import readconfig

cfg = readconfig()
if cfg['ANKIPATH'] not in sys.path:
    sys.path.append(cfg['ANKIPATH'])
import anki


__all__ = ['Deck']


class Deck:
    def __init__(self,collectionpath:str, deck_name_or_id:Union[str, int]=None):
        self._col   = anki.Collection(collectionpath)
        self.decks  = self._col.decks
        self.change_deck(deck_name_or_id)

    def get_deck_names(self, ids=False):
        if ids: return (self.decks.allNames(), self.decks.allIds())
        else:   return  self.decks.allNames()

    def fields(self) -> List:
        ''' Return the fields associated with this deck's model '''
        ret = [(i['ord'],i['name']) for i in deck._model()['flds']]
        return [i[1] for i in sorted(ret)]

    def change_deck(self, name_or_id=None):
        names, ids  = self.get_deck_names(True)
        if not name_or_id:
            name_or_id = names[0]
            print(f'No deck specified, will select "{names[0]}".')
            print( 'Use `get_deck_names()` to list all available. Use `change_deck()` to change the selection')

        self.id = name_or_id if str(name_or_id) in ids else self.decks.id(name_or_id)
        self._strid = str(self.id)
        self.decks.select(self.id)
        self.name   = self._col.decks.decks[self._strid]['name']
        self._model  = self._col.models.current

    def add_note(self, *fargs, tags:Sequence=None):
        f = self.fields()
        if len(fargs) != len(f):
            strf = ', '.join(f'"{i}"' for i in f)
            raise NoteError(f'The number of passed arguments must be the same as the number of fields: {len(f)}, where each argument is the value of the respective field -- {strf}.')
        note = deck._col.newNote()
        note.fields = [str(i) for i in fargs]
        if tags:
            note.tags += [str(i) for i in tags]
        note.model()['did'] = self.id
        self._col.addNote(note)


    @property
    def config(self):
        return self.decks.confForDid(self._strid)

    @config.setter
    def config(self, value):
        conf = self.config
        conf.update(value)
        self.decks.setConf(conf, self._strid)
        self.col.save()

    def close(self):
        self._col.close()


# %%
# Testing
# deck = Deck('../data/collection.anki2','Yomichan')
# deck.fields()
# deck.add_note('this', 'is', 'note', 'nr', 'one', 'for', 'japanese')
# deck.change_deck(1)
#
#
# n.fields = [str(i) for i in range(7)]
# deck._col.findTemplates(n)
# deck._col.addNote(n)
# deck._col._newCard(n, deck.model()['tmpls'][0], 1)
# deck._col.save()
#
# deck._col.close()
