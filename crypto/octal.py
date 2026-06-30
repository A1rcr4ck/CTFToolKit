from .base import Cipher


class OctalCipher(Cipher):
    def encode(self, data: str) -> str:
        return " ".join(format(ord(char), "03o") for char in data)

    def decode(self, data: str) -> str:
        return "".join(chr(int(value, 8)) for value in data.split())