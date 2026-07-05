from rev.fileinfo import get_file_info


def info_command(args):
    """Display basic information about a file."""

    data = get_file_info(args.file)

    print(f"{'Path':15}: {data['path']}")
    print(f"{'Name':15}: {data['filename']}")
    print(f"{'Extension':15}: {data['extension'] or 'None'}")
    print(f"{'Size':15}: {data['size']} bytes")
    print(f"{'MIME':15}: {data['mime']}")
    print(f"{'Type':15}: {data['type']}")
    print(f"{'Architecture':15}: {data['architecture']}")
    print(f"{'Executable':15}: {'Yes' if data['is_executable'] else 'No'}")


def register_info(subparsers):
    """
    Register reverse commands.
    """

    reverse_parser = subparsers.add_parser(
        "reverse",
        help="Reverse engineering utilities"
    )

    reverse_subparsers = reverse_parser.add_subparsers(
        dest="reverse_command",
        required=True
    )

    info_parser = reverse_subparsers.add_parser(
        "info",
        help="Display file information"
    )

    info_parser.add_argument(
        "file",
        help="Path to input file"
    )

    info_parser.set_defaults(func=info_command)