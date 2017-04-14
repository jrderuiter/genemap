# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from genemap.mappers import get_mappers


def main(args):
    """Main function."""

    mapper = args.mapper.from_args(args)
    mapped = mapper.map_ids(args.ids)

    print(' '.join(mapped))


def configure_subparser(subparser):
    """Configures subparser for subcommand."""

    parser = subparser.add_parser('map_ids')
    parser.set_defaults(main=main)

    mapper_subparser = parser.add_subparsers(dest='mapper')
    mapper_subparser.required = True

    mappers = get_mappers(with_command_line=True).items()

    for name, class_ in mappers:
        mapper_parser = mapper_subparser.add_parser(name)
        class_.configure_parser(mapper_parser)
        mapper_parser.add_argument('ids', nargs='+')
        mapper_parser.set_defaults(mapper=class_)
