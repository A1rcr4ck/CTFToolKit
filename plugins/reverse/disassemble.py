from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from rev.parser import BinaryParser
from rev.disassembler import Disassembler


def disassemble_command(args):

    parser = BinaryParser.open(args.file)

    dis = Disassembler(parser)

    instructions = dis.section(
        args.section,
        args.count,
    )

    table = (
        "Disassembly",
        ["Address", "Bytes", "Mnemonic", "Operands"],
        [
            (
                hex(ins.address),
                ins.bytes.hex(" "),
                ins.mnemonic,
                ins.operands,
            )
            for ins in instructions
        ],
    )

    json_data = [
        {
            "address": hex(ins.address),
            "bytes": ins.bytes.hex(" "),
            "mnemonic": ins.mnemonic,
            "operands": ins.operands,
        }
        for ins in instructions
    ]

    dispatch(
        args.output,
        table_data=table,
        json_data=json_data,
    )


def register_disassemble(subparsers):

    parser = subparsers.add_parser(
        "disassemble",
        help="Disassemble a section",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    parser.add_argument(
        "--section",
        default=".text",
        help="Section to disassemble",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=30,
        help="Number of instructions",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=disassemble_command,
    )