from rev.checksec import checksec


def checksec_command(args):
    data = checksec(args.file)

    print(f"Binary Type : {data['type']}")

    if data["type"] == "ELF":
        print(f"NX      : {data['nx']}")
        print(f"PIE     : {data['pie']}")
        print(f"RELRO   : {data['relro']}")
        print(f"Canary  : {data['canary']}")

    elif data["type"] == "PE":
        print(f"ASLR    : {data['aslr']}")
        print(f"DEP     : {data['dep']}")
        print(f"CFG     : {data['cfg']}")

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