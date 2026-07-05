from crypto.modern import RSACipher


def test_keygen():
    rsa = RSACipher()

    d = rsa.generate_private_key(61, 53, 17)

    assert d == 2753


def test_encrypt():
    rsa = RSACipher()

    assert rsa.encrypt(65, 17, 3233) == 2790


def test_decrypt():
    rsa = RSACipher()

    assert rsa.decrypt(2790, 2753, 3233) == 65