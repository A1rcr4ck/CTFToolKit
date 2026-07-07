from pathlib import Path
import struct
from rev.constants.elf import ELF_MACHINE, ELF_TYPE
from rev.constants.elf import PROGRAM_TYPES
from rev.constants.elf import SECTION_TYPES
from rev.models import DynamicEntry, ProgramHeader, Relocation, SectionHeader, ELFHeader, Symbol

class ELFParser:

    def __init__(self, path):
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(self.path)

        self.data = self.path.read_bytes()

        if self.data[:4] != b"\x7fELF":
            raise ValueError("Not an ELF file")

        self.ident = self.data[:16]

        self.is_64 = self.ident[4] == 2
        self.is_32 = self.ident[4] == 1

        self.endian = "<" if self.ident[5] == 1 else ">"

        from rev.models import (
            ELFHeader,
            ProgramHeader,
            SectionHeader,
            Symbol,
            DynamicEntry,
            Relocation,
        )

        self.header = None
        self.program_headers = []
        self.section_headers = []
        self.symbols = []
        self.dynamic = []
        self.relocations = []

        self._parse_header()
        self._parse_program_headers()
        self._parse_section_headers()
        self._parse_symbols()
        self._parse_dynamic()
        self._parse_relocations()

    def _parse_header(self):

        if self.is_64:

            (
                e_type,
                e_machine,
                e_version,
                e_entry,
                e_phoff,
                e_shoff,
                e_flags,
                e_ehsize,
                e_phentsize,
                e_phnum,
                e_shentsize,
                e_shnum,
                e_shstrndx,
            ) = struct.unpack(
                self.endian + "HHIQQQIHHHHHH",
                self.data[16:64],
            )

        else:

            (
                e_type,
                e_machine,
                e_version,
                e_entry,
                e_phoff,
                e_shoff,
                e_flags,
                e_ehsize,
                e_phentsize,
                e_phnum,
                e_shentsize,
                e_shnum,
                e_shstrndx,
            ) = struct.unpack(
                self.endian + "HHIIIIIHHHHHH",
                self.data[16:52],
            )

        self.header = ELFHeader(
            type=ELF_TYPE.get(e_type, hex(e_type)),
            machine=ELF_MACHINE.get(e_machine, hex(e_machine)),
            entry=e_entry,
            phoff=e_phoff,
            shoff=e_shoff,
            phentsize=e_phentsize,
            phnum=e_phnum,
            shentsize=e_shentsize,
            shnum=e_shnum,
            shstrndx=e_shstrndx,
        )
    def _parse_program_headers(self):

        phoff = self.header.phoff
        phentsize = self.header.phentsize
        phnum = self.header.phnum

        for i in range(phnum):

            offset = phoff + i * phentsize

            if self.is_64:

                header = struct.unpack(
                    self.endian + "IIQQQQQQ",
                    self.data[offset:offset + 56],
                )

                (
                    p_type,
                    p_flags,
                    p_offset,
                    p_vaddr,
                    p_paddr,
                    p_filesz,
                    p_memsz,
                    p_align,
                ) = header

            else:

                header = struct.unpack(
                    self.endian + "IIIIIIII",
                    self.data[offset:offset + 32],
                )

                (
                    p_type,
                    p_offset,
                    p_vaddr,
                    p_paddr,
                    p_filesz,
                    p_memsz,
                    p_flags,
                    p_align,
                ) = header

            self.program_headers.append(
                ProgramHeader(
                    type=PROGRAM_TYPES.get(p_type, hex(p_type)),
                    offset=p_offset,
                    vaddr=p_vaddr,
                    filesz=p_filesz,
                    memsz=p_memsz,
                    flags=p_flags,
                    align=p_align,
                )
            )
        
    def _parse_section_headers(self):

        shoff = self.header.shoff
        shentsize = self.header.shentsize
        shnum = self.header.shnum
        shstrndx = self.header.shstrndx

        raw_headers = []

        if self.is_64:

            for i in range(shnum):

                offset = shoff + (i * shentsize)

                raw_headers.append(
                    struct.unpack(
                        self.endian + "IIQQQQIIQQ",
                        self.data[offset:offset + 64],
                    )
                )

        else:

            for i in range(shnum):

                offset = shoff + (i * shentsize)

                raw_headers.append(
                    struct.unpack(
                        self.endian + "IIIIIIIIII",
                        self.data[offset:offset + 40],
                    )
                )

        shstr = raw_headers[shstrndx]
        shstr_offset = shstr[4]

        for header in raw_headers:

            name_offset = header[0]

            end = self.data.find(
                b"\x00",
                shstr_offset + name_offset,
            )

            name = self.data[
                shstr_offset + name_offset:end
            ].decode(errors="ignore")

            self.section_headers.append(
                SectionHeader(
                    name=name,
                    type=SECTION_TYPES.get(header[1], hex(header[1])),
                    flags=header[2],
                    address=header[3],
                    offset=header[4],
                    size=header[5],
                    link=header[6],
                    info=header[7],
                    align=header[8],
                    entry_size=header[9],
                )
            )
    def _parse_symbols(self):

        for section in self.section_headers:

            if section.type not in ("SYMTAB", "DYNSYM"):  # SHT_SYMTAB / SHT_DYNSYM
                continue

            strtab = self.section_headers[section.link]

            string_table = self.data[
                strtab.offset:
                strtab.offset + strtab.size
            ]

            count = (
                section.size // section.entry_size
                if section.entry_size
                else 0
            )

            for i in range(count):

                base = section.offset + i * section.entry_size

                if self.is_64:

                    (
                        st_name,
                        st_info,
                        st_other,
                        st_shndx,
                        st_value,
                        st_size,
                    ) = struct.unpack(
                        self.endian + "IBBHQQ",
                        self.data[base:base + 24],
                    )

                else:

                    (
                        st_name,
                        st_value,
                        st_size,
                        st_info,
                        st_other,
                        st_shndx,
                    ) = struct.unpack(
                        self.endian + "IIIBBH",
                        self.data[base:base + 16],
                    )

                end = string_table.find(b"\x00", st_name)

                if end == -1:
                    name = ""
                else:
                    name = string_table[
                        st_name:end
                    ].decode(errors="ignore")

                self.symbols.append(
                    Symbol(
                        name=name,
                        value=st_value,
                        size=st_size,
                        info=st_info,
                        other=st_other,
                        section=st_shndx,
                    )
                )
    def _parse_dynamic(self):

        for section in self.section_headers:

            if section.type != "DYNAMIC":      # SHT_DYNAMIC
                continue

            count = (
                section.size // section.entry_size
                if section.entry_size
                else 0
            )

            for i in range(count):

                base = section.offset + i * section.entry_size

                if self.is_64:

                    tag, value = struct.unpack(
                        self.endian + "QQ",
                        self.data[base:base + 16],
                    )

                else:

                    tag, value = struct.unpack(
                        self.endian + "II",
                        self.data[base:base + 8],
                    )

                self.dynamic.append(
                    DynamicEntry(
                        tag=tag,
                        value=value,
                    )
                )
    def _parse_relocations(self):

        for section in self.section_headers:

            if section.type not in ("RELA", "REL"):   # SHT_RELA / SHT_REL
                continue

            if section.entry_size == 0:
                continue

            count = section.size // section.entry_size

            for i in range(count):

                base = section.offset + (i * section.entry_size)

                if self.is_64:

                    if section.type == "RELA":      # RELA

                        r_offset, r_info, r_addend = struct.unpack(
                            self.endian + "QQq",
                            self.data[base:base + 24],
                        )

                    else:                         # REL

                        r_offset, r_info = struct.unpack(
                            self.endian + "QQ",
                            self.data[base:base + 16],
                        )

                        r_addend = None

                else:

                    if section.type == "RELA":

                        r_offset, r_info, r_addend = struct.unpack(
                            self.endian + "IIi",
                            self.data[base:base + 12],
                        )

                    else:

                        r_offset, r_info = struct.unpack(
                            self.endian + "II",
                            self.data[base:base + 8],
                        )

                        r_addend = None

                self.relocations.append(
                    Relocation(
                        offset=r_offset,
                        info=r_info,
                        type=r_info & 0xffffffff,
                        symbol=r_info >> 32 if self.is_64 else r_info >> 8,
                        addend=r_addend,
                    )
                )