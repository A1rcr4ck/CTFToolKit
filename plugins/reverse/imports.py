from rev.elf import ELFParser
from rev.pe import PEParser
from rev.parser import BinaryParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def imports_command(args):

    parser = BinaryParser.open(args.file)

    if isinstance(parser, PEParser):

        rows = []

        for imp in parser.imports:
            rows.append(
                (
                    imp.dll,
                    imp.name,
                )
            )

        table = (
            "PE Imports",
            ["DLL", "Function"],
            rows,
        )

        dispatch(
            args.output,
            table_data=table,
            json_data=parser.imports,
        )

    elif isinstance(parser, ELFParser):

        rows = []

        for sym in parser.symbols:

            if sym.section == 0 and sym.name:

                rows.append(
                    (
                        sym.name,
                        sym.type,
                        sym.bind,
                    )
                )

        table = (
            "ELF Imports",
            ["Name", "Type", "Bind"],
            rows,
        )

        dispatch(
            args.output,
            table_data=table,
            json_data=rows,
        )


def register_imports(subparsers):

    parser = subparsers.add_parser(
        "imports",
        help="Display imported functions",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=imports_command)