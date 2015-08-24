import argparse
from itertools import chain

from .ensembl import (map_homology, map_ids, get_id_map,
                      get_homology_id_map, list_versions)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Setup id argument parser.
    _add_id_parser(subparsers)
    _add_homology_parser(subparsers)

    # Parse arguments and dispatch.
    args = parser.parse_args()
    args.main(args)


# -- Argument parsers -- #

def _add_id_parser(subparsers):
    id_parser = subparsers.add_parser('id')
    id_parser = _setup_basic_parser(id_parser)

    id_parser.set_defaults(main=_main_id)

    return id_parser


def _add_homology_parser(subparsers):
    hom_parser = subparsers.add_parser('homology')
    hom_parser = _setup_basic_parser(hom_parser)

    hom_parser.add_argument('--from-org', default='hsapiens')
    hom_parser.add_argument('--to-org', default='hsapiens')

    hom_parser.set_defaults(main=_main_homology)

    return hom_parser


def _setup_basic_parser(parser):
    # Add i/o options.
    parser.add_argument('--input', type=argparse.FileType('r'))
    parser.add_argument('--output', default=None)

    # Add from/to type options.
    parser.add_argument('--from-type', default='ensembl')
    parser.add_argument('--to-type', default='ensembl')
    parser.add_argument('--organism', default='hsapiens')

    # Add version specification.
    parser.add_argument('--version', choices=list_versions(),
                        default='current')

    # Add print options.
    parser.add_argument('--as-map', default=False, action='store_true')
    parser.add_argument('--na-value', default='None')

    # Add cache options.
    parser.add_argument('--cache-dir', default='_gm_cache')
    parser.add_argument('--no-cache', default=False, action='store_true')

    # Add gene id list.
    parser.add_argument('gene_id', nargs='+')

    return parser


# -- Main functions -- #

def _main_id(args):
    gene_ids = _get_gene_ids(args)

    if gene_ids is not None:
        # Get id mapping for the passed gene ids.
        mapped = map_ids(
            gene_ids, from_type=args.from_type, to_type=args.to_type,
            organism=args.organism, remove_duplicates='from',
            cache=not args.no_cache, cache_dir=args.cache_dir,
            version=args.version)

        if args.as_map:
            # Print as map (from --> to).
            _print_map(mapped.reset_index(), file_path=args.output,
                       na_value=args.na_value)
        else:
            # Only print the mapped ids.
            _print_ids(mapped, file_path=args.output, na_value=args.na_value)
    else:
        # Get and print the entire gene map.
        mapped = get_id_map(from_type=args.from_type, to_type=args.to_type,
                            version=args.version, organism=args.organism,
                            cache=not args.no_cache, cache_dir=args.cache_dir)
        _print_map(mapped, file_path=args.output, na_value=args.na_value)


def _main_homology(args):
    gene_ids = _get_gene_ids(args)

    if gene_ids is not None:
        # Get id mapping for the passed gene ids.
        mapped = map_homology(
            args.gene_id, from_type=args.from_type, to_type=args.to_type,
            from_org=args.from_org, to_org=args.to_org, remove_duplicates='from',
            cache=not args.no_cache, cache_dir=args.cache_dir,
            version=args.version)

        if args.as_map:
            # Print as map (from --> to).
            _print_map(mapped.reset_index(), file_path=args.output,
                       na_value=args.na_value)
        else:
            # Only print the mapped ids.
            _print_ids(mapped, file_path=args.output, na_value=args.na_value)
    else:
        # Get and print the entire gene map.
        mapped = get_homology_id_map(
            from_org=args.from_org, to_org=args.to_org,
            from_type=args.from_type, to_type=args.to_type,
            version=args.version,
            cache=not args.no_cache, cache_dir=args.cache_dir)
        _print_map(mapped, file_path=args.output, na_value=args.na_value)


# -- Support functions -- #

def _get_gene_ids(args):
    if args.input is not None:
        input_lines = (line.strip() for line in args.input.readlines())
        gene_ids = list(chain.from_iterable((l.split() for l in input_lines)))
    elif len(args.gene_id) > 0:
        gene_ids = args.gene_id
    else:
        gene_ids = None

    return gene_ids


def _print_map(map_frame, file_path=None, na_value='None'):
    map_frame = map_frame.fillna(na_value)

    if file_path is not None:
        map_frame.to_csv(file_path, sep='\t', index=False)
    else:
        print('\t'.join(map_frame.columns))
        for _, row in map_frame.iterrows():
            print('\t'.join(row))


def _print_ids(map_series, file_path=None, na_value='None'):
    map_series = map_series.fillna(na_value)

    if file_path is not None:
        map_series.to_csv(file_path, sep='\t', index=False, header=False)
    else:
        print('\n'.join(map_series))
