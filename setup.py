#!/usr/bin/python
from distutils.core import setup

setup(name='loco',
      version='0.1',
      description='Edit remote files locally',
      author='Ian Preston',
      author_email='ian@ian-preston.com',
      scripts=['loco', 'locod', 'locossh'],
     )