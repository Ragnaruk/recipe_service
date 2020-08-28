import json
import logging

from functools import wraps


def log():
    """
    Decorator that logs function input and output.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            message = {
                "function": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "output": result,
            }

            logging.getLogger().debug(
                "{}".format(json.dumps(message, ensure_ascii=False))
            )

            return func(*args, **kwargs)

        return wrapper

    return decorator
