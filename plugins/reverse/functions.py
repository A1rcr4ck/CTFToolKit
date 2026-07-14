from rev.parser import BinaryParser
from rev.functions import FunctionFinder
from rev.engine import ReverseEngine
from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def functions_command(args):

    engine = ReverseEngine(args.file)

    functions = engine.functions.find()

    rows = []

    for function in functions:

        rows.append(
            (
                function["name"],
                hex(function["address"]),
                function["size"],
                function["source"],
            )
        )

    table = (
        "Functions",
        ["Name", "Address", "Size", "Source"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=functions,
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