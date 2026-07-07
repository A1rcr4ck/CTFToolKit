from rev.pe import PEParser


def pe_checksec(path):

    pe = PEParser(path)

    dll = pe.pe.OPTIONAL_HEADER.DllCharacteristics

    return {
        "ASLR": bool(dll & 0x40),               # IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE
        "DEP": bool(dll & 0x0100),              # NX_COMPAT
        "HighEntropyVA": bool(dll & 0x20),      # HIGH_ENTROPY_VA
        "CFG": bool(dll & 0x4000),              # GUARD_CF
        "TerminalServerAware": bool(dll & 0x8000),
    }