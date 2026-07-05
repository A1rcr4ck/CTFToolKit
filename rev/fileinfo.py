from pathlib import Path
import mimetypes
import os
import stat
import struct


ELF_MAGIC = b"\x7fELF"
PE_MAGIC = b"MZ"

MACHO_MAGICS = {
    b"\xfe\xed\xfa\xce",
    b"\xfe\xed\xfa\xcf",
    b"\xce\xfa\xed\xfe",
    b"\xcf\xfa\xed\xfe",
    b"\xca\xfe\xba\xbe",
    b"\xbe\xba\xfe\xca",
}


ELF_ARCH = {
    3: "x86",
    40: "ARM",
    62: "x86-64",
    183: "AArch64",
}

PE_ARCH = {
    0x14C: "x86",
    0x8664: "x86-64",
    0xAA64: "ARM64",
}


def get_size(path: str) -> int:
    return Path(path).stat().st_size


def get_extension(path: str) -> str:
    return Path(path).suffix


def get_mime_type(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    return mime or "Unknown"


def is_executable(path: str) -> bool:
    if os.name == "nt":
        return Path(path).suffix.lower() in {
            ".exe",
            ".dll",
            ".bat",
            ".cmd",
            ".com",
        }

    mode = os.stat(path).st_mode
    return bool(mode & stat.S_IXUSR)


def detect_binary_type(path: str) -> str:
    with open(path, "rb") as f:
        magic = f.read(4)

    if magic == ELF_MAGIC:
        return "ELF"

    if magic[:2] == PE_MAGIC:
        return "PE"

    if magic in MACHO_MAGICS:
        return "Mach-O"

    return "Unknown"


def detect_architecture(path: str) -> str:
    binary_type = detect_binary_type(path)

    with open(path, "rb") as f:

        if binary_type == "ELF":
            f.seek(18)
            machine = struct.unpack("<H", f.read(2))[0]
            return ELF_ARCH.get(machine, "Unknown")

        elif binary_type == "PE":
            f.seek(0x3C)
            pe_offset = struct.unpack("<I", f.read(4))[0]

            f.seek(pe_offset + 4)
            machine = struct.unpack("<H", f.read(2))[0]

            return PE_ARCH.get(machine, "Unknown")

    return "Unknown"


def get_file_info(path: str) -> dict:
    p = Path(path)

    return {
        "path": str(p.resolve()),
        "filename": p.name,
        "extension": get_extension(path),
        "size": get_size(path),
        "mime": get_mime_type(path),
        "type": detect_binary_type(path),
        "architecture": detect_architecture(path),
        "is_executable": is_executable(path),
    }