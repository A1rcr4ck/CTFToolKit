from crypto.encoders import Base64Cipher


def test_encode():
    cipher = Base64Cipher()
    assert cipher.encode("hello") == "aGVsbG8="


def test_decode():
    cipher = Base64Cipher()
    assert cipher.decode("aGVsbG8=") == "hello"


def test_roundtrip():
    cipher = Base64Cipher()

    text = "CTFToolKit"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text