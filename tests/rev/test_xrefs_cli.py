from pathlib import Path

from plugins.reverse.xrefs import xrefs_command


class Args:

    file = Path(
        "tests/samples/reverse/hello_elf64"
    )

    target = "puts"

    type = "call"

    output = "table"


def test_xrefs_cli():

    xrefs_command(
        Args()
    )