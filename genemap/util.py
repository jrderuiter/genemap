from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

from functools import reduce


def drop_duplicates(mapping, how='from'):
    # Determine which columns to consider for duplicates.
    if how == 'none':
        return mapping
    if how == 'from':
        columns = [mapping.columns[0]]
    elif how == 'both':
        columns = [mapping.columns[0], mapping.columns[1]]
    else:
        raise ValueError(('Unknown value for from ({}), '
                          'should be either "from" or "both"').format(how))
    # Apply column masks.
    masks = [_duplicate_mask(mapping, c) for c in columns]
    mask = reduce(lambda m1, m2: m1 | m2, masks)
    masked_mapping = mapping.ix[~mask]

    return masked_mapping


def _duplicate_mask(frame, column):
    duplicate_rows = frame.duplicated(subset=column)
    duplicate_values = set(frame.ix[duplicate_rows][column])
    return frame[column].isin(duplicate_values)
