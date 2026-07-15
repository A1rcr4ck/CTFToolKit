from forensic.entropy import FileEntropy


def test_zero_entropy(tmp_path):

    sample = tmp_path / "zero.bin"

    sample.write_bytes(b"\x00" * 1024)

    entropy = FileEntropy(sample).entropy()

    assert entropy["Entropy"] == 0.0


def test_high_entropy(tmp_path):

    sample = tmp_path / "high.bin"

    sample.write_bytes(bytes(range(256)))

    entropy = FileEntropy(sample).entropy()

    assert entropy["Entropy"] > 7.5


def test_entropy_contains_keys(tmp_path):

    sample = tmp_path / "sample.bin"

    sample.write_bytes(b"Hello World")

    result = FileEntropy(sample).entropy()

    assert "File" in result
    assert "Size" in result
    assert "Entropy" in result