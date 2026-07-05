from rev.strings import extract_strings


def strings_command(args):
    strings = extract_strings(
        args.file,
        args.min_length
    )

    for string in strings:
        print(string)


def register_strings(subparsers):
    parser = subparsers.add_parser(
        "strings",
        help="Extract printable strings"
    )

    parser.add_argument(
        "file",
        help="Input file"
    )

    parser.add_argument(
        "-n",
        "--min-length",
        type=int,
        default=4,
        help="Minimum string length (default: 4)"
    )

    parser.set_defaults(func=strings_command)