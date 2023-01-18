"""Terminal timer display."""
from rich.console import Console, ConsoleOptions, RenderResult

from terminal_timer.bar import Bar
from terminal_timer.timer import Timer


class Display:
    """Display the terminal timer."""

    def __init__(self, bar: Bar, timer: Timer) -> None:
        self.bar = bar
        self.timer = timer

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        yield self.timer
        yield self.bar
