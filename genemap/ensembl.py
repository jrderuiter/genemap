from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

from functools import reduce

import pybiomart
import pandas as pd


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


# --- Main mapping functions --- #


def list_versions():
    """ List the available versions.

    Returns:
        List[str]: List of available versions.

    """
    return list(ENSEMBL_HOSTS.keys())


def list_aliases(version='current'):
    """ Return the available aliases for gene ids.

    Returns:
        Dict[str,str]: Dict of aliases.

    """
    return ENSEMBL_ALIASES[version]


def map_ids(ids, from_type='ensembl', to_type='ensembl',
            remove_duplicates='from', version='current',
            organism='hsapiens', cache=True):
    """Maps gene ids between two different id types.

    This function using biomart (via biomaRt for now) to translate
    a given set of gene ids from one id type to another. Examples
    are symbol --> entrez or ensembl --> symbol. The most commonly
    used ids can be referenced via aliases (e.g. symbol for gene
    symbol), for a full list of these aliases see `list_aliases`.

    Args:
        ids (List[str]): List of gene ids to translate.
        from_type (str): Name of the id type to translate from.
        to_type (str): Name of the id type to translate to.
        remove_duplicates (str): String specifying how to handle duplicates.
            Possible values are `from`, which only drops one-to-many mappings
            from the `from` side of the mapping, or `both` which drops
            mappings that have a one-to-many mapping in any direction.
        version (str): String specifying which ensembl version to use.
            See `list_versions` for possible values.
        organism (str): The organism to use.
        cache (bool): Whether to cache requests.

    Returns:
        pandas.Series: Mapping of ids from their original id (contained in
            the index of the series) and the mapped id. Ids without a mapping
            will be represented by a NaN value.

    Raises:
        ValueError: If `from_type` is equal to `to_type`.

    Examples:
        Translating human gene symbols to ensembl ids:

        >>> list(map_ids(['FGFR2', 'MYH9'], from_type='symbol', cache=False))
        ['ENSG00000066468', 'ENSG00000100345']

    """

    if from_type == to_type:
        raise ValueError('from_type and to_type should not be the same')

    # Get map frame.
    map_frame = get_id_map(from_type, to_type, version=version,
                           organism=organism, cache=cache)

    # Select from/to columns.
    from_col = _format_name(organism, from_type)
    to_col = _format_name(organism, to_type)

    # Return mapped ids.
    return map_ids_with_map(ids, map_frame, remove_duplicates,
                            from_col=from_col, to_col=to_col)


def map_homology(ids, from_org='hsapiens', to_org='hsapiens',
                 from_type='ensembl', to_type='ensembl',
                 remove_duplicates='from', version='current', cache=True):
    """Maps gene ids between two different species (and id types).

    This function using biomart (via biomaRt for now) to translate
    a given set of gene ids from one organism to orthologous genes
    in another species, optionally translating between different
    identifier types if needed (using map_ids). Examples are translating
    from mouse --> human of human --> mouse.

    Args:
        ids (List[str]): List of gene ids to translate.

        from_org (str): Name of the species to translate from.
        to_org (str): Name of the species to translate to.

        from_type (str): Name of the id type to translate from.
        to_type (str): Name of the id type to translate to.

        remove_duplicates (str): String specifying how to handle duplicates.
            Possible values are `from`, which only drops one-to-many mappings
            from the `from` side of the mapping, or `both` which drops
            mappings that have a one-to-many mapping in any direction.
        version (str): String specifying which ensembl version to use.
            See `list_versions` for possible values.

        cache (bool): Whether to cache requests.

    Returns:
        pandas.Series: Mapping of ids from their original id (contained in
            the index of the series) and the mapped id. Ids without a mapping
            will be represented by a NaN value.

    Raises:
        ValueError: If `from_type` is equal to `to_type`.

    Examples:
        Mapping human gene symbols to mouse gene symbols:

        >>> list(map_homology(['FGFR2', 'MYH9'], from_org='hsapiens',
        >>>                   to_type='symbol', from_type='symbol',
        >>>                   cache=False))
            ['Fgfr2', 'Myh9']

    """

    if from_org == to_org:
        raise ValueError('from_org and to_org should not be the same')

    # Get map frame.
    map_frame = get_homology_id_map(
        from_org, to_org, from_type=from_type,
        to_type=to_type, version=version, cache=cache)

    # Select from/to columns.
    from_col = _format_name(from_org, from_type)
    to_col = _format_name(to_org, to_type)

    # Return mapped ids.
    return map_ids_with_map(ids, map_frame, remove_duplicates,
                            from_col=from_col, to_col=to_col)


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

def get_id_map(from_type, to_type, version='current',
               organism='hsapiens', cache=True):
    # Try to lookup column as alias.
    from_column = ENSEMBL_ALIASES[version].get(from_type, from_type)
    to_column = ENSEMBL_ALIASES[version].get(to_type, to_type)

    # Get map_frame from Ensembl.
    server = pybiomart.Server(host=ENSEMBL_HOSTS[version], use_cache=cache)

    map_frame = (server.marts['ENSEMBL_MART_ENSEMBL']
                       .datasets[organism + '_gene_ensembl']
                       .query(attributes=[from_column, to_column]))

    # Override map names to reflect requested types.
    map_frame.columns = [_format_name(organism, from_type),
                         _format_name(organism, to_type)]

    return map_frame


def get_homology_map(from_org, to_org, version='current', cache=True):
    # Determine column names for version.
    from_column = 'ensembl_gene_id'
    to_column = to_org + '_homolog_ensembl_gene'

    # Get map_frame from Ensembl.
    server = pybiomart.Server(host=ENSEMBL_HOSTS[version], use_cache=cache)

    map_frame = (server.marts['ENSEMBL_MART_ENSEMBL']
                       .datasets[from_org + '_gene_ensembl']
                       .query(attributes=[from_column, to_column]))

    # Override map names to reflect requested types.
    map_frame.columns = [_format_name(from_org, 'ensembl'),
                         _format_name(to_org, 'ensembl')]

    return map_frame


def get_homology_id_map(from_org, to_org, from_type='ensembl',
                        to_type='ensembl', version='current', cache=True):

    # Get 'from' map.
    if from_type != 'ensembl':
        from_map = get_id_map(from_type=from_type, to_type='ensembl',
                              organism=from_org, version=version, cache=cache)
    else:
        from_map = None

    # Get 'homology' map.
    homology_map = get_homology_map(from_org, to_org,
                                    version=version, cache=cache)

    # Get 'to' map.
    if to_type != 'ensembl':
        to_map = get_id_map(from_type='ensembl', to_type=to_type,
                            organism=to_org, version=version, cache=cache)
    else:
        to_map = None

    # Join the three maps together.
    if from_map is not None:
        map_frame = pd.merge(from_map, homology_map,
                             on=_format_name(from_org, 'ensembl'))
    else:
        map_frame = homology_map

    if to_map is not None:
        map_frame = pd.merge(map_frame, to_map,
                             on=_format_name(to_org, 'ensembl'))

    return map_frame


def _format_name(organism, id_name):
    return '{}_{}'.format(organism, id_name)
