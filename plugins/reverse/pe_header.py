from rev.pe import PEParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def pe_header_command(args):

    pe = PEParser(args.file)
    h = pe.header

    rows = [
        ("Machine", h.machine),
        ("Timestamp", h.timestamp),
        ("Sections", h.sections),
        ("Entrypoint", hex(h.entrypoint)),
        ("Image Base", hex(h.imagebase)),
        ("Subsystem", h.subsystem),
        ("DLL", h.dll),
    ]

    table = (
        "PE Header",
        ["Field", "Value"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=h,
    )


def register_pe_header(subparsers):

    parser = subparsers.add_parser(
        "pe-header",
        help="Display PE header",
    )

    parser.add_argument(
        "file",
        help="Input PE binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=pe_header_command)