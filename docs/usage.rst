=====
Usage
=====


Mapping ids
-----------

.. code:: bash

    genemap map_ids ensembl \
        --from_type symbol --to_type ensembl \
        --host http://aug2014.archive.ensembl.org \
        TP53 BRCA1 PPP1R12A

Mapping dataframes
------------------

.. code:: bash

    genemap get_map ensembl \
        --from_type symbol --to_type ensembl \
        --host http://aug2014.archive.ensembl.org \
        input.txt mapped.txt

Fetching maps
-------------

.. code:: bash

    genemap get_map ensembl \
        --from_type symbol --to_type ensembl \
        --host http://aug2014.archive.ensembl.org \
        mapping.txt
