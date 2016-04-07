from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

# pylint: disable=E0401,W0406
from ..mapping import get_map
from ._base import add_ensembl_options
# pylint: enable=E0401


def add_argparser(subparsers):
    parser = subparsers.add_parser('get_map')

    # Add default options.
    add_ensembl_options(parser)

    # Add i/o options.
    parser.add_argument('output')

    parser.set_defaults(main=main)

    return parser


def main(args):
    # Get the mapping
    mapping = get_map(from_type=args.from_type, to_type=args.to_type,
                       from_org=args.from_organism, to_org=args.to_organism,
                       drop_duplicates='from', cache=not args.no_cache,
                       version=args.ensembl_version)

    # Write mapping.
    mapping.to_csv(args.output, sep='\t', index=False)
