import logging
import sys

def setup_logger(*, debug: bool = False, quiet: bool = False) -> logging.Logger:
    """
    Central logger configuration for Ateru/Xolo Pipeline using built-in logging.
    """

    logger = logging.getLogger("ateru")
    logger.handlers.clear()  # Limpia handlers previos
    logger.propagate = False  # Evita duplicar logs si ya hay root logger

    if quiet:
        logger.disabled = True
        return logger

    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)

    # Handler de consola
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)

    # Formato
    formatter = logging.Formatter(_log_format())
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def _log_format() -> str:
    """
    Custom log format for Ateru/Xolo Pipeline.
    """
    # No soporta colores nativos; los placeholders de time y level se usan así
    return "%(asctime)s | %(levelname)-7s | %(message)s"

