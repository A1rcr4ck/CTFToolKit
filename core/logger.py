from rich.console import Console

console = Console()


def title(text):
    console.rule(f"[bold cyan]{text}")


def info(text):
    console.print(f"[cyan][*][/cyan] {text}")


def success(text):
    console.print(f"[green][+][/green] {text}")


def warning(text):
    console.print(f"[yellow][!][/yellow] {text}")


def error(text):
    console.print(f"[red][-][/red] {text}")