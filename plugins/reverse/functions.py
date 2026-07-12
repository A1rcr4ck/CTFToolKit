from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from rev.parser import BinaryParser
from rev.functions import FunctionFinder


def functions_command(args):

    parser = BinaryParser.open(args.file)

    rows = FunctionFinder(
        parser
    ).find()

    table = (
        "Functions",
        ["Name", "Address", "Size"],
        [
            (
                name,
                hex(addr),
                size,
            )
            for name, addr, size in rows
        ],
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=rows,
    )


def register_functions(subparsers):

    parser = subparsers.add_parser(
        "functions",
        help="List discovered functions",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=functions_command,
    )