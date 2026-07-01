from crypto.hash import HashToolkit
from core.input import read_input

def register_hash(subparsers):

    parser = subparsers.add_parser(
        "hash",
        help="Hash Generator"
    )

    parser.add_argument(
        "algorithm",
        choices=[
            "md5",
            "sha1",
            "sha224",
            "sha256",
            "sha384",
            "sha512"
        ]
    )

    parser.add_argument("text")

    parser.set_defaults(func=run_hash)


def run_hash(args):
    print(
        HashToolkit().generate(
            args.algorithm,
            read_input(args.text)
        )
    )