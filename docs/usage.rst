.. _usage:

=====
Usage
=====

Mapper interface
----------------

The main interface of genemap is provided by the different ``Mapper`` classes,
which provide the functionality for mapping different identifier types using
specific data sources. Each mapper provides the following three methods:

    - ``map_ids`` - Maps a given list of identifiers to another identifier type.
    - ``map_dataframe`` - Maps the index of the passed dataframe to
      another identifier type. This method can, for example, be used to
      translate gene identifiers in matrix containing expression values
      to other identifier types.
    - ``fetch_mapping`` - Returns the used mapping (as a DataFrame with
      two columns).

The actual mapping that is performed depends on the underlying mapper and the
arguments with which it was created. For example, basic usage of the Ensembl
mapper for mapping a list of gene symbols to Ensembl IDs is as follows:

.. code:: python

    from genemap.mappers import EnsemblMapper

    mapper = EnsemblMapper(from_type='symbol', to_type='ensembl')
    mapper.map_ids(['TP53', 'BRCA1', 'PPP1R12A'])

Here, ``from_type`` specifies the type of identifier that is used in the input
and ``to_type`` specifies the output identifier type. Similarly, the same
mapper can be used to translate gene symbols between different species:

.. code:: python

    from genemap.mappers import EnsemblMapper

    mapper = EnsemblMapper(from_type='symbol', to_type='ensembl',
                           from_organism='hsapiens', to_organism='mmusculus')
    mapper.map_ids(['TP53', 'BRCA1', 'PPP1R12A'])

For an overview of the different ``Mapper`` classes and the arguments supported
by each mapper, see the Mapper API reference or the docstring of
the corresponding Mapper class.

Functional interface
--------------------

For convenience, genemap also provides a functional interface to access the
different mappers. This interface consists of three functions, ``map_ids``
``map_dataframe`` and ``fetch_mapping``, which essentially perform the same
function as the corresponding methods on the ``Mapper`` class. The functions
take an additional ``mapper`` argument that indicates which mapper should be
used. Other extra arguments are passed to the corresponding mapper class.

As an example, we can use the Ensembl mapper to translate gene symbols to
Ensembl IDs using the functional interface as follows:

.. code:: python

    from genemap import map_ids

    mapper.map_ids(['TP53', 'BRCA1', 'PPP1R12A'], mapper='ensembl',
                   from_type='symbol', to_type='ensembl')

Similarly, we can also translate symbols between species using:


.. code:: python

    from genemap import map_ids

    mapper.map_ids(['TP53', 'BRCA1', 'PPP1R12A'], mapper='ensembl',
                   from_type='symbol', to_type='ensembl',
                   from_organism='hsapiens', to_organism='mmusculus')
