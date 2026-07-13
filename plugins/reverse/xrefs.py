from rev.parser import BinaryParser
from rev.xrefs import XRefFinder

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def xrefs_command(args):

    parser = BinaryParser.open(args.file)

    finder = XRefFinder(parser)

    if args.type == "call":
        rows = finder.calls(args.target)
    else:
        rows = finder.jumps(args.target)

    table = (
        "Cross References",
        ["Address", "Mnemonic", "Operands"],
        [
            (
                hex(ins.address),
                ins.mnemonic,
                ins.operands,
            )
            for ins in rows
        ],
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=[
            {
                "address": hex(ins.address),
                "mnemonic": ins.mnemonic,
                "operands": ins.operands,
            }
            for ins in rows
        ],
    )


def register_xrefs(subparsers):

    parser = subparsers.add_parser(
        "xrefs",
        help="Find instruction cross references",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    parser.add_argument(
        "target",
        help="Target symbol or operand",
    )

    parser.add_argument(
        "--type",
        choices=["call", "jump"],
        default="call",
        help="Reference type",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=xrefs_command,
    )