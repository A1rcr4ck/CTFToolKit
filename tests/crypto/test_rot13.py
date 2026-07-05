from crypto.classical import ROT13Cipher


def test_encode():
    cipher = ROT13Cipher()
    assert cipher.encode("HELLO") == "URYYB"


def test_decode():
    cipher = ROT13Cipher()
    assert cipher.decode("URYYB") == "HELLO"


def test_roundtrip():
    cipher = ROT13Cipher()

    text = "CTFToolKit"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text