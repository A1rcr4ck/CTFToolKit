from math import gcd

from ..base import Cipher


class AffineCipher(Cipher):

    def mod_inverse(self, a: int, m: int) -> int:
        for i in range(m):
            if (a * i) % m == 1:
                return i
        raise ValueError(f"{a} has no modular inverse modulo {m}")

    def encode(self, data: str, a: int, b: int) -> str:
        if gcd(a, 26) != 1:
            raise ValueError("Key 'a' must be coprime with 26.")

        result = []

        for ch in data:
            if ch.isupper():
                x = ord(ch) - ord("A")
                result.append(chr(((a * x + b) % 26) + ord("A")))
            elif ch.islower():
                x = ord(ch) - ord("a")
                result.append(chr(((a * x + b) % 26) + ord("a")))
            else:
                result.append(ch)

        return "".join(result)

    def decode(self, data: str, a: int, b: int) -> str:
        if gcd(a, 26) != 1:
            raise ValueError("Key 'a' must be coprime with 26.")

        inv = self.mod_inverse(a, 26)

        result = []

        for ch in data:
            if ch.isupper():
                y = ord(ch) - ord("A")
                result.append(chr(((inv * (y - b)) % 26) + ord("A")))
            elif ch.islower():
                y = ord(ch) - ord("a")
                result.append(chr(((inv * (y - b)) % 26) + ord("a")))
            else:
                result.append(ch)

        return "".join(result)