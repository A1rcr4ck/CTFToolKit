from crypto.analyzer import CryptoAnalyzer


def test_entropy():
    analyzer = CryptoAnalyzer()

    assert analyzer.entropy("AAAA") == 0


def test_ioc():
    analyzer = CryptoAnalyzer()

    assert analyzer.ioc("AAAA") == 1.0


def test_frequency():
    analyzer = CryptoAnalyzer()

    freq = analyzer.frequency("AABB")

    assert freq["A"] == 50.0
    assert freq["B"] == 50.0