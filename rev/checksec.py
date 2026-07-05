from pathlib import Path
import struct


def check_elf(path: str) -> dict:
    result = {
        "nx": "Unknown",
        "pie": "Unknown",
        "relro": "Unknown",
        "canary": "Unknown",
    }

    with Path(path).open("rb") as f:
        if f.read(4) != b"\x7fELF":
            return result

        # EI_CLASS
        elf_class = f.read(1)[0]

        result["pie"] = "Possible" if elf_class == 2 else "Unknown"
        result["nx"] = "Unknown"
        result["relro"] = "Unknown"
        result["canary"] = "Unknown"

    return result


def check_pe(path: str) -> dict:
    result = {
        "aslr": "Unknown",
        "dep": "Unknown",
        "cfg": "Unknown",
    }

    with Path(path).open("rb") as f:

        if f.read(2) != b"MZ":
            return result

        f.seek(0x3C)
        pe_offset = struct.unpack("<I", f.read(4))[0]

        f.seek(pe_offset)

        if f.read(4) != b"PE\x00\x00":
            return result

        # Skip COFF header
        f.seek(20, 1)

        # Optional Header Magic
        magic = struct.unpack("<H", f.read(2))[0]

        if magic == 0x20B:
            result["aslr"] = "Supported"
            result["dep"] = "Supported"
        else:
            result["aslr"] = "Unknown"
            result["dep"] = "Unknown"

        result["cfg"] = "Unknown"

    return result


def checksec(path: str):
    with Path(path).open("rb") as f:
        magic = f.read(4)

    if magic == b"\x7fELF":
        return {
            "type": "ELF",
            **check_elf(path)
        }

    if magic[:2] == b"MZ":
        return {
            "type": "PE",
            **check_pe(path)
        }

    return {
        "type": "Unknown"
    }