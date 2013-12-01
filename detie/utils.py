import logging


class ColorLoggingFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelno
        if level == logging.DEBUG:
            fmt = '\x1b[36;1m%s\x1b[0m'
        elif level == logging.INFO:
            fmt = '\x1b[34;1m%s\x1b[0m'
        elif level == logging.WARNING:
            fmt = '\x1b[33;1m%s\x1b[0m'
        elif level == logging.ERROR:
            fmt = '\x1b[31;1m%s\x1b[0m'
        elif level == logging.CRITICAL:
            fmt = '\x1b[37;41;1m%s\x1b[0m'
        else:
            fmt = '\x1b[39;2m%s:\x1b[0m'

        level_fmt = fmt % record.levelname
        record.levelname = level_fmt
        return logging.Formatter.format(self, record)

logging_handler = logging.StreamHandler()
logging_handler.setLevel(logging.INFO)
logging_handler.setFormatter(ColorLoggingFormatter('%(levelname)s: %(message)s'))

logger = logging.getLogger('detie')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_handler)
