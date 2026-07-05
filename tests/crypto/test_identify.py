from crypto.identify import CryptoIdentifier


def test_base64():
    c = CryptoIdentifier()

    result = c.identify("aGVsbG8=")

    assert "Base64" in result


def test_hex():
    c = CryptoIdentifier()

    result = c.identify("68656c6c6f")

    assert "Hex" in result


def test_binary():
    c = CryptoIdentifier()

    result = c.identify(
        "01101000 01100101 01101100 01101100 01101111"
    )

    assert "Binary" in result