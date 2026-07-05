from crypto.encoders import HexCipher


def test_encode():
    cipher = HexCipher()
    assert cipher.encode("hello") == "68656c6c6f"


def test_decode():
    cipher = HexCipher()
    assert cipher.decode("68656c6c6f") == "hello"


def test_roundtrip():
    cipher = HexCipher()

    text = "OpenAI"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text