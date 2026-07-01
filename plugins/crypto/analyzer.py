from crypto.analyzer import CryptoAnalyzer
from core.input import read_input

def register_analyzer(subparsers):

    analyzer = subparsers.add_parser(
        "analyze",
        help="Analyze ciphertext"
    )

    analyzer.add_argument("text")

    analyzer.set_defaults(func=run_analyzer)


def run_analyzer(args):

    text = read_input(args.text)

    analyzer = CryptoAnalyzer()

    print("\nEntropy")
    print("--------")
    print(analyzer.entropy(text))

    print("\nIndex of Coincidence")
    print("--------------------")
    print(analyzer.ioc(text))

    print("\nFrequency")
    print("---------")

    freq = analyzer.frequency(text)

    for k, v in freq.items():
        print(f"{k}: {v}%")