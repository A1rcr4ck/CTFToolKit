from pathlib import Path

from usb.keyboard import decode_file


SAMPLE = Path("tests/samples/usb/keyboard.txt")


def test_keyboard_decode():
    assert SAMPLE.exists(), f"Missing sample file: {SAMPLE}"

    text = decode_file(str(SAMPLE))

    assert isinstance(text, str)
    assert len(text) > 0