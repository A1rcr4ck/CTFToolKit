from ..base import Cipher


class VigenereCipher(Cipher):
    def _shift(self, char: str, key_char: str, encrypt: bool = True) -> str:
        if not char.isalpha():
            return char

        base = ord("A") if char.isupper() else ord("a")
        key = ord(key_char.lower()) - ord("a")

        if not encrypt:
            key = -key

        return chr((ord(char) - base + key) % 26 + base)

    def encode(self, data: str, key: str) -> str:
        result = []
        j = 0

        for char in data:
            if char.isalpha():
                result.append(self._shift(char, key[j % len(key)], True))
                j += 1
            else:
                result.append(char)

        return "".join(result)

    def decode(self, data: str, key: str) -> str:
        result = []
        j = 0

        for char in data:
            if char.isalpha():
                result.append(self._shift(char, key[j % len(key)], False))
                j += 1
            else:
                result.append(char)

        return "".join(result)