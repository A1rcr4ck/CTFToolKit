import string
from pathlib import Path


class StringsExtractor:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def extract(self, min_length=4):

        with self.file_path.open("rb") as f:
            data = f.read()

        result = []
        current = []

        for byte in data:

            char = chr(byte)

            if char in string.printable and char not in "\r\n\t\x0b\x0c":
                current.append(char)
            else:
                if len(current) >= min_length:
                    result.append("".join(current))
                current = []

        if len(current) >= min_length:
            result.append("".join(current))

        return result