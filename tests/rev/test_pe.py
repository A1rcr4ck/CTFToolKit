from rev.pe import PEParser


def test_pe_header():
    pe = PEParser(r"C:\Users\saran\Downloads\ChromeSetup.exe")

    assert pe.header["machine"] in ("x86", "x86-64")