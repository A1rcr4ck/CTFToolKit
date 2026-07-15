from pathlib import Path


class FileHexDump:

    def __init__(self, file_path):

        self.file_path = Path(file_path)

    def dump(
        self,
        offset: int = 0,
        size: int = 256,
        width: int = 16,
    ):

        data = self.file_path.read_bytes()

        end = min(offset + size, len(data))

        data = data[offset:end]

        rows = []

        for i in range(0, len(data), width):

            chunk = data[i:i + width]

            hex_bytes = " ".join(
                f"{b:02X}"
                for b in chunk
            )

            ascii_bytes = "".join(
                chr(b)
                if 32 <= b <= 126
                else "."
                for b in chunk
            )

            rows.append(
                {
                    "offset": offset + i,
                    "hex": hex_bytes,
                    "ascii": ascii_bytes,
                }
            )

        return rows