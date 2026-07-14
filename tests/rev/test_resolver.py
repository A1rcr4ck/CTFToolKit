from pathlib import Path

from rev.engine import ReverseEngine


def test_symbol_resolver():

    engine = ReverseEngine(
        Path("tests/samples/reverse/hello_elf64")
    )

    assert isinstance(
        engine.resolver.symbols,
        dict,
    )