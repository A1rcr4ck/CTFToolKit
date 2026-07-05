from rev.entropy import calculate_entropy


def entropy_command(args):
    entropy = calculate_entropy(args.file)

    print(f"Entropy : {entropy:.4f} bits/byte")

    if entropy > 7.2:
        print("Assessment : High (Possibly packed/encrypted)")
    elif entropy > 6.5:
        print("Assessment : Medium")
    else:
        print("Assessment : Low")


def register_entropy(subparsers):
    parser = subparsers.add_parser(
        "entropy",
        help="Calculate Shannon entropy"
    )

    parser.add_argument(
        "file",
        help="Input file"
    )

    parser.set_defaults(func=entropy_command)