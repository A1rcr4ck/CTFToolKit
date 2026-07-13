from rev.parser import BinaryParser
from rev.rop import ROPFinder

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def rop_command(args):

    parser = BinaryParser.open(args.file)

    finder = ROPFinder(parser)

    rows = []

    json_data = []

    for gadget in finder.gadgets():

        text = " ; ".join(
            f"{ins.mnemonic} {ins.operands}".strip()
            for ins in gadget
        )

        address = hex(gadget[0].address)

        rows.append(
            (
                address,
                text,
            )
        )

        json_data.append(
            {
                "address": address,
                "gadget": text,
            }
        )

    table = (
        "ROP Gadgets",
        ["Address", "Instructions"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=json_data,
    )


def register_rop(subparsers):

    parser = subparsers.add_parser(
        "rop",
        help="Find simple ROP gadgets",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=rop_command,
    )