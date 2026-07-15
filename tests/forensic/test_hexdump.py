from forensic.hexdump import FileHexDump


def test_hexdump_rows(tmp_path):

    sample = tmp_path / "sample.bin"

    sample.write_bytes(b"Hello World")

    rows = FileHexDump(sample).dump()

    assert len(rows) == 1

    assert rows[0]["offset"] == 0
    assert rows[0]["ascii"] == "Hello World"


def test_hexdump_offset(tmp_path):

    sample = tmp_path / "sample.bin"

    sample.write_bytes(b"ABCDEFGHIJKLMNOP")

    rows = FileHexDump(sample).dump(
        offset=8,
        size=8,
    )

    assert rows[0]["offset"] == 8
    assert rows[0]["ascii"] == "IJKLMNOP"


def test_hexdump_size(tmp_path):

    sample = tmp_path / "sample.bin"

    sample.write_bytes(bytes(range(64)))

    rows = FileHexDump(sample).dump(size=16)

    assert len(rows) == 1