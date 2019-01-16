#!/usr/bin/env python

"""Setup script for the package."""

import os
import sys

import setuptools
from distutils.extension import Extension

PACKAGE_NAME = 'core'
MINIMUM_PYTHON_VERSION = '3.7'


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {0}+ is required.".format(MINIMUM_PYTHON_VERSION))


def read_package_variable(key, filename='__init__.py'):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, filename)
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ', 2)
            if parts[:-1] == [key, '=']:
                return parts[-1].strip("'")
    sys.exit("'{0}' not found in '{1}'".format(key, module_path))


def get_package_data():
    return {'tlsat': ['*.yaml',
                      '*.md',
                      '*.txt',
                      '*.so']}


def build_description():
    """Build a description for the project from documentation files."""
    return open('README.md').read()


check_python_version()

setuptools.setup(
    name=read_package_variable('__project__'),
    version=read_package_variable('__version__'),

    description="The monorepo, the one and only you\'ll ever need to know.",
    long_description=build_description(),
    url='',
    author='Josh Marcus',
    author_email='jdm@integrichain.com',

    entry_points={'console_scripts': [
        'corecli = core.cli:cli',
    ]},

    packages=setuptools.find_packages(),

    license='proprietary and confidential',
    classifiers=[
        # TODO: update this list to match your application: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    install_requires=[
        # TODO: Add your library's requirements here
        # "testpackage ~= 2.26",
    ],
)
