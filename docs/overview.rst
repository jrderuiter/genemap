.. _overview:

========
Overview
========

Genemaps main purpose is provide an easy approach for mapping (gene) identifers
from one identifier type to another, which is unfortunately often not a trivial
task. This may be useful for translating identifiers into a format that you
are more familiar with (such as gene symbols instead of Ensembl IDs) or
even for translating between different species (e.g., from mouse IDs to human
IDs) to compare datasets or annotations between species.

Basic mappers
-------------

Mappings in genemap are implemented by ``Mapper`` classes, which interface with
external data sources to perform different types of mappings. Currently, the
following main mappers are supported:

    - **EnsemblMapper** - Translates identifiers using Ensembl
      via Biomart. Supports mapping between various types of gene identifiers
      that are present in Ensembl (gene symbols, Ensembl/Entrez identifiers,
      e.g.) and between different species (using orthologous genes).
    - **MgiMapper** - Translates identifers using the homology table
      provided by MGI. Supports mapping between gene symbols and Entrez
      identifers and between several specifies (using orthologous genes).
    - **CustomMapper** - Translates identifiers using a custom mapping
      provided by the user. The nature of the performed mapping depends on the
      provided mapping table.

Each of these Mappers can be used by instantiating the corresponding ``Mapper``
class and calling the mapping methods on the ``Mapper`` object (``map_ids``,
``map_dataframe`` and ``fetch_mapping``). Alternatively, each mapper can be
accessed using the functional interface of genemap (see :ref:`usage` for more
details).

Compound mappers
----------------

Besides the basic ``Mapper`` classes, genemap provides two additional classes
that enable the creation of *compound* mappers (combinations of basic mappers):

    - **ChainedMapper** - Chains a series of mappers into a single mapping.
      For example, if two mappers are provided that map from identifier types
      a --> b and b --> c respectfully, these mappers are combined into a
      single mapper that maps from a --> c.
    - **CombinedMapper** - Combines the results of multiple mappers into a
      single mapper. This can be used to combine the mappings of two mappers
      with incomplete mappings (e.g., missing genes) into a single mapping
      combining the results of both mappers.

The compound mappers are also available in the functional interface, but
can currently not be used directly from the command line.
