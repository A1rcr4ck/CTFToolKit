import math
from pathlib import Path


class FileEntropy:

    def __init__(self, file_path):

        self.file_path = Path(file_path)

    @staticmethod
    def calculate(data: bytes) -> float:

        if not data:
            return 0.0

        frequency = [0] * 256

        for byte in data:
            frequency[byte] += 1

        entropy = 0.0
        length = len(data)

        for count in frequency:

            if count == 0:
                continue

            probability = count / length
            entropy -= probability * math.log2(probability)

        return round(entropy, 4)

    def entropy(self):

        data = self.file_path.read_bytes()

        return {
            "File": self.file_path.name,
            "Size": len(data),
            "Entropy": self.calculate(data),
        }