from pathlib import Path


def read_input(value: str) -> str:
    """
    If value is a file, return its contents.
    Otherwise return the value itself.
    """

    path = Path(value)

    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8").strip()

    return value