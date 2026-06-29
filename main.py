#!/usr/bin/env python3

import argparse
import importlib

from core.banner import show_banner
from core.logger import error
from core.utils import file_exists


PLUGINS = {
    "usb": "plugins.usb",
    "crypto": "plugins.crypto",
    "forensic": "plugins.forensic",
    "reverse": "plugins.reverse",
    "web": "plugins.web",
}


def load_plugin(name):

    if name not in PLUGINS:
        return None

    return importlib.import_module(PLUGINS[name])


def main():

    show_banner()

    parser = argparse.ArgumentParser(
        prog="ctf",
        description="CTF Toolkit"
    )

    sub = parser.add_subparsers(dest="module")

    usb = sub.add_parser("usb")
    usb.add_argument("type", choices=["keyboard", "mouse"])
    usb.add_argument("file")

    args = parser.parse_args()

    if args.module is None:
        parser.print_help()
        return

    if not file_exists(args.file):
        error("Input file not found.")
        return

    plugin = load_plugin(args.module)

    if plugin is None:
        error("Plugin not found.")
        return

    plugin.run(args)


if __name__ == "__main__":
    main()