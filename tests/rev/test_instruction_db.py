from pathlib import Path

from rev.engine import ReverseEngine


def test_instruction_database():

    engine = ReverseEngine(
        Path("tests/samples/reverse/hello_elf64")
    )

    instructions = engine.database.all()

    assert len(instructions) > 0

    first = instructions[0]

    assert (
        engine.database.by_address(first.address)
        is first
    )