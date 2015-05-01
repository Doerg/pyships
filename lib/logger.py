import logging

LOG_LEVELS = ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET')
LOG_FORMAT = "%(levelname)s::%(asctime)s::%(threadName)s::" + \
             "%(filename)s:%(lineno)d:: %(msg)s"


def setup_logging(is_server, lvl, path):
    if path:
        handler = logging.FileHandler(path, 'w')
    else:
        if is_server:
            handler = logging.StreamHandler()
        else:    #client shouldn't log to stdout, use default logfile instead
            handler = logging.FileHandler('client.log', 'w')

    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(lvl)