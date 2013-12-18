#!/usr/bin/env python

from distutils.core import setup

DESCRIPTION = 'Small mocking/unit-testing improvements on top of mock library'
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

setup(name='mockstar',
      version='1.1.0',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='Konstantine Rybnikov',
      author_email='k-bx@k-bx.com',
      url='https://bitbucket.org/k_bx/mockstar',
      py_modules=['mockstar'],
      requires=['mock (>=0.8.0)'])
