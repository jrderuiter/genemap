# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from functools import reduce

import pandas as pd

from .base import Mapper, register_mapper


class CustomMapper(Mapper):
    """Custom mapper class.

    Maps identifiers using a custom mapping provided by the user. The nature
    of the performed mapping depends on the provided mapping table.

    Parameters
    ----------
    mapping : pandas.DataFrame
        Dataframe containing the mapping. Is expected to contain exactly two
        columns, the first of which contains the source ID type, the second
        of which contains the target ID type.
    drop_duplicates : str
        How to handle duplicates. If 'both', then entries with duplicates in
        either the source/target columns are dropped from the mapping. If
        'mto' (many-to-one), then only duplicates in the source column are
        dropped. If 'otm', then only duplicates in the target column are
        dropped. Finally, if 'none', no duplicates are removed from the mapping.

    """

    def __init__(self, mapping, drop_duplicates='both'):
        if not mapping.shape[1] == 2:
            raise ValueError(
                'Requires a dataframe containing exactly two columns')

        super().__init__(drop_duplicates=drop_duplicates)
        self._map = mapping

    def _fetch_mapping(self):
        return self._map


register_mapper('custom', CustomMapper)


class ChainedMapper(Mapper):
    """Chained mapper class.

    Maps identifiers using multiple mappers in a chained fashion. In this
    approach the first mapper maps from type a --> type b, whilst the second
    maps b --> c, etc. This chained mapper essentially 'chains' the mappings
    of the given mappers to provide a mapping from the ``to_type`` of the
    first mapper to the ``from_type`` of the last mapper. (In the two mapper
    example, this provides a mapping from a --> c).

    Parameters
    ----------
    mappers : List[Mapper]
        List of Mapper instances to chain.
    drop_duplicates : str
        How to handle duplicates in the mapping.

    """

    def __init__(self, mappers, drop_duplicates='both'):
        if len(mappers) < 2:
            raise ValueError('At least two mappers must be provided')

        super().__init__(drop_duplicates=drop_duplicates)
        self._mappers = mappers

    def _fetch_mapping(self):
        def _chain_maps(df_a, df_b):
            df_b = df_b.rename(columns={df_b.columns[0]: df_a.columns[1]})
            merged = pd.merge(df_a, df_b, on=df_a.columns[1], how='inner')
            return merged.iloc[:, [0, -1]]

        mappings = (mapper.fetch_mapping() for mapper in self._mappers)
        mapping = reduce(_chain_maps, mappings)
        return mapping.drop_duplicates()


register_mapper('chained', ChainedMapper)


class CombinedMapper(Mapper):
    """Combined mapper class.

    Maps identifiers by combining the mappings of multiple mappers. In this
    setup, mappers are assumed to map the same identifier types (mapper 1 maps
    from a --> b, as does mapper 2). The mappers may however not be complete,
    meaning that mapper 2 may contain additional mappings not contained in
    mapper 1 and vice versa. This combined mapper essentially merges the
    mappings from both mappers, providing a more comprehensive mapping
    containing entries from each mapper.

    Parameters
    ----------
    mappers : List[Mapper]
        List of Mapper instances to combine.
    drop_duplicates : str
        How to handle duplicates in the mapping.

    """

    def __init__(self, mappers, augment=False, drop_duplicates='both'):
        if len(mappers) < 2:
            raise ValueError('At least two mappers must be provided')

        super().__init__(drop_duplicates=drop_duplicates)
        self._mappers = mappers
        self._augment = augment

    def _fetch_mapping(self):
        # Combine mappings, using column names from first dataframe.
        mappings = (mapper.fetch_mapping() for mapper in self._mappers)

        if self._augment:
            mapping = self._augment_mappings(mappings)
        else:
            mapping = self._merge_mappings(mappings)

        return mapping

    @staticmethod
    def _merge_mappings(mappings):
        """Concats mappings, dropping only exact duplicates."""

        mappings = _consolidate_column_names(mappings)
        mapping = pd.concat(mappings, axis=0, ignore_index=False)
        return mapping.drop_duplicates()

    @staticmethod
    def _augment_mappings(mappings):
        """Concats mappings, dropping overlaps (based on from column)."""

        def _augment_frame(df_a, df_b):
            """Merges a and b, dropping overlaps from b (from column)."""
            values_a = set(df_a.iloc[:, 0])
            filt_b = df_b.loc[~df_b.iloc[:, 0].isin(values_a)]
            return pd.concat([df_a, filt_b], axis=0, ignore_index=True)

        mappings = _consolidate_column_names(mappings)
        mapping = reduce(_augment_frame, mappings)
        return mapping.drop_duplicates()


register_mapper('combined', CombinedMapper)


def _consolidate_column_names(dataframes):
    """Returns dataframes with the same column names as the first dataframe."""

    first = next(dataframes)
    yield first

    for df in dataframes:
        df = df.copy()
        df.columns = first.columns
        yield df
