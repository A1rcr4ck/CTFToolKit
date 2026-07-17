from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from forensic.exif import ExifExtractor


def exif_command(args):

    result = ExifExtractor(args.file).extract()

    rows = [
        ("File", result["File"]),
        ("Format", result["Format"]),
        ("Mode", result["Mode"]),
        ("Width", result["Width"]),
        ("Height", result["Height"]),
    ]

    for key, value in result["Metadata"].items():

        rows.append((key, value))

    table = (
        "EXIF Metadata",
        ["Property", "Value"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=result,
    )


def register_exif(subparsers):

    parser = subparsers.add_parser(
        "exif",
        help="Extract EXIF metadata",
    )

    parser.add_argument(
        "file",
        help="Image file",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=exif_command,
    )