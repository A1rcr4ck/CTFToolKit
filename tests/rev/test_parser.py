from pathlib import Path

from rev.parser import BinaryParser
from rev.elf import ELFParser
from rev.pe import PEParser


def test_open_elf():

    parser = BinaryParser.open(
        Path("tests/samples/reverse/hello_elf64")
    )

    assert isinstance(parser, ELFParser)


def test_open_pe():

    parser = BinaryParser.open(
        Path("tests/samples/reverse/hello64.exe")
    )

    assert isinstance(parser, PEParser)