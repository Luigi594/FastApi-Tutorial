import logging
from logging.config import dictConfig

from config import DevConfig, config
from utils.obfuscate_email import obfuscated_email


# A logging filer is a class that has a function, and that function
# takes a log record and modifies it or adds variables to it
# and returns it
class EmailObfuscationFilter(logging.Filter):
    # this obfuscation class is for any case we log an email accidentally
    # so these emails will be hidden
    def __init__(self, name: str = "", obfuscate_length: int = 2) -> None:
        super(EmailObfuscationFilter, self).__init__(name)
        self.obfuscate_length = obfuscate_length

    def filter(self, record: logging.LogRecord) -> bool:
        # obfuscate the email addresses that are included as an extra
        # argument to the log record
        if "email" in record.__dict__:
            record.email = obfuscated_email(record.email, self.obfuscate_length)
        return True


handlers = ["default", "rotating_file"]
if isinstance(config, DevConfig):
    handlers = ["default", "rotating_file", "logtail"]


# it won't return anything, but here we'll configure
# out loggers
# by doing it this way, it is more easier to configure
# rather than setting the loggers, handlers and formatters separately
def configure_loggin() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    # any configuration after the line above, will be passed as
                    # keyword arguments to the constructor
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-",
                },
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
                    "obfuscate_length": 2 if isinstance(config, DevConfig) else 0,
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s : %(lineno)d - %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)03d %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
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
                    "filters": ["correlation_id", "email_obfuscation"],
                },
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                    "source_token": config.LOGTAIL_API_KEY,
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "backend": {
                    # not send logs to logtail until we deploy the API
                    "handlers": handlers,
                    # if the config is DevConfig, then the level will be DEBUG
                    # otherwise it will be INFO
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,  # will not send any loggin to the root logger
                },
            },
        }
    )
