from pathlib import Path

from rev.elf import ELFParser
from rev.reader import BinaryReader
from rev.hexdump import HexDump


def test_hexdump():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    reader = BinaryReader(
        elf.memory
    )

    dump = HexDump(
        reader
    ).dump(
        elf.header.entry,
        64,
    )

    assert len(dump) > 0