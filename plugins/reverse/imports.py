from rev.elf import ELFParser
from rev.pe import PEParser


def imports_command(args):

    with open(args.file, "rb") as f:
        magic = f.read(4)

    if magic[:2] == b"MZ":

        pe = PEParser(args.file)

        current = None

        for imp in pe.imports:

            if current != imp.dll:
                current = imp.dll
                print(f"\n[{current}]")

            print(f"  {imp.name}")

    elif magic == b"\x7fELF":

        elf = ELFParser(args.file)

        for symbol in elf.symbols:

            if symbol.section == 0 and symbol.name:
                print(symbol.name)

    else:

        print("Unsupported binary.")

def register_imports(subparsers):

    parser = subparsers.add_parser(
        "imports",
        help="Display imported functions",
    )

    parser.add_argument(
        "file",
        help="Input binary",
    )

    parser.set_defaults(func=imports_command)