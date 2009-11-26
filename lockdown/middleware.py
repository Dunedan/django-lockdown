import re

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from lockdown import settings


# An extra layer of indirection here so the tests can force this to be
# recalculated.
def _compile_url_exceptions():
    return [re.compile(p) for p in settings.URL_EXCEPTIONS]

_url_exceptions = _compile_url_exceptions()


def get_lockdown_form(form_path):
    form_path = settings.FORM
    if not form_path or '.' not in form_path:
        raise ImproperlyConfigured('The form module path was not provided.')
    last_dot = form_path.rfind('.')
    module, attr = form_path[:last_dot], form_path[last_dot + 1:]
    try:
        mod = import_module(module)
    except (ImportError, ValueError), e:
        raise ImproperlyConfigured('Error importing LOCKDOWN_FORM %s: "%s"'
                                   % (form_path, e))
    try:
        form = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" form.'
                                   % (module, attr))
    return form

_lockdown_form = get_lockdown_form(settings.FORM)


class LockdownMiddleware(object):
    def process_request(self, request):
        try:
            session = request.session
        except AttributeError:
            raise ImproperlyConfigured('django-lockdown requires the Django '
                                       'sessions framework')

        # Don't lock down if the URL matches an exception pattern.
        for pattern in _url_exceptions:
            if pattern.search(request.path):
                return None

        form_data = request.method == 'POST' and request.POST or None
        form = _lockdown_form(data=form_data)

        # Don't lock down if the user is already authorized for previewing.
        token = session.get(settings.SESSION_KEY)
        if hasattr(form, 'authenticate'):
            if self.form.authenticate(token):
                return None
        elif token is True:
            return None

        if form.is_valid():
            if hasattr(form, 'generate_token'):
                token = form.generate_token()
            else:
                token = True
            session[settings.SESSION_KEY] = token
            return HttpResponseRedirect(request.path)

        page_data = {}
        if not hasattr(form, 'show_form') or form.show_form():
            page_data['form'] = form

        return render_to_response('lockdown/form.html', page_data,
                                  context_instance=RequestContext(request))
