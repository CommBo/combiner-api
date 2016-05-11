#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Based on https://github.com/pypa/sampleproject/blob/master/setup.py."""
from __future__ import unicode_literals
# To use a consistent encoding
from codecs import open
import os
import sys

from pip.req import parse_requirements
kwargs = {}
try:
    # pip's parse_requirements added a required 'session=' argument after version 6.0+.
    #
    # Given that the pip installed on our Jenkins is older, we can't just use the newer
    # config. So I'm catching the import error and defaulting to None if it's older pip.
    from pip.download import PipSession
    kwargs['session'] = PipSession()
except ImportError:
    pass

from setuptools import setup, find_packages
from setuptools.command.install import install
from distutils.command.build import build

install_requirements = [str(requirement.req) for requirement in
                        parse_requirements('./requirements.txt', **kwargs)]

# Get the long description from the relevant file
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='combiner-api',
    version='1.0-dev',
    description='''API for multiple data sources''',
    long_description=long_description,
    author='',
    author_email='kevin1chun@gmail.com',
    license='Proprietary',
    # The project's main homepage
    url='https://github.com/CommBo/combiner-api',
    packages=find_packages(exclude=('tests*', 'docs', 'examples')),
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    include_package_data=True,
    zip_safe=False,

    install_requires=install_requirements,
    tests_require=test_requirements,

    entry_points = {
        'console_scripts' : [
            'combiner-api=combiner-api.__main__:main'
        ]
    }
)
