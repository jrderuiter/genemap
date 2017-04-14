# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import numpy as np
import pandas as pd
import pybiomart

from .base import Mapper, CommandLineMixin, register_mapper

ID_ALIASES = {
    'symbol': 'external_gene_name',
    'entrez': 'entrezgene',
    'ensembl': 'ensembl_gene_id'
}


class EnsemblMapper(CommandLineMixin, Mapper):
    """Ensembl mapper class."""

    # 80: 'may2015.archive.ensembl.org', Empty datasets?
    # '79': 'mar2015.archive.ensembl.org',
    # '78': 'dec2014.archive.ensembl.org',
    # '77': 'oct2014.archive.ensembl.org',
    # '76': 'aug2014.archive.ensembl.org',
    # '75': 'feb2014.archive.ensembl.org',
    # '74': 'dec2013.archive.ensembl.org',
    # '67': 'may2012.archive.ensembl.org'

    # ID_ALIASES_PRE_76 = dict(ID_ALIASES)
    # ID_ALIASES_PRE_76.update({'symbol': 'external_gene_id'})

    def __init__(self,
                 from_type,
                 to_type,
                 drop_duplicates='both',
                 from_organism='hsapiens',
                 to_organism=None,
                 host='http://ensembl.org',
                 drop_lrg=True):
        super().__init__(drop_duplicates=drop_duplicates)

        self._from_type = from_type
        self._to_type = to_type

        self._from_organism = from_organism
        self._to_organism = to_organism
        self._host = host
        self._drop_lrg = drop_lrg

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('--from_organism', default='hsapiens')
        parser.add_argument('--to_organism', default=None)
        parser.add_argument('--host', default='ensembl.org')

    @classmethod
    def from_args(cls, args):
        return cls(from_type=args.from_type,
                   to_type=args.to_type,
                   from_organism=args.from_organism,
                   to_organism=args.to_organism,
                   host=args.host)

    def _fetch_mapping(self):
        mapping = _fetch_map(
            self._from_type,
            self._to_type,
            from_organism=self._from_organism,
            to_organism=self._to_organism,
            host=self._host,
            drop_lrg=self._drop_lrg)

        return mapping

    def available_aliases(self):
        """ Return the available aliases for gene ids.

        Returns:
            Dict[str,str]: Dict of aliases.

        """
        return dict(ID_ALIASES)


register_mapper('ensembl', EnsemblMapper)


def _fetch_map(from_type,
               to_type,
               host,
               from_organism='hsapiens',
               to_organism=None,
               cache=True,
               drop_lrg=True):
    """Fetches ensembl map."""

    # Check we are actually mapping something.
    if from_type == to_type:
        if to_organism is None or from_organism == to_organism:
            raise ValueError('Cannot map between same id types '
                             'within the same organism')

    # Get mapping.
    if to_organism is None:
        mapping = _id_map(
            from_type=from_type,
            to_type=to_type,
            host=host,
            organism=from_organism,
            cache=cache)
    else:
        mapping = _id_homology_map(
            from_org=from_organism,
            to_org=to_organism,
            from_type=from_type,
            to_type=to_type,
            host=host,
            cache=True)

    mapping = mapping.dropna()

    # Hacky fix to avoid pulling along LRG entries together with the
    # ENSEMBL ids, which we aren't interested in.
    if to_type == 'ensembl' and drop_lrg:
        mask = mapping[mapping.columns[1]].str.startswith('LRG_')
        mapping = mapping.loc[~mask]
    elif from_type == 'ensembl' and drop_lrg:
        mask = mapping[mapping.columns[0]].str.startswith('LRG_')
        mapping = mapping.loc[~mask]

    return mapping


def _id_map(from_type, to_type, host, organism='hsapiens', cache=True):
    # Try to lookup column as alias.
    from_column = ID_ALIASES.get(from_type, from_type)
    to_column = ID_ALIASES.get(to_type, to_type)

    # Get map_frame from Ensembl.
    dataset = pybiomart.Dataset(
        host=host, name=organism + '_gene_ensembl', use_cache=cache)

    map_frame = dataset.query(attributes=[from_column, to_column])

    # Override map names to reflect requested types.
    map_frame.columns = [
        _format_name(organism, from_type), _format_name(organism, to_type)
    ]

    return _convert_to_str(map_frame)


def _homology_map(from_org, to_org, host, cache=True):
    # Determine column names for version.
    from_column = 'ensembl_gene_id'
    to_column = to_org + '_homolog_ensembl_gene'

    # Get map_frame from Ensembl.
    dataset = pybiomart.Dataset(
        host=host, name=from_org + '_gene_ensembl', use_cache=cache)
    map_frame = dataset.query(attributes=[from_column, to_column])

    # Override map names to reflect requested types.
    map_frame.columns = [
        _format_name(from_org, 'ensembl'), _format_name(to_org, 'ensembl')
    ]

    return _convert_to_str(map_frame)


def _id_homology_map(from_type, to_type, from_org, to_org, host, cache=True):

    # Get 'from' map.
    if from_type != 'ensembl':
        from_map = _id_map(
            from_type=from_type,
            to_type='ensembl',
            organism=from_org,
            host=host,
            cache=cache)
    else:
        from_map = None

    # Get 'homology' map.
    homology_map = _homology_map(from_org, to_org, host=host, cache=cache)

    # Get 'to' map.
    if to_type != 'ensembl':
        to_map = _id_map(
            from_type='ensembl',
            to_type=to_type,
            organism=to_org,
            host=host,
            cache=cache)
    else:
        to_map = None

    # Join the three maps together.
    if from_map is not None:
        map_frame = pd.merge(
            from_map,
            homology_map,
            how='left',
            on=_format_name(from_org, 'ensembl'))
    else:
        map_frame = homology_map

    if to_map is not None:
        map_frame = pd.merge(
            map_frame, to_map, how='left', on=_format_name(to_org, 'ensembl'))

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
