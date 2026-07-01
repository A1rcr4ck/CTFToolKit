from ..base import Cipher


class AtbashCipher(Cipher):
    def encode(self, data: str) -> str:
        result = ""

        for char in data:
            if char.isupper():
                result += chr(ord("Z") - (ord(char) - ord("A")))
            elif char.islower():
                result += chr(ord("z") - (ord(char) - ord("a")))
            else:
                result += char

        return result

    def decode(self, data: str) -> str:
        return self.encode(data)