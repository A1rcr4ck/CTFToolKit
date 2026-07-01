from .caesar import CaesarCipher


class ROT13Cipher(CaesarCipher):
    def encode(self, data: str) -> str:
        return super().encode(data, 13)

    def decode(self, data: str) -> str:
        return super().decode(data, 13)