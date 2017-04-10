# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from genemap.mappers.ensembl import EnsemblMapper

HOST = 'http://aug2014.archive.ensembl.org'


# pylint: disable=R0201,W0621
class TestEnsemblMapperMapIds(object):
    """Unit tests for the map_ids method of the EnsemblMapper class."""

    def test_human_sym_to_ens(self):
        """Tests conversion from symbols to ensembl ids."""

        mapper = EnsemblMapper(
            from_type='symbol', to_type='ensembl', host=HOST)
        mapped = mapper.map_ids(['TP53', 'BRCA1'])

        assert mapped == ['ENSG00000141510', 'ENSG00000012048']

    def test_human_ens_to_sym(self):
        """Tests conversion from ensembl ids to symbols."""

        mapper = EnsemblMapper(
            from_type='ensembl', to_type='symbol', host=HOST)
        mapped = mapper.map_ids(['ENSG00000141510', 'ENSG00000012048'])

        assert mapped == ['TP53', 'BRCA1']

    def test_mouse_sym_to_ens(self):
        """Tests conversion from symbols to ensembl ids for mouse."""

        mapper = EnsemblMapper(
            from_type='symbol',
            to_type='ensembl',
            host=HOST,
            from_organism='mmusculus')
        mapped = mapper.map_ids(['Trp53', 'Brca1'])
        assert mapped == ['ENSMUSG00000059552', 'ENSMUSG00000017146']


# # pylint: disable=R0201,W0621
# class TestGetMap(object):
#     """Tests get_map function."""

#     def test_same_organism(self):
#         """Tests conversion beteen different id types within same organism."""

#         map_ = get_map(from_type='ensembl', to_type='symbol')

#         # Check mapping shape and columns.
#         assert map_.shape[0] > 0
#         assert list(map_.columns) == ['hsapiens_ensembl', 'hsapiens_symbol']

#         # Check known entries.
#         map_indexed = map_.set_index('hsapiens_ensembl')
#         assert map_indexed.ix['ENSG00000141510', 'hsapiens_symbol'] == 'TP53'
#         assert map_indexed.ix['ENSG00000012048', 'hsapiens_symbol'] == 'BRCA1'

#     def test_between_organisms(self):
#         """Tests conversion between organisms using only ensembl ids."""

#         map_ = get_map(
#             from_type='ensembl',
#             to_type='ensembl',
#             from_org='hsapiens',
#             to_org='mmusculus')

#         # Check mapping shape and columns.
#         assert map_.shape[0] > 0
#         assert list(map_.columns) == ['hsapiens_ensembl', 'mmusculus_ensembl']

#         # Check known entries.
#         map_indexed = map_.set_index('hsapiens_ensembl')
#         assert map_indexed.ix['ENSG00000141510', 0] == 'ENSMUSG00000059552'
#         assert map_indexed.ix['ENSG00000012048', 0] == 'ENSMUSG00000017146'

#     def test_between_organisms_symbol(self):
#         """Tests conversion with different ids types between organisms."""

#         map_ = get_map(
#             from_type='symbol',
#             to_type='symbol',
#             from_org='hsapiens',
#             to_org='mmusculus')

#         # Check mapping shape and columns.
#         assert map_.shape[0] > 0
#         assert list(map_.columns) == ['hsapiens_symbol', 'mmusculus_symbol']

#         # Check known entries.
#         map_indexed = map_.set_index('hsapiens_symbol')
#         assert map_indexed.ix['TP53', 'mmusculus_symbol'] == 'Trp53'
#         assert map_indexed.ix['BRCA1', 'mmusculus_symbol'] == 'Brca1'

#     def test_available_versions(self):
#         """Tests available versions."""

#         versions = available_versions()
#         assert len(versions) > 0

#     def test_available_aliases(self):
#         """Tests available aliases."""

#         aliases = available_aliases(version='current')
#         assert len(aliases) > 0
