from forensic.hashing import FileHasher
from core.output.argument import add_output_argument


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