import hashlib

from forensic.hashing import FileHasher


def test_md5(tmp_path):

    sample = tmp_path / "sample.txt"
    sample.write_text("hello world")

    hasher = FileHasher(sample)

    expected = hashlib.md5(b"hello world").hexdigest()

    assert hasher.md5() == expected


def test_sha1(tmp_path):

    sample = tmp_path / "sample.txt"
    sample.write_text("hello world")

    hasher = FileHasher(sample)

    expected = hashlib.sha1(b"hello world").hexdigest()

    assert hasher.sha1() == expected


def test_sha256(tmp_path):

    sample = tmp_path / "sample.txt"
    sample.write_text("hello world")

    hasher = FileHasher(sample)

    expected = hashlib.sha256(b"hello world").hexdigest()

    assert hasher.sha256() == expected


def test_sha512(tmp_path):

    sample = tmp_path / "sample.txt"
    sample.write_text("hello world")

    hasher = FileHasher(sample)

    expected = hashlib.sha512(b"hello world").hexdigest()

    assert hasher.sha512() == expected


def test_all_hashes(tmp_path):

    sample = tmp_path / "sample.txt"
    sample.write_text("hello world")

    hashes = FileHasher(sample).all()

    assert hashes["MD5"] == hashlib.md5(b"hello world").hexdigest()
    assert hashes["SHA1"] == hashlib.sha1(b"hello world").hexdigest()
    assert hashes["SHA256"] == hashlib.sha256(b"hello world").hexdigest()
    assert hashes["SHA512"] == hashlib.sha512(b"hello world").hexdigest()