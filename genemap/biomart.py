from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

import numpy as np

from rpy2.robjects import NA_Logical

from .rpy2 import dataframe_to_pandas, importr

r_biomart_instance = None


def _get_r_biomart():
    global r_biomart_instance
    if r_biomart_instance is None:
        r_biomart_instance = importr('biomaRt')
    return r_biomart_instance


def use_mart(biomart, dataset, host='www.biomart.org',
             path='/biomart/martservice', port=80, verbose=False):
    r_biomart = _get_r_biomart()
    return r_biomart.useMart(biomart=biomart, dataset=dataset, host=host,
                             path=path, port=port, verbose=verbose)


def get_bm(mart, attributes, filters=None, values=None, unique_rows=True):
    if filters is not None or values is not None:
        raise NotImplementedError()

    # Get biomart result and convert to frame.
    r_biomart = _get_r_biomart()
    result = r_biomart.getBM(mart=mart, attributes=attributes,
                             uniqueRows=unique_rows)
    result_frame = dataframe_to_pandas(result)

    # Correct some columns as needed (hacky solution
    # to fix the entrezgene conversion for now).
    result_frame = _cleanup_frame(result, result_frame)

    # Replace any empty strings by NaNs.
    result_frame.replace('', np.nan, inplace=True)

    return result_frame


def _cleanup_frame(result, result_frame):
    if 'entrezgene' in result_frame:
        index = result.names.index('entrezgene')
        result_frame['entrezgene'] = list(map(_convert_na, result[index]))
    return result_frame


def _convert_na(value, convert_func=str, na_value=''):
    if value == NA_Logical:
        return na_value
    return convert_func(value)


def list_datasets(mart):
    r_biomart = _get_r_biomart()
    result = r_biomart.listDatasets(mart)
    return dataframe_to_pandas(result)


def list_attributes(mart):
    r_biomart = _get_r_biomart()
    result = r_biomart.listAttributes(mart)
    return dataframe_to_pandas(result)
