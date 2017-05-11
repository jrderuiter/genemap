#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()

# General requirements.
REQUIREMENTS = [
    'future', 'numpy', 'pandas>=0.18.0', 'pybiomart>0.1', 'requests_cache'
]

EXTRAS_REQUIRE = {
    'dev': [
        'sphinx', 'sphinx-autobuild', 'sphinx-rtd-theme', 'bumpversion',
        'pytest>=2.7', 'pytest-mock', 'pytest-helpers-namespace', 'pytest-cov',
        'python-coveralls'
    ]
}

setuptools.setup(
    name='genemap',
    version='0.2.0',
    description=('Python library for mapping gene identifiers between '
                 'different identifier types and different species.'),
    long_description=README + '\n\n' + HISTORY,
    url='https://github.com/jrderuiter/genemap',
    author='Julian de Ruiter',
    author_email='julianderuiter@gmail.com',
    license='MIT license',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={'console_scripts': ['genemap = genemap.main:main']},
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
    zip_safe=False,
    classifiers=[])
