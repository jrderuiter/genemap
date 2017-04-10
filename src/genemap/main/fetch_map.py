# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from genemap.mappers import get_mappers


def main(args):
    """Main function."""

    mapper = args.mapper.from_args(args)
    mapper.mapping.to_csv(str(args.output), sep='\t', index=False)


def configure_subparser(subparser):
    """Configures subparser for subcommand."""

    parser = subparser.add_parser('fetch_map')
    parser.set_defaults(main=main)

    mapper_subparser = parser.add_subparsers(dest='mapper')
    mapper_subparser.required = True

    for name, class_ in get_mappers().items():
        mapper_parser = mapper_subparser.add_parser(name)
        class_.configure_parser(mapper_parser)
        mapper_parser.add_argument('output')
        mapper_parser.set_defaults(mapper=class_)
