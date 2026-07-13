from pathlib import Path

from plugins.reverse.search import search_command


class Args:

    file = Path(
        "tests/samples/reverse/hello_elf64"
    )

    section = ".text"

    mnemonic = "call"

    operand = None

    output = "table"


def test_search_cli():

    search_command(
        Args()
    )