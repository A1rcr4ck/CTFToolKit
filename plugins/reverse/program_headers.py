from rev.elf import ELFParser


def program_headers_command(args):

    elf = ELFParser(args.file)

    print(
        f"{'Type':<18}"
        f"{'Offset':<12}"
        f"{'VAddr':<18}"
        f"{'FileSz':<10}"
        f"{'MemSz':<10}"
        f"{'Flags'}"
    )

    print("-" * 80)

    for ph in elf.program_headers:

        print(
            f"{ph.type:<18}"
            f"{hex(ph.offset):<12}"
            f"{hex(ph.vaddr):<18}"
            f"{ph.filesz:<10}"
            f"{ph.memsz:<10}"
            f"{hex(ph.flags)}"
        )


def register_program_headers(subparsers):

    parser = subparsers.add_parser(
        "program-headers",
        help="Display ELF program headers",
    )

    parser.add_argument(
        "file",
        help="Input ELF binary",
    )

    parser.set_defaults(func=program_headers_command)
    