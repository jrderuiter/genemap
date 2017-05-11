.. _command-line:

============
Command line
============

Genemaps main functions (``map_ids``, ``map_dataframe`` and
``fetch_mapping``) are also accessible via the command line. Each of these
functions is implemented in its own subcommand. Examples are shown below.

Mapping ids
-----------

A list of gene ids can be mapped from the command line as follows:

.. code:: bash

    genemap map_ids ensembl \
        --from_type symbol --to_type ensembl \
        --host http://aug2014.archive.ensembl.org \
        TP53 BRCA1 PPP1R12A

This commands prints the translated identifiers to the console.

Mapping dataframes
------------------

DataFrames (in tab-separated format) can be mapped using the following command:

.. code:: bash

    genemap map_datataframe ensembl \
        --from_type symbol --to_type ensembl \
        --host http://aug2014.archive.ensembl.org \
        input.txt mapped.txt

In this example, the translated DataFrame is written to ``mapped.txt``.

Fetching maps
-------------

Mappings can also be extracted using the ``fetch_mapping`` subcommand:

.. code:: bash

    genemap fetch_mapping ensembl \
        --from_type symbol --to_type ensembl \
        --host http://aug2014.archive.ensembl.org \
        mapping.txt

This writes the mapping (a DataFrame containing two columns with the source/target identifiers) to the ``mapping.txt`` output file.
