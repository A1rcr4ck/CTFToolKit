from forensic.filetype import FileTypeDetector


def test_detect_png(tmp_path):

    sample = tmp_path / "image.png"

    sample.write_bytes(
        b"\x89PNG\r\n\x1A\n"
        + b"\x00" * 32
    )

    result = FileTypeDetector(sample).detect()

    assert result["Type"] == "PNG Image"


def test_detect_pdf(tmp_path):

    sample = tmp_path / "file.pdf"

    sample.write_bytes(
        b"%PDF-1.7"
    )

    result = FileTypeDetector(sample).detect()

    assert result["Type"] == "PDF Document"


def test_detect_unknown(tmp_path):

    sample = tmp_path / "unknown.bin"

    sample.write_bytes(
        b"ABCDEFGH"
    )

    result = FileTypeDetector(sample).detect()

    assert result["Type"] == "Unknown"