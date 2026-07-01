import base64

from base58 import b58decode

from crypto.encoders import (
    Base64Cipher,
    Base32Cipher,
    Base58Cipher,
    Base85Cipher,
    HexCipher,
    BinaryCipher,
    OctalCipher,
)


class CryptoSolver:

    def solve(self, text: str):

        history = []

        while True:

            changed = False

            # Hex
            try:
                decoded = HexCipher().decode(text)

                if decoded != text:
                    history.append(("Hex", decoded))
                    text = decoded
                    changed = True
                    continue
            except Exception:
                pass

            # Base64
            try:
                decoded = Base64Cipher().decode(text)

                if decoded != text:
                    history.append(("Base64", decoded))
                    text = decoded
                    changed = True
                    continue
            except Exception:
                pass

            # Base32
            try:
                decoded = Base32Cipher().decode(text)

                if decoded != text:
                    history.append(("Base32", decoded))
                    text = decoded
                    changed = True
                    continue
            except Exception:
                pass

            # Base58
            try:
                decoded = Base58Cipher().decode(text)

                if decoded != text:
                    history.append(("Base58", decoded))
                    text = decoded
                    changed = True
                    continue
            except Exception:
                pass

            # Base85
            try:
                decoded = Base85Cipher().decode(text)

                if decoded != text:
                    history.append(("Base85", decoded))
                    text = decoded
                    changed = True
                    continue
            except Exception:
                pass

            # Binary
            try:
                decoded = BinaryCipher().decode(text)

                if decoded != text:
                    history.append(("Binary", decoded))
                    text = decoded
                    changed = True
                    continue
            except Exception:
                pass

            # Octal
            try:
                decoded = OctalCipher().decode(text)

                if decoded != text:
                    history.append(("Octal", decoded))
                    text = decoded
                    changed = True
                    continue
            except Exception:
                pass

            if not changed:
                break

        return history