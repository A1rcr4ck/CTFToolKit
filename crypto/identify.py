import base64
import re
import string

from base58 import b58decode


class CryptoIdentifier:

    @staticmethod
    def _is_printable(text: str) -> bool:
        if not text:
            return False

        printable = sum(c in string.printable for c in text)
        return printable / len(text) > 0.95

    def identify(self, text: str):
        text = text.strip()

        candidates = []

        # Binary
        if re.fullmatch(r"(?:[01]{8})(?: [01]{8})*", text):
            candidates.append("Binary")
            return candidates

        # Octal
        if re.fullmatch(r"(?:[0-7]{3})(?: [0-7]{3})*", text):
            candidates.append("Octal")
            return candidates

        # Hex
        if re.fullmatch(r"[0-9A-Fa-f]+", text) and len(text) % 2 == 0:
            try:
                decoded = bytes.fromhex(text).decode()

                if self._is_printable(decoded):
                    candidates.append("Hex")
                    return candidates
            except Exception:
                pass

        # Base64
        try:
            decoded = base64.b64decode(text, validate=True).decode()

            if self._is_printable(decoded):
                candidates.append("Base64")
        except Exception:
            pass

        # Base32
        try:
            decoded = base64.b32decode(text).decode()

            if self._is_printable(decoded):
                candidates.append("Base32")
        except Exception:
            pass

        # Base58
        try:
            decoded = b58decode(text).decode()

            if self._is_printable(decoded):
                candidates.append("Base58")
        except Exception:
            pass

        # Base85
        try:
            decoded = base64.b85decode(text).decode()

            if self._is_printable(decoded):
                candidates.append("Base85")
        except Exception:
            pass

        return candidates