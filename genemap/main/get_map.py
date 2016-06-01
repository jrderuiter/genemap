from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

from genemap.mapping import get_map
from genemap.mapping.registry import available_mappers, get_mapper_options


def register(subparsers):
    parser = subparsers.add_parser('get_map')

    mapper_subparser = parser.add_subparsers(dest='mapper')
    mapper_subparser.required = True

    for mapper_name in available_mappers():
        # Create mapper parser.
        mapper_parser = mapper_subparser.add_parser(mapper_name)

        # Add default options.
        mapper_parser.add_argument('--from_type', required=True)
        mapper_parser.add_argument('--to_type', required=True)

        mapper_parser.add_argument('output')

        # Add mapper specific options.
        opt_func = get_mapper_options(mapper_name)
        opt_func(mapper_parser)

    parser.set_defaults(main=main)

    return parser


def main(args):
    # Extract kwargs from args.
    kwargs = {k: v for k, v in vars(args).items()
              if k not in {'main', 'command', 'output'}}

    # Fetch and write mapping.
    mapping = get_map(**kwargs)
    mapping.to_csv(args.output, sep='\t', index=False)
