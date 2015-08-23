from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

import os
from functools import reduce

import pandas as pd

from .biomart import use_mart, get_bm


ENSEMBL_HOSTS = {
    'current': 'ensembl.org',
    # 80: 'may2015.archive.ensembl.org', Empty datasets?
    'ensembl_79': 'mar2015.archive.ensembl.org',
    'ensembl_78': 'dec2014.archive.ensembl.org',
    'ensembl_77': 'oct2014.archive.ensembl.org',
    'ensembl_76': 'aug2014.archive.ensembl.org',
    'ensembl_75': 'feb2014.archive.ensembl.org',
    'ensembl_74': 'dec2013.archive.ensembl.org',
    'ensembl_67': 'may2012.archive.ensembl.org'
}

ID_ALIASES = {
    'symbol': 'external_gene_name',
    'entrez': 'entrezgene',
    'ensembl': 'ensembl_gene_id'
}

ID_ALIASES_PRE_76 = dict(ID_ALIASES)
ID_ALIASES_PRE_76.update({'symbol': 'external_gene_id'})

ENSEMBL_ALIASES = {
    'current': ID_ALIASES,
    'ensembl_79': ID_ALIASES,
    'ensembl_78': ID_ALIASES,
    'ensembl_77': ID_ALIASES,
    'ensembl_76': ID_ALIASES,
    'ensembl_75': ID_ALIASES_PRE_76,
    'ensembl_74': ID_ALIASES_PRE_76,
    'ensembl_67': ID_ALIASES_PRE_76
}

DEFAULT_CACHE_DIR = '_gm_cache'


# --- Main mapping functions --- #


def list_versions():
    return list(ENSEMBL_HOSTS.keys())


def list_aliases(version='current'):
    return ENSEMBL_ALIASES[version]


def map_ids(ids, from_='ensembl', to='ensembl',
            remove_duplicates='from', version='current',
            organism='hsapiens', cache=True,
            cache_dir=DEFAULT_CACHE_DIR, map_filter=None):
    if from_ == to:
        raise ValueError('from_ and to should not be the same')

    # Get map frame.
    map_frame = get_id_map(from_, to, version=version, organism=organism,
                           cache=cache, cache_dir=cache_dir)

    # Select from/to columns.
    from_col = _format_name(organism, from_)
    to_col = _format_name(organism, to)

    # Return mapped ids.
    return map_ids_with_map(ids, map_frame, remove_duplicates,
                            from_col=from_col, to_col=to_col,
                            map_filter=map_filter)


def map_homology(ids, from_, to, from_type='ensembl', to_type='ensembl',
                 remove_duplicates='from', version='current',
                 cache=True, cache_dir=DEFAULT_CACHE_DIR, map_filter=None):
    if from_ == to:
        raise ValueError('from_ and to should not be the same')

    # Get map frame.
    map_frame = get_homology_id_map(
        from_, to, from_type=from_type,
        to_type=to_type, version=version,
        cache=cache, cache_dir=cache_dir)

    # Select from/to columns.
    from_col = _format_name(from_, from_type)
    to_col = _format_name(to, to_type)

    # Return mapped ids.
    return map_ids_with_map(ids, map_frame, remove_duplicates,
                            from_col=from_col, to_col=to_col,
                            map_filter=map_filter)


def map_ids_with_map(ids, map_frame, remove_duplicates='from',
                     from_col=None, to_col=None, map_filter=None):

    # Determine to/from columns from argument or map.
    if from_col is None or to_col is None:
        if not map_frame.shape[1] == 2:
            raise ValueError('Map frame must contain two columns if '
                             'from_col/to_col are not specified')
        from_col, to_col = map_frame.columns

    # First, subset map_frame for the passed ids.
    map_frame = map_frame.ix[map_frame[from_col].isin(set(ids))]

    # Second, filter the map using map_filter (if supplied).
    if map_filter is not None:
        map_frame = map_filter(map_frame)

    # Third, remove duplicates from map_frame (delaying removal
    # to after the sub-setting allows us to map ids as long as
    # the mapping is unique within the queried ids).
    map_frame = _drop_duplicates_map(
        map_frame, from_col, to_col, remove_duplicates)

    # Convert frame to 'map'.
    map_ = map_frame.set_index(from_col)[to_col]

    return map_.ix[ids]


def _drop_duplicates_map(map_frame, from_col, to_col, how='from'):
    if how == 'from':
        duplicate_columns = [from_col]
    elif how == 'both':
        duplicate_columns = [from_col, to_col]
    else:
        raise ValueError(('Unknown value for from ({}), '
                          'should be either "from" or "both"').format(how))

    return drop_duplicates(map_frame, columns=duplicate_columns)


def drop_duplicates(frame, columns=None):
    columns = columns or frame.columns

    masks = map(lambda c: duplicate_mask(frame, c), columns)
    mask = reduce(lambda m1, m2: m1 | m2, masks)

    return frame.ix[~mask]


def duplicate_mask(frame, column):
    duplicate_rows = frame.duplicated(subset=column)
    duplicate_values = set(frame.ix[duplicate_rows][column])
    return frame[column].isin(duplicate_values)


# --- Map retrieval functions --- #

def get_id_map(from_, to, version='current', organism='hsapiens',
               cache=True, cache_dir=DEFAULT_CACHE_DIR):
    # Try to lookup column as alias.
    from_column = ENSEMBL_ALIASES[version].get(from_, from_)
    to_column = ENSEMBL_ALIASES[version].get(to, to)

    # Get map from Ensembl.
    map_ = get_map(from_=from_column, to=to_column, version=version,
                   organism=organism, cache=cache, cache_dir=cache_dir)

    # Override map names.
    map_.columns = [_format_name(organism, from_),
                    _format_name(organism, to)]

    return map_


def get_homology_map(from_, to, version='current',
                     cache=True, cache_dir=DEFAULT_CACHE_DIR):
    # Determine column names for version.
    from_column = 'ensembl_gene_id'
    to_column = to + '_homolog_ensembl_gene'

    # Get map from Ensembl.
    map_ = get_map(from_=from_column, to=to_column, version=version,
                   organism=from_, cache=cache, cache_dir=cache_dir)

    # Override map names.
    map_.columns = [_format_name(from_, 'ensembl'),
                    _format_name(to, 'ensembl')]

    return map_


def get_homology_id_map(
        from_, to, from_type='ensembl', to_type='ensembl',
        version='current', cache=True, cache_dir=DEFAULT_CACHE_DIR):

    # Get 'from' map.
    if from_type != 'ensembl':
        from_map = get_id_map(from_=from_type, to='ensembl', organism=from_,
                              version=version, cache=cache, cache_dir=cache_dir)
    else:
        from_map = None

    # Get 'homology' map.
    homology_map = get_homology_map(from_, to, version=version,
                                    cache=cache, cache_dir=cache_dir)

    # Get 'to' map.
    if to_type != 'ensembl':
        to_map = get_id_map(from_='ensembl', to=to_type, organism=to,
                            version=version, cache=cache, cache_dir=cache_dir)
    else:
        to_map = None

    # Join the three maps together.
    if from_map is not None:
        map_frame = pd.merge(from_map, homology_map,
                             on=_format_name(from_, 'ensembl'))
    else:
        map_frame = homology_map

    if to_map is not None:
        map_frame = pd.merge(map_frame, to_map,
                             on=_format_name(to, 'ensembl'))

    return map_frame


def _format_name(organism, id_name):
    return '{}_{}'.format(organism, id_name)


# --- 'Low-level' map retrieval/caching functions --- #

def get_map(from_, to, version='current', organism='hsapiens',
            cache=True, cache_dir=DEFAULT_CACHE_DIR):
    # Try to fetch map_frame from cache.
    map_frame = None
    if cache:
        map_frame = _map_cache_get(organism, version, from_, to, cache_dir)

    if map_frame is None:
        # Get Ensembl mart if not in cache or no cache.
        mart = use_mart(biomart='ENSEMBL_MART_ENSEMBL',
                        host=ENSEMBL_HOSTS[version],
                        dataset=organism + '_gene_ensembl')

        # Fetch mapping frame from biomart.
        map_frame = get_bm(mart=mart, attributes=[from_, to])
        map_frame.dropna(inplace=True)

    # Write to cache if needed.
    if cache:
        _map_cache_put(map_frame, organism, version, from_, to, cache_dir)

    # Convert to string to ensure that ids are strings.
    # TODO: handle this more intelligently?
    map_frame = map_frame.astype(str)

    return map_frame


def _map_cache_get(organism, version, from_col, to_col, cache_dir):
    map_frame = None

    if os.path.exists(cache_dir):
        cache_names = [_map_cache_name(organism, version, from_col, to_col),
                       _map_cache_name(organism, version, to_col, from_col)]

        # Try both from-to and to-from names, break on hit.
        for cache_name in cache_names:
            cache_path = os.path.join(cache_dir, cache_name)

            if os.path.exists(cache_path):
                map_frame = pd.read_csv(cache_path, sep='\t')
                map_frame = map_frame[[from_col, to_col]]
                break

    return map_frame


def _map_cache_put(frame, organism, version, from_col, to_col, cache_dir):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    cache_name = _map_cache_name(organism, version, from_col, to_col)
    cache_path = os.path.join(cache_dir, cache_name)

    frame.to_csv(cache_path, sep='\t', index=False)


def _map_cache_name(organism, version, from_col, to_col):
    return '{}.{}.{}-{}.txt'.format(organism, version, from_col, to_col)
