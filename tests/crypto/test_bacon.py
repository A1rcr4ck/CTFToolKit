from crypto.classical import BaconCipher


def test_encode():
    cipher = BaconCipher()

    assert cipher.encode("ABC") == "AAAAA AAAAB AAABA"


def test_decode():
    cipher = BaconCipher()

    assert cipher.decode("AAAAA AAAAB AAABA") == "ABC"


def test_roundtrip():
    cipher = BaconCipher()

    text = "HELLO"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text