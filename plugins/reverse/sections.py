from core.output.dispatcher import dispatch
from rev.parser import BinaryParser
from rev.elf import ELFParser
from rev.pe import PEParser
from core.output import print_table
from core.cli import add_output_argument


def sections_command(args):

    parser = BinaryParser.open(args.file)

    if isinstance(parser, ELFParser):

        rows = []

        for section in parser.section_headers:

            rows.append(
                (
                    section.name,
                    section.type,
                    hex(section.address),
                    str(section.size),
                )
            )

        table = (
            "ELF Sections",
            ["Name", "Type", "Address", "Size"],
            rows,
        )

        dispatch(
            args.output,
            table_data=table,
            json_data=parser.section_headers,
        )

    elif isinstance(parser, PEParser):

        rows = []

        for section in parser.sections:

            rows.append(
                (
                    section.name,
                    hex(section.virtual_address),
                    str(section.raw_size),
                    f"{section.entropy:.2f}",
                )
            )

        table = (
            "PE Sections",
            ["Name", "Virtual Address", "Raw Size", "Entropy"],
            rows,
        )

        dispatch(
            args.output,
            table_data=table,
            json_data=parser.section_headers,
        )

    else:

        print("Unsupported binary.")

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