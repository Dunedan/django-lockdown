"""Provide a decorator based on the LockdownMiddleware.

This module provides a decorator that takes the same arguments as the
middleware, but allows more granular locking than the middleware.
"""
from django.utils.decorators import decorator_from_middleware_with_args

from lockdown.middleware import LockdownMiddleware

lockdown = decorator_from_middleware_with_args(LockdownMiddleware)
