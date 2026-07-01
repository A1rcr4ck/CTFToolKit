from collections import Counter
from math import log2


class CryptoAnalyzer:

    def frequency(self, text: str):
        text = text.upper()

        letters = [c for c in text if c.isalpha()]

        total = len(letters)

        if total == 0:
            return {}

        counter = Counter(letters)

        return {
            k: round((v / total) * 100, 2)
            for k, v in sorted(counter.items())
        }

    def entropy(self, text: str):
        if not text:
            return 0

        counter = Counter(text)

        length = len(text)

        entropy = 0

        for count in counter.values():
            p = count / length
            entropy -= p * log2(p)

        return round(entropy, 4)

    def ioc(self, text: str):
        text = "".join(c for c in text.upper() if c.isalpha())

        n = len(text)

        if n <= 1:
            return 0

        counter = Counter(text)

        numerator = sum(v * (v - 1) for v in counter.values())

        denominator = n * (n - 1)

        return round(numerator / denominator, 6)