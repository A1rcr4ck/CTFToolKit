from crypto.classical import AffineCipher


def test_roundtrip():
    cipher = AffineCipher()

    text = "HELLOWORLD"

    encoded = cipher.encode(text, 5, 8)

    assert cipher.decode(encoded, 5, 8) == text


def test_encode_decode():
    cipher = AffineCipher()

    plaintext = "AFFINECIPHER"

    encoded = cipher.encode(plaintext, 5, 8)

    decoded = cipher.decode(encoded, 5, 8)

    assert decoded == plaintext