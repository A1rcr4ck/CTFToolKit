from ..base import Cipher


class CaesarCipher(Cipher):
    def encode(self, data: str, shift: int) -> str:
        result = ""

        for char in data:
            if char.isalpha():
                base = ord("A") if char.isupper() else ord("a")
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char

        return result

    def decode(self, data: str, shift: int) -> str:
        return self.encode(data, -shift)

    def crack(self, data: str):
        results = []

        for shift in range(26):
            results.append(
                (shift, self.decode(data, shift))
            )

        return results