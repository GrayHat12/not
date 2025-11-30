import logging
import logging.handlers
from discord.utils import stream_supports_colour, _ColourFormatter

dt_fmt = '%Y-%m-%d %H:%M:%S'


class ColourFormatter(_ColourFormatter):
    LEVEL_COLOURS = [
        (logging.DEBUG, '\x1b[94;1m'),
        (logging.INFO, '\x1b[96;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]

    FORMATS = {
        level: logging.Formatter(
            f'\x1b[90;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)-24s\x1b[0m {colour}%(message)s\x1b[0m',
            dt_fmt
        )
        for level, colour in LEVEL_COLOURS
    }


file_handler = logging.handlers.RotatingFileHandler(
    filename='out.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)

stream_handler = logging.StreamHandler()

plain_formatter = logging.Formatter(
    '[{asctime}] [{levelname:<8}] {name:<24}: {message}', dt_fmt, style='{'
)
color_formatter = ColourFormatter()

if stream_supports_colour(stream_handler.stream):
    stream_handler.setFormatter(color_formatter)
else:
    stream_handler.setFormatter(plain_formatter)

file_handler.setFormatter(plain_formatter)


def setup_discord_logger():
    discord_logger = logging.getLogger('discord')
    http_logger = logging.getLogger('discord.http')
    # client_logger = logging.getLogger('discord.client')
    gateway_logger = logging.getLogger('discord.gateway')

    discord_logger.propagate = False
    http_logger.propagate = False
    gateway_logger.propagate = False

    for logger in [discord_logger, http_logger, gateway_logger]:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    gateway_logger.setLevel(logging.INFO)
    # client_logger.setLevel(logging.DEBUG)
    http_logger.setLevel(logging.INFO)
    discord_logger.setLevel(logging.DEBUG)

    discord_logger.addHandler(file_handler)
    # client_logger.addHandler(file_handler)
    http_logger.addHandler(file_handler)
    gateway_logger.addHandler(file_handler)

    discord_logger.addHandler(stream_handler)
    # client_logger.addHandler(stream_handler)
    http_logger.addHandler(stream_handler)
    gateway_logger.addHandler(stream_handler)


def setup_application_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.debug("TEST LOG")
    logger.info("TEST LOG")
    logger.warning("TEST LOG")
    logger.error("TEST LOG")
    logger.critical("TEST LOG")
