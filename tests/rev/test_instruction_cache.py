from pathlib import Path

from rev.engine import ReverseEngine


def test_instruction_cache():

    engine = ReverseEngine(
        Path("tests/samples/reverse/hello_elf64")
    )

    first = engine.decoded_instructions
    second = engine.decoded_instructions

    assert first is second