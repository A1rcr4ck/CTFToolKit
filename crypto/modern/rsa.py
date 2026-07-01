from ..base import Cipher


class RSACipher(Cipher):

    def gcd(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def egcd(self, a: int, b: int):
        if a == 0:
            return b, 0, 1

        gcd, x1, y1 = self.egcd(b % a, a)

        x = y1 - (b // a) * x1
        y = x1

        return gcd, x, y

    def mod_inverse(self, e: int, phi: int) -> int:
        gcd, x, _ = self.egcd(e, phi)

        if gcd != 1:
            raise ValueError("Inverse does not exist.")

        return x % phi

    def generate_private_key(self, p: int, q: int, e: int):
        phi = (p - 1) * (q - 1)
        d = self.mod_inverse(e, phi)
        return d

    def encrypt(self, plaintext: int, e: int, n: int) -> int:
        return pow(plaintext, e, n)

    def decrypt(self, ciphertext: int, d: int, n: int) -> int:
        return pow(ciphertext, d, n)

    def encode(self, data: str):
        raise NotImplementedError

    def decode(self, data: str):
        raise NotImplementedError