"""
Backport of ``decorator_from_middleware_with_args`` from Django
1.2dev, for Django 1.1 compatibility.

"""

import types
try:
    from functools import wraps, update_wrapper
except ImportError:
    from django.utils.functional import wraps, update_wrapper  # Python 2.3, 2.4 fallback.

# Licence for MethodDecoratorAdaptor and auto_adapt_to_methods
#
# This code is taken from stackoverflow.com [1], the code being supplied by
# users 'Ants Aasma' [2] and 'Silent Ghost' [3] with modifications.  It is
# legally included here under the terms of the Creative Commons
# Attribution-Share Alike 2.5 Generic Licence [4]
#
# [1] http://stackoverflow.com/questions/1288498/using-the-same-decorator-with-arguments-with-functions-and-methods
# [2] http://stackoverflow.com/users/107366/ants-aasma
# [3] http://stackoverflow.com/users/12855/silentghost
# [4] http://creativecommons.org/licenses/by-sa/2.5/

class MethodDecoratorAdaptor(object):
    """
    Generic way of creating decorators that adapt to being
    used on methods
    """
    def __init__(self, decorator, func):
        update_wrapper(self, func)
        # NB: update the __dict__ first, *then* set
        # our own .func and .decorator, in case 'func' is actually
        # another MethodDecoratorAdaptor object, which has its
        # 'func' and 'decorator' attributes in its own __dict__
        self.decorator = decorator
        self.func = func
    def __call__(self, *args, **kwargs):
        return self.decorator(self.func)(*args, **kwargs)
    def __get__(self, instance, owner):
        return self.decorator(self.func.__get__(instance, owner))

def auto_adapt_to_methods(decorator):
    """
    Takes a decorator function, and returns a decorator-like callable that can
    be used on methods as well as functions.
    """
    def adapt(func):
        return MethodDecoratorAdaptor(decorator, func)
    return wraps(decorator)(adapt)

def decorator_from_middleware_with_args(middleware_class):
    """
    Like decorator_from_middleware, but returns a function
    that accepts the arguments to be passed to the middleware_class.
    Use like::

         cache_page = decorator_from_middleware_with_args(CacheMiddleware)
         # ...

         @cache_page(3600)
         def my_view(request):
             # ...
    """
    return make_middleware_decorator(middleware_class)

def make_middleware_decorator(middleware_class):
    def _make_decorator(*m_args, **m_kwargs):
        middleware = middleware_class(*m_args, **m_kwargs)
        def _decorator(view_func):
            def _wrapped_view(request, *args, **kwargs):
                if hasattr(middleware, 'process_request'):
                    result = middleware.process_request(request)
                    if result is not None:
                        return result
                if hasattr(middleware, 'process_view'):
                    result = middleware.process_view(request, view_func, args, kwargs)
                    if result is not None:
                        return result
                try:
                    response = view_func(request, *args, **kwargs)
                except Exception, e:
                    if hasattr(middleware, 'process_exception'):
                        result = middleware.process_exception(request, e)
                        if result is not None:
                            return result
                    raise
                if hasattr(middleware, 'process_response'):
                    result = middleware.process_response(request, response)
                    if result is not None:
                        return result
                return response
            return wraps(view_func)(_wrapped_view)
        return auto_adapt_to_methods(_decorator)
    return _make_decorator
