from rev.fileinfo import get_file_info


def info_command(args):
    data = get_file_info(args.file)

    print(f"{'Path':15}: {data['path']}")
    print(f"{'Name':15}: {data['filename']}")
    print(f"{'Extension':15}: {data['extension']}")
    print(f"{'Size':15}: {data['size']} bytes")
    print(f"{'Type':15}: {data['type']}")
    print(f"{'Format':15}: {data['format']}")
    print(f"{'Architecture':15}: {data['architecture']}")
    print(f"{'Entry Point':15}: {data['entrypoint']}")


def register_info(subparsers):
    parser = subparsers.add_parser(
        "info",
        help="Display binary information"
    )

    parser.add_argument(
        "file",
        help="Input binary"
    )

    parser.set_defaults(func=info_command)