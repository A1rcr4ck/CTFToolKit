from rev.elf import ELFParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def elf_header_command(args):

    elf = ELFParser(args.file)
    h = elf.header

    rows = [
        ("Type", h.type),
        ("Machine", h.machine),
        ("Entry", hex(h.entry)),
        ("Program Header Offset", hex(h.phoff)),
        ("Section Header Offset", hex(h.shoff)),
        ("Program Headers", h.phnum),
        ("Section Headers", h.shnum),
    ]

    table = (
        "ELF Header",
        ["Field", "Value"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=h,
    )


def register_elf_header(subparsers):

    parser = subparsers.add_parser(
        "elf-header",
        help="Display ELF header",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=elf_header_command)