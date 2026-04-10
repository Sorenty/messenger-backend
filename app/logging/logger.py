import logging
import sys
from flask import current_app, g, has_app_context, has_request_context
from pythonjsonlogger import jsonlogger


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        record.service = current_app.config.get("SERVICE_NAME", "messenger-backend") if has_app_context() else "messenger-backend"
        record.app_version = current_app.config.get("APP_VERSION", "dev") if has_app_context() else "dev"
        record.request_id = getattr(g, "request_id", None) if has_request_context() else None
        return True


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


def configure_logging(app):
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(service)s %(app_version)s %(request_id)s %(name)s %(message)s"
    )

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(MaxLevelFilter(logging.WARNING))
    stdout_handler.addFilter(RequestContextFilter())
    stdout_handler.setFormatter(formatter)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.addFilter(RequestContextFilter())
    stderr_handler.setFormatter(formatter)

    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)

    app.logger.handlers.clear()
    app.logger.propagate = True