from rich.console import Console
from rich.theme import Theme

theme = Theme ({
    "title" : "bold cyan",
    "info" : "cyan",
    "success" : "bold green",
    "warning" : "bold yellow",
    "error" : "bold red",
    "path" : "bright_blue"
})

def get_console (no_color : bool = False) -> Console :
    return Console (theme = theme, no_color = no_color)