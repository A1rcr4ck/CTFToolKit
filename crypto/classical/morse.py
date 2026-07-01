from ..base import Cipher


MORSE_CODE = {
    "A": ".-",     "B": "-...",   "C": "-.-.",   "D": "-..",
    "E": ".",      "F": "..-.",   "G": "--.",    "H": "....",
    "I": "..",     "J": ".---",   "K": "-.-",    "L": ".-..",
    "M": "--",     "N": "-.",     "O": "---",    "P": ".--.",
    "Q": "--.-",   "R": ".-.",    "S": "...",    "T": "-",
    "U": "..-",    "V": "...-",   "W": ".--",    "X": "-..-",
    "Y": "-.--",   "Z": "--..",

    "0": "-----",  "1": ".----",  "2": "..---",  "3": "...--",
    "4": "....-",  "5": ".....",  "6": "-....",  "7": "--...",
    "8": "---..",  "9": "----."
}

REVERSE = {v: k for k, v in MORSE_CODE.items()}


class MorseCipher(Cipher):

    def encode(self, data: str) -> str:
        words = []

        for word in data.upper().split():
            letters = []

            for ch in word:
                if ch in MORSE_CODE:
                    letters.append(MORSE_CODE[ch])

            words.append(" ".join(letters))

        return " / ".join(words)

    def decode(self, data: str) -> str:
        words = []

        for word in data.split(" / "):
            letters = []

            for code in word.split():
                letters.append(REVERSE.get(code, "?"))

            words.append("".join(letters))

        return " ".join(words)