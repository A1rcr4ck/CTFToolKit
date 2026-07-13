from pathlib import Path

from rev.parser import BinaryParser
from rev.xrefs import XRefFinder


def test_xrefs():

    parser = BinaryParser.open(
        Path("tests/samples/reverse/hello_elf64")
    )

    xrefs = XRefFinder(parser)

    calls = xrefs.calls("puts")

    assert isinstance(calls, list)