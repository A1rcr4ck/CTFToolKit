from forensic.strings import StringsExtractor


def test_extract_strings(tmp_path):

    sample = tmp_path / "sample.bin"

    sample.write_bytes(
        b"\x00Hello\x00World123\x00ABC\x00Python\x00"
    )

    strings = StringsExtractor(sample).extract()

    assert "Hello" in strings
    assert "World123" in strings
    assert "Python" in strings
    assert "ABC" not in strings


def test_min_length(tmp_path):

    sample = tmp_path / "sample.bin"

    sample.write_bytes(
        b"\x00Test\x00ABCDE\x00ABCDEFG\x00"
    )

    strings = StringsExtractor(sample).extract(6)

    assert "ABCDEFG" in strings
    assert "ABCDE" not in strings
    assert "Test" not in strings