from functools import wraps

from flask import abort

from lcah.errors import ObjectNotFound


def catch_object_not_found(app):

    def decorator(func):
        if app.debug:
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ObjectNotFound:
                abort(404)

        return wrapper

    return decorator
