from pathlib import Path

import pefile

from rev.memory import MemoryRegion
from rev.models import (
    PEHeader,
    PESection,
    Import,
    Export,
    Resource,
)
from rev.constants.pe import (
    MACHINE_TYPES,
    SUBSYSTEMS,
)


class PEParser:

    def __init__(self, path):

        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(self.path)

        self.pe = pefile.PE(str(self.path))

        self.header = None
        self.sections = []
        self.imports = []
        self.exports = []
        self.resources = []

        self._parse_header()
        self._parse_sections()
        self._parse_imports()
        self._parse_exports()
        self._parse_resources()

    def _parse_header(self):

        self.header = PEHeader(
            machine=MACHINE_TYPES.get(
                self.pe.FILE_HEADER.Machine,
                hex(self.pe.FILE_HEADER.Machine),
            ),
            timestamp=self.pe.FILE_HEADER.TimeDateStamp,
            sections=self.pe.FILE_HEADER.NumberOfSections,
            entrypoint=self.pe.OPTIONAL_HEADER.AddressOfEntryPoint,
            imagebase=self.pe.OPTIONAL_HEADER.ImageBase,
            subsystem=SUBSYSTEMS.get(
                self.pe.OPTIONAL_HEADER.Subsystem,
                "Unknown",
            ),
            dll=self.pe.is_dll(),
        )

    def _parse_sections(self):

        for section in self.pe.sections:

            self.sections.append(
                PESection(
                    name=section.Name.decode(
                        errors="ignore"
                    ).rstrip("\x00"),

                    virtual_address=section.VirtualAddress,
                    virtual_size=section.Misc_VirtualSize,

                    raw_size=section.SizeOfRawData,
                    pointer_to_raw_data=section.PointerToRawData,

                    entropy=round(section.get_entropy(), 2),

                    characteristics=section.Characteristics,
                )
            )

    def _parse_imports(self):

        if not hasattr(self.pe, "DIRECTORY_ENTRY_IMPORT"):
            return

        for dll in self.pe.DIRECTORY_ENTRY_IMPORT:

            for func in dll.imports:

                self.imports.append(
                    Import(
                        dll=dll.dll.decode(errors="ignore"),
                        name=(
                            func.name.decode(errors="ignore")
                            if func.name
                            else ""
                        ),
                        ordinal=func.ordinal,
                    )
                )

    def _parse_exports(self):

        if not hasattr(self.pe, "DIRECTORY_ENTRY_EXPORT"):
            return

        for symbol in self.pe.DIRECTORY_ENTRY_EXPORT.symbols:

            self.exports.append(
                Export(
                    name=(
                        symbol.name.decode(errors="ignore")
                        if symbol.name
                        else ""
                    ),
                    ordinal=symbol.ordinal,
                    address=symbol.address,
                )
            )

    def _parse_resources(self):

        if not hasattr(self.pe, "DIRECTORY_ENTRY_RESOURCE"):
            return

        for entry in self.pe.DIRECTORY_ENTRY_RESOURCE.entries:

            self.resources.append(
                Resource(
                    id=entry.id,
                    name=str(entry.name) if entry.name else None,
                )
            )
    @property
    def memory(self):

        regions = []

        for section in self.sections:

            regions.append(
                MemoryRegion(
                    name=section.name,
                    virtual_address=section.virtual_address,
                    virtual_size=section.virtual_size,
                    file_offset=section.pointer_to_raw_data,
                    file_size=section.raw_size,
                    data=self.path.read_bytes()[
                        section.pointer_to_raw_data:
                        section.pointer_to_raw_data + section.raw_size
                    ],
                )
            )

        return regions