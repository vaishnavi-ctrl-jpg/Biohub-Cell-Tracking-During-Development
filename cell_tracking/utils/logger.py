"""
Structured logging utility powered by Rich console formatting.
"""

import logging
from rich.logging import RichHandler


def get_logger(name: str = "cell_tracking", level: int = logging.INFO) -> logging.Logger:
    """Get a structured logger with Rich console formatting."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = RichHandler(rich_tracebacks=True, show_time=True, show_path=False)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger
