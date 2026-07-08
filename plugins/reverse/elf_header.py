from rev.elf import ELFParser


def elf_header_command(args):

    elf = ELFParser(args.file)
    h = elf.header

    print(f"{'Type':<15}: {h.type}")
    print(f"{'Machine':<15}: {h.machine}")
    print(f"{'Entry':<15}: {hex(h.entry)}")
    print(f"{'PH Offset':<15}: {hex(h.phoff)}")
    print(f"{'SH Offset':<15}: {hex(h.shoff)}")
    print(f"{'PH Count':<15}: {h.phnum}")
    print(f"{'SH Count':<15}: {h.shnum}")


def register_elf_header(subparsers):

    parser = subparsers.add_parser(
        "elf-header",
        help="Display ELF header",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    parser.set_defaults(func=elf_header_command)