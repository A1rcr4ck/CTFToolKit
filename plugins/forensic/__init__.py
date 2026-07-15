from .hash import register_hash
from .info import register_info
from .strings import register_strings
from .entropy import register_entropy


def register(subparsers):

    forensic = subparsers.add_parser(
        "forensic",
        help="Forensics Toolkit",
    )

    forensic_sub = forensic.add_subparsers(
        dest="command",
        required=True,
    )

    register_hash(forensic_sub)
    register_info(forensic_sub)
    register_strings(forensic_sub)
    register_entropy(forensic_sub)