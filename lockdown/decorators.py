try:
    from django.utils.decorators import decorator_from_middleware_with_args
except ImportError:
    from lockdown.decutils import decorator_from_middleware_with_args

from lockdown.middleware import LockdownMiddleware

lockdown = decorator_from_middleware_with_args(LockdownMiddleware)
