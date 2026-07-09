from rev.elf import ELFParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def symbols_command(args):

    elf = ELFParser(args.file)

    rows = []

    for sym in elf.symbols:

        rows.append(
            (
                hex(sym.value),
                str(sym.size),
                sym.bind,
                sym.type,
                sym.name,
            )
        )

    table = (
        "ELF Symbols",
        ["Value", "Size", "Bind", "Type", "Name"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=elf.symbols,
    )


def register_symbols(subparsers):

    parser = subparsers.add_parser(
        "symbols",
        help="Display ELF symbols",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=symbols_command)