from rich.console import Console
from rich.panel import Panel

console = Console()


def show_banner():
    banner = r"""
 ██████╗████████╗███████╗
██╔════╝╚══██╔══╝██╔════╝
██║        ██║   █████╗
██║        ██║   ██╔══╝
╚██████╗   ██║   ██║
 ╚═════╝   ╚═╝   ╚═╝

      CTF TOOLKIT
"""

    console.print(
        Panel.fit(
            banner,
            title="[bold cyan]Version 1.0[/]",
            border_style="green"
        )
    )