from django.utils.decorators import decorator_from_middleware_with_args

from lockdown.middleware import LockdownMiddleware


def lockdown(*args, **kwargs):
    """Define a decorator based on the LockdownMiddleware.

    This decorator takes the same arguments as the middleware, but allows a
    more granular locking than the middleware.
    """
    return decorator_from_middleware_with_args(LockdownMiddleware)(*args,
                                                                   **kwargs)
