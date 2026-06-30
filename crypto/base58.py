from base58 import b58encode, b58decode

from .base import Cipher


class Base58Cipher(Cipher):
    def encode(self, data: str) -> str:
        return b58encode(data.encode()).decode()

    def decode(self, data: str) -> str:
        return b58decode(data).decode()