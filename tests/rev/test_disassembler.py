from pathlib import Path

from rev.elf import ELFParser
from rev.disassembler import Disassembler


def test_disassemble_text():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    dis = Disassembler(elf)

    instructions = dis.section(".text")

    assert len(instructions) > 0