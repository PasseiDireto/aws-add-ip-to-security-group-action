"""
Logger/Rich base config settings
"""

import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True, rich_tracebacks=True)],
)

install()
