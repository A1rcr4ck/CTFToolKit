from pathlib import Path

from rev.elf import ELFParser
from rev.reader import BinaryReader


def test_reader():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    reader = BinaryReader(
        elf.memory
    )

    text = reader.region(".text")

    assert text is not None

    assert len(text.data) > 0