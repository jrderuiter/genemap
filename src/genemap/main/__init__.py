# -*- coding: utf-8 -*-

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from __future__ import absolute_import, division, print_function
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import argparse
import logging

from . import get_map


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Setup id argument parser.
    get_map.register(subparsers)

    # Parse arguments and dispatch.
    args = parser.parse_args()
    args.main(args)
