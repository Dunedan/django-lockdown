import datetime
import re
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import render

from lockdown import settings


def compile_url_exceptions(url_exceptions):
    """Return a list of compiled regex objects, containing the url exceptions.

    All URLs in that list returned won't be considered as locked.
    """
    return [re.compile(p) for p in url_exceptions]


def get_lockdown_form(form_path):
    """Return a form class for a given string pointing to a lockdown form."""
    if not form_path:
        raise ImproperlyConfigured('No LOCKDOWN_FORM specified.')
    form_path_list = form_path.split(".")
    module = ".".join(form_path_list[:-1])
    attr = form_path_list[-1]
    try:
        mod = import_module(module)
    except (ImportError, ValueError):
        raise ImproperlyConfigured('Module configured in LOCKDOWN_FORM (%s) to'
                                   ' contain the form class couldn\'t be '
                                   'found.' % module)
    try:
        form = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('The module configured in LOCKDOWN_FORM '
                                   ' (%s) doesn\'t define a "%s" form.'
                                   % (module, attr))
    return form


class LockdownMiddleware(object):

    """Middleware to lock down a whole Django site."""

    def __init__(self, get_response=None, form=None, until_date=None,
                 after_date=None, logout_key=None, session_key=None,
                 url_exceptions=None, extra_context=None, **form_kwargs):
        """Initialize the middleware, by setting the configuration values."""
        if logout_key is None:
            logout_key = settings.LOGOUT_KEY
        if session_key is None:
            session_key = settings.SESSION_KEY
        self.get_response = get_response
        self.form = form
        self.form_kwargs = form_kwargs
        self.until_date = until_date
        self.after_date = after_date
        self.logout_key = logout_key
        self.session_key = session_key
        self.url_exceptions = url_exceptions
        self.extra_context = extra_context

    def __call__(self, request):
        response = self.process_request(request)

        if not response:
            response = self.get_response(request)

        return response

    def process_request(self, request):
        """Check if each request is allowed to access the current resource."""
        try:
            session = request.session
        except AttributeError:
            raise ImproperlyConfigured('django-lockdown requires the Django '
                                       'sessions framework')

        # Don't lock down if django-lockdown is disabled altogether.
        if settings.ENABLED is False:
            return None

        # Don't lock down if the URL matches an exception pattern.
        if self.url_exceptions:
            url_exceptions = compile_url_exceptions(self.url_exceptions)
        else:
            url_exceptions = compile_url_exceptions(settings.URL_EXCEPTIONS)
        for pattern in url_exceptions:
            if pattern.search(request.path):
                return None

        # Don't lock down if outside of the lockdown dates.
        if self.until_date is None:
            until_date = settings.UNTIL_DATE
        else:
            until_date = self.until_date
        if self.after_date is None:
            after_date = settings.AFTER_DATE
        else:
            after_date = self.after_date
        if until_date or after_date:
            locked_date = False
            if until_date and datetime.datetime.now() < until_date:
                locked_date = True
            if after_date and datetime.datetime.now() > after_date:
                locked_date = True
            if not locked_date:
                return None

        form_data = request.method == 'POST' and request.POST or None
        if self.form:
            form_class = self.form
        else:
            form_class = get_lockdown_form(settings.FORM)
        form = form_class(data=form_data, **self.form_kwargs)

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

        page_data = {'until_date': until_date, 'after_date': after_date}
        if not hasattr(form, 'show_form') or form.show_form():
            page_data['form'] = form

        if self.extra_context is not None:
            page_data.update(self.extra_context)

        return render(request, 'lockdown/form.html', page_data)

    def redirect(self, request):
        """Utility method to handle redirects."""
        url = request.path
        querystring = request.GET.copy()
        if self.logout_key and self.logout_key in request.GET:
            del querystring[self.logout_key]
        if querystring:
            url = '%s?%s' % (url, querystring.urlencode())
        return HttpResponseRedirect(url)
