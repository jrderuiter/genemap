=====
Usage
=====

General interface
-----------------

Mapping identifiers
~~~~~~~~~~~~~~~~~~~

Genemap has three main functions for mapping (gene) identifiers: ``map_ids``,
``map_dataframe`` and ``fetch_map``. The ``map_ids`` function is the simplest
of the three and is used to map a list of identifiers to a different
type of identifier. A basic call to ``map_ids`` is as follows:

.. code:: python

    genemap.map_ids(['TP53', 'BRCA1', 'PPP1R12A'], mapper='ensembl',
                    from_type='symbol', to_type='ensembl')

Here, the ``mapper`` parameter specifies which mapper should be used
for mapping the identifiers, ``from_type`` specifies the type of identifier
that is used in the input and ``to_type`` specifies the output identifier type.
In this example, the given parameters specify that the input identifiers are
gene symbols that should be translated to Ensembl identifiers using the
Ensembl mapper.

Any extra keyword arguments are passed to the specified mapper. For an
overview of the available mappers, see :ref:`usage-mapper-classes`.

Mapping dataframes
~~~~~~~~~~~~~~~~~~

The ``map_dataframe`` function maps gene identifiers in the index of a
DataFrame in the same fashion as the ``map_ids`` function. The function can
be used to, for example, translate gene identifiers in matrix containing
expression values to other identifier types. The call to ``map_dataframe``
is very similar to ``map_ids``:

.. code:: python

    genemap.map_dataframe(df, mapper='ensembl', from_type='symbol',
                          to_type='ensembl')

This returns a new DataFrame, in which the index values are translated to
new identifiers.

Fetching mappings
~~~~~~~~~~~~~~~~~

The ``fetch_mapping`` function can be used to retrieve the mapping that is used
by a specific mapper to translate gene identifiers. This can be useful in cases
where we are interested in the mapping itself, or if we want to perform some
custom pre-processing before mapping identifiers. The basic call to
``fetch_mapping`` is as follows:

.. code:: python

    genemap.fetch_mapping(mapper='ensembl', from_type='symbol',
                          to_type='ensembl')

This returns a pandas DataFrame with two columns. The first column of this
DataFrame contains the source identifiers (which we are translating from),
the second contains the target identifiers (which we are translating to).

.. _usage-mapper-classes:

Mapper classes
--------------

The actual mappings are performed by ``Mapper`` classes, which provide
functionality for mapping different types of identifiers using specific data
sources. The types of mappings that are supported by each mapper depends
strongly on the underlying data source. For example, the Ensembl mapper uses
Ensembl data (via Biomart) to translate various types of identifiers even
between different organisms. However, other mappers may be much more specific
and limited in their scope.

Currently, the following mapper classes are provided:

    - **EnsemblMapper (ensembl)** - Translates identifiers using Ensembl
      via Biomart. Supports mapping between various types of gene identifiers
      (gene symbols, Ensembl/Entrez identifiers, e.g.) and between species
      (using orthologous genes).

Mapper classes can be used directly by instantiating the class and calling its
``map_ids``, ``map_dataframe`` and ``fetch_mapping`` methods, which are
analogous to the functions described above. For example, we can construct
an ``EnsemblMapper`` instance and use it to translate ids in the following
manner:

.. code:: python

    from genemap.mappers import EnsemblMapper

    mapper = EnsemblMapper(from_type='symbol', to_type='ensembl')
    mapper.map_ids(['TP53', 'BRCA1', 'PPP1R12A'])

This is equivalent to the following call to ``map_ids``:

.. code:: python

    genemap.map_ids(['TP53', 'BRCA1', 'PPP1R12A'], mapper='ensembl',
                    from_type='symbol', to_type='ensembl')

Mapper classes typically take several additional arguments, which allow more
complex mappings to be performed. For example, we can translate gene symbols
between species using the ``EnsemblMapper`` using its ``from_organism``
and ``to_organism`` parameters:

.. code:: python

    from genemap.mappers import EnsemblMapper

    mapper = EnsemblMapper(from_type='symbol', to_type='ensembl',
                           from_organism='hsapiens', to_organism='mmusculus')
    mapper.map_ids(['TP53', 'BRCA1', 'PPP1R12A'])

This gives the same results as calling ``map_ids`` with these extra parameters:

.. code:: python

    genemap.map_ids(['TP53', 'BRCA1', 'PPP1R12A'], mapper='ensembl',
                    from_type='symbol', to_type='ensembl',
                    from_organism='hsapiens', to_organism='mmusculus')

For an overview of the arguments supported by each mapper, see the Mapper API
reference or the docstring of the corresponding Mapper class.