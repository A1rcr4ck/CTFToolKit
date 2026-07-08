from rev.elf import ELFParser


def relocations_command(args):

    elf = ELFParser(args.file)

    if not elf.relocations:
        print("No relocations found.")
        return

    print(
        f"{'Offset':<18}"
        f"{'Type':<12}"
        f"{'Symbol':<10}"
        f"{'Addend'}"
    )

    print("-" * 60)

    for rel in elf.relocations:

        addend = (
            hex(rel.addend)
            if rel.addend is not None
            else "-"
        )

        print(
            f"{hex(rel.offset):<18}"
            f"{rel.type:<12}"
            f"{rel.symbol:<10}"
            f"{addend}"
        )


def register_relocations(subparsers):

    parser = subparsers.add_parser(
        "relocations",
        help="Display ELF relocations",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    parser.set_defaults(func=relocations_command)