from pathlib import Path


def file_exists(path: str) -> bool:
    return Path(path).exists()


def get_extension(path: str):
    return Path(path).suffix.lower()


def get_filename(path: str):
    return Path(path).name