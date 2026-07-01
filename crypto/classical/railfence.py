from ..base import Cipher


class RailFenceCipher(Cipher):
    def encode(self, data: str, rails: int) -> str:
        if rails <= 1:
            return data

        fence = [""] * rails
        rail = 0
        direction = 1

        for char in data:
            fence[rail] += char

            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1

            rail += direction

        return "".join(fence)

    def decode(self, data: str, rails: int) -> str:
        if rails <= 1:
            return data

        pattern = []
        rail = 0
        direction = 1

        for _ in data:
            pattern.append(rail)

            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1

            rail += direction

        counts = [pattern.count(r) for r in range(rails)]

        fence = []
        index = 0

        for count in counts:
            fence.append(list(data[index:index + count]))
            index += count

        result = []

        for r in pattern:
            result.append(fence[r].pop(0))

        return "".join(result)