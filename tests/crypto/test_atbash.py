from crypto.classical import AtbashCipher


def test_encode():
    cipher = AtbashCipher()
    assert cipher.encode("HELLO") == "SVOOL"


def test_decode():
    cipher = AtbashCipher()
    assert cipher.decode("SVOOL") == "HELLO"


def test_roundtrip():
    cipher = AtbashCipher()

    text = "CTFTOOLKIT"

    encoded = cipher.encode(text)

    assert cipher.decode(encoded) == text