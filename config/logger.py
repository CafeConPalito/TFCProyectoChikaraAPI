import logging
import sys
from loguru._defaults import LOGURU_FORMAT
from pprint import pformat
from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth,
                   exception=record.exc_info).log(level, record.getMessage())


def format_record(record: dict) -> str:
    format_string = LOGURU_FORMAT

    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(record["extra"]["payload"],
                                             indent=4,
                                             compact=True,
                                             width=88)
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def startLogger():
    logging.getLogger().handlers = [InterceptHandler()]

    logger.configure(handlers=[{
        "sink": sys.stdout,
        "level": logging.DEBUG,
        "format": format_record
    }])

    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logger.add("./logs/ALL.log",
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               compression="zip",
               rotation="500 MB")
    logger.add("./logs/ERROR.log",
               level=logging.WARNING,
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               compression="zip",
               rotation="500 MB")
