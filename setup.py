#!/usr/bin/env python

# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

import setuptools

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# General requirements.
requirements = ['future', 'pandas', 'pybiomart', 'requests_cache']
extra_requirements = {}

setuptools.setup(
    name='genemap',
    version='0.2.0',
    description=('Python library for mapping gene identifiers between '
                 'different identifier types and different species.'),
    long_description=readme + '\n\n' + history,
    url='https://github.com/jrderuiter/genemap',
    author='Julian de Ruiter',
    author_email='julianderuiter@gmail.com',
    license='MIT license',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={'console_scripts': ['genemap = genemap.main:main']},
    install_requires=requirements,
    extras_require=extra_requirements,
    zip_safe=False,
    classifiers=[])
