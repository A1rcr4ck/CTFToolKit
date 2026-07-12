from pathlib import Path

from rev.elf import ELFParser
from rev.functions import FunctionFinder


def test_functions():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    funcs = FunctionFinder(
        elf
    ).find()

    assert len(funcs) > 0