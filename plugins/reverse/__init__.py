from .info import register_info
from .hashes import register_hashes
from .entropy import register_entropy
from .strings import register_strings
from .checksec import register_checksec
from .sections import register_sections



def register(subparsers):
    reverse = subparsers.add_parser(
        "reverse",
        help="Reverse engineering utilities"
    )

    reverse_sub = reverse.add_subparsers(
        dest="command",
        required=True
    )

    register_info(reverse_sub)
    register_hashes(reverse_sub)
    register_entropy(reverse_sub)
    register_strings(reverse_sub)
    register_checksec(reverse_sub)
    register_sections(reverse_sub)