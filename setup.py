# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages


__version__ = ''
exec(open('bitsio/_version.py').read())


requirements = open('requirements.txt').readlines()
requirements = [r.strip() for r in requirements]


setup(
    name='bitsio',
    version=__version__,
    description='The BitsIO is a bit stream I/O class.',
    author='Minoru Hiki',
    author_email='minoruhiki@gmail.com',
    url='https://github.com/m-hiki/bitsio',
    keywords=["bitstream", "io"],
    license='MIT License',
    install_requires=requirements,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    long_description=open('README.rst').read()
)
