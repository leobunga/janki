from setuptools import setup, find_packages
from os import sep
from os.path import join as opj
from janki import __version__

packages = ['janki']+['janki.'+i for i in find_packages('janki')]

description = """
Janki allows to quickly search Jisho.org for vocabulary
and add relevant results to an existing Anki collection.
The aim of this package is to reduce user input to a minimum.
"""

setup(
    name             = 'janki',
    version          = __version__,
    author           = 'Leo Komissarov',
    author_email     = 'koimssarov@scm.com',
    url              = 'https://github.com/leobunga/janki',
    download_url     = 'https://github.com/leobunga/janki/archive/master.zip',
    license          = 'GPLv3+',
    description      = 'Quickly add Jsho.org search results to your Anki Collection',
    long_description = description,
    classifiers      = [
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Education',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 3.6',
            'Topic :: Database',
            'Topic :: Educaion',
            'Topic :: Text Processing :: Linguistic',
            'Natural Language :: Japanese',
    ],
    keywords         = ['jisho', 'anki', 'jisho.org', 'japanese', 'flashcards', 'vocabulary', 'foreign language'],
    python_requires  = '>=3.5',
    tests_require    = ['pytest'],
    packages         = packages,
    package_dir      = {'janki' : 'janki'},
    package_data     = {'janki' : ['tests/*','tests/*/*']},
    scripts          = [opj('scripts', 'janki')],
)
