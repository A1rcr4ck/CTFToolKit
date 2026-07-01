from crypto.atbash import AtbashCipher
from crypto.caesar import CaesarCipher
from crypto.rot13 import ROT13Cipher
from crypto.vigenere import VigenereCipher


def register_classical(subparsers):

    # Caesar
    caesar = subparsers.add_parser(
        "caesar",
        help="Caesar Cipher"
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
    rot13 = subparsers.add_parser(
        "rot13",
        help="ROT13 Cipher"
    )

    rot13.add_argument("text")
    rot13.set_defaults(func=run_rot13)

    # Atbash
    atbash = subparsers.add_parser(
        "atbash",
        help="Atbash Cipher"
    )

    atbash.add_argument("text")
    atbash.set_defaults(func=run_atbash)

    # Vigenere
    vigenere = subparsers.add_parser(
        "vigenere",
        help="Vigenere Cipher"
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


def run_caesar_encode(args):
    print(CaesarCipher().encode(args.text, args.shift))


def run_caesar_decode(args):
    print(CaesarCipher().decode(args.text, args.shift))


def run_caesar_crack(args):
    for shift, text in CaesarCipher().crack(args.text):
        print(f"{shift:2}: {text}")


def run_rot13(args):
    print(ROT13Cipher().encode(args.text))


def run_atbash(args):
    print(AtbashCipher().encode(args.text))


def run_vigenere_encode(args):
    print(VigenereCipher().encode(args.text, args.key))


def run_vigenere_decode(args):
    print(VigenereCipher().decode(args.text, args.key))