from crypto.hash import HashToolkit


def test_md5():
    h = HashToolkit()

    assert (
        h.generate("md5", "hello")
        == "5d41402abc4b2a76b9719d911017c592"
    )


def test_sha256():
    h = HashToolkit()

    assert (
        h.generate("sha256", "hello")
        == "2cf24dba5fb0a30e26e83b2ac5b9e29e"
           "1b161e5c1fa7425e73043362938b9824"
    )