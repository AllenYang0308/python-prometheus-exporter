import logging
import sys

logger_level = logging.WARNING


def init_logger(filename=""):

    logger = logging.getLogger()
    logger.setLevel(logger_level)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | {%(pathname)s:%(lineno)d}| %(message)s",
        "%m-%d-%Y %H:%M:%S"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logger_level)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logger_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    return logger


def SingletonMeta(cls):

    instances = {}

    def _singleton(*args, **kwargs):

        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton


@SingletonMeta
class SingletonLogger(object):

    def __init__(self, *args, **kwargs):
        self.logger = init_logger(**kwargs)
