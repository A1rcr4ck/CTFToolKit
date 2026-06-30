LETTER_FREQ = {
    "e": 12.70,
    "t": 9.06,
    "a": 8.17,
    "o": 7.51,
    "i": 6.97,
    "n": 6.75,
    "s": 6.33,
    "h": 6.09,
    "r": 5.99,
    "d": 4.25,
    "l": 4.03,
    "u": 2.76,
}


def score(text: str) -> float:
    text = text.lower()

    value = 0

    for c in text:
        if c in LETTER_FREQ:
            value += LETTER_FREQ[c]
        elif c == " ":
            value += 13
        elif 32 <= ord(c) <= 126:
            value += 0.2
        else:
            value -= 20

    return value