from rich.console import Console

from .options import CLIOptions

class CLIContext:
    stdout: Console
    stderr: Console

    argv: list[str]

    options: CLIOptions

    colored: bool
    interactive: bool

    def __init__(
        self,
        argv: list[str],
        colored: bool
    ):
        self.stdout = Console()
        self.stderr = Console(stderr = True)

        self.argv = argv
        self.colored = colored

        self.options = CLIOptions()

    def parse_arguments(self):
        pass
