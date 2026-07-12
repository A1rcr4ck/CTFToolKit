import math
from pathlib import Path


def calculate_entropy(data: bytes) -> float:

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


def calculate_entropy_from_file(path: str) -> float:

    return calculate_entropy(
        Path(path).read_bytes()
    )