import logging


LOG_LEVELS = ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET')
LOG_FORMAT = "%(levelname)s::%(asctime)s::" + \
             "%(filename)s:%(lineno)d:: %(msg)s"

def setup_logging(lvl, path):
    handler = logging.FileHandler(path if path else 'client.log', 'w')
    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(lvl)
