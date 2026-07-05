from crypto.solver import CryptoSolver


def test_base64():
    solver = CryptoSolver()

    history = solver.solve("aGVsbG8=")

    assert history[-1][1] == "hello"


def test_double_base64():
    solver = CryptoSolver()

    history = solver.solve("YUdWc2JHOD0=")

    assert history[-1][1] == "hello"