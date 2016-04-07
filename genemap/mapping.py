from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

import pandas as pd

# pylint: disable=E0401
from . import ensembl
# pylint: enable=E0401


def map_ids(ids, from_type, to_type, as_series=False, **kwargs):
    # Fetch mapping.
    mapping = get_map(from_type, to_type, **kwargs)
    mapping = mapping.set_index(mapping.columns[0])[mapping.columns[1]]

    # Lookup ids.
    mapped = mapping.ix[ids]

    if not as_series:
        # Convert to list.
        mapped = mapped.where((pd.notnull(mapped)), None)
        mapped = list(mapped)

    return mapped


def map_frame(df, from_type, to_type, **kwargs):
    # Fetch mapping.
    mapping = get_map(from_type, to_type, **kwargs)
    mapping = mapping.set_index(mapping.columns[0])[mapping.columns[1]]

    # Subset mapping for input frame and drop missing entries.
    mapping = mapping.ix[df.index]
    mapping.dropna(inplace=True)

    # Apply mapping to frame.
    mapped = df.ix[mapping.index].copy()
    mapped.index = mapping

    return mapped


def get_map(from_type, to_type, **kwargs):
    return ensembl.get_map(from_type=from_type, to_type=to_type, **kwargs)
