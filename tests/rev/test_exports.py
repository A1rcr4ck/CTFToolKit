from pathlib import Path

from rev.pe import PEParser


def test_exports():

    pe = PEParser(
        Path(r"C:\Windows\System32\kernel32.dll")
    )

    assert len(pe.exports) > 0