
from .. import ensembl


def add_ensembl_options(parser):
    # Add from/to type options.
    parser.add_argument('--from_type', required=True)
    parser.add_argument('--to_type', required=True)

    # Add from/to organism options.
    parser.add_argument('--from_organism', default='hsapiens')
    parser.add_argument('--to_organism', default=None)

    # Add version specification.
    parser.add_argument('--ensembl_version', default='current',
                        choices=ensembl.available_versions())

    # Extra options.
    parser.add_argument('--no_cache', default=False, action='store_true')

    return parser
