# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import pandas as pd

from genemap.mappers import get_mappers


def main(args):
    """Main function."""

    mapper = args.mapper.from_args(args)

    frame = pd.read_csv(args.input, sep='\t', comment='#', index_col=0)
    mapped = mapper.map_dataframe(frame)

    mapped.to_csv(args.output, sep='\t', index=True)


def configure_subparser(subparser):
    """Configures subparser for subcommand."""

    parser = subparser.add_parser('map_frame')
    parser.set_defaults(main=main)

    mapper_subparser = parser.add_subparsers(dest='mapper')
    mapper_subparser.required = True

    for name, class_ in get_mappers().items():
        mapper_parser = mapper_subparser.add_parser(name)
        class_.configure_parser(mapper_parser)

        mapper_parser.add_argument('input')
        mapper_parser.add_argument('output')

        mapper_parser.set_defaults(mapper=class_)
