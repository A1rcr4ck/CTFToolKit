from rev.pe import PEParser
from rev.elf import ELFParser


def sections_command(args):

    with open(args.file, "rb") as f:
        magic = f.read(4)

    if magic == b"\x7fELF":

        parser = ELFParser(args.file)

        print(
            f"{'Name':<20}"
            f"{'Type':<12}"
            f"{'Address':<18}"
            f"{'Size':<12}"
        )

        print("-" * 65)

        for section in parser.section_headers:

            print(
                f"{section.name:<20}"
                f"{section.type:<12}"
                f"{hex(section.address):<18}"
                f"{section.size:<12}"
            )

    elif magic[:2] == b"MZ":

        parser = PEParser(args.file)

        print(
            f"{'Name':<12}"
            f"{'VA':<12}"
            f"{'Raw Size':<12}"
            f"{'Entropy':<10}"
        )

        print("-" * 50)

        for section in parser.sections:

            print(
                f"{section.name:<12}"
                f"{hex(section.virtual_address):<12}"
                f"{section.raw_size:<12}"
                f"{section.entropy:<10}"
            )

    else:

        print("Unsupported binary.")

def register_sections(subparsers):

    parser = subparsers.add_parser(
        "sections",
        help="Display binary sections",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    parser.set_defaults(func=sections_command)