
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
      author_email = 'jim@j2mfk.com',
      url = 'http://j2mfk.com/projects/bugz/',
      packages = ['bugz'],
      scripts = ['scripts/hatch'],
      )