# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import numpy as np
import pandas as pd
import pytest

from genemap import map_ids, map_dataframe

HOST = 'http://aug2014.archive.ensembl.org'


@pytest.fixture
def ensembl_kws():
    """Default keyword arguments from the Ensembl mapper."""
    return {'host': HOST, 'mapper': 'ensembl'}


# pylint: disable=R0201,W0621
class TestMapIds(object):
    """Tests for map_ids function."""

    def test_same_organism(self, ensembl_kws):
        """Tests conversion beteen different id types within same organism."""

        mapped = map_ids(
            ['ENSG00000141510', 'ENSG00000012048'],
            from_type='ensembl',
            to_type='symbol',
            **ensembl_kws)
        assert mapped == ['TP53', 'BRCA1']

    def test_between_organisms(self, ensembl_kws):
        """Tests conversion between organisms using only ensembl ids."""

        mapped = map_ids(
            ['ENSG00000141510', 'ENSG00000012048'],
            from_type='ensembl',
            to_type='ensembl',
            from_organism='hsapiens',
            to_organism='mmusculus',
            **ensembl_kws)
        assert mapped == ['ENSMUSG00000059552', 'ENSMUSG00000017146']

    def test_between_organisms_symbol(self, ensembl_kws):
        """Tests conversion with different ids types between organisms."""

        mapped = map_ids(
            ['TP53', 'BRCA1'],
            from_type='symbol',
            to_type='symbol',
            from_organism='hsapiens',
            to_organism='mmusculus',
            **ensembl_kws)
        assert mapped == ['Trp53', 'Brca1']

    def test_invalid_id(self, ensembl_kws):
        """Tests querying with invalid (or unknown) ids."""

        mapped = map_ids(
            ['ENSG00000141510', 'ENSG00000012048', 'INVALID'],
            from_type='ensembl',
            to_type='symbol',
            **ensembl_kws)
        assert mapped == ['TP53', 'BRCA1', None]


# def build_df(index):
#     """Helper function to build a random data frame."""
#     return pd.DataFrame(
#         {
#             'S1': np.random.randn(len(index)),
#             'S2': np.random.randn(len(index))
#         },
#         index=index)

# # pylint: disable=R0201,W0621
# class TestMapFrame(object):
#     """Tests for map_frame function."""

#     def test_same_organism(self):
#         """Tests conversion beteen different id types within same organism."""

#         df = build_df(index=['ENSG00000141510', 'ENSG00000012048'])
#         mapped = map_frame(df, from_type='ensembl', to_type='symbol')

#         assert list(mapped.index) == ['TP53', 'BRCA1']

#     def test_between_organisms(self):
#         """Tests conversion between organisms using only ensembl ids."""

#         df = build_df(index=['ENSG00000141510', 'ENSG00000012048'])
#         mapped = map_frame(
#             df,
#             from_type='ensembl',
#             to_type='ensembl',
#             from_organism='hsapiens',
#             to_organism='mmusculus')

#         assert list(mapped.index) == [
#             'ENSMUSG00000059552', 'ENSMUSG00000017146'
#         ]

#     def test_between_organisms_symbol(self):
#         """Tests conversion with different ids types between organisms."""

#         df = build_df(index=['TP53', 'BRCA1'])
#         mapped = map_frame(
#             df,
#             from_type='symbol',
#             to_type='symbol',
#             from_organism='hsapiens',
#             to_organism='mmusculus')

#         assert list(mapped.index) == ['Trp53', 'Brca1']
