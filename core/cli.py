import argparse

from core.output import OutputFormat


def add_output_argument(parser: argparse.ArgumentParser):

    parser.add_argument(
        "--output",
        choices=[fmt.value for fmt in OutputFormat],
        default=OutputFormat.TABLE.value,
        help="Output format",
    )