from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

import pandas as pd

# pylint: disable=E0401
from ..mapping import map_frame
from .map_ids import add_ensembl_options
# pylint: enable=E0401


def add_argparser(subparsers):
    parser = subparsers.add_parser('map_frame')

    # Add default options.
    add_ensembl_options(parser)

    # Add i/o options.
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default=None)

    parser.set_defaults(main=main)

    return parser

def main(args):
    # Read frame.
    df = pd.read_csv(args.input, sep='\t', comment='#', index_col=0)

    mapped = map_frame(df, from_type=args.from_type, to_type=args.to_type,
                       from_org=args.from_organism, to_org=args.to_organism,
                       drop_duplicates='from', cache=not args.no_cache,
                       version=args.ensembl_version)

    mapped.to_csv(args.output, sep='\t', index=True)
