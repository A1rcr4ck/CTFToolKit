from pathlib import Path

from rev.parser import BinaryParser
from rev.search import InstructionSearcher


def test_search_call():

    parser = BinaryParser.open(
        Path("tests/samples/reverse/hello_elf64")
    )

    search = InstructionSearcher(parser)

    result = search.mnemonic(
        mnemonic="call"
    )

    assert len(result) > 0