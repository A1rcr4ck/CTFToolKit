from rev.pe import PEParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def exports_command(args):

    pe = PEParser(args.file)

    if not pe.exports:
        print("No exports found.")
        return

    rows = []

    for export in pe.exports:

        rows.append(
            (
                export.ordinal,
                hex(export.address),
                export.name,
            )
        )

    table = (
        "PE Exports",
        ["Ordinal", "Address", "Name"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=pe.exports,
    )


def register_exports(subparsers):

    parser = subparsers.add_parser(
        "exports",
        help="Display exported functions",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=exports_command)