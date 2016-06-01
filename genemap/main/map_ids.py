from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

import argparse
from itertools import chain

from genemap.mapping import map_ids
from genemap.mapping.registry import available_mappers, get_mapper_options


def register(subparsers):
    parser = subparsers.add_parser('map_ids')
    
    mapper_subparser = parser.add_subparsers(dest='mapper')
    mapper_subparser.required = True

    for mapper_name in available_mappers():
        # Create mapper parser.
        mapper_parser = mapper_subparser.add_parser(mapper_name)

        # Add default options.
        mapper_parser.add_argument('--from_type', required=True)
        mapper_parser.add_argument('--to_type', required=True)

        # Add i/o options.
        mapper_parser.add_argument('--input', type=argparse.FileType('r'))
        mapper_parser.add_argument('--output', default=None)

        # Add gene id list.
        mapper_parser.add_argument('gene_id', nargs='*')

        # Option to print as map.
        mapper_parser.add_argument('--as_map', default=False,
                                   action='store_true')

        # Add mapper specific options.
        opt_func = get_mapper_options(mapper_name)
        opt_func(mapper_parser)

    parser.set_defaults(main=main)

    return parser


def main(args):
    # Try to get gene ids from arguments.
    try:
        gene_ids = _get_gene_ids(args)
    except ValueError:
        raise ValueError('Either --input or gene_ids options must be provided')

    # Extract kwargs from args.
    kwargs = {k: v for k, v in vars(args).items()
              if k not in {'main', 'command', 'input', 'output',
                           'gene_id', 'as_map'}}

    # Perform the actual mapping.
    mapped = map_ids(gene_ids, as_series=True, **kwargs)

    # Print/write output.
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
