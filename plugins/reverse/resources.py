from rev.pe import PEParser

from core.cli import add_output_argument
from core.output.dispatcher import dispatch


RESOURCE_TYPES = {
    1: "CURSOR",
    2: "BITMAP",
    3: "ICON",
    4: "MENU",
    5: "DIALOG",
    6: "STRING",
    7: "FONTDIR",
    8: "FONT",
    9: "ACCELERATOR",
    10: "RCDATA",
    11: "MESSAGETABLE",
    12: "GROUP_CURSOR",
    14: "GROUP_ICON",
    16: "VERSION",
    24: "MANIFEST",
}


def resources_command(args):

    pe = PEParser(args.file)

    if not pe.resources:
        print("No resources found.")
        return

    rows = []

    for resource in pe.resources:

        resource_id = (
            resource.id
            if resource.id is not None
            else "-"
        )

        if resource.name:
            resource_type = resource.name

        elif resource.id is not None:

            resource_type = RESOURCE_TYPES.get(
                resource.id,
                f"Unknown ({resource.id})",
            )

        else:

            resource_type = "Named Resource"

        rows.append(
            (
                resource_id,
                resource_type,
            )
        )

    table = (
        "PE Resources",
        ["ID", "Type"],
        rows,
    )

    dispatch(
        args.output,
        table_data=table,
        json_data=pe.resources,
    )


def register_resources(subparsers):

    parser = subparsers.add_parser(
        "resources",
        help="Display PE resources",
    )

    parser.add_argument(
        "file",
        help="Input PE file",
    )

    add_output_argument(parser)

    parser.set_defaults(func=resources_command)