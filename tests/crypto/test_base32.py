from crypto.encoders import Base32Cipher


def test_encode():
    cipher = Base32Cipher()
    assert cipher.encode("hello") == "NBSWY3DP"


def test_decode():
    cipher = Base32Cipher()
    assert cipher.decode("NBSWY3DP") == "hello"


def test_roundtrip():
    cipher = Base32Cipher()

    text = "CTFToolKit"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text