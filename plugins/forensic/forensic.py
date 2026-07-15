from forensic.hashing import FileHasher
from forensic.fileinfo import FileInfo
from core.cli import add_output_argument
from forensic.strings import StringsExtractor


def hash_command(args):

    hasher = FileHasher(args.file)
    hashes = hasher.all()

    if args.output == "json":
        import json
        print(json.dumps(hashes, indent=4))
        return

    width = max(len(name) for name in hashes)

    for name, value in hashes.items():
        print(f"{name:<{width}} : {value}")


def info_command(args):

    info = FileInfo(args.file).info()

    if args.output == "json":
        import json
        print(json.dumps(info, indent=4))
        return

    width = max(len(k) for k in info)

    for key, value in info.items():
        print(f"{key:<{width}} : {value}")


def register(subparsers):

    forensic = subparsers.add_parser(
        "forensic",
        help="Forensics tools",
    )

    forensic_sub = forensic.add_subparsers(
        dest="forensic_command",
        required=True,
    )

    hash_parser = forensic_sub.add_parser(
        "hash",
        help="Calculate file hashes",
    )

    hash_parser.add_argument(
        "file",
        help="Input file",
    )

    add_output_argument(hash_parser)

    hash_parser.set_defaults(
        func=hash_command,
    )

    info_parser = forensic_sub.add_parser(
        "info",
        help="Display file information",
    )

    info_parser.add_argument(
        "file",
        help="Input file",
    )

    add_output_argument(info_parser)

    info_parser.set_defaults(
        func=info_command,
    )

    strings_parser = forensic_sub.add_parser(
    "strings",
    help="Extract printable strings",
    )

    strings_parser.add_argument(
        "file",
        help="Input file",
    )

    strings_parser.add_argument(
        "-m",
        "--min-length",
        type=int,
        default=4,
        help="Minimum string length",
    )

    add_output_argument(strings_parser)

    strings_parser.set_defaults(
        func=strings_command,
    )

def strings_command(args):

    strings = StringsExtractor(args.file).extract(args.min_length)

    if args.output == "json":
        import json
        print(json.dumps(strings, indent=4))
        return

    for s in strings:
        print(s)