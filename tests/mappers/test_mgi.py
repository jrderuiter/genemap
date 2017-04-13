# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import pytest

from genemap.mappers.mgi import MgiMapper


# pylint: disable=R0201,W0621
class TestMgiMapperMapIds(object):
    """Unit tests for the map_ids method of the MgiMapper class."""

    def test_human_sym_to_entrez(self):
        """Tests conversion from symbols to ensembl ids."""

        mapper = MgiMapper(
            from_type='symbol', to_type='entrez', from_organism='human')
        mapped = mapper.map_ids(['TP53', 'BRCA1'])

        assert mapped == ['7157', '672']

    def test_human_entrez_to_sym(self):
        """Tests conversion from ensembl ids to symbols."""

        mapper = MgiMapper(
            from_type='entrez', to_type='symbol', from_organism='human')
        mapped = mapper.map_ids(['7157', '672'])

        assert mapped == ['TP53', 'BRCA1']

    def test_mouse_sym_to_entrez(self):
        """Tests conversion from symbols to ensembl ids for mouse."""

        mapper = MgiMapper(
            from_type='symbol', to_type='entrez', from_organism='mouse')
        mapped = mapper.map_ids(['Trp53', 'Brca1'])

        assert mapped == ['22059', '12189']

    def test_unknown_from_organism(self):
        """Tests if unknown from_organism raises error."""

        with pytest.raises(ValueError):
            mapper = MgiMapper(
                from_type='symbol', to_type='entrez', from_organism='unknown')
            mapper.map_ids(['Trp53', 'Brca1'])

    def test_unknown_to_organism(self):
        """Tests if unknown to_organism raises error."""

        with pytest.raises(ValueError):
            mapper = MgiMapper(
                from_type='symbol', to_type='entrez', to_organism='unknown')
            mapper.map_ids(['Trp53', 'Brca1'])
