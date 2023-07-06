#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

import os
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


is_py3 = sys.version_info >= (3,)

if len(sys.argv) <= 1:
    print("""
Suggested setup.py parameters:

    * build
    * install
    * sdist  --formats=zip
    * sdist  # NOTE requires tar/gzip commands

    python -m pip install -e .
""")

readme_filename = 'README.md'
if os.path.exists(readme_filename):
    f = open(readme_filename)
    long_description = f.read()
    f.close()
else:
    long_description = None


setup(
    name='pyhexedit_vim',
    version=__version__,
    author='clach04',
    url='https://github.com/clach04/pyhexedit_vim',
    description='Demo filter for use with vim. Work-In-Progress (WIP)!',  # FIXME
    long_description=long_description,
    packages=find_packages(where=os.path.dirname(__file__), include=['*']),
    #py_modules=[''], # TODO scripts
    entry_points={
        'console_scripts': [
            'dumb_hex_filter = dumb_hex_filter:main',
        ],
    },
    #data_files=[('.', [readme_filename])],  # does not work :-( Also tried setup.cfg [metadata]\ndescription-file = README.md # Maybe try include_package_data = True and a MANIFEST.in?
    classifiers=[  # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Filters',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',  # Python 3.6.9
        'Programming Language :: Python :: 3.10',
        # FIXME TODO more
        ],
    platforms='any',  # or distutils.util.get_platform()
)
