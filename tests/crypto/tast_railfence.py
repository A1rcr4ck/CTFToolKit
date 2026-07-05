from crypto.classical import RailFenceCipher


def test_encode():
    cipher = RailFenceCipher()

    assert (
        cipher.encode("WEAREDISCOVEREDFLEEATONCE", 3)
        == "WECRLTEERDSOEEFEAOCAIVDEN"
    )


def test_decode():
    cipher = RailFenceCipher()

    assert (
        cipher.decode(
            "WECRLTEERDSOEEFEAOCAIVDEN",
            3
        )
        == "WEAREDISCOVEREDFLEEATONCE"
    )


def test_roundtrip():
    cipher = RailFenceCipher()

    text = "CTFTOOLKIT"

    encoded = cipher.encode(text, 4)

    assert cipher.decode(encoded, 4) == text