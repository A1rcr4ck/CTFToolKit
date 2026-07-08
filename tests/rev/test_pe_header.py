from pathlib import Path

from rev.pe import PEParser


def test_pe_header():

    pe = PEParser(
        Path("tests/samples/reverse/hello64.exe")
    )

    assert pe.header.machine == "x86-64"
    assert pe.header.sections > 0