from logging.config import dictConfig

from config import DevConfig, config


# it won't return anything, but here we'll configure
# out loggers
# by doing it this way, it is more easier to configure
# rather than setting the loggers, handlers and formatters separately
def configure_loggin() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s - %(name)s : %(lineno)d - %(message)s",
                },
                "file": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                },
                # this will allow to maitain other file logs
                # if one file reaches the maxBytes, it will create another file
                # and the old will stick around for as long as we tell it to
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "backend.log",
                    "maxBytes": 1024 * 1024 * 3,  # 3MB
                    "backupCount": 3,
                    "encoding": "utf8",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "backend": {
                    "handlers": ["default", "rotating_file"],
                    # if the config is DevConfig, then the level will be DEBUG
                    # otherwise it will be INFO
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,  # will not send any loggin to the root logger
                },
            },
        }
    )
