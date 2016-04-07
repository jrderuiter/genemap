from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

import argparse
from itertools import chain

# pylint: disable=E0401,W0406
from ..mapping import map_ids
from ._base import add_ensembl_options
# pylint: enable=E0401


def add_argparser(subparsers):
    parser = subparsers.add_parser('map_ids')

    # Add default options.
    add_ensembl_options(parser)

    # Add i/o options.
    parser.add_argument('--input', type=argparse.FileType('r'))
    parser.add_argument('--output', default=None)

    # Add gene id list.
    parser.add_argument('gene_id', nargs='*')

    # Option to print as map.
    parser.add_argument('--as_map', default=False, action='store_true')

    parser.set_defaults(main=main)

    return parser

def main(args):
    # Try to get gene ids.
    try:
        gene_ids = _get_gene_ids(args)
    except ValueError:
        raise ValueError('Either --input or gene_ids options must be provided')

    # Perform the actual mapping.
    mapped = map_ids(gene_ids, from_type=args.from_type, to_type=args.to_type,
                     from_org=args.from_organism, to_org=args.to_organism,
                     drop_duplicates='from', cache=not args.no_cache,
                     version=args.ensembl_version, as_series=True)

    if args.as_map:
        # Print as map (from --> to).
        _print_map(mapped.reset_index(), file_path=args.output)
    else:
        # Only print the mapped ids.
        _print_ids(mapped, file_path=args.output)


def _get_gene_ids(args):
    if args.input is not None:
        input_lines = (line.strip() for line in args.input.readlines())
        gene_ids = list(chain.from_iterable((l.split() for l in input_lines)))
    elif len(args.gene_id) > 0:
        gene_ids = args.gene_id
    else:
        raise ValueError('No gene ids')

    return gene_ids


def _print_map(mapping, file_path=None, na_value='None'):
    mapping = mapping.fillna(na_value)

    if file_path is not None:
        mapping.to_csv(file_path, sep='\t', index=False)
    else:
        print('\t'.join(mapping.columns))
        for _, row in mapping.iterrows():
            print('\t'.join(row))


def _print_ids(map_series, file_path=None, na_value='None'):
    map_series = map_series.fillna(na_value)

    if file_path is not None:
        map_series.to_csv(file_path, sep='\t', index=False, header=False)
    else:
        print('\n'.join(map_series))
