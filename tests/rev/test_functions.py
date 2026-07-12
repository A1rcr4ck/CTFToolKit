from pathlib import Path

from rev.elf import ELFParser
from rev.functions import FunctionFinder


def test_functions():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    functions = FunctionFinder(
        elf
    ).find()

    assert len(functions) > 0

    assert any(
        function["name"] == "main"
        for function in functions
    )