from pathlib import Path

from rev.engine import ReverseEngine


def test_engine():

    engine = ReverseEngine(
        Path("tests/samples/reverse/hello_elf64")
    )

    assert engine.parser is not None
    assert engine.reader is not None
    assert engine.disassembler is not None
    assert engine.instructions is not None
    assert engine.functions is not None