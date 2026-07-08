from rev.elf import ELFParser


def symbols_command(args):

    elf = ELFParser(args.file)

    if not elf.symbols:
        print("No symbols found.")
        return

    print(f"{'Value':<18}{'Size':<8}{'Bind':<10}{'Type':<10}Name")
    print("-" * 70)

    for sym in elf.symbols:

        print(
            f"{hex(sym.value):<18}"
            f"{sym.size:<8}"
            f"{sym.bind:<10}"
            f"{sym.type:<10}"
            f"{sym.name}"
        )


def register_symbols(subparsers):

    parser = subparsers.add_parser(
        "symbols",
        help="Display ELF symbols",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    parser.set_defaults(func=symbols_command)