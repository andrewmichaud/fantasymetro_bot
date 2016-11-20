"""Util functions for fantasymetro_bot."""
import logging
import sys
from logging.handlers import RotatingFileHandler

LOG = logging.getLogger("root")

LAST_CALLED = {}


def set_up_logging():
    """Set up proper logging."""
    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG)

    # Log everything verbosely to a file.
    file_handler = RotatingFileHandler(filename="log", maxBytes=1024000000, backupCount=10)
    verbose_form = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    file_handler.setFormatter(verbose_form)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Provide a stdout handler logging at INFO.
    stream_handler = logging.StreamHandler(sys.stdout)
    simple_form = logging.Formatter(fmt="%(message)s")
    stream_handler.setFormatter(simple_form)
    stream_handler.setLevel(logging.INFO)

    logger.addHandler(stream_handler)

    return logger
