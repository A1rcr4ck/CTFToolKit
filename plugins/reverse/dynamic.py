from rev.elf import ELFParser


def dynamic_command(args):

    elf = ELFParser(args.file)

    if not elf.dynamic:
        print("No dynamic section found.")
        return

    print(f"{'Tag':<18}Value")
    print("-" * 35)

    for entry in elf.dynamic:
        print(
            f"{hex(entry.tag):<18}"
            f"{hex(entry.value)}"
        )


def register_dynamic(subparsers):

    parser = subparsers.add_parser(
        "dynamic",
        help="Display ELF dynamic section",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    parser.set_defaults(func=dynamic_command)