from crypto.identify import CryptoIdentifier
from core.input import read_input

def register_identify(subparsers):

    parser = subparsers.add_parser(
        "identify",
        help="Identify possible encodings"
    )

    parser.add_argument("text")

    parser.set_defaults(func=run_identify)


def run_identify(args):

    results = CryptoIdentifier().identify(read_input(args.text))

    if not results:
        print("No encoding identified.")
        return

    print("Possible Encodings")
    print("------------------")

    for result in results:
        print(result)