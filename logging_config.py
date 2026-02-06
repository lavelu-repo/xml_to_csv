import logging
import os
import sys
from colorama import Fore, Style, init

# Initialize colorama (handles Windows auto-conversion)
init(autoreset=True)

_LEVEL_COLORS = {
    "DEBUG": Fore.CYAN,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.RED + "[CRITICAL]",
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        color = _LEVEL_COLORS.get(levelname, "")
        record.levelname = f"{color}{levelname}{Style.RESET_ALL}"
        return super().format(record)


def setup_logging(level: str | None = None) -> None:
    """Minimal console-only logging setup with colored output.

    - Reads `LOG_LEVEL` env var if `level` not provided.
    - Configures a single `StreamHandler` to stdout with ANSI colors.
    """
    lvl = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    numeric_level = getattr(logging, lvl, logging.INFO)

    root = logging.getLogger()
    root.setLevel(numeric_level)

    # remove existing handlers to avoid duplicate logs on repeated setup
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler(stream=sys.stdout)
    fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    handler.setFormatter(ColoredFormatter(fmt))
    handler.setLevel(numeric_level)
    root.addHandler(handler)
