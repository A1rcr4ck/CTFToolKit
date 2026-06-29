"""
USB HID Keyboard Lookup Tables
"""

# HID Keycodes
HID_KEYS = {

    # Letters
    0x04: "a",
    0x05: "b",
    0x06: "c",
    0x07: "d",
    0x08: "e",
    0x09: "f",
    0x0A: "g",
    0x0B: "h",
    0x0C: "i",
    0x0D: "j",
    0x0E: "k",
    0x0F: "l",
    0x10: "m",
    0x11: "n",
    0x12: "o",
    0x13: "p",
    0x14: "q",
    0x15: "r",
    0x16: "s",
    0x17: "t",
    0x18: "u",
    0x19: "v",
    0x1A: "w",
    0x1B: "x",
    0x1C: "y",
    0x1D: "z",

    # Numbers
    0x1E: "1",
    0x1F: "2",
    0x20: "3",
    0x21: "4",
    0x22: "5",
    0x23: "6",
    0x24: "7",
    0x25: "8",
    0x26: "9",
    0x27: "0",

    # Symbols
    0x2C: " ",
    0x2D: "-",
    0x2E: "=",
    0x2F: "[",
    0x30: "]",
    0x31: "\\",
    0x33: ";",
    0x34: "'",
    0x35: "`",
    0x36: ",",
    0x37: ".",
    0x38: "/",

    # Special
    0x28: "<ENTER>",
    0x29: "<ESC>",
    0x2A: "<BACKSPACE>",
    0x2B: "<TAB>",
}

SHIFT_KEYS = {
    "1": "!",
    "2": "@",
    "3": "#",
    "4": "$",
    "5": "%",
    "6": "^",
    "7": "&",
    "8": "*",
    "9": "(",
    "0": ")",
    "-": "_",
    "=": "+",
    "[": "{",
    "]": "}",
    "\\": "|",
    ";": ":",
    "'": "\"",
    "`": "~",
    ",": "<",
    ".": ">",
    "/": "?"
}


def is_shift(modifier: int) -> bool:
    """
    Returns True if Left or Right Shift is pressed.
    """
    return bool(modifier & 0x22)


def hid_to_char(modifier: int, keycode: int):
    """
    Convert HID usage code to character.
    """

    if keycode not in HID_KEYS:
        return ""

    char = HID_KEYS[keycode]

    if is_shift(modifier):

        if len(char) == 1:

            if char.isalpha():
                return char.upper()

            if char in SHIFT_KEYS:
                return SHIFT_KEYS[char]

    return char