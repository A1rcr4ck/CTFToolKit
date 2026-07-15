from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from forensic.hexdump import FileHexDump


def hexdump_command(args):

    rows = FileHexDump(args.file).dump(
        offset=args.offset,
        size=args.size,
    )

    table = (
        "Hexdump",
        ["Offset", "Hex", "ASCII"],
        [
            (
                hex(row["offset"]),
                row["hex"],
                row["ascii"],
            )
            for row in rows
        ],
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=rows,
    )


def register_hexdump(subparsers):

    parser = subparsers.add_parser(
        "hexdump",
        help="Display hexadecimal dump",
    )

    parser.add_argument(
        "file",
        help="Input file",
    )

    parser.add_argument(
        "--offset",
        type=lambda x: int(x, 0),
        default=0,
        help="Start offset",
    )

    parser.add_argument(
        "--size",
        type=int,
        default=256,
        help="Bytes to display",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=hexdump_command,
    )