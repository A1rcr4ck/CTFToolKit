from crypto.detect import Detector
from core.input import read_input

def register_detect(subparsers):

    detect = subparsers.add_parser(
        "detect",
        help="Detect common encodings"
    )

    detect.add_argument("text")

    detect.set_defaults(func=run_detect)


def run_detect(args):

    detector = Detector()

    results = detector.detect(read_input(args.text))

    if not results:
        print("No encoding detected.")
        return

    print(f"{'Encoding':<12}Decoded")
    print("-" * 60)

    for encoding, decoded in results:
        print(f"{encoding:<12}{decoded}")