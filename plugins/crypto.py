import argparse

from crypto.base64 import Base64Cipher
from crypto.base32 import Base32Cipher
from crypto.base58 import Base58Cipher
from crypto.base85 import Base85Cipher
from crypto.hex import HexCipher
from crypto.binary import BinaryCipher
from crypto.octal import OctalCipher
from crypto.caesar import CaesarCipher
from crypto.rot13 import ROT13Cipher
from crypto.atbash import AtbashCipher
from crypto.vigenere import VigenereCipher

def register(subparsers):
    crypto = subparsers.add_parser(
        "crypto",
        help="Crypto utilities"
    )

    crypto_sub = crypto.add_subparsers(dest="algorithm")

    # Base64
    base64_parser = crypto_sub.add_parser(
        "base64",
        help="Base64 encode/decode"
    )

    base64_parser.add_argument(
        "action",
        choices=["encode", "decode"]
    )

    base64_parser.add_argument(
        "text"
    )

    base64_parser.set_defaults(func=run_base64)

        # Base32
    base32_parser = crypto_sub.add_parser(
        "base32",
        help="Base32 encode/decode"
    )

    base32_parser.add_argument(
        "action",
        choices=["encode", "decode"]
    )

    base32_parser.add_argument(
        "text"
    )

    base32_parser.set_defaults(func=run_base32)

        # Base58
    base58_parser = crypto_sub.add_parser(
        "base58",
        help="Base58 encode/decode"
    )

    base58_parser.add_argument(
        "action",
        choices=["encode", "decode"]
    )

    base58_parser.add_argument("text")

    base58_parser.set_defaults(func=run_base58)

    # Base85
    base85_parser = crypto_sub.add_parser(
        "base85",
        help="Base85 encode/decode"
    )

    base85_parser.add_argument(
        "action",
        choices=["encode", "decode"]
    )

    base85_parser.add_argument("text")

    base85_parser.set_defaults(func=run_base85)

    # Hex
    hex_parser = crypto_sub.add_parser(
        "hex",
        help="Hex encode/decode"
    )

    hex_parser.add_argument(
        "action",
        choices=["encode", "decode"]
    )

    hex_parser.add_argument("text")

    hex_parser.set_defaults(func=run_hex)

        # Binary
    binary_parser = crypto_sub.add_parser(
        "binary",
        help="Binary encode/decode"
    )

    binary_parser.add_argument(
        "action",
        choices=["encode", "decode"]
    )

    binary_parser.add_argument("text")

    binary_parser.set_defaults(func=run_binary)

    # Octal
    octal_parser = crypto_sub.add_parser(
        "octal",
        help="Octal encode/decode"
    )

    octal_parser.add_argument(
        "action",
        choices=["encode", "decode"]
    )

    octal_parser.add_argument("text")

    octal_parser.set_defaults(func=run_octal)

        # Caesar
    caesar = crypto_sub.add_parser(
        "caesar",
        help="Caesar cipher"
    )

    caesar_sub = caesar.add_subparsers(
        dest="action",
        required=True
    )

    encode = caesar_sub.add_parser("encode")
    encode.add_argument("shift", type=int)
    encode.add_argument("text")
    encode.set_defaults(func=run_caesar_encode)

    decode = caesar_sub.add_parser("decode")
    decode.add_argument("shift", type=int)
    decode.add_argument("text")
    decode.set_defaults(func=run_caesar_decode)

    crack = caesar_sub.add_parser("crack")
    crack.add_argument("text")
    crack.set_defaults(func=run_caesar_crack)

        # ROT13
    rot13 = crypto_sub.add_parser(
        "rot13",
        help="ROT13 cipher"
    )

    rot13.add_argument(
        "text"
    )

    rot13.set_defaults(func=run_rot13)

        # Atbash
    atbash = crypto_sub.add_parser(
        "atbash",
        help="Atbash cipher"
    )

    atbash.add_argument(
        "text"
    )

    atbash.set_defaults(func=run_atbash)

        # Vigenere
    vigenere = crypto_sub.add_parser(
        "vigenere",
        help="Vigenere cipher"
    )

    vigenere_sub = vigenere.add_subparsers(
        dest="action",
        required=True
    )

    encode = vigenere_sub.add_parser("encode")
    encode.add_argument("key")
    encode.add_argument("text")
    encode.set_defaults(func=run_vigenere_encode)

    decode = vigenere_sub.add_parser("decode")
    decode.add_argument("key")
    decode.add_argument("text")
    decode.set_defaults(func=run_vigenere_decode)


def run_base64(args: argparse.Namespace):
    cipher = Base64Cipher()

    if args.action == "encode":
        print(cipher.encode(args.text))
    else:
        print(cipher.decode(args.text))

def run_base32(args: argparse.Namespace):
    cipher = Base32Cipher()

    if args.action == "encode":
        print(cipher.encode(args.text))
    else:
        print(cipher.decode(args.text))

def run_base58(args: argparse.Namespace):
    cipher = Base58Cipher()

    if args.action == "encode":
        print(cipher.encode(args.text))
    else:
        print(cipher.decode(args.text))


def run_base85(args: argparse.Namespace):
    cipher = Base85Cipher()

    if args.action == "encode":
        print(cipher.encode(args.text))
    else:
        print(cipher.decode(args.text))

def run_hex(args: argparse.Namespace):
    cipher = HexCipher()

    if args.action == "encode":
        print(cipher.encode(args.text))
    else:
        print(cipher.decode(args.text))

def run_binary(args: argparse.Namespace):
    cipher = BinaryCipher()

    if args.action == "encode":
        print(cipher.encode(args.text))
    else:
        print(cipher.decode(args.text))


def run_octal(args: argparse.Namespace):
    cipher = OctalCipher()

    if args.action == "encode":
        print(cipher.encode(args.text))
    else:
        print(cipher.decode(args.text))

def run_caesar_encode(args):
    cipher = CaesarCipher()
    print(cipher.encode(args.text, args.shift))


def run_caesar_decode(args):
    cipher = CaesarCipher()
    print(cipher.decode(args.text, args.shift))


def run_caesar_crack(args):
    cipher = CaesarCipher()

    for shift, text in cipher.crack(args.text):
        print(f"{shift:2}: {text}")

def run_rot13(args):
    cipher = ROT13Cipher()
    print(cipher.encode(args.text))

def run_atbash(args):
    cipher = AtbashCipher()
    print(cipher.encode(args.text))

def run_vigenere_encode(args):
    cipher = VigenereCipher()
    print(cipher.encode(args.text, args.key))


def run_vigenere_decode(args):
    cipher = VigenereCipher()
    print(cipher.decode(args.text, args.key))