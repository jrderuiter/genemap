from __future__ import absolute_import, division, print_function
# pylint: disable=W0622,W0401,W0614
from builtins import *
# pylint: enable=W0622,W0401,W0614

import argparse

from . import map_ids, map_frame


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Setup id argument parser.
    map_ids.add_argparser(subparsers)
    map_frame.add_argparser(subparsers)

    # Parse arguments and dispatch.
    args = parser.parse_args()
    args.main(args)
