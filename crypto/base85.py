import base64

from .base import Cipher


class Base85Cipher(Cipher):
    def encode(self, data: str) -> str:
        return base64.b85encode(data.encode()).decode()

    def decode(self, data: str) -> str:
        return base64.b85decode(data).decode()
    