from rev.elf import ELFParser
from rev.pe import PEParser
from rev.parser import BinaryParser


def imports_command(args):

    parser = BinaryParser.open(args.file)


    if isinstance(parser, PEParser):

        current = None

        for imp in parser.imports:

            if current != imp.dll:
                current = imp.dll
                print(f"\n[{current}]")

            print(f"  {imp.name}")

    elif isinstance(parser, ELFParser):

        for symbol in parser.symbols:
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