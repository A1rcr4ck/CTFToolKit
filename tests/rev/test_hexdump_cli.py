from pathlib import Path

from plugins.reverse.hexdump import hexdump_command


class Args:

    file = Path("tests/samples/reverse/hello_elf64")

    section = ".text"

    address = None

    size = 64

    output = "table"


def test_hexdump_cli():

    hexdump_command(Args())