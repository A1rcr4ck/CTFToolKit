import hashlib
from pathlib import Path


class FileHasher:
    """
    Compute common cryptographic hashes for a file.
    """

    CHUNK_SIZE = 8192

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def _calculate(self, algorithm):
        hasher = algorithm()

        with self.file_path.open("rb") as f:
            while chunk := f.read(self.CHUNK_SIZE):
                hasher.update(chunk)

        return hasher.hexdigest()

    def md5(self):
        return self._calculate(hashlib.md5)

    def sha1(self):
        return self._calculate(hashlib.sha1)

    def sha256(self):
        return self._calculate(hashlib.sha256)

    def sha512(self):
        return self._calculate(hashlib.sha512)

    def all(self):
        return {
            "MD5": self.md5(),
            "SHA1": self.sha1(),
            "SHA256": self.sha256(),
            "SHA512": self.sha512(),
        }