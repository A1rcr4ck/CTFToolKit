from forensic.fileinfo import FileInfo
from core.cli import add_output_argument


def info_command(args):

    info = FileInfo(args.file).info()

    if args.output == "json":
        import json
        print(json.dumps(info, indent=4))
        return

    width = max(len(k) for k in info)

    for key, value in info.items():
        print(f"{key:<{width}} : {value}")


def register_info(subparsers):

    parser = subparsers.add_parser(
        "info",
        help="Display file information",
    )

    parser.add_argument(
        "file",
        help="Input file",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=info_command,
    )