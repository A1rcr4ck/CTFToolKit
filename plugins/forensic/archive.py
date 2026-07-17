from core.cli import add_output_argument
from core.output.dispatcher import dispatch

from forensic.archive import ArchiveInspector


def archive_command(args):

    try:
        result = ArchiveInspector(args.file).inspect()

    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    rows = []

    for entry in result["Files"]:

        rows.append(
            (
                entry["Name"],
                entry["Original Size"],
                entry["Compressed Size"],
                entry["Modified"],
            )
        )

    table = (
        "Archive Contents",
        ["Name", "Size", "Compressed", "Modified"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=result,
    )


def register_archive(subparsers):

    parser = subparsers.add_parser(
        "archive",
        help="Inspect ZIP archives",
    )

    parser.add_argument(
        "file",
        help="ZIP archive",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=archive_command,
    )