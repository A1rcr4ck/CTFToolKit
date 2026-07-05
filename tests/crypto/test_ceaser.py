from crypto.classical import CaesarCipher


def test_encode():
    cipher = CaesarCipher()
    assert cipher.encode("HELLO", 3) == "KHOOR"


def test_decode():
    cipher = CaesarCipher()
    assert cipher.decode("KHOOR", 3) == "HELLO"


def test_roundtrip():
    cipher = CaesarCipher()

    text = "CTFTOOLKIT"

    encoded = cipher.encode(text, 7)

    assert cipher.decode(encoded, 7) == text


def test_crack():
    cipher = CaesarCipher()

    results = cipher.crack("KHOOR")

    assert any(text == "HELLO" for _, text in results)