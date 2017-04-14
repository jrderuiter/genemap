# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import pandas as pd

from .base import Mapper, register_mapper


class CustomMapper(Mapper):
    """Custom mapper class.

    Maps idenifiers using a provided mapping.
    """

    def __init__(self, mapping):
        if not mapping.shape[1] == 2:
            raise ValueError(
                'Requires a dataframe containing exactly two columns')

        super().__init__()
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

    """

    def __init__(self, mappers, drop_duplicates='both'):
        if len(mappers) < 2:
            raise ValueError('At least two mappers must be provided')

        super().__init__(drop_duplicates=drop_duplicates)
        self._mappers = mappers

    def _fetch_mapping(self):
        mapping = self._mappers[0].fetch_mapping()

        for mapper in self._mappers[1:]:
            prev_target = mapping.columns[-1]

            new_mapping = mapper.fetch_mapping()
            new_mapping = mapping.rename(
                columns={new_mapping.columns[0]: prev_target})

            mapping = pd.merge(
                mapping, new_mapping, on=prev_target, how='left')

        return mapping.iloc[:, [0, -1]]


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

    def __init__(self, mappers, how='merge', drop_duplicates='both'):
        if len(mappers) < 2:
            raise ValueError('At least two mappers must be provided')

        if how not in {'merge', 'augment'}:
            raise ValueError('Unknown value for how ({}). Possible values '
                             'are \'merge\' and \'augment\'.'.format(how))

        super().__init__(drop_duplicates=drop_duplicates)
        self._mappers = mappers
        self._how = how

    def _fetch_mapping(self):
        mappings = (mapper.fetch_mapping() for mapper in self._mappers)

        if self._how == 'augment':
            raise NotImplementedError()
        elif self._how == 'merge':
            mapping = self._merge_mappings(mappings)
        else:
            raise ValueError('Unknwon value for how')

        return mapping

    @staticmethod
    def _merge_mappings(mappings):
        mappings = iter(mappings)

        # Fetch first map (used as example).
        mapping = next(mappings)

        # Merge extra mappings.
        for extra_mapping in mappings:
            extra_mapping.columns = mapping.columns

            mapping = pd.concat(
                [mapping, extra_mapping], axis=0, ignore_index=True)

        # Remove any duplicates that were introduced.
        mapping = mapping.drop_duplicates()

        return mapping


register_mapper('combined', CombinedMapper)
