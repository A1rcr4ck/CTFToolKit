import base64

from ..base import Cipher


class Base32Cipher(Cipher):
    def encode(self, data: str) -> str:
        return base64.b32encode(data.encode()).decode()

    def decode(self, data: str) -> str:
        return base64.b32decode(data).decode()