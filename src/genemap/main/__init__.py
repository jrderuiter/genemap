"""Dispatcher script that redirects calls to subcommands.

This script allows users to call subcommands from a single binary
(``imfusion build ...`` instead of ``imfusion-build`` by redirecting calls to
to the appropriate subcommands.

"""

import argparse

from . import map_ids, map_dataframe, fetch_mapping


def main():
    """Main function, parses the subcommand and executes the right script."""

    # Setup main parser + subparser.
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='subcommand')
    subparser.required = True

    # Configure subcommands.
    map_ids.configure_subparser(subparser)
    map_dataframe.configure_subparser(subparser)
    fetch_mapping.configure_subparser(subparser)

    # Distpatch.
    args = parser.parse_args()
    args.main(args)


if __name__ == '__main__':
    main()
