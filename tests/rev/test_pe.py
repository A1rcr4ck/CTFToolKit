
from pathlib import Path

from rev.pe import PEParser


def test_pe_header():

    pe = PEParser(
        Path("tests/samples/reverse/hello64.exe")
    )

    assert pe.header.machine == "x86-64"


def test_pe_sections():

    pe = PEParser(
        Path("tests/samples/reverse/hello64.exe")
    )

    assert len(pe.sections) > 0


def test_pe_imports():

    pe = PEParser(
        Path("tests/samples/reverse/hello64.exe")
    )

    assert len(pe.imports) > 0


def test_pe_exports():

    pe = PEParser(
        Path("tests/samples/reverse/resources.exe")
    )

    assert len(pe.exports) > 0


def test_pe_resources():

    pe = PEParser(
        Path("tests/samples/reverse/resources.exe")
    )

    assert len(pe.resources) > 0

def test_pe32_header():

    pe = PEParser(
        Path("tests/samples/reverse/hello32.exe")
    )

    assert pe.header.machine == "x86"