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

    def __init__(self, from_type, to_type, drop_duplicates='both'):

        self._from_type = from_type
        self._to_type = to_type
        self._drop_duplicates = drop_duplicates

        self._map = None

    @classmethod
    def configure_args(cls, parser):
        pass

    @classmethod
    def parse_args(cls, args):
        return {}

    @classmethod
    def from_args(cls, args):
        return cls(**cls.parse_args(args))

    @property
    def mapping(self):
        """Returns mapping used to map ids."""

        if self._map is None:
            self._map = self._fetch_map().dropna()

        return self._map

    def _fetch_map(self):
        raise NotImplementedError()

    def map_ids(self, ids):
        """Maps given ids to new values."""

        # One to many mappings are not possible for lists.
        if not self._drop_duplicates in {'both', 'from'}:
            raise ValueError(
                'One to many mappings are not possible for lists. '
                'Drop_duplicates should be either \'both\' or \'otm\', '
                'not \'none\' or \'mto\'.')

        mapping = util.drop_duplicates(self.mapping, how=self._drop_duplicates)

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

        mapping = util.drop_duplicates(self.mapping, how=self._drop_duplicates)

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
