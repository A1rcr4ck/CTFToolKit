# from rev import parser
from csv import reader

from rev.strings import extract_strings
from rev.parser import BinaryParser
from rev.reader import BinaryReader


def strings_command(args):
    parser = BinaryParser.open(args.file)
    reader = BinaryReader(parser.memory)

    seen = set()
    strings = []

    for region in reader.regions:

        for string in extract_strings(
            region.data,
            args.min_length,
        ):

            if string not in seen:
                seen.add(string)
                strings.append(string)

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