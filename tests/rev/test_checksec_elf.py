from pathlib import Path

from rev.checksec_elf import ELFChecksec


def test_checksec_elf():

    result = ELFChecksec(
        Path("tests/samples/reverse/hello_elf64")
    ).result()

    assert "RELRO" in result
    assert "NX" in result
    assert "PIE" in result
    assert "Canary" in result

def test_checksec_fields():

    result = ELFChecksec(
        Path("tests/samples/reverse/hello_elf64")
    ).result()

    assert isinstance(result["NX"], bool)
    assert isinstance(result["PIE"], bool)
    assert isinstance(result["Canary"], bool)
    assert result["RELRO"] in (
        "None",
        "Partial",
        "Full",
    )