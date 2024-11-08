import json
from types import TracebackType
from typing import Optional, Type

from rich.console import Console, RenderableType
from rich.jupyter import JupyterMixin


class JSONTextStatus(JupyterMixin):
    """Displays a status with JSON

    Args:
        status (RenderableType): A status renderable (str or Text typically).
        console (Console): Console instance to use, or None for global console. Defaults to None.
    """

    _console: Console
    _current_value: Optional[RenderableType]

    def __init__(
        self,
        console: Console,
        status: Optional[RenderableType] = None,
    ):
        self.status = status
        self._console = console
        self._current_value = status

    @property
    def renderable(self) -> RenderableType:
        return self._current_value or ""

    @property
    def console(self) -> Console:
        """Get the Console used by the Status objects."""
        return self._console

    def update(
        self,
        status: Optional[RenderableType] = None,
    ) -> None:
        """Update status.

        Args:
            status (Optional[RenderableType], optional): New status renderable or None for no change. Defaults to None.
        """
        if status is not None:
            self._current_value = status

        self._console.print(
            json.dumps({
                'type': 'status',
                'value': self._current_value,
                'event': 'update'
            }),
            crop = False,
            overflow = 'ignore',
            soft_wrap = False
        )

    def start(self) -> None:
        """Start the status animation."""
        self._console.print(
            json.dumps({
                'type': 'status',
                'value': self._current_value,
                'event': 'begin'
            }),
            crop = False,
            overflow = 'ignore',
            soft_wrap = False
        )

    def stop(self) -> None:
        """Stop the spinner animation."""
        self._console.print(
            json.dumps({
                'type': 'status',
                'value': self._current_value,
                'event': 'end'
            }),
            crop = False,
            overflow = 'ignore',
            soft_wrap = False
        )

    def __rich__(self) -> RenderableType:
        return self.renderable

    def __enter__(self) -> "JSONTextStatus":
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.stop()
