import hashlib


class HashToolkit:

    ALGORITHMS = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha224": hashlib.sha224,
        "sha256": hashlib.sha256,
        "sha384": hashlib.sha384,
        "sha512": hashlib.sha512,
    }

    def generate(self, algorithm: str, text: str) -> str:
        algorithm = algorithm.lower()

        if algorithm not in self.ALGORITHMS:
            raise ValueError("Unsupported hash algorithm.")

        return self.ALGORITHMS[algorithm](text.encode()).hexdigest()