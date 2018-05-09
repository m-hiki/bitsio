# -*- coding: utf-8 -*-
"""
isobmff
version: 0.1
"""

import sys
from setuptools import setup, find_packages

VERSION = '0.1'
REQUIRES = []

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='bitsio',
    version=VERSION,
    description='The BitsIO is a python library for '
                'reading/writing bitstream.',
    author='Minoru Hiki'
    author_email='minoruhiki@gmail.com',
    url='https://github.com/m-hiki/bitsio',
    keywords=["bitstream", "io"],
    license=license,
    install_requires=REQUIRES,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    long_description=readme
)
