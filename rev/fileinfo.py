from pathlib import Path
import pefile
from rev.elf import ELFParser
from rev.pe import PEParser


def get_file_info(path: str):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    data = path.read_bytes()

    info = {
        "path": str(path.resolve()),
        "filename": path.name,
        "extension": path.suffix,
        "size": path.stat().st_size,
        "type": "Unknown",
        "architecture": "Unknown",
        "entrypoint": "-",
        "format": "Unknown",
    }

    try:
        if data.startswith(b"\x7fELF"):
            elf = ELFParser(path)

            info["type"] = "ELF"
            info["format"] = "ELF64" if elf.is_64 else "ELF32"
            info["architecture"] = elf.header.machine
            info["entrypoint"] = hex(elf.header.entry)

            return info

        if data.startswith(b"MZ"):
            pe = PEParser(path)

            info["type"] = "PE"

            info["format"] = (
                "PE32+"
                if pe.pe.PE_TYPE == pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS
                else "PE32"
            )

            info["architecture"] = pe.header.machine
            info["entrypoint"] = hex(pe.header.entrypoint)

            return info

    except Exception:
        pass

    return info