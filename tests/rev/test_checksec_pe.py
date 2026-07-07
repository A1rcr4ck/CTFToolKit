from pathlib import Path

from rev.checksec_pe import pe_checksec


def test_checksec():

    result = pe_checksec(
        Path("C:\\Users\\saran\\Downloads\\ChromeSetup.exe")
    )

    assert "ASLR" in result
    assert "DEP" in result