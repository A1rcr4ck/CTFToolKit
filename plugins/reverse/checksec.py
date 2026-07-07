from rev.checksec import checksec
from rev.checksec_pe import pe_checksec


def checksec_command(args):
    data = checksec(args.file)

    print(f"Binary Type : {data['type']}")

    if data["type"] == "ELF":
        print(f"NX      : {data['nx']}")
        print(f"PIE     : {data['pie']}")
        print(f"RELRO   : {data['relro']}")
        print(f"Canary  : {data['canary']}")

    elif data["type"] == "PE":

        result = pe_checksec(args.file)

        for key, value in result.items():
            print(f"{key:<20}: {'Enabled' if value else 'Disabled'}")

def register_checksec(subparsers):
    parser = subparsers.add_parser(
        "checksec",
        help="Display binary security mitigations"
    )

    parser.add_argument(
        "file",
        help="Input binary"
    )

    parser.set_defaults(func=checksec_command)