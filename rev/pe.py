from pathlib import Path

import pefile


MACHINE_TYPES = {
    0x014C: "x86",
    0x8664: "x86-64",
    0x01C0: "ARM",
    0xAA64: "ARM64",
}

SUBSYSTEMS = {
    1: "Native",
    2: "Windows GUI",
    3: "Windows CUI",
    5: "OS/2 CUI",
    7: "POSIX CUI",
    9: "Windows CE GUI",
    10: "EFI Application",
    11: "EFI Boot Service Driver",
    12: "EFI Runtime Driver",
}


class PEParser:

    def __init__(self, path: str):
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(self.path)

        self.pe = pefile.PE(str(self.path))

    @property
    def header(self):
        return {
            "machine": MACHINE_TYPES.get(
                self.pe.FILE_HEADER.Machine,
                hex(self.pe.FILE_HEADER.Machine),
            ),
            "timestamp": self.pe.FILE_HEADER.TimeDateStamp,
            "sections": self.pe.FILE_HEADER.NumberOfSections,
            "entrypoint": hex(
                self.pe.OPTIONAL_HEADER.AddressOfEntryPoint
            ),
            "imagebase": hex(
                self.pe.OPTIONAL_HEADER.ImageBase
            ),
            "subsystem": SUBSYSTEMS.get(
                self.pe.OPTIONAL_HEADER.Subsystem,
                "Unknown",
            ),
            "dll": self.pe.is_dll(),
        }

    @property
    def sections(self):
        sections = []

        for section in self.pe.sections:
            sections.append({
                "name": section.Name.decode(errors="ignore").rstrip("\x00"),
                "virtual_address": hex(section.VirtualAddress),
                "virtual_size": section.Misc_VirtualSize,
                "raw_size": section.SizeOfRawData,
                "entropy": round(section.get_entropy(), 2),
                "characteristics": hex(section.Characteristics),
            })

        return sections

    @property
    def imports(self):
        imports = {}

        if not hasattr(self.pe, "DIRECTORY_ENTRY_IMPORT"):
            return imports

        for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
            dll = entry.dll.decode(errors="ignore")

            imports[dll] = []

            for imp in entry.imports:
                imports[dll].append(
                    imp.name.decode(errors="ignore")
                    if imp.name
                    else f"Ordinal {imp.ordinal}"
                )

        return imports

    @property
    def exports(self):
        exports = []

        if not hasattr(self.pe, "DIRECTORY_ENTRY_EXPORT"):
            return exports

        for symbol in self.pe.DIRECTORY_ENTRY_EXPORT.symbols:
            exports.append(
                symbol.name.decode(errors="ignore")
                if symbol.name
                else f"Ordinal {symbol.ordinal}"
            )

        return exports