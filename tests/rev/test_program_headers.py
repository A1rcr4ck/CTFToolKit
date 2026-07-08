from pathlib import Path

from rev.elf import ELFParser


def test_program_headers():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    assert len(elf.program_headers) > 0