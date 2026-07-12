from rev.pe import PEParser

from core.command import BaseCommand
from core.cli import add_output_argument


class ExportsCommand(BaseCommand):

    def __init__(self, path):

        self.pe = PEParser(path)

    def build_table(self):

        rows = []

        for export in self.pe.exports:

            rows.append(
                (
                    export.ordinal,
                    hex(export.address),
                    export.name,
                )
            )

        return (
            "PE Exports",
            ["Ordinal", "Address", "Name"],
            rows,
        )

    def build_json(self):

        return self.pe.exports


def exports_command(args):

    ExportsCommand(args.file).run(args.output)


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