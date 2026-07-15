from forensic.fileinfo import FileInfo


def test_file_info(tmp_path):

    sample = tmp_path / "hello.txt"

    sample.write_text("Hello World")

    info = FileInfo(sample).info()

    assert info["Name"] == "hello.txt"
    assert info["Extension"] == ".txt"
    assert info["Size (Bytes)"] == 11
    assert "Created" in info
    assert "Modified" in info
    assert "Absolute Path" in info


def test_format_size(tmp_path):

    sample = tmp_path / "a.bin"

    sample.write_bytes(b"A" * 2048)

    info = FileInfo(sample).info()

    assert info["Size"] == "2.00 KB"