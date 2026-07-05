from pathlib import Path
import re


ASCII_PATTERN = re.compile(rb"[\x20-\x7E]{4,}")


def extract_ascii(data: bytes, min_length: int):
    pattern = re.compile(rb"[\x20-\x7E]{%d,}" % min_length)
    return [match.decode("ascii", errors="ignore")
            for match in pattern.findall(data)]


def extract_utf16le(data: bytes, min_length: int):
    strings = []

    pattern = re.compile(
        rb"(?:[\x20-\x7E]\x00){%d,}" % min_length
    )

    for match in pattern.findall(data):
        try:
            strings.append(match.decode("utf-16le"))
        except UnicodeDecodeError:
            pass

    return strings


def extract_utf16be(data: bytes, min_length: int):
    strings = []

    pattern = re.compile(
        rb"(?:\x00[\x20-\x7E]){%d,}" % min_length
    )

    for match in pattern.findall(data):
        try:
            strings.append(match.decode("utf-16be"))
        except UnicodeDecodeError:
            pass

    return strings


def extract_strings(path: str, min_length: int = 4):
    data = Path(path).read_bytes()

    results = []
    seen = set()

    for string in (
        extract_ascii(data, min_length)
        + extract_utf16le(data, min_length)
        + extract_utf16be(data, min_length)
    ):
        if string not in seen:
            seen.add(string)
            results.append(string)

    return results