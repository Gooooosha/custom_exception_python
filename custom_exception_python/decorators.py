from functools import wraps
from inspect import iscoroutinefunction
from .sync import capture_exception

def handle_error(e: Exception, level: str):
    capture_exception(e, level)

def handle_exception(level: str = "unmarked"):
    def decorator(func):
        if iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    handle_error(e, level)
                    raise e
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    handle_error(e, level)
                    raise e
        return wrapper
    return decorator