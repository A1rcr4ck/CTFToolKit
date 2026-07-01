from crypto.encoders.base32 import Base32Cipher
from crypto.encoders.base58 import Base58Cipher
from crypto.encoders.base64 import Base64Cipher
from crypto.encoders.base85 import Base85Cipher
from crypto.encoders.binary import BinaryCipher
from crypto.encoders.hex import HexCipher
from crypto.encoders.octal import OctalCipher
from core.input import read_input


def register_base(subparsers):

    base64 = subparsers.add_parser("base64")
    base64.add_argument("action", choices=["encode", "decode"])
    base64.add_argument("text")
    base64.set_defaults(func=run_base64)

    base32 = subparsers.add_parser("base32")
    base32.add_argument("action", choices=["encode", "decode"])
    base32.add_argument("text")
    base32.set_defaults(func=run_base32)

    base58 = subparsers.add_parser("base58")
    base58.add_argument("action", choices=["encode", "decode"])
    base58.add_argument("text")
    base58.set_defaults(func=run_base58)

    base85 = subparsers.add_parser("base85")
    base85.add_argument("action", choices=["encode", "decode"])
    base85.add_argument("text")
    base85.set_defaults(func=run_base85)

    hex_parser = subparsers.add_parser("hex")
    hex_parser.add_argument("action", choices=["encode", "decode"])
    hex_parser.add_argument("text")
    hex_parser.set_defaults(func=run_hex)

    binary = subparsers.add_parser("binary")
    binary.add_argument("action", choices=["encode", "decode"])
    binary.add_argument("text")
    binary.set_defaults(func=run_binary)

    octal = subparsers.add_parser("octal")
    octal.add_argument("action", choices=["encode", "decode"])
    octal.add_argument("text")
    octal.set_defaults(func=run_octal)


def run_base64(args):
    text = read_input(args.text)
    cipher = Base64Cipher()
    print(cipher.encode(text) if args.action == "encode" else cipher.decode(text))


def run_base32(args):
    text = read_input(args.text)
    cipher = Base32Cipher()
    print(cipher.encode(text) if args.action == "encode" else cipher.decode(text))


def run_base58(args):
    text = read_input(args.text)
    cipher = Base58Cipher()
    print(cipher.encode(text) if args.action == "encode" else cipher.decode(text))


def run_base85(args):
    text = read_input(args.text)
    cipher = Base85Cipher()
    print(cipher.encode(text) if args.action == "encode" else cipher.decode(text))


def run_hex(args):
    text = read_input(args.text)
    cipher = HexCipher()
    print(cipher.encode(text) if args.action == "encode" else cipher.decode(text))


def run_binary(args):
    text = read_input(args.text)
    cipher = BinaryCipher()
    print(cipher.encode(text) if args.action == "encode" else cipher.decode(text))


def run_octal(args):
    text = read_input(args.text)
    cipher = OctalCipher()
    print(cipher.encode(text) if args.action == "encode" else cipher.decode(text))