from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

import numpy as np
import pandas as pd

import pybiomart

# pylint: disable=E0401
from ..registry import mapper
from ..util import drop_duplicates as drop_duplicates_
# pylint: enable=E0401


ENSEMBL_HOSTS = {
    'current': 'ensembl.org',
    # 80: 'may2015.archive.ensembl.org', Empty datasets?
    '79': 'mar2015.archive.ensembl.org',
    '78': 'dec2014.archive.ensembl.org',
    '77': 'oct2014.archive.ensembl.org',
    '76': 'aug2014.archive.ensembl.org',
    '75': 'feb2014.archive.ensembl.org',
    '74': 'dec2013.archive.ensembl.org',
    '67': 'may2012.archive.ensembl.org'
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


def available_versions():
    """ List the available versions.

    Returns:
        List[str]: List of available versions.

    """
    return sorted(ENSEMBL_HOSTS.keys())


def available_aliases(version='current'):
    """ Return the available aliases for gene ids.

    Returns:
        Dict[str,str]: Dict of aliases.

    """
    return ENSEMBL_ALIASES[version]


# --- Map retrieval functions --- #

def ensembl_options(parser):
    # Add from/to organism options.
    parser.add_argument('--from_organism', default='hsapiens')
    parser.add_argument('--to_organism', default=None)

    # Add version specification.
    parser.add_argument('--version', default='current',
                        choices=available_versions())

    # Extra options.
    parser.add_argument('--no_cache', dest='cache',
                        default=True, action='store_false')

    return parser


@mapper(name='ensembl', option_func=ensembl_options)
def get_map(from_type, to_type, from_organism='hsapiens', to_organism=None,
            version='current', drop_duplicates='both', drop_na=True,
            cache=True):

    # Check we are actually mapping something.
    if from_type == to_type:
        if (to_organism is None or from_organism == to_organism):
            raise ValueError('Cannot map between same id types '
                             'within the same organism')

    # Get mapping.
    if to_organism is None:
        mapping = _id_map(from_type=from_type, to_type=to_type,
                          version=version, organism=from_organism, cache=cache)
    else:
        mapping = _id_homology_map(from_org=from_organism, to_org=to_organism,
                                   from_type=from_type, to_type=to_type,
                                   version='current', cache=True)
    # Handle NAs.
    if drop_na:
        mapping = mapping.dropna()

    # Handle duplicates.
    mapping = drop_duplicates_(mapping, how=drop_duplicates)

    return mapping


def _id_map(from_type, to_type, version='current',
            organism='hsapiens', cache=True):
    # Try to lookup column as alias.
    from_column = ENSEMBL_ALIASES[version].get(from_type, from_type)
    to_column = ENSEMBL_ALIASES[version].get(to_type, to_type)

    # Get map_frame from Ensembl.
    dataset = pybiomart.Dataset(host=ENSEMBL_HOSTS[version],
                                name=organism + '_gene_ensembl',
                                use_cache=cache)
    map_frame = dataset.query(attributes=[from_column, to_column])

    # Override map names to reflect requested types.
    map_frame.columns = [_format_name(organism, from_type),
                         _format_name(organism, to_type)]

    return _convert_to_str(map_frame)


def _homology_map(from_org, to_org, version='current', cache=True):
    # Determine column names for version.
    from_column = 'ensembl_gene_id'
    to_column = to_org + '_homolog_ensembl_gene'

    # Get map_frame from Ensembl.
    dataset = pybiomart.Dataset(host=ENSEMBL_HOSTS[version],
                                name=from_org + '_gene_ensembl',
                                use_cache=cache)
    map_frame = dataset.query(attributes=[from_column, to_column])

    # Override map names to reflect requested types.
    map_frame.columns = [_format_name(from_org, 'ensembl'),
                         _format_name(to_org, 'ensembl')]

    return _convert_to_str(map_frame)


def _id_homology_map(from_type, to_type, from_org, to_org,
                     version='current', cache=True):

    # Get 'from' map.
    if from_type != 'ensembl':
        from_map = _id_map(from_type=from_type, to_type='ensembl',
                           organism=from_org, version=version, cache=cache)
    else:
        from_map = None

    # Get 'homology' map.
    homology_map = _homology_map(from_org, to_org,
                                 version=version, cache=cache)

    # Get 'to' map.
    if to_type != 'ensembl':
        to_map = _id_map(from_type='ensembl', to_type=to_type,
                         organism=to_org, version=version, cache=cache)
    else:
        to_map = None

    # Join the three maps together.
    if from_map is not None:
        map_frame = pd.merge(from_map, homology_map, how='left',
                             on=_format_name(from_org, 'ensembl'))
    else:
        map_frame = homology_map

    if to_map is not None:
        map_frame = pd.merge(map_frame, to_map, how='left',
                             on=_format_name(to_org, 'ensembl'))

    # Select the to/from columns.
    from_col = _format_name(from_org, from_type)
    to_col = _format_name(to_org, to_type)
    map_frame = map_frame[[from_col, to_col]]

    return map_frame


def _format_name(organism, id_name):
    return '{}_{}'.format(organism, id_name)


def _convert_to_str(df):
    return df.apply(_series_to_str, axis=0)


def _series_to_str(x):
    if issubclass(np.dtype(x).type, np.object_):
        return x
    else:
        return x.apply(_value_to_str)

def _value_to_str(x):
    try:
        return str(int(x))
    except (TypeError, ValueError):
        return np.nan
