Genemap
================

.. image:: https://travis-ci.org/jrderuiter/genemap.svg?branch=master
    :target: https://travis-ci.org/jrderuiter/genemap

.. image:: https://coveralls.io/repos/github/jrderuiter/genemap/badge.svg?branch=master
    :target: https://coveralls.io/github/jrderuiter/genemap?branch=master

Genemap is a simple python library for mapping gene identifiers between
different identifier types and different species. This mapping is currently
performed using Ensembl, though different mappers may be added in the
future.

Documentation
----------------

Detailed documentation will soon be available on ReadTheDocs.

Examples
----------------

Translating human gene symbols to ensembl ids:

.. code::

    from genemap import map_ids

    map_ids(['FGFR2', 'MYH9'], from_type='symbol', to_type='ensembl')

Translating human gene symbols to mouse gene symbols:

.. code::

    map_ids(['FGFR2', 'MYH9'], from_type='symbol', to_type='ensembl',
            from_org='hsapiens', to_org='mmusculus')


Mapping an indexed pandas DataFrame:

.. code::

  from genemap import map_frame

  map_frame(df, from_type='symbol', to_type='ensembl',
            from_org='hsapiens', to_org='mmusculus')


Installation
----------------

The source code is currently hosted on GitHub at: `https://github.com/jrderuiter/genemap  <https://github.com/jrderuiter/genemap>`_.

The package can be installed via pip:

.. code::

    pip install git+git://github.com/jrderuiter/genemap.git#egg=genemap

It will also soon be available in pypi.

Dependencies
----------------
- Python 2.7, 3.3+
- future
- pandas
- `pybiomart <https://github.com/jrderuiter/pybiomart>`_

License
----------------

Released under the MIT license.
