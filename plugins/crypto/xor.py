from crypto.xor import XORCipher


def register_xor(subparsers):

    xor = subparsers.add_parser(
        "xor",
        help="XOR Cipher"
    )

    xor_sub = xor.add_subparsers(
        dest="action",
        required=True
    )

    encode = xor_sub.add_parser("encode")
    encode.add_argument("key")
    encode.add_argument("text")
    encode.set_defaults(func=run_xor_encode)

    decode = xor_sub.add_parser("decode")
    decode.add_argument("key")
    decode.add_argument("text")
    decode.set_defaults(func=run_xor_decode)

    crack = xor_sub.add_parser("crack")
    crack.add_argument("ciphertext")
    crack.set_defaults(func=run_xor_crack)


def run_xor_encode(args):
    print(XORCipher().encode(args.text, args.key))


def run_xor_decode(args):
    print(XORCipher().decode(args.text, args.key))


def run_xor_crack(args):

    print(f"{'Key':<5}{'Score':<10}Plaintext")
    print("-" * 60)

    for score, key, text in XORCipher().crack(args.ciphertext):
        print(f"{key:<5}{score:<10.2f}{text}")