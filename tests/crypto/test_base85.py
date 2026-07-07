from crypto.encoders import Base85Cipher


def test_encode():
    cipher = Base85Cipher()
    assert cipher.decode(cipher.encode("hello")) == "hello"


def test_roundtrip():
    cipher = Base85Cipher()

    text = "CTFToolKit"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text