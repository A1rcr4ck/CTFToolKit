from pathlib import Path

from rev.elf import ELFParser
from rev.pe import PEParser


def test_elf_memory():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    assert len(elf.memory) > 0


def test_pe_memory():

    pe = PEParser(
        Path("tests/samples/reverse/hello64.exe")
    )

    assert len(pe.memory) > 0