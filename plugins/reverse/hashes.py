from rev.hashes import get_hashes


def hashes_command(args):
    hashes = get_hashes(args.file)

    print(f"MD5    : {hashes['md5']}")
    print(f"SHA1   : {hashes['sha1']}")
    print(f"SHA256 : {hashes['sha256']}")


def register_hashes(subparsers):
    parser = subparsers.add_parser(
        "hashes",
        help="Calculate file hashes"
    )

    parser.add_argument(
        "file",
        help="Input file"
    )

    parser.set_defaults(func=hashes_command)