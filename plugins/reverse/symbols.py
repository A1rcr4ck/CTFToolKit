from rev.elf import ELFParser

from core.command import BaseCommand
from core.cli import add_output_argument


class SymbolsCommand(BaseCommand):

    def __init__(self, path):

        self.elf = ELFParser(path)

    def build_table(self):

        rows = []

        for sym in self.elf.symbols:

            rows.append(
                (
                    hex(sym.value),
                    str(sym.size),
                    sym.bind,
                    sym.type,
                    sym.name,
                )
            )

        return (
            "ELF Symbols",
            ["Value", "Size", "Bind", "Type", "Name"],
            rows,
        )

    def build_json(self):

        return self.elf.symbols


def symbols_command(args):

    SymbolsCommand(args.file).run(args.output)


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