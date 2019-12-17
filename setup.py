from setuptools import setup, find_packages
from os.path import join as opj

packages = ['janki']#['scm.gpp'] + ['scm.gpp.'+i for i in find_packages('.')]

description = """
Janki allows to quickly search Jisho.org for vocabulary
and add relevant results to an existing Anki collection.
The aim of this package is to reduce user input to a minimum.
"""

setup(
    name             = 'janki',
    version          = '0.1',
    author           = 'Leo Komissarov',
    author_email     = 'koimssarov@scm.com',
    url              = '',
    download_url     = '',
    license          = 'LGPLv3',
    description      = 'Quickly add Jsho.org search results to your Anki Collection',
    long_description = description,
    classifiers      = [
            # 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
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
    install_requires = ['urllib', 'json'],
    packages         = packages,
    package_dir      = {'janki': '.'},
    scripts          = [opj('janki', 'scripts', 'janki.py')]
)
