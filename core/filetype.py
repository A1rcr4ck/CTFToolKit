from pathlib import Path


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def is_pcap(filename: str) -> bool:
    return get_extension(filename) in [".pcap", ".pcapng"]


def is_text(filename: str) -> bool:
    return get_extension(filename) == ".txt"


def is_image(filename: str) -> bool:
    return get_extension(filename) in [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
    ]


def is_binary(filename: str) -> bool:
    return get_extension(filename) in [
        ".exe",
        ".dll",
        ".elf",
        ".bin",
        ".so",
    ]