from rev.elf import ELFParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def relocations_command(args):

    elf = ELFParser(args.file)

    if not elf.relocations:
        print("No relocations found.")
        return

    rows = []

    for rel in elf.relocations:

        rows.append(
            (
                hex(rel.offset),
                rel.type,
                rel.symbol,
                hex(rel.addend)
                if rel.addend is not None
                else "-",
            )
        )

    table = (
        "ELF Relocations",
        ["Offset", "Type", "Symbol", "Addend"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=elf.relocations,
    )


def register_relocations(subparsers):

    parser = subparsers.add_parser(
        "relocations",
        help="Display ELF relocations",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=relocations_command)