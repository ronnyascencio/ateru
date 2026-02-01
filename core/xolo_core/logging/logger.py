from loguru import logger
import sys


def setup_logger(
    *,
    debug: bool = False,
    quiet: bool = False,
):
    """
    Central logger configuration for XOLO Pipeline.
    """


    logger.remove()

    if quiet:
        return logger

    level = "DEBUG" if debug else "INFO"

    logger.add(
        sys.stderr,
        level=level,
        format=_log_format(),
        colorize=True,
        backtrace=debug,
        diagnose=debug,
    )

    return logger


def _log_format() -> str:
    """
    Custom log format for XOLO Pipeline.
    """
    return (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level:<7}</level> | "
        "{message}"
    )
