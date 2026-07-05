from crypto.encoders import OctalCipher


def test_encode():
    cipher = OctalCipher()
    assert cipher.encode("A") == "101"


def test_decode():
    cipher = OctalCipher()
    assert cipher.decode("101") == "A"


def test_roundtrip():
    cipher = OctalCipher()

    text = "Hello"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text