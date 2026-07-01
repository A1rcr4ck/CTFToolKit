from ..base import Cipher


class HexCipher(Cipher):
    def encode(self, data: str) -> str:
        return data.encode().hex()

    def decode(self, data: str) -> str:
        return bytes.fromhex(data).decode()