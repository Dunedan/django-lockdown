from django.utils.decorators import decorator_from_middleware

from lockdown.middleware import LockdownMiddleware

protect = decorator_from_middleware(LockdownMiddleware)
