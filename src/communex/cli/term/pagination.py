import os
import sys
from typing import Any

from rich.console import Console

if os.name != 'nt':
    import termios
    import tty
else:
    import msvcrt

class PaginationContext():
    """
    This class implements a new pagination scheme for the given `console` instance,
    you SHOULD print and do your stuff in here instead of using `console` directly,
    this class is going to implement everything of the `Console` class as an wrapper into
    this pagination context.
    """

    console: Console
    lines: list[dict[str, tuple[Any, ...] | dict[str, Any]]]

    if os.name != 'nt':
        _old_tcstate: Any = None

    def __init__(self, console: Console):
        self.console = console
        self.lines = []

    def __enter__(self):
        if os.name != 'nt':
            self._old_tcstate = termios.tcgetattr(sys.stdin.fileno())

            tty.setraw(sys.stdin.fileno(), termios.TCSANOW)

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        for i in range(0, len(self.lines), 5):
            print(i)

        if os.name != 'nt':
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self._old_tcstate)

    def _next_chr(self):
        if os.name == 'nt':
            return msvcrt.getch().decode()
        else:
            return sys.stdin.read(1)

    def print(self, *args: Any, **kwargs: Any):
        self.lines.append({ 'args': args, 'kwargs': kwargs })
