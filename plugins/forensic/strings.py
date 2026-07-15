from forensic.strings import StringsExtractor
from core.cli import add_output_argument


def strings_command(args):

    strings = StringsExtractor(args.file).extract(args.min_length)

    if args.output == "json":
        import json
        print(json.dumps(strings, indent=4))
        return

    for s in strings:
        print(s)


def register_strings(subparsers):

    parser = subparsers.add_parser(
        "strings",
        help="Extract printable strings",
    )

    parser.add_argument(
        "file",
        help="Input file",
    )

    parser.add_argument(
        "-m",
        "--min-length",
        type=int,
        default=4,
        help="Minimum string length",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=strings_command,
    )