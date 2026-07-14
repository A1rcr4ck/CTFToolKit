from pathlib import Path

from rev.elf import ELFParser
from rev.disassembler import Disassembler
from rev.engine import ReverseEngine


def test_disassemble_text():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    dis = Disassembler(elf)

    instructions = dis.section(".text")

    assert len(instructions) > 0

def test_disassembler_with_resolver():

    engine = ReverseEngine(
        Path("tests/samples/reverse/hello_elf64")
    )

    instructions = engine.disassembler.section(".text")

    assert len(instructions) > 0