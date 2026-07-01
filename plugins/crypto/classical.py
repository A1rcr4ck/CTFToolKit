from crypto.classical.atbash import AtbashCipher
from crypto.classical.caesar import CaesarCipher
from crypto.classical.rot13 import ROT13Cipher
from crypto.classical.vigenere import VigenereCipher
from crypto.classical.railfence import RailFenceCipher
from crypto.classical.morse import MorseCipher
from crypto.classical.bacon import BaconCipher
from crypto.classical.affine import AffineCipher
from crypto.modern.rsa import RSACipher
from core.input import read_input


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

    railfence = subparsers.add_parser(
        "railfence",
        help="Rail Fence Cipher"
    )

    railfence_sub = railfence.add_subparsers(
        dest="action",
        required=True
    )

    encode = railfence_sub.add_parser("encode")
    encode.add_argument("rails", type=int)
    encode.add_argument("text")
    encode.set_defaults(func=run_railfence_encode)

    decode = railfence_sub.add_parser("decode")
    decode.add_argument("rails", type=int)
    decode.add_argument("text")
    decode.set_defaults(func=run_railfence_decode)


    morse = subparsers.add_parser(
        "morse",
        help="Morse Code"
    )

    morse_sub = morse.add_subparsers(
        dest="action",
        required=True
    )

    encode = morse_sub.add_parser("encode")
    encode.add_argument("text")
    encode.set_defaults(func=run_morse_encode)

    decode = morse_sub.add_parser("decode")
    decode.add_argument("text")
    decode.set_defaults(func=run_morse_decode)


    bacon = subparsers.add_parser(
        "bacon",
        help="Baconian Cipher"
    )

    bacon_sub = bacon.add_subparsers(
        dest="action",
        required=True
    )

    encode = bacon_sub.add_parser("encode")
    encode.add_argument("text")
    encode.set_defaults(func=run_bacon_encode)

    decode = bacon_sub.add_parser("decode")
    decode.add_argument("text")
    decode.set_defaults(func=run_bacon_decode)


    affine = subparsers.add_parser(
        "affine",
        help="Affine Cipher"
    )

    affine_sub = affine.add_subparsers(
        dest="action",
        required=True
    )

    encode = affine_sub.add_parser("encode")
    encode.add_argument("a", type=int)
    encode.add_argument("b", type=int)
    encode.add_argument("text")
    encode.set_defaults(func=run_affine_encode)

    decode = affine_sub.add_parser("decode")
    decode.add_argument("a", type=int)
    decode.add_argument("b", type=int)
    decode.add_argument("text")
    decode.set_defaults(func=run_affine_decode)

    rsa = subparsers.add_parser(
        "rsa",
        help="RSA Utilities"
    )

    rsa_sub = rsa.add_subparsers(
        dest="action",
        required=True
    )

    encrypt = rsa_sub.add_parser("encrypt")
    encrypt.add_argument("e", type=int)
    encrypt.add_argument("n", type=int)
    encrypt.add_argument("plaintext", type=int)
    encrypt.set_defaults(func=run_rsa_encrypt)

    decrypt = rsa_sub.add_parser("decrypt")
    decrypt.add_argument("d", type=int)
    decrypt.add_argument("n", type=int)
    decrypt.add_argument("ciphertext", type=int)
    decrypt.set_defaults(func=run_rsa_decrypt)

    keygen = rsa_sub.add_parser("keygen")
    keygen.add_argument("p", type=int)
    keygen.add_argument("q", type=int)
    keygen.add_argument("e", type=int)
    keygen.set_defaults(func=run_rsa_keygen)


def run_caesar_encode(args):
    print(CaesarCipher().encode(read_input(args.text), args.shift))


def run_caesar_decode(args):
    print(CaesarCipher().decode(read_input(args.text), args.shift))


def run_caesar_crack(args):
    for shift, text in CaesarCipher().crack(read_input(args.text)):
        print(f"{shift:2}: {text}")


def run_rot13(args):
    print(ROT13Cipher().encode(read_input(args.text)))


def run_atbash(args):
    print(AtbashCipher().encode(read_input(args.text)))


def run_vigenere_encode(args):
    print(VigenereCipher().encode(read_input(args.text), args.key))


def run_vigenere_decode(args):
    print(VigenereCipher().decode(read_input(args.text), args.key))


def run_railfence_encode(args):
    print(RailFenceCipher().encode(read_input(args.text), args.rails))


def run_railfence_decode(args):
    print(RailFenceCipher().decode(read_input(args.text), args.rails))


def run_morse_encode(args):
    print(MorseCipher().encode(read_input(args.text)))


def run_morse_decode(args):
    print(MorseCipher().decode(read_input(args.text)))


def run_bacon_encode(args):
    print(BaconCipher().encode(read_input(args.text)))


def run_bacon_decode(args):
    print(BaconCipher().decode(read_input(args.text)))


def run_affine_encode(args):
    print(AffineCipher().encode(read_input(args.text), args.a, args.b))


def run_affine_decode(args):
    print(AffineCipher().decode(read_input(args.text), args.a, args.b))

def run_rsa_encrypt(args):
    print(
        RSACipher().encrypt(
            read_input(args.plaintext),
            args.e,
            args.n
        )
    )


def run_rsa_decrypt(args):
    print(
        RSACipher().decrypt(
            read_input(args.ciphertext),
            args.d,
            args.n
        )
    )


def run_rsa_keygen(args):
    rsa = RSACipher()

    d = rsa.generate_private_key(
        args.p,
        args.q,
        args.e
    )

    n = args.p * args.q

    print(f"n   = {n}")
    print(f"phi = {(args.p-1)*(args.q-1)}")
    print(f"e   = {args.e}")
    print(f"d   = {d}")