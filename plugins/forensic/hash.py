from forensic.hashing import FileHasher
from core.cli import add_output_argument


def hash_command(args):
    hashes = FileHasher(args.file).all()

    if args.output == "json":
        import json
        print(json.dumps(hashes, indent=4))
        return

    width = max(len(k) for k in hashes)

    for key, value in hashes.items():
        print(f"{key:<{width}} : {value}")


def register_hash(subparsers):

    parser = subparsers.add_parser(
        "hash",
        help="Calculate file hashes",
    )

    parser.add_argument(
        "file",
        help="Input file",
    )

    add_output_argument(parser)

    parser.set_defaults(
        func=hash_command,
    )