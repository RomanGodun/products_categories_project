import logging
from logging.handlers import RotatingFileHandler
import sys


def getСustomLogger(
    servicename="service",
    filepath="service.log",
    levelG=20,
    levelstdout=10,
    levelfile=10,
):
    logger = logging.getLogger(name=servicename)
    logger.setLevel(levelG)

    handler_stdout = logging.StreamHandler(stream=sys.stdout)
    handler_stdout.setLevel(levelstdout)
    logger.addHandler(handler_stdout)

    handler_file = RotatingFileHandler(
        filepath,
        mode="a",
        maxBytes=10485760,
        backupCount=40,
        encoding=None,
        delay=False,
    )
    handler_file.setLevel(levelfile)
    logger.addHandler(handler_file)

    strfmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
    handler_stdout.setFormatter(formatter)
    handler_file.setFormatter(formatter)

    return logger
