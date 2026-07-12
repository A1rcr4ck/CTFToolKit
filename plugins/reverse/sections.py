from rev.parser import BinaryParser
from rev.elf import ELFParser
from rev.pe import PEParser

from core.command import BaseCommand
from core.cli import add_output_argument


class SectionsCommand(BaseCommand):

    def __init__(self, path):

        self.parser = BinaryParser.open(path)

    def build_table(self):

        if isinstance(self.parser, ELFParser):

            rows = []

            for section in self.parser.section_headers:

                rows.append(
                    (
                        section.name,
                        section.type,
                        hex(section.address),
                        str(section.size),
                    )
                )

            return (
                "ELF Sections",
                ["Name", "Type", "Address", "Size"],
                rows,
            )

        rows = []

        for section in self.parser.sections:

            rows.append(
                (
                    section.name,
                    hex(section.virtual_address),
                    str(section.raw_size),
                    f"{section.entropy:.2f}",
                )
            )

        return (
            "PE Sections",
            ["Name", "VA", "Raw Size", "Entropy"],
            rows,
        )

    def build_json(self):

        if isinstance(self.parser, ELFParser):
            return self.parser.section_headers

        return self.parser.sections


def sections_command(args):

    SectionsCommand(args.file).run(args.output)

def register_sections(subparsers):

    parser = subparsers.add_parser(
        "sections",
        help="Display binary sections",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=sections_command)