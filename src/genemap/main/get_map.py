# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from genemap.mappers import get_mappers


def main(args):
    mapper = args.mapper.from_args(args)

    mapping = mapper.get_map(
        from_type=args.from_type,
        to_type=args.to_type,
        drop_duplicates=args.drop_duplicates,
        drop_na=not args.keep_na)

    mapping.to_csv(str(args.output), sep='\t', index=False)


def register(subparsers):
    parser = subparsers.add_parser('get_map')

    subparser = parser.add_subparsers(dest='mapper')
    subparser.required = True

    for name, class_ in get_mappers().items():
        # Create mapper parser.
        mapper_parser = subparser.add_parser(name)

        # Add default options.
        mapper_parser.add_argument('--from_type', required=True)
        mapper_parser.add_argument('--to_type', required=True)

        mapper_parser.add_argument(
            '--drop_duplicates',
            default='both',
            choices=['both', 'from', 'none'])
        mapper_parser.add_argument(
            '--keep_na', default=False, action='store_true')

        mapper_parser.add_argument('output')

        # Add mapper specific options.
        class_.configure_args(mapper_parser)
        mapper_parser.set_defaults(mapper=class_)

    parser.set_defaults(main=main)

    return parser
