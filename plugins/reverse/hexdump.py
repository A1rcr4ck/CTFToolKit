from rev.parser import BinaryParser
from rev.reader import BinaryReader
from rev.hexdump import HexDump

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def hexdump_command(args):

    parser = BinaryParser.open(args.file)

    reader = BinaryReader(parser.memory)

    if args.section:

        region = reader.region(args.section)

        if region is None:
            print(f"Section '{args.section}' not found.")
            return

        address = region.virtual_address

    else:

        address = args.address

    rows = HexDump(reader).dump(
        address,
        args.size,
    )

    table = (
        "Hexdump",
        ["Address", "Hex", "ASCII"],
        [
            (
                hex(addr),
                hex_bytes,
                ascii_bytes,
            )
            for addr, hex_bytes, ascii_bytes in rows
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
        help="Hex dump memory",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--section",
        help="Section name",
    )

    group.add_argument(
        "--address",
        type=lambda x: int(x, 0),
        help="Virtual address",
    )

    parser.add_argument(
        "--size",
        type=int,
        default=128,
        help="Bytes to dump",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=hexdump_command,
    )