from rev.parser import BinaryParser
from rev.search import InstructionSearcher

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def search_command(args):

    parser = BinaryParser.open(args.file)

    search = InstructionSearcher(parser)

    if args.mnemonic:

        rows = search.mnemonic(
            section=args.section,
            mnemonic=args.mnemonic,
        )

    else:

        rows = search.operand(
            section=args.section,
            text=args.operand,
        )

    table = (
        "Instruction Search",
        [
            "Address",
            "Bytes",
            "Mnemonic",
            "Operands",
        ],
        [
            (
                hex(ins.address),
                ins.bytes.hex(" "),
                ins.mnemonic,
                ins.operands,
            )
            for ins in rows
        ],
    )

    json_data = [
        {
            "address": hex(ins.address),
            "bytes": ins.bytes.hex(" "),
            "mnemonic": ins.mnemonic,
            "operands": ins.operands,
        }
        for ins in rows
    ]

    dispatch(
        args.output,
        table_data=table,
        json_data=json_data,
    )


def register_search(subparsers):

    parser = subparsers.add_parser(
        "search",
        help="Search assembly instructions",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    parser.add_argument(
        "--section",
        default=".text",
        help="Section to search",
    )

    group = parser.add_mutually_exclusive_group(
        required=True,
    )

    group.add_argument(
        "--mnemonic",
        help="Search by mnemonic",
    )

    group.add_argument(
        "--operand",
        help="Search by operand",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=search_command,
    )