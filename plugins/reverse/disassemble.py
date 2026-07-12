from rev.disassembler import Disassembler


def disassemble_command(args):

    print("Coming soon")


def register_disassemble(subparsers):

    parser = subparsers.add_parser(
        "disassemble",
        help="Disassemble binary",
    )

    parser.add_argument("file")
    parser.add_argument("--count", type=int, default=20)

    parser.set_defaults(func=disassemble_command)