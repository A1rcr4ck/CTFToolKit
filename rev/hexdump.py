from rev.reader import BinaryReader


class HexDump:

    def __init__(self, reader: BinaryReader):

        self.reader = reader

    def dump(
        self,
        address: int,
        size: int = 256,
        width: int = 16,
    ):

        data = self.reader.read(address, size)

        lines = []

        for i in range(0, len(data), width):

            chunk = data[i:i + width]

            hex_bytes = " ".join(
                f"{b:02x}"
                for b in chunk
            )

            ascii_bytes = "".join(
                chr(b)
                if 32 <= b <= 126
                else "."
                for b in chunk
            )

            lines.append(
                (
                    address + i,
                    hex_bytes,
                    ascii_bytes,
                )
            )

        return lines