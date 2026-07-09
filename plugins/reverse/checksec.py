from rev.checksec_pe import pe_checksec
from rev.checksec_elf import ELFChecksec
from rev.parser import BinaryParser
from rev.elf import ELFParser
from rev.pe import PEParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def checksec_command(args):

    parser = BinaryParser.open(args.file)

    if isinstance(parser, ELFParser):

        result = ELFChecksec(args.file).result()

        rows = []

        for key, value in result.items():
            rows.append((key, value))

        table = (
            "ELF Checksec",
            ["Mitigation", "Status"],
            rows,
        )

        dispatch(
            args.output,
            table_data=table,
            json_data=result,
        )

    elif isinstance(parser, PEParser):

        result = pe_checksec(args.file)

        rows = []

        for key, value in result.items():

            rows.append(
                (
                    key,
                    "Enabled" if value else "Disabled",
                )
            )

        table = (
            "PE Checksec",
            ["Mitigation", "Status"],
            rows,
        )

        dispatch(
            args.output,
            table_data=table,
            json_data=result,
        )


def register_checksec(subparsers):

    parser = subparsers.add_parser(
        "checksec",
        help="Display binary security mitigations",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=checksec_command)