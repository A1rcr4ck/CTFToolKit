from pathlib import Path

from rev.elf import ELFParser


def test_relocations():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    assert len(elf.relocations) > 0