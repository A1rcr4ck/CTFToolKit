from rev.fileinfo import get_file_info

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def info_command(args):

    data = get_file_info(args.file)

    rows = [
        ("Path", data["path"]),
        ("Name", data["filename"]),
        ("Extension", data["extension"]),
        ("Size", f"{data['size']} bytes"),
        ("Type", data["type"]),
        ("Format", data["format"]),
        ("Architecture", data["architecture"]),
        ("Entry Point", data["entrypoint"]),
    ]

    table = (
        "Binary Information",
        ["Field", "Value"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=data,
    )


def register_info(subparsers):

    parser = subparsers.add_parser(
        "info",
        help="Display binary information",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    add_output_argument(parser)

    parser.set_defaults(func=info_command)