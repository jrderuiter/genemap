# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *

# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pandas as pd
import requests
import requests_cache

from .base import Mapper, CommandLineMixin, register_mapper

MAP_IDS = {'symbol', 'entrez'}
MAP_URL = 'http://www.informatics.jax.org/downloads/reports/HOM_AllOrganism.rpt'

MAP_DTYPES = {
    'HomoloGene ID': 'str',
    'Common Organism Name': 'str',
    'Symbol': 'str',
    'EntrezGene ID': 'str'
}

requests_cache.install_cache('.genemap')


class MgiMapper(CommandLineMixin, Mapper):
    """MGI mapper class.

    Maps IDs using the homology table provided by MGI. Supports mapping between
    gene symbols and Entrez identifers and between several specifies
    (using orthologous genes).

    Parameters
    ----------
    from_type : str
        The source identifier type. Can be either 'symbol' or 'entrez'.
    to_type : str
        The target identifier type (see ``from_type`` for more details).
    drop_duplicates : str
        How to handle duplicates. If 'both', then entries with duplicates in
        either the source/target columns are dropped from the mapping. If
        'mto' (many-to-one), then only duplicates in the source column are
        dropped. If 'otm', then only duplicates in the target column are
        dropped. Finally, if 'none', no duplicates are removed from the mapping.
    from_organism : str
        Name of the source organism.
    to_organism : str
        Name of the target organism. If not given, no mapping between
        organisms is performed.
    map_url : str
        The URL to use to fetch the mapping table from MGI.

    """

    def __init__(self,
                 from_type,
                 to_type,
                 drop_duplicates='both',
                 from_organism='mouse',
                 to_organism=None,
                 map_url=MAP_URL):
        super().__init__(drop_duplicates=drop_duplicates)

        if from_type == to_type and (from_organism == to_organism or
                                     to_organism is None):
            raise ValueError('Cannot map between identical identifier types '
                             'within the same organism')

        self._from_type = from_type
        self._to_type = to_type

        self._from_organism = from_organism
        self._to_organism = to_organism

        self._map_url = map_url

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('--from_type', required=True, choices=MAP_IDS)
        parser.add_argument('--to_type', required=True, choices=MAP_IDS)
        parser.add_argument('--from_organism', default='mouse')
        parser.add_argument('--to_organism', default=None)
        parser.add_argument('--drop_duplicates', default='both')
        parser.add_argument('--map_url', default=MAP_URL)

    @classmethod
    def from_args(cls, args):
        return cls(from_type=args.from_type,
                   to_type=args.to_type,
                   from_organism=args.from_organism,
                   to_organism=args.to_organism,
                   drop_duplicates=args.drop_duplicates,
                   map_url=args.map_url)

    def _fetch_mapping(self):
        # Fetch and read MGI data.
        req = requests.get(self._map_url)
        data = pd.read_csv(StringIO(req.text), sep='\t', dtype=MAP_DTYPES)

        # Subset and tidy column names.
        column_map = {
            'HomoloGene ID': 'id',
            'Common Organism Name': 'organism',
            'Symbol': 'symbol',
            'EntrezGene ID': 'entrez'
        }

        data = data[list(column_map.keys())].rename(columns=column_map)

        # Extract main organism name (before comma).
        data['organism'] = data['organism'].str.extract(
            r'(\w+),?', expand=False)

        data['entrez'] = data['entrez'].astype(str)

        # Check if organisms are known.
        organisms = set(data['organism'])
        if self._from_organism not in organisms:
            raise ValueError('Unknown from organism {}'.format(
                self._from_organism))

        if self._to_organism is not None:
            if self._to_organism not in organisms:
                raise ValueError('Unknown to organism {}'.format(
                    self._to_organism))

            # Extract rows belong to each organism.
            from_data = data.loc[data['organism'] == self._from_organism]
            to_data = data.loc[data['organism'] == self._to_organism]

            # Merge into single frame based on the 'HomoloGene ID'.
            suffixes = ['_' + self._from_organism, '_' + self._to_organism]
            mapping = pd.merge(
                from_data, to_data, on='id', how='inner', suffixes=suffixes)

            # Extract relevant columns.
            mapping = mapping[[
                self._from_type + '_' + self._from_organism,
                self._to_type + '_' + self._to_organism
            ]]
        else:
            # Extract rows/columns belonging to organisms + types.
            mapping = data.loc[data['organism'] == self._from_organism,
                               [self._from_type, self._to_type]]

        return mapping


register_mapper('mgi', MgiMapper)
