# Janki

Search [Jisho.org](https://jisho.org/) for vocabulary and add it to your [Anki](https://apps.ankiweb.net) collection with the press of a button (maybe two presses).

Janki allows to quickly search Jisho.org for vocabulary and add relevant results to an existing Anki collection.
The aim of this package is to reduce user input to a minimum: After linking the Jisho search result fields to the fields of your Anki Model, all there's left to do is search for a word, and hit a single button to add it.



## Installation
Assuming the package will be installed into `JANKIDIR`, alternatively replace it with a path of your choice.

1. `git clone git@github.com:leobunga/janki.git JANKIDIR`
2. `pip install -e JANKIDIR`
3. `janki` to create a config file, or `janki -c CONFIGPATH` if you do not want to store your config in the default location
4. [Configure](#configuration)
5. *Optional*: To run the unit tests: `pytest` TODO


## Configuration
A newly created *config* file will look similar to this:

```python
# v0.1

## Path to your top level anki folder (https://github.com/dae/anki):
# Try `find / -name anki 2> /dev/null` if you do not know your anki path
# Note: An `anki` directory should be present at `ANKIPATH/anki`
ANKIPATH = '/path/to/anki'

## Path to the .anki2 collection you would like to edit
COLPATH  = '/path/to/collection.anki2'

## Name or ID of the Anki deck you would like to edit
DECK = 'MyDeckName'

## Mapping of the four Janki search result fields to the fields in your Anki DECK.
# Replace each 'ANKIFIELD' with the actual field name.
# If you dont know your DECKS field names, run `janki setup`: If all the paths above
# are properly defined, the script will give a hint about the names you can use.
# Note: Unassigned fields will be left blank.
FIELDS = {
'ANKIFIELD' : 'Kanji'      ,
'ANKIFIELD' : 'Reading'    ,
'ANKIFIELD' : 'Translation',
'ANKIFIELD' : 'Info'       ,
}

## Miscellaneous settings
MISC = {
'Add parts of speech' : True,
'Add tags'            : True,
'Enumerate entries'   : True,
'Entry separator'     : '<br>',
}
```

To properly communicate with your Anki collection, Janki requires all of the above variables (except for *MISC*) to have a valid value specified.
The comments above every variable provide further help.
If everything is configured correctly, you can type `janki` in your prompt and should see an output similar to this:

```yaml
****************
Welcome to Janki
****************

Version:         0.1
Install path:    JANKIDIR
Config path:     JANKIDIR/config
Collection path: /path/to/collection.anki2
Selected deck:   MyDeckName

Actions: (s)earch, (q)uit
What to do? (s/q): s
```

If instead of the above output an error message is printed, it is likely that
at least one variable is not properly defined and you need to check the config file again.
Read the error messages for more info - they are designed to provide additional hints on what has gone wrong.
