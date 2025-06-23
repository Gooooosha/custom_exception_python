import sys
from .config import Config
from .client import ErrorClient

def init(dsn: str, release: str = None, environment: str = None):
    Config.init(dsn, release, environment)

def capture_exception(exc: Exception, level="error"):
    exc_type, exc_value, tb = sys.exc_info()
    tb = tb or exc.__traceback__
    payload = ErrorClient.build_payload(exc, tb, level)
    ErrorClient.send(payload)
