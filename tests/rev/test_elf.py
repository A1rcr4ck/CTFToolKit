# from pathlib import Path

# from rev.elf import ELFParser
#     # elf = ELFParser(Path("tests/samples/reverse/hello_elf64"))

# def test_symbols():
#     elf = ELFParser(Path("tests/samples/reverse/hello_elf64"))
#     assert len(elf.symbols) > 0

#     for symbol in elf.symbols[:20]:
#         print(symbol)

from pathlib import Path
from rev.elf import ELFParser


def test_relocations():

    elf = ELFParser(Path("tests/samples/reverse/hello_elf64"))

    assert len(elf.relocations) > 0