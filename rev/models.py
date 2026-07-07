from dataclasses import dataclass


@dataclass(slots=True)
class ELFHeader:
    type: str
    machine: str
    entry: int
    phoff: int
    shoff: int
    phentsize: int
    phnum: int
    shentsize: int
    shnum: int
    shstrndx: int


@dataclass(slots=True)
class ProgramHeader:
    type: str
    offset: int
    vaddr: int
    filesz: int
    memsz: int
    flags: int
    align: int


@dataclass(slots=True)
class SectionHeader:
    name: str
    type: str
    flags: int
    address: int
    offset: int
    size: int
    link: int
    info: int
    align: int
    entry_size: int


@dataclass(slots=True)
class Symbol:
    name: str
    value: int
    size: int
    info: int
    other: int
    section: int


@dataclass(slots=True)
class DynamicEntry:
    tag: int
    value: int


@dataclass(slots=True)
class Relocation:
    offset: int
    info: int
    type: int
    symbol: int
    addend: int | None