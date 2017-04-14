# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import pandas as pd

import pytest

from genemap.mappers.compound import (CustomMapper, CombinedMapper,
                                      ChainedMapper)

# pylint: disable=R0201,W0621


@pytest.fixture
def custom_mapping1():
    """A simple custom mapping."""
    return pd.DataFrame({'a': ['A1', 'A2', 'A3'], 'b': ['B1', 'B2', 'B3']})


@pytest.fixture
def custom_mapping2():
    """A second custom mapping, extending the first."""
    return pd.DataFrame({'a': ['A3', 'A4', 'A5'], 'b': ['B3-2', 'B4', 'B5']})


@pytest.fixture
def custom_mapping3():
    """A third custom mapping, chaining the first."""
    return pd.DataFrame({'b': ['B1', 'B2', 'B3'], 'c': ['C1', 'C2', 'C3']})


class TestCustomMapper(object):
    """Unit tests for the CustomMapper class."""

    def test_example(self, custom_mapping1):
        """Tests simple case with custom mapping."""

        mapper = CustomMapper(custom_mapping1)
        mapped = mapper.map_ids(['A1', 'A3'])

        assert mapped == ['B1', 'B3']

    def test_wrong_shape(self, custom_mapping1):
        """Tests if error is raised if only one column is given."""

        with pytest.raises(ValueError):
            CustomMapper(custom_mapping1.iloc[:, [0]])

    def test_wrong_shape2(self, custom_mapping1, custom_mapping3):
        """Tests if error is raised if only more than two columns are given."""

        with pytest.raises(ValueError):
            mapping = pd.concat([custom_mapping1, custom_mapping3], axis=1)
            CustomMapper(mapping)


class TestCombinedMapper(object):
    """Unit tests for the CombinedMapper class."""

    def test_merged(self, custom_mapping1, custom_mapping2):
        """Tests example case with merge behaviour."""

        mapper1 = CustomMapper(custom_mapping1)
        mapper2 = CustomMapper(custom_mapping2)

        mapper = CombinedMapper([mapper1, mapper2])
        mapped = mapper.map_ids(['A1', 'A3', 'A5'])

        # Note that A3 is not mapped due to duplicate entries
        # in the merged mapping (B3 and B3-2).
        assert mapped == ['B1', None, 'B5']

    def test_augmented(self, custom_mapping1, custom_mapping2):
        """Tests example case with augmented behaviour."""

        mapper1 = CustomMapper(custom_mapping1)
        mapper2 = CustomMapper(custom_mapping2)

        mapper = CombinedMapper([mapper1, mapper2], augment=True)
        mapped = mapper.map_ids(['A1', 'A3', 'A5'])

        assert mapped == ['B1', 'B3', 'B5']

    def test_single_mapper(self, custom_mapping1):
        """Tests if error is raised if only one mapper is given."""

        with pytest.raises(ValueError):
            mapper1 = CustomMapper(custom_mapping1)
            CombinedMapper([mapper1])


class TestChainedMapper(object):
    """Unit tests for the ChainedMapper class."""

    def test_example(self, custom_mapping1, custom_mapping3):
        """Tests simple chained example."""

        mapper1 = CustomMapper(custom_mapping1)
        mapper2 = CustomMapper(custom_mapping3)

        mapper = ChainedMapper([mapper1, mapper2])
        mapped = mapper.map_ids(['A1', 'A2', 'A3'])

        assert mapped == ['C1', 'C2', 'C3']

    def test_example_diff_names(self, custom_mapping1, custom_mapping3):
        """Tests example with different column names."""

        custom_mapping3 = custom_mapping3.rename(columns={'b': 'd'})

        mapper1 = CustomMapper(custom_mapping1)
        mapper2 = CustomMapper(custom_mapping3)

        mapper = ChainedMapper([mapper1, mapper2])
        mapped = mapper.map_ids(['A1', 'A2', 'A3'])

        assert mapped == ['C1', 'C2', 'C3']

    def test_example_missing(self, custom_mapping1, custom_mapping3):
        """Tests example with missing entries."""

        mapper1 = CustomMapper(custom_mapping1.iloc[1:])
        mapper2 = CustomMapper(custom_mapping3.iloc[:2])

        mapper = ChainedMapper([mapper1, mapper2])
        mapped = mapper.map_ids(['A1', 'A2', 'A3'])

        assert mapped == [None, 'C2', None]

    def test_single_mapper(self, custom_mapping1):
        """Tests if error is raised if only one mapper is given."""

        with pytest.raises(ValueError):
            mapper1 = CustomMapper(custom_mapping1)
            ChainedMapper([mapper1])
