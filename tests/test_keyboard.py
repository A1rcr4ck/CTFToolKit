from usb.keyboard import decode_file

text = decode_file("tests/keyboard.txt")

print()
print("=" * 50)
print("Decoded Output")
print("=" * 50)
print(text)
print("=" * 50)