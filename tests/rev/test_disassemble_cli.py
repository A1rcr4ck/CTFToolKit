from pathlib import Path

from plugins.reverse.disassemble import disassemble_command


class Args:

    file = Path(
        "tests/samples/reverse/hello_elf64"
    )

    section = ".text"

    count = 20

    output = "table"


def test_disassemble_cli():

    disassemble_command(
        Args()
    )