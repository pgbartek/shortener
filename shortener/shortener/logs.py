import logging.config

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from . import settings


CONFIGURATION = {
    "version": 1,
    "formatters": {
        "default": {
            "format": (
                "[%(asctime)s:"
                " %(levelname)s/%(name)s/%(processName)s/%(threadName)s]"
                " %(message)s"
            )
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": settings.LOG_LEVEL,
            "formatter": "default",
        },
    },
    "root": {"level": "INFO", "handlers": ["stdout"]},
    "loggers": {
        "shortener": {
            "level": "DEBUG",
            "handlers": ["stdout"],
            "qualname": "shortener",
            "propagate": 0,
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": ["stdout"],
            "qualname": "uvicorn",
            "propagate": 0,
        },
    },
}


def setup():
    logging.config.dictConfig(CONFIGURATION)
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.WARNING)
    sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[sentry_logging])
