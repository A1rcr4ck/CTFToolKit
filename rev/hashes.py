import hashlib
from pathlib import Path


def _calculate_hash(path: str, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)

    with Path(path).open("rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()


def get_hashes(path: str) -> dict:
    return {
        "md5": _calculate_hash(path, "md5"),
        "sha1": _calculate_hash(path, "sha1"),
        "sha256": _calculate_hash(path, "sha256"),
    }