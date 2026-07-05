from crypto.encoders import Base58Cipher


def test_encode():
    cipher = Base58Cipher()
    assert cipher.decode(cipher.encode("hello")) == "hello"


def test_roundtrip():
    cipher = Base58Cipher()

    text = "CTFToolKit"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text