"""Main module."""
import time

import typer
from rich.console import Console
from rich.live import Live

from terminal_timer.bar import Bar
from terminal_timer.display import Display
from terminal_timer.themes import set_builtin_terminal_theme
from terminal_timer.timer import Timer

console = Console()
app = typer.Typer()


@app.command()
def timer(
    timer: str = typer.Argument(..., help="Timer length, in '1h30m30s' style."),
    gradient: str = typer.Option(
        default="blue cyan", help="Color gradient, start to end."
    ),
    theme: str = typer.Option(
        default="gruvbox", help="Built-in terminal theme, for ANSI color definitions."
    ),
    size: int = typer.Option(
        default=None, help="Size of the timer bar. None to auto detect."
    ),
) -> None:
    """Set a timer."""
    # Set bar width
    if size:
        console.width = size

    # Set theme
    terminal_theme = set_builtin_terminal_theme(theme)

    colors = gradient.split()
    col_1 = colors[0]
    col_2 = colors[1]

    bar = Bar(col_1, col_2, terminal_theme)
    t = Timer(timer)

    total_seconds = t.timer_amount
    elapsed = 0

    def update_display() -> Display:
        """Wrapper for updating a `Display` with `Rich.Live`."""
        percent = int((elapsed / total_seconds) * 100)

        bar.set_filled(percent)
        d = Display(bar, t)

        return d

    # Render the bar
    with Live(
        update_display(), console=console, refresh_per_second=4, transient=True
    ) as live:
        while elapsed <= total_seconds + 1:

            if elapsed == total_seconds:
                break

            elapsed += 1
            live.update(update_display())

            # increment 1 second
            t.update_time_remaining()
            time.sleep(1.0)

    console.print("Done!")


def main() -> None:
    """Main function."""
    app()


if __name__ == "__main__":
    main()
