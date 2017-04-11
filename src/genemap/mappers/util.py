# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from functools import reduce


def drop_duplicates(mapping, how='both'):
    # Determine which columns to consider for duplicates.
    if how == 'none':
        return mapping
    if how == 'otm':
        columns = [mapping.columns[0]]
    elif how == 'mto':
        columns = [mapping.columns[1]]
    elif how == 'both':
        columns = [mapping.columns[0], mapping.columns[1]]
    else:
        raise ValueError(('Unknown value for how ({}). Possible values are '
                          '\'none\', \'otm\' (one-to-many), \'mto\' '
                          '(many-to-one) or \'both\'').format(how))

    # Apply column masks.
    masks = [_duplicate_mask(mapping, c) for c in columns]
    mask = reduce(lambda m1, m2: m1 | m2, masks)
    masked_mapping = mapping.ix[~mask]

    return masked_mapping


def _duplicate_mask(frame, column):
    duplicate_rows = frame.duplicated(subset=column)
    duplicate_values = set(frame.ix[duplicate_rows][column])
    return frame[column].isin(duplicate_values)
