from crypto.classical import VigenereCipher


def test_encode():
    cipher = VigenereCipher()
    assert cipher.encode("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"


def test_decode():
    cipher = VigenereCipher()
    assert cipher.decode("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"


def test_roundtrip():
    cipher = VigenereCipher()

    text = "CTFTOOLKIT"

    encoded = cipher.encode(text, "KEY")

    assert cipher.decode(encoded, "KEY") == text