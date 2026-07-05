from crypto.encoders import BinaryCipher


def test_encode():
    cipher = BinaryCipher()
    assert cipher.encode("A") == "01000001"


def test_decode():
    cipher = BinaryCipher()
    assert cipher.decode("01000001") == "A"


def test_roundtrip():
    cipher = BinaryCipher()

    text = "Hello"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text