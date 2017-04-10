# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import pytest

import pandas as pd

# pylint: disable=E0401
from genemap.mappers.util import drop_duplicates
# pylint: enable=E0401


@pytest.fixture()
def mapping():
    """Example mapping."""
    return pd.DataFrame({
        'from': ['a', 'b', 'c', 'c', 'd'],
        'to': ['1', '1', '2', '3', '4']
    })


# pylint: disable=R0201,W0621
class TestDropDuplicates(object):
    """Unit tests for the drop_duplicates function."""

    # TODO: add mto test.

    def test_none(self, mapping):
        """Test no dropping."""

        deduped = drop_duplicates(mapping, how='none')
        assert list(mapping.index) == list(deduped.index)

    def test_otm(self, mapping):
        """Test dropping with from column."""

        deduped = drop_duplicates(mapping, how='otm')
        assert list(deduped['from']) == ['a', 'b', 'd']

    def test_both(self, mapping):
        """Test dropping from both columns."""

        deduped = drop_duplicates(mapping, how='both')
        assert list(deduped['from']) == ['d']

    def test_invalid_how(self, mapping):
        """Testing invalid how option."""
        with pytest.raises(ValueError):
            drop_duplicates(mapping, how='invalid')
