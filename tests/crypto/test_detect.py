from crypto.detect import Detector


def test_detect_base64():

    detector = Detector()

    results = detector.detect("aGVsbG8=")

    assert any(name == "Base64" for name, _ in results)


def test_detect_binary():

    detector = Detector()

    results = detector.detect(
        "01101000 01100101 01101100 01101100 01101111"
    )

    assert any(name == "Binary" for name, _ in results)