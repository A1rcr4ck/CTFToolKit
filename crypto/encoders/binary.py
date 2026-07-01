from ..base import Cipher


class BinaryCipher(Cipher):
    def encode(self, data: str) -> str:
        return " ".join(format(ord(char), "08b") for char in data)

    def decode(self, data: str) -> str:
        return "".join(chr(int(bits, 2)) for bits in data.split())