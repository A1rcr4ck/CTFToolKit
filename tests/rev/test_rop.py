from pathlib import Path

from rev.parser import BinaryParser
from rev.rop import ROPFinder


def test_rop():

    parser = BinaryParser.open(
        Path("tests/samples/reverse/hello_elf64")
    )

    rop = ROPFinder(parser)

    gadgets = rop.gadgets()

    assert len(gadgets) > 0