from rev.elf import ELFParser
from rev.pe import PEParser


class BinaryParser:

    @staticmethod
    def open(path):

        with open(path, "rb") as f:
            magic = f.read(4)

        if magic == b"\x7fELF":
            return ELFParser(path)

        if magic[:2] == b"MZ":
            return PEParser(path)

        raise ValueError("Unsupported binary format")