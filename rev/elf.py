from pathlib import Path
import struct


ELF_MAGIC = b"\x7fELF"

ELF_CLASS = {
    1: "ELF32",
    2: "ELF64",
}

ELF_DATA = {
    1: "Little Endian",
    2: "Big Endian",
}

ELF_OSABI = {
    0: "System V",
    3: "Linux",
    6: "Solaris",
    9: "FreeBSD",
}

ELF_MACHINE = {
    3: "x86",
    40: "ARM",
    62: "x86-64",
    183: "AArch64",
}


class ELFParser:

    def __init__(self, path: str):
        self.path = Path(path)
        self.data = self.path.read_bytes()

        if self.data[:4] != ELF_MAGIC:
            raise ValueError("Not an ELF file")

        self.header = self._parse_header()

    def _parse_header(self):
        ident = self.data[:16]

        elf_class = ident[4]
        endian = ident[5]

        fmt = "<" if endian == 1 else ">"

        machine = struct.unpack(
            fmt + "H",
            self.data[18:20]
        )[0]

        entry = (
            struct.unpack(fmt + "Q", self.data[24:32])[0]
            if elf_class == 2
            else struct.unpack(fmt + "I", self.data[24:28])[0]
        )

        return {
            "class": ELF_CLASS.get(elf_class, "Unknown"),
            "endianness": ELF_DATA.get(endian, "Unknown"),
            "osabi": ELF_OSABI.get(ident[7], "Unknown"),
            "machine": ELF_MACHINE.get(machine, "Unknown"),
            "entry": hex(entry),
        }