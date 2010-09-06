# -*- Mode: python; tab-width: 2; indent-tabs-mode: nil; encoding: utf-8 -*-

"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

# python setup ...
#              install
#              sdist
#              bdist_egg

from setuptools import setup

import bugz

setup( name = 'bugz',
      version = bugz.__version__,
      license = 'Mozilla Public License (MPL) 1.1',
      description = 'A python bug tracking tool for the command line and DVCS',
      author = 'J. Knight',
      author_email = 'emptyvee@gmail.com',
      url = 'http://j2mfk.com/projects/bugz/',
      packages = ['bugz'],
      scripts = ['bgz'],
      long_description = """A simple command line bug tracker that lives in
      the project root and gets versioned along with the source.
      """,
      # cheeseshop stuff
      # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Mozilla Public Licence 1.1 (MPL 1.1)',
            'Operating System :: OS Independant',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Utilities'
            ]
      )