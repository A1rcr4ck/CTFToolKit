#"C:\Users\saran\Downloads\ChromeSetup.exe"
from pathlib import Path

from rev.pe import PEParser


def test_pe_header():

    pe = PEParser(
        Path("C:\\Users\\saran\\Downloads\\ChromeSetup.exe")
    )

    assert pe.header.machine in (
        "x86",
        "x86-64",
    )


def test_pe_sections():

    pe = PEParser(
        Path("C:\\Users\\saran\\Downloads\\ChromeSetup.exe")
    )

    assert len(pe.sections) > 0


def test_pe_imports():

    pe = PEParser(
        Path("C:\\Users\\saran\\Downloads\\ChromeSetup.exe")
    )

    assert len(pe.imports) > 0


def test_pe_exports():

    pe = PEParser(
        Path("C:\\Users\\saran\\Downloads\\ChromeSetup.exe")
    )

    assert len(pe.exports) > 0


def test_pe_resources():

    pe = PEParser(
        Path("C:\\Users\\saran\\Downloads\\ChromeSetup.exe")
    )

    assert len(pe.resources) > 0