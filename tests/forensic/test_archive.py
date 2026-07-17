import zipfile
import gzip
import tarfile
from forensic.archive import ArchiveInspector


def test_zip_archive(tmp_path):

    archive = tmp_path / "sample.zip"

    with zipfile.ZipFile(archive, "w") as z:

        z.writestr("hello.txt", "Hello")
        z.writestr("flag.txt", "CTF{TEST}")

    result = ArchiveInspector(archive).inspect()

    assert result["Archive Type"] == "ZIP"
    assert result["File Count"] == 2


def test_zip_contains_files(tmp_path):

    archive = tmp_path / "sample.zip"

    with zipfile.ZipFile(archive, "w") as z:

        z.writestr("test.txt", "ABC")

    result = ArchiveInspector(archive).inspect()

    assert result["Files"][0]["Name"] == "test.txt"

def test_tar_archive(tmp_path):

    archive = tmp_path / "sample.tar"

    file = tmp_path / "hello.txt"
    file.write_text("Hello")

    with tarfile.open(archive, "w") as tar:
        tar.add(file, arcname="hello.txt")

    result = ArchiveInspector(archive).inspect()

    assert result["Archive Type"] == "TAR"
    assert result["File Count"] == 1

def test_gzip_archive(tmp_path):

    archive = tmp_path / "sample.gz"

    with gzip.open(archive, "wb") as gz:
        gz.write(b"Hello World")

    result = ArchiveInspector(archive).inspect()

    assert result["Archive Type"] == "GZIP"
