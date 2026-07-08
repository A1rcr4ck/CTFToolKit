from rev.pe import PEParser


def pe_header_command(args):

    pe = PEParser(args.file)
    h = pe.header

    print(f"{'Machine':<15}: {h.machine}")
    print(f"{'Timestamp':<15}: {h.timestamp}")
    print(f"{'Sections':<15}: {h.sections}")
    print(f"{'Entrypoint':<15}: {hex(h.entrypoint)}")
    print(f"{'Image Base':<15}: {hex(h.imagebase)}")
    print(f"{'Subsystem':<15}: {h.subsystem}")
    print(f"{'DLL':<15}: {h.dll}")


def register_pe_header(subparsers):

    parser = subparsers.add_parser(
        "pe-header",
        help="Display PE header",
    )

    parser.add_argument(
        "file",
        help="Input PE binary",
    )

    parser.set_defaults(func=pe_header_command)