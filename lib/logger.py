import logging

LOG_LEVELS = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}

LOG_FORMAT = "%(levelname)s::%(asctime)s::%(threadName)s::%(filename)s:%(lineno)d:: %(msg)s"

def setup_logging(lvl, path):
    logger = logging.getLogger()

    formatter = logging.Formatter(LOG_FORMAT)

    if path:
        handler = logging.FileHandler(path, 'w')
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(LOG_LEVELS['INFO'])