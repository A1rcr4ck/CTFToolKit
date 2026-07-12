from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from rev.parser import BinaryParser
from rev.entropy import calculate_entropy


def entropy_command(args):

    binary = BinaryParser.open(args.file)

    rows = []

    for region in binary.memory:

        rows.append(
            (
                region.name,
                region.file_size,
                calculate_entropy(region.data),
            )
        )

    table = (
        "Section Entropy",
        ["Section", "Size", "Entropy"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=rows,
    )


def register_entropy(subparsers):

    parser = subparsers.add_parser(
        "entropy",
        help="Calculate Shannon entropy",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=entropy_command,
    )