Genemap
=======

Genemap is a python library for mapping (gene) identifiers. Genemaps main
purpose is provide an easy approach for mapping (gene) identifers
from one identifier type to another, which is unfortunately often not a trivial
task. This may be useful for translating identifiers into a format that you
are more familiar with (such as gene symbols instead of Ensembl IDs) or
even for translating between different species (e.g., from mouse IDs to human
IDs) to compare datasets or annotations between species.

Genemap currently supports the following mappings:

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


For a complete overview of the provided mappers and their basic usage, see the
the :ref:`overview` and :ref:`usage` sections. More details on the API are
available in the :ref:`api` section. Finally, for an overview of genemaps
command line usage, see the :ref:`command-line` section.

.. toctree::
   :maxdepth: 2
   :hidden:

   self
   installation
   overview
   usage
   command_line
   api
   contributing
   authors
   history
