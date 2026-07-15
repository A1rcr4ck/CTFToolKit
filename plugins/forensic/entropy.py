from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from forensic.entropy import FileEntropy


def entropy_command(args):

    result = FileEntropy(args.file).entropy()

    rows = [
        (
            result["File"],
            result["Size"],
            result["Entropy"],
        )
    ]

    table = (
        "File Entropy",
        ["File", "Size", "Entropy"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=result,
    )


def register_entropy(subparsers):

    parser = subparsers.add_parser(
        "entropy",
        help="Calculate Shannon entropy",
    )

    parser.add_argument(
        "file",
        help="Input file",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=entropy_command,
    )