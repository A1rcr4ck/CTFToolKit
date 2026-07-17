from .hash import register_hash
from .info import register_info
from .strings import register_strings
from .entropy import register_entropy
from .hexdump import register_hexdump
from .filetype import register_filetype
from .exif import register_exif
from .archive import register_archive
from .pcap import register_pcap


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
    register_hexdump(forensic_sub)
    register_filetype(forensic_sub)
    register_exif(forensic_sub)
    register_archive(forensic_sub)
    register_pcap(forensic_sub)