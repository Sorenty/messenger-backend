import logging
import signal
import threading

shutdown_event = threading.Event()
logger = logging.getLogger(__name__)


def is_shutting_down() -> bool:
    return shutdown_event.is_set()


def _handle_shutdown(signum, frame):
    shutdown_event.set()
    logger.warning("shutdown_requested", extra={"signal": signal.Signals(signum).name})


def register_signal_handlers():
    signal.signal(signal.SIGTERM, _handle_shutdown)
    signal.signal(signal.SIGINT, _handle_shutdown)