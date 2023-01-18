"""Bar module."""
from rich.console import Console, ConsoleOptions, RenderResult
from rich.style import Style
from rich.terminal_theme import TerminalTheme
from rich.text import Text

from terminal_timer._color import color_bar_colors


class Bar:
    """A bar, displayed in the terminal."""

    def __init__(
        self,
        low_color: str,
        high_color: str,
        terminal_theme: TerminalTheme,
    ) -> None:
        self.low = low_color
        self.high = high_color
        self.terminal_theme = terminal_theme
        self._filled = 0

    def set_filled(self, filled: int) -> None:
        """Set filled percentage."""
        self._filled = filled

    @property
    def filled(self) -> int:
        """Get filled percentage."""
        return self._filled

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        # Subtract 2 for bracket characters, 5 for ' 33% ' characters
        width = options.max_width - 2 - 5

        colors = color_bar_colors(self.low, self.high, width, self.terminal_theme)

        percentage = self.filled / 100.0
        index = int(width * percentage)
        used_colors = colors[0:index]

        background = Text("·" * width)

        # Alternative chars: ■, █,

        bar_chars = Text()
        for color in used_colors:
            bar_chars.append_text(Text("■", Style(color=color)))

        padded_bar = bar_chars.append_text(background[index:])

        yield Text("⟨") + padded_bar + Text("⟩") + Text(f" {int(percentage * 100)}%")
