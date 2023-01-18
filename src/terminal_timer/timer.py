"""Timer module."""

import re
import time
from datetime import timedelta

from rich.console import Console, ConsoleOptions, RenderResult
from rich.style import Style
from rich.text import Text

REGEX = re.compile(r"((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?")


def _parse_time(time_str: str) -> timedelta:
    """Parse 'hms' string into timedelta object."""
    parts = REGEX.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


class Timer:
    """Simple countdown timer."""

    def __init__(self, timer_amount: str) -> None:
        self.timer_amount = int(_parse_time(timer_amount).total_seconds())

        self.start_time = time.asctime(time.localtime())[11:16]  # Get starting time
        self.time_remaining = self.timer_amount

    def update_time_remaining(self) -> None:
        """Update the remaining time."""
        self.time_remaining -= 1

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        start_time = Text(
            self.start_time,
            style=Style(color="bright_white", bold=True),
        )
        remaining_td = Text(
            str(timedelta(seconds=self.time_remaining)),
            style=Style(color="bright_white"),
        )

        display = Text(" - ").join([start_time, remaining_td])

        yield display
