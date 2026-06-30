from .base import Cipher
from .frequency import score

class XORCipher(Cipher):
    def encode(self, data: str, key: str, repeat: bool = True) -> str:
        data = data.encode()

        if repeat:
            key = key.encode()

            result = bytes(
                data[i] ^ key[i % len(key)]
                for i in range(len(data))
            )
        else:
            if len(key) != 1:
                raise ValueError("Single-byte XOR requires a one-character key.")

            k = ord(key)

            result = bytes(b ^ k for b in data)

        return result.hex()

    def decode(self, data: str, key: str, repeat: bool = True) -> str:
        data = bytes.fromhex(data)

        if repeat:
            key = key.encode()

            result = bytes(
                data[i] ^ key[i % len(key)]
                for i in range(len(data))
            )
        else:
            if len(key) != 1:
                raise ValueError("Single-byte XOR requires a one-character key.")

            k = ord(key)

            result = bytes(b ^ k for b in data)

        return result.decode(errors="replace")

    def crack(self, data: str, top: int = 10):
        ciphertext = bytes.fromhex(data)

        results = []

        for key in range(256):
            plaintext = "".join(
                chr(byte ^ key)
                if 32 <= (byte ^ key) <= 126
                else "."
                for byte in ciphertext
            )

            results.append(
                (score(plaintext), key, plaintext)
            )

        results.sort(reverse=True)

        return results[:top]