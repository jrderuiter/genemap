# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from .mappers import get_mappers

__author__ = 'Julian de Ruiter'
__email__ = 'julianderuiter@gmail.com'
__version__ = '0.2.0'


def map_ids(ids, mapper, from_type, to_type, drop_duplicates='both', **kwargs):
    """Maps ids using the given mapper."""

    mapper_obj = _build_mapper(
        mapper=mapper,
        from_type=from_type,
        to_type=to_type,
        drop_duplicates=drop_duplicates,
        **kwargs)

    return mapper_obj.map_ids(ids)


def _build_mapper(mapper, from_type, to_type, drop_duplicates, **kwargs):

    try:
        mapper_class = get_mappers()[mapper]
    except KeyError:
        raise ValueError('Unknown mapper {!r}. Available mappers are: {}.'
                         .format(mapper, list(get_mappers().keys())))

    return mapper_class(
        from_type=from_type,
        to_type=to_type,
        drop_duplicates=drop_duplicates,
        **kwargs)


def map_dataframe(df,
                  mapper,
                  from_type,
                  to_type,
                  drop_duplicates='both',
                  **kwargs):
    """Maps dataframe index using the given mapper."""

    mapper_obj = _build_mapper(
        mapper=mapper,
        from_type=from_type,
        to_type=to_type,
        drop_duplicates=drop_duplicates,
        **kwargs)

    return mapper_obj.map_dataframe(df)
