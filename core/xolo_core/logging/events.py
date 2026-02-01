from loguru import logger
from pathlib import Path


def debug(msg: str):
    logger.debug(msg)


def info(msg: str):
    logger.info(msg)


def success(msg: str):
    logger.success(msg)


def error(msg: str):
    logger.error(msg)
