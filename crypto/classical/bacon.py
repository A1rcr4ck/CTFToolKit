from ..base import Cipher


class BaconCipher(Cipher):
    ALPHABET = {
        "A": "AAAAA", "B": "AAAAB", "C": "AAABA", "D": "AAABB",
        "E": "AABAA", "F": "AABAB", "G": "AABBA", "H": "AABBB",
        "I": "ABAAA", "J": "ABAAB", "K": "ABABA", "L": "ABABB",
        "M": "ABBAA", "N": "ABBAB", "O": "ABBBA", "P": "ABBBB",
        "Q": "BAAAA", "R": "BAAAB", "S": "BAABA", "T": "BAABB",
        "U": "BABAA", "V": "BABAB", "W": "BABBA", "X": "BABBB",
        "Y": "BBAAA", "Z": "BBAAB",
    }

    REVERSE = {v: k for k, v in ALPHABET.items()}

    def encode(self, data: str) -> str:
        result = []

        for ch in data.upper():
            if ch == " ":
                result.append("/")
            elif ch in self.ALPHABET:
                result.append(self.ALPHABET[ch])

        return " ".join(result)

    def decode(self, data: str) -> str:
        result = []

        for token in data.split():
            if token == "/":
                result.append(" ")
            else:
                result.append(self.REVERSE.get(token, "?"))

        return "".join(result)