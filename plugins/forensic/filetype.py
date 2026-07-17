from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from forensic.filetype import FileTypeDetector


def filetype_command(args):

    result = FileTypeDetector(args.file).detect()

    table = (
        "File Type",
        ["File", "Type", "Signature"],
        [
            (
                result["File"],
                result["Type"],
                result["Signature"],
            )
        ],
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=result,
    )


def register_filetype(subparsers):

    parser = subparsers.add_parser(
        "type",
        help="Detect file type using magic bytes",
    )

    parser.add_argument(
        "file",
        help="Input file",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=filetype_command,
    )