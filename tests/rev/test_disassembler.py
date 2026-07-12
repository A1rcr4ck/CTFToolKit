from pathlib import Path

from rev.elf import ELFParser
from rev.disassembler import Disassembler


def test_disassembler():

    elf = ELFParser(
        Path("tests/samples/reverse/hello_elf64")
    )

    text = next(
        section
        for section in elf.memory
        if section.name == ".text"
    )

    dis = Disassembler(elf)

    instructions = dis.disassemble(text)

    assert len(instructions) > 0