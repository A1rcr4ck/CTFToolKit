from rev.pe import PEParser


def exports_command(args):

    pe = PEParser(args.file)

    if not pe.exports:
        print("No exports found.")
        return

    print(f"{'Ordinal':<10}{'Address':<12}Name")
    print("-" * 50)

    for export in pe.exports:
        print(
            f"{export.ordinal:<10}"
            f"{hex(export.address):<12}"
            f"{export.name}"
        )


def register_exports(subparsers):

    parser = subparsers.add_parser(
        "exports",
        help="Display exported functions",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    parser.set_defaults(func=exports_command)