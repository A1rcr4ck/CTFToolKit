import base64
import string

from base58 import b58decode


class Detector:
    def detect(self, text: str):
        results = []

        text = text.strip()

        # Binary
        if all(c in "01 " for c in text):
            try:
                decoded = "".join(chr(int(x, 2)) for x in text.split())
                return [("Binary", decoded)]
            except Exception:
                pass

        # Octal
        if all(c in "01234567 " for c in text):
            try:
                decoded = "".join(chr(int(x, 8)) for x in text.split())
                return [("Octal", decoded)]
            except Exception:
                pass

        # Hex
        if len(text) % 2 == 0:
            try:
                decoded = bytes.fromhex(text).decode()
                return [("Hex", decoded)]
            except Exception:
                pass

        # Base64
        try:
            decoded = base64.b64decode(text, validate=True).decode()
            results.append(("Base64", decoded))
        except Exception:
            pass

        # Base32
        try:
            decoded = base64.b32decode(text).decode()
            results.append(("Base32", decoded))
        except Exception:
            pass

        # Base85
        try:
            decoded = base64.b85decode(text).decode()
            results.append(("Base85", decoded))
        except Exception:
            pass

        # Base58
        try:
            decoded = b58decode(text).decode()
            results.append(("Base58", decoded))
        except Exception:
            pass

        return results