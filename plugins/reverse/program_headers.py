from rev.elf import ELFParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def program_headers_command(args):

    elf = ELFParser(args.file)

    rows = []

    for ph in elf.program_headers:

        rows.append(
            (
                ph.type,
                hex(ph.offset),
                hex(ph.vaddr),
                str(ph.filesz),
                str(ph.memsz),
                hex(ph.flags),
            )
        )

    table = (
        "ELF Program Headers",
        ["Type", "Offset", "VAddr", "FileSz", "MemSz", "Flags"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=elf.program_headers,
    )


def register_program_headers(subparsers):

    parser = subparsers.add_parser(
        "program-headers",
        help="Display ELF program headers",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=program_headers_command)