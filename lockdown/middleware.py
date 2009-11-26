import re

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from lockdown import settings


def compile_url_exceptions(url_exceptions):
    return [re.compile(p) for p in url_exceptions]

_default_url_exceptions = compile_url_exceptions(settings.URL_EXCEPTIONS)


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

_default_form = get_lockdown_form(settings.FORM)


class LockdownMiddleware(object):
    def __init__(self, form=None, logout_key=None, session_key=None,
                 url_exceptions=None, **form_kwargs):
        if form is None:
            form = _default_form
        if logout_key is None:
            logout_key = settings.LOGOUT_KEY
        if session_key is None:
            session_key = settings.SESSION_KEY
        if url_exceptions is None:
            url_exceptions = _default_url_exceptions
        self.form = form
        self.form_kwargs = form_kwargs
        self.logout_key = logout_key
        self.session_key = session_key
        self.url_exceptions = url_exceptions

    def process_request(self, request):
        try:
            session = request.session
        except AttributeError:
            raise ImproperlyConfigured('django-lockdown requires the Django '
                                       'sessions framework')

        # Don't lock down if the URL matches an exception pattern.
        for pattern in self.url_exceptions:
            if pattern.search(request.path):
                return None

        form_data = request.method == 'POST' and request.POST or None
        form = self.form(data=form_data, **self.form_kwargs)

        authorized = False
        token = session.get(self.session_key)
        if hasattr(form, 'authenticate'):
            if form.authenticate(token):
                authorized = True
        elif token is True:
            authorized = True

        if authorized and self.logout_key and self.logout_key in request.GET:
            if self.session_key in session:
                del session[self.session_key]
            url = request.path
            querystring = request.GET.copy()
            del querystring[self.logout_key]
            if querystring:
                url = '%s?%s' % (url, querystring.urlencode())
            return self.redirect(request)

        # Don't lock down if the user is already authorized for previewing.
        if authorized:
            return None

        if form.is_valid():
            if hasattr(form, 'generate_token'):
                token = form.generate_token()
            else:
                token = True
            session[self.session_key] = token
            return self.redirect(request)

        page_data = {}
        if not hasattr(form, 'show_form') or form.show_form():
            page_data['form'] = form

        return render_to_response('lockdown/form.html', page_data,
                                  context_instance=RequestContext(request))

    def redirect(self, request):
        url = request.path
        querystring = request.GET.copy()
        if self.logout_key and self.logout_key in request.GET:
            del querystring[self.logout_key]
        if querystring:
            url = '%s?%s' % (url, querystring.urlencode())
        return HttpResponseRedirect(url)
