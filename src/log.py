import logging
import logging.handlers

from pathlib import Path
from sys import stdout

from data.config import LOG_PATH, LOGGER_NAME, LOGGER_LEVEL, LOGGER_FORMAT


def get_logger(
    logger_name: str = LOGGER_NAME,
    logger_level: int = LOGGER_LEVEL,
    logger_format: str = LOGGER_FORMAT,
    stdout_handler: bool = False,
    file_handler: bool = False,
    file_name: Path = LOG_PATH,
) -> logging.Logger:
    """
    Get logger.

    :param logger_name: name of the logger.
    :param logger_level: level of logs.
    :param logger_format: format of logs.
    :param stdout_handler: create stdout handler or not.
    :param file_handler: create file handler or not.
    :param file_name: name of log files.
    :return: logger object.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    if stdout_handler:
        handler = logging.StreamHandler(stdout)
        handler.setFormatter(logging.Formatter(logger_format))
        logger.addHandler(handler)

    if file_handler:
        handler = logging.handlers.TimedRotatingFileHandler(file_name, when="midnight")
        handler.setFormatter(logging.Formatter(logger_format))
        logger.addHandler(handler)

    return logger


logger = get_logger()
