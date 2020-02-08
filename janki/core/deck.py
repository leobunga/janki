import sys
from typing import *
from  .config            import readconfig
from ..common.exceptions import *

cfg = readconfig()
import anki

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
            print(fargs)
            raise NoteError(f'The number of passed arguments must be the same as the number of fields: {len(f)}, where each argument is the value of the respective field.\nThis deck\'s fields are: {strf}.')
        note = COL.newNote()
        note.fields = [str(i) for i in fargs]
        if tags:
            note.tags += [str(i) for i in tags]
        note.model()['did'] = self.id
        COL.addNote(note)
        cclose(COL)

    def add(self, d:Dict):
        #  add( jsearch()[i] )

        def flat_d(d:Dict):
            # 'Flatten' the dictionary
            ret = {k:d[k] for k in ['Kanji', 'Reading', 'Tags']}
            ret['Translation']     = []
            ret['Info']            = []
            for i in d['Meaning']:
                for k in ['Translation', 'Tags', 'Info']:
                    if k == 'Translation' and 'Add parts of speech' in cfg['MISC'] and cfg['MISC']['Add parts of speech'] and i["parts_of_speech"]:
                        ret[k] += [f'{j} ({" ".join(i["parts_of_speech"])})' for j in i[k]]
                    else:
                        ret[k] += i[k]

            enum = True  if 'Eumerate entries' not in cfg['MISC'] else cfg['MISC']['Enumerate entries']
            if enum:
                for k in ['Kanji', 'Reading', 'Translation', 'Info']:
                    if len(ret[k]) > 1:
                        ret[k] = [f'{num}. {i}' for num,i in enumerate(ret[k], 1)]
            return ret

        a2j = cfg['FIELDS'] # Mapping anki fields to janki fields
        d    = flat_d(d)
        sep  = '<br>' if 'Entry separator'  not in cfg['MISC'] else cfg['MISC']['Entry separator']
        tags = False  if 'Add tags'         not in cfg['MISC'] else cfg['MISC']['Add tags']

        field_args = [] # List of properly ordered field values for `add_note()`
        for f in self.fields():
            if f in a2j:
                k   = a2j[f]
                try:    ret = d[k]
                except: raise NoteError(f"Janki does not understand the field '{k}'. Check your FIELDS variable in the config file")
                field_args.append(f"{sep}".join(ret))
            else:
                field_args.append('')
        self.add_note(*field_args, tags=d['Tags'] if tags else None)

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


COL  = copen()
DECK = Deck(cfg['DECK'])
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
