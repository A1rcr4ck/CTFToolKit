from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from rev.parser import BinaryParser
from rev.disassembler import Disassembler


def disassemble_command(args):

    parser = BinaryParser.open(args.file)

    dis = Disassembler(parser)

    rows = dis.section(
        args.section,
        args.count,
    )

    table = (
        "Disassembly",
        ["Address", "Bytes", "Mnemonic", "Operands"],
        [
            (
                hex(addr),
                bytes_,
                mnemonic,
                operands,
            )
            for addr, bytes_, mnemonic, operands in rows
        ],
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=rows,
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