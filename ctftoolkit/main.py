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

    subparsers = parser.add_subparsers(
        dest="module",
        required=True
    )

    # Register all plugins
    for module in PLUGINS:
        plugin = load_plugin(module)
        if hasattr(plugin, "register"):
            plugin.register(subparsers)

    args = parser.parse_args()

    # Check input file only if the plugin expects one
    if hasattr(args, "file"):
        if not file_exists(args.file):
            error("Input file not found.")
            return

    if hasattr(args, "func"):
        args.func(args)
    else:
        error("Invalid command.")


if __name__ == "__main__":
    main()