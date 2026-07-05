from crypto.classical import MorseCipher


def test_encode():
    cipher = MorseCipher()

    assert cipher.encode("SOS") == "... --- ..."


def test_decode():
    cipher = MorseCipher()

    assert cipher.decode("... --- ...") == "SOS"


def test_roundtrip():
    cipher = MorseCipher()

    text = "HELLO WORLD"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text