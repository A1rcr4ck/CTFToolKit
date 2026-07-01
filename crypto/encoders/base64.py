import base64

from ..base import Cipher


class Base64Cipher(Cipher):
    def encode(self, data: str) -> str:
        return base64.b64encode(data.encode()).decode()

    def decode(self, data: str) -> str:
        return base64.b64decode(data).decode()