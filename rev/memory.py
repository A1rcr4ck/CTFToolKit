from dataclasses import dataclass


@dataclass(slots=True)
class MemoryRegion:

    name: str

    virtual_address: int

    virtual_size: int

    file_offset: int

    file_size: int

    data: bytes