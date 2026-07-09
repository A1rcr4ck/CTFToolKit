from rev.elf import ELFParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


def dynamic_command(args):

    elf = ELFParser(args.file)

    if not elf.dynamic:
        print("No dynamic section found.")
        return

    rows = []

    for entry in elf.dynamic:

        rows.append(
            (
                hex(entry.tag),
                hex(entry.value),
            )
        )

    table = (
        "ELF Dynamic Section",
        ["Tag", "Value"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=elf.dynamic,
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

    add_output_argument(parser)

    parser.set_defaults(func=dynamic_command)