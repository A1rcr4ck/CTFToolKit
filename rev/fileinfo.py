from pathlib import Path

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
            info["format"] = elf.header["class"]
            info["architecture"] = elf.header["machine"]
            info["entrypoint"] = elf.header["entry"]

            return info

        if data.startswith(b"MZ"):
            pe = PEParser(path)

            info["type"] = "PE"
            info["format"] = "PE32+"
            info["architecture"] = pe.header["machine"]
            info["entrypoint"] = pe.header["entrypoint"]

            return info

    except Exception:
        pass

    return info