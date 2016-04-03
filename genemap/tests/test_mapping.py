from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

import numpy as np
import pandas as pd

# pylint: disable=E0401
from ..mapping import map_ids, map_frame
# pylint: enable=E0401

# pylint: disable=R0201,W0621
class TestMapIds(object):
    """Tests for map_ids function."""

    def test_same_organism(self):
        """Tests conversion beteen different id types within same organism."""

        mapped = map_ids(['ENSG00000141510', 'ENSG00000012048'],
                         from_type='ensembl', to_type='symbol')
        assert mapped == ['TP53', 'BRCA1']

    def test_between_organisms(self):
        """Tests conversion between organisms using only ensembl ids."""

        mapped = map_ids(['ENSG00000141510', 'ENSG00000012048'],
                         from_type='ensembl', to_type='ensembl',
                         from_org='hsapiens', to_org='mmusculus')
        assert mapped == ['ENSMUSG00000059552', 'ENSMUSG00000017146']

    def test_between_organisms_symbol(self):
        """Tests conversion with different ids types between organisms."""

        mapped = map_ids(['TP53', 'BRCA1'],
                         from_type='symbol', to_type='symbol',
                         from_org='hsapiens', to_org='mmusculus')
        assert mapped == ['Trp53', 'Brca1']

    def test_invalid_id(self):
        """Tests querying with invalid (or unknown) ids."""

        mapped = map_ids(['ENSG00000141510', 'ENSG00000012048', 'INVALID'],
                         from_type='ensembl', to_type='symbol')
        assert mapped == ['TP53', 'BRCA1', None]

    def test_return_map(self):
        """Tests returning results as a pandas Series."""

        mapped = map_ids(['ENSG00000141510', 'ENSG00000012048'],
                         from_type='ensembl', to_type='symbol', as_series=True)
        assert isinstance(mapped, pd.Series)
        assert list(mapped.index) == ['ENSG00000141510', 'ENSG00000012048']
        assert list(mapped) == ['TP53', 'BRCA1']



def build_df(index):
    """Helper function to build a random data frame."""
    return pd.DataFrame({'S1': np.random.randn(len(index)),
                         'S2': np.random.randn(len(index))},
                         index=index)


# pylint: disable=R0201,W0621
class TestMapFrame(object):
    """Tests for map_frame function."""

    def test_same_organism(self):
        """Tests conversion beteen different id types within same organism."""

        df = build_df(index=['ENSG00000141510', 'ENSG00000012048'])
        mapped = map_frame(df, from_type='ensembl', to_type='symbol')

        assert list(mapped.index) == ['TP53', 'BRCA1']

    def test_between_organisms(self):
        """Tests conversion between organisms using only ensembl ids."""

        df = build_df(index=['ENSG00000141510', 'ENSG00000012048'])
        mapped = map_frame(df, from_type='ensembl', to_type='ensembl',
                           from_org='hsapiens', to_org='mmusculus')

        assert list(mapped.index) == ['ENSMUSG00000059552',
                                      'ENSMUSG00000017146']

    def test_between_organisms_symbol(self):
        """Tests conversion with different ids types between organisms."""

        df = build_df(index=['TP53', 'BRCA1'])
        mapped = map_frame(df, from_type='symbol', to_type='symbol',
                           from_org='hsapiens', to_org='mmusculus')

        assert list(mapped.index) == ['Trp53', 'Brca1']
