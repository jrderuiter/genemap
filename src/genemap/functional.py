# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *

# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from .mappers import get_mappers


def map_ids(ids, mapper, drop_duplicates='both', **kwargs):
    """Maps a list of IDs to new values using the given mapper.

    Parameters
    ----------
    ids : List[str]
        List of IDs to map.
    mapper : str
        Name of the required mapper (e.g. 'ensembl', 'mgi', 'custom').
    drop_duplicates : str
        How to handle duplicates. If 'both', then entries with duplicates in
        either the source/target columns are dropped from the mapping. If
        'mto' (many-to-one), then only duplicates in the source column are
        dropped. If 'otm', then only duplicates in the target column are
        dropped. Finally, if 'none', no duplicates are removed from the mapping.
    kwargs : Dict[str, Any]
        Extra keyword arguments for the requested mapper.

    Returns
    -------
    List[str]
        List of mapped IDs.

    """

    mapper_obj = _build_mapper(
        mapper=mapper, drop_duplicates=drop_duplicates, **kwargs)

    return mapper_obj.map_ids(ids)


def _build_mapper(mapper, drop_duplicates, **kwargs):

    try:
        mapper_class = get_mappers()[mapper]
    except KeyError:
        raise ValueError('Unknown mapper {!r}. Available mappers are: {}.'
                         .format(mapper, list(get_mappers().keys())))

    return mapper_class(drop_duplicates=drop_duplicates, **kwargs)


def map_dataframe(df, mapper, drop_duplicates='both', **kwargs):
    """Maps dataframe index using the given mapper.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to map.
    mapper : str
        Name of the required mapper (e.g. 'ensembl', 'mgi', 'custom').
    drop_duplicates : str
        How to handle duplicates. If 'both', then entries with duplicates in
        either the source/target columns are dropped from the mapping. If
        'mto' (many-to-one), then only duplicates in the source column are
        dropped. If 'otm', then only duplicates in the target column are
        dropped. Finally, if 'none', no duplicates are removed from the mapping.
    kwargs : Dict[str, Any]
        Extra keyword arguments for the requested mapper.

    Returns
    -------
    List[str]
        List of mapped IDs.

    """

    mapper_obj = _build_mapper(
        mapper=mapper, drop_duplicates=drop_duplicates, **kwargs)

    return mapper_obj.map_dataframe(df)


def fetch_mapping(mapper, drop_duplicates='both', **kwargs):
    """Fetches map used by given mapper.

    Returns the mapping that is actually used to map the IDs. This is is mainly
    useful if you are interested in the mapping itself or want to perform more
    complicated mappings than are provided by the map_ids and map_dataframe
    methods.

    Parameters
    ----------
    mapper : str
        Name of the required mapper (e.g. 'ensembl', 'mgi', 'custom').
    drop_duplicates : str
        How to handle duplicates. If 'both', then entries with duplicates in
        either the source/target columns are dropped from the mapping. If
        'mto' (many-to-one), then only duplicates in the source column are
        dropped. If 'otm', then only duplicates in the target column are
        dropped. Finally, if 'none', no duplicates are removed from the mapping.
    kwargs : Dict[str, Any]
        Extra keyword arguments for the requested mapper.

    Returns
    -------
    pandas.DataFrame
        DataFrame describing the used mapping. The DataFrame contains two
        columns, the first of which contains the source idenfiers (from
        which we map), whereas the second contains the target idenfiers
        (to which we map).

    """

    mapper_obj = _build_mapper(
        mapper=mapper, drop_duplicates=drop_duplicates, **kwargs)
    return mapper_obj.mapping
