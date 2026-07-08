from pathlib import Path

from rev.elf import ELFParser


def test_elf_header():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    assert elf.header.machine == "x86-64"