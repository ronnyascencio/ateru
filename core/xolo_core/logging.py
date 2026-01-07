from loguru import logger


def x_debug(ms: str):
    logger.debug("XOLO CORE: {}", ms)


def x_info(ms: str):
    logger.info("XOLO INFOL: {}", ms)


def x_succes(ms: str):
    logger.success("XOLO SUCCES: {}", ms)
