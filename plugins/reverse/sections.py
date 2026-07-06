from rev.pe import PEParser
from rev.elf import ELFParser


def sections_command(args):
    with open(args.file, "rb") as f:
        magic = f.read(4)

    if magic.startswith(b"MZ"):
        parser = PEParser(args.file)
    elif magic == b"\x7fELF":
        parser = ELFParser(args.file)
    else:
        print("Unsupported binary format.")
        return

    print(
        f"{'Name':<10} {'VA':<12} {'Raw Size':<10} {'Entropy':<8}"
    )
    print("-" * 50)

    for section in parser.sections:
        print(
            f"{section['name']:<10} "
            f"{section['virtual_address']:<12} "
            f"{section['raw_size']:<10} "
            f"{section['entropy']:<8}"
        )


def register_sections(subparsers):
    parser = subparsers.add_parser(
        "sections",
        help="Display binary sections"
    )

    parser.add_argument(
        "file",
        help="Input binary"
    )

    parser.set_defaults(func=sections_command)