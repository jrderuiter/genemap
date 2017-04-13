# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import pandas as pd

from . import util

_registry = {}


def register_mapper(name, mapper):
    """Registers a mapper class under given name."""
    _registry[name] = mapper


def get_mappers():
    """Returns dict of registered mapper classes."""
    return dict(_registry)


class Mapper(object):
    """Base mapper class."""

    def __init__(self, drop_duplicates='both'):
        self._mapping = None
        self._drop_duplicates = drop_duplicates

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('--from_type', required=True)
        parser.add_argument('--to_type', required=True)
        parser.add_argument('--drop_duplicates', default='both')

    @classmethod
    def parse_args(cls, args):
        return {}

    @classmethod
    def from_args(cls, args):
        return cls(**cls.parse_args(args))

    def fetch_mapping(self):
        """Returns mapping used to map ids."""

        if self._mapping is None:
            self._mapping = self._fetch_mapping().dropna()

        return self._mapping

    def _fetch_mapping(self):
        raise NotImplementedError()

    def map_ids(self, ids):
        """Maps given ids to new values."""

        # One to many mappings are not possible for lists.
        if not self._drop_duplicates in {'both', 'otm'}:
            raise ValueError(
                'One to many mappings are not possible for lists. '
                'Drop_duplicates should be either \'both\' or \'otm\', '
                'not \'none\' or \'mto\'.')

        mapping = self.fetch_mapping()
        mapping = util.drop_duplicates(mapping, how=self._drop_duplicates)

        from_col, to_col = mapping.columns
        lookup = mapping.set_index(from_col)[to_col]

        try:
            mapped = lookup.loc[ids]
            mapped = list(mapped.where((pd.notnull(mapped)), None))
        except KeyError:
            # None of the ids are in the index.
            mapped = [None] * len(ids)

        return mapped

    def map_dataframe(self, df):
        """Maps index of a dataframe to new values."""

        mapping = self.fetch_mapping()
        mapping = util.drop_duplicates(mapping, how=self._drop_duplicates)

        index_name = df.index.name
        from_col, to_col = mapping.columns

        mapped = pd.merge(
            df.reset_index(),
            mapping.rename(columns={from_col: index_name}),
            on=index_name,
            how='left')

        mapped = (mapped.dropna(subset=[to_col]).set_index(to_col).drop(
            index_name, axis=1))

        return mapped
