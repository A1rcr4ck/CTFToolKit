from pathlib import Path

from rev.parser import BinaryParser
from rev.instructions import InstructionIndex


def test_instruction_index():

    parser = BinaryParser.open(
        Path("tests/samples/reverse/hello_elf64")
    )

    index = InstructionIndex(parser)

    instructions = index.all()

    assert len(instructions) > 0

    assert any(
        ins.mnemonic == "call"
        for ins in instructions
    )