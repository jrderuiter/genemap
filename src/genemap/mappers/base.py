# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import pandas as pd

from . import util

_registry = {}
_cli_registry = {}


def register_mapper(name, mapper_class):
    """Registers a mapper class under given name.

    Parameters
    ----------
    name : str
        Name to register mapper under.
    mapper_class : Class[Mapper]
        Mapper class to register.

    """

    _registry[name] = mapper_class

    if issubclass(mapper_class, CommandLineMixin):
        _cli_registry[name] = mapper_class


def get_mappers(with_command_line=False):
    """Returns dict of registered mapper classes.

    Parameters
    ----------
    with_command_line : bool
        Whether to return all mappers (False) or only those with a command
        line interface (True).

    Returns
    -------
    Dict[str, Mapper]
        Dictionary of registered Mapper classes.

    """

    if with_command_line:
        return dict(_cli_registry)
    else:
        return dict(_registry)


class Mapper(object):
    """Base mapper class."""

    def __init__(self, drop_duplicates='both'):
        self._mapping = None
        self._drop_duplicates = drop_duplicates

    def fetch_mapping(self):
        """Fetches mapping used to map ids.

        Returns the mapping that is actually used to map the IDs. This is
        is mainly useful if you are interested in the mapping itself or want
        to perform more complicated mappings than are provided by the
        ``map_ids`` and ``map_dataframe`` methods.

        Returns
        -------
        pandas.DataFrame
            DataFrame describing the used mapping. The DataFrame contains two
            columns, the first of which contains the source idenfiers (from
            which we map), whereas the second contains the target idenfiers
            (to which we map).
        """

        if self._mapping is None:
            self._mapping = self._fetch_mapping().dropna()

        return self._mapping

    def _fetch_mapping(self):
        raise NotImplementedError()

    def map_ids(self, ids):
        """Maps a list of IDs to new values.

        Parameters
        ----------
        ids : List[str]
            List of IDs to map.

        Returns
        -------
        List[str]
            List of mapped IDs.

        """

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
        """Maps index of a dataframe to new values.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to map.

        Returns
        -------
        pandas.DataFrame
            Mapped DataFrame in which the index values have been mapped
            to a new identifier type.

        """

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


class CommandLineMixin(object):
    """Simple mixin that defines functions for mappers with CLI interfaces."""

    @classmethod
    def configure_parser(cls, parser):
        """Configures an argparse Parser for parsing command line args."""
        raise NotImplementedError()

    @classmethod
    def from_args(cls, args):
        """Instantiates the mapper from the given parsed arguments."""
        raise NotImplementedError()
