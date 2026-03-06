from ateru.core.logging.logger import setup_logger


logger = setup_logger()

def debug(msg: str):
    logger.debug(msg)

def info(msg: str):
    logger.info(msg)

def success(msg: str):
 
    logger.info(msg)

def warning(msg: str):
    logger.warning(msg)

def error(msg: str):
    logger.error(msg)
