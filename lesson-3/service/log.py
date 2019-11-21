import logging
import os
from settings import config


LOG_DIR = '/var/log/photoserver'
ACCESS_LOG_FILE = os.path.join(LOG_DIR, 'access.log')
ERROR_LOG_FILE = os.path.join(LOG_DIR, 'error.log')
LOGGING_FORMAT = '[%(asctime)s] %(levelname).1s %(message)s'


class LevelFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno == self.__level


def create_log_files_if_not_exist():
    if not os.path.exists(ACCESS_LOG_FILE):
        os.mknod(ACCESS_LOG_FILE)
    if not os.path.exists(ERROR_LOG_FILE):
        os.mknod(ERROR_LOG_FILE)


def setup_loggers():
    logFormatter = logging.Formatter(LOGGING_FORMAT)
    rootLogger = logging.getLogger()

    access_file_handler = logging.FileHandler(ACCESS_LOG_FILE)
    access_file_handler.setFormatter(logFormatter)
    access_file_handler.addFilter(LevelFilter(logging.INFO))
    rootLogger.addHandler(access_file_handler)

    error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
    error_file_handler.setFormatter(logFormatter)
    error_file_handler.addFilter(LevelFilter(logging.ERROR))
    rootLogger.addHandler(error_file_handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(logging.INFO)


def set_logs():
    if config.LOGGING:
        create_log_files_if_not_exist()
        setup_loggers()
    else:
        logging.basicConfig(format=LOGGING_FORMAT, datefmt='%Y.%m.%d %H:%M:%S', level=logging.WARNING)
