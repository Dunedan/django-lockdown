import re

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from lockdown import settings

# an extra layer of indirection here so the tests can force this to be
# recalculated
_compiled_url_exceptions = ()
def _compile_url_exceptions():
    global _compiled_url_exceptions
    _compiled_url_exceptions = [re.compile(p)
                                for p in settings.LOCKDOWN_URL_EXCEPTIONS]
_compile_url_exceptions()

_lockdown_form = None
def _get_lockdown_form():
    global _lockdown_form
    path = settings.LOCKDOWN_FORM
    if path is None:
        if settings.LOCKDOWN_PASSWORD:
            path = 'lockdown.forms.LockdownForm'
        else:
            return None
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing LOCKDOWN_FORM %s: "%s"'
                                   % (path, e))
    except ValueError, e:
        raise ImproperlyConfigured('Error import LOCKDOWN_FORM %s: "%s"'
                                   % (path, e))
    try:
        form = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" form.'
                                   % (module, attr))
    _lockdown_form = form
_get_lockdown_form()

class LockdownMiddleware(object):
    def process_request(self, request):
        # check if they are already authorized for preview
        try:
            if request.session.get(settings.LOCKDOWN_SESSION_KEY, False):
                return None
        except AttributeError:
            raise ImproperlyConfigured('django-lockdown requires the Django sessions framework')

        # check if the URL matches an exception pattern
        for pattern in _compiled_url_exceptions:
            if pattern.search(request.path):
                return None

        # validate form data, if form is in use and submitted
        if _lockdown_form:
            if request.method == 'POST':
                form = _lockdown_form(request.POST)
                if form.is_valid():
                    request.session[settings.LOCKDOWN_SESSION_KEY] = True
                    return HttpResponseRedirect(request.path)
            else:
                form = _lockdown_form()
        else:
            form = None
        return render_to_response('lockdown/form.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))
        return None
