import datetime
import ipaddress
import re
from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import Resolver404, resolve


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
    new_module = ".".join(form_path_list[:-1])
    attr = form_path_list[-1]
    try:
        mod = import_module(new_module)
    except (ImportError, ValueError):
        raise ImproperlyConfigured("Module configured in LOCKDOWN_FORM (%s) to"
                                   " contain the form class couldn't be "
                                   "found." % new_module)
    try:
        form = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('The module configured in LOCKDOWN_FORM '
                                   ' (%s) doesn\'t define a "%s" form.'
                                   % (new_module, attr))
    return form


# pylint: disable=too-many-instance-attributes
class LockdownMiddleware(object):
    """Middleware to lock down a whole Django site."""

    # pylint: disable=too-many-arguments
    def __init__(self, get_response=None, form=None, until_date=None,
                 after_date=None, logout_key=None, session_key=None,
                 url_exceptions=None, remote_addr_exceptions=None,
                 trusted_proxies=None, extra_context=None, **form_kwargs):
        """Initialize the middleware, by setting the configuration values."""
        if logout_key is None:
            logout_key = getattr(settings,
                                 'LOCKDOWN_LOGOUT_KEY',
                                 'preview-logout')
        if session_key is None:
            session_key = getattr(settings,
                                  'LOCKDOWN_SESSION_KEY',
                                  'lockdown-allow')
        self.get_response = get_response
        self.form = form
        self.form_kwargs = form_kwargs
        self.until_date = until_date
        self.after_date = after_date
        self.logout_key = logout_key
        self.session_key = session_key
        self.url_exceptions = url_exceptions
        self.remote_addr_exceptions = remote_addr_exceptions
        self.trusted_proxies = trusted_proxies
        self.extra_context = extra_context

    def __call__(self, request):
        """Handle calls to the class instance."""
        response = self.process_request(request)

        if not response:
            response = self.get_response(request)

        return response

    # pylint: disable=too-many-locals,too-many-return-statements
    # pylint: disable=too-many-statements,too-many-branches
    def process_request(self, request):
        """Check if each request is allowed to access the current resource."""
        try:
            session = request.session
        except AttributeError:
            raise ImproperlyConfigured('django-lockdown requires the Django '
                                       'sessions framework')

        # Don't lock down if django-lockdown is disabled altogether.
        if getattr(settings, 'LOCKDOWN_ENABLED', True) is False:
            return None

        # Don't lock down if the client REMOTE_ADDR matched and is part of the
        # exception list.
        if self.remote_addr_exceptions:
            remote_addr_exceptions = self.remote_addr_exceptions
        else:
            remote_addr_exceptions = getattr(settings,
                                             'LOCKDOWN_REMOTE_ADDR_EXCEPTIONS',
                                             [])

        remote_addr_exceptions = [ipaddress.ip_network(ip)
                                  for ip in remote_addr_exceptions]
        if remote_addr_exceptions:
            # If forwarding proxies are used they must be listed as trusted
            trusted_proxies = self.trusted_proxies or \
                getattr(settings, 'LOCKDOWN_TRUSTED_PROXIES', [])
            trusted_proxies = [ipaddress.ip_network(ip)
                               for ip in trusted_proxies]

            remote_addr = ipaddress.ip_address(request.META.get('REMOTE_ADDR'))
            if any(remote_addr for ip_exceptions in remote_addr_exceptions
                   if remote_addr in ip_exceptions):
                return None

            if any(remote_addr for proxy in trusted_proxies
                   if remote_addr in proxy):
                # If REMOTE_ADDR is a trusted proxy check x-forwarded-for
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    remote_addr = ipaddress.ip_address(
                        x_forwarded_for.split(',')[-1].strip())
                    if any(remote_addr for ip_exceptions in
                           remote_addr_exceptions
                           if remote_addr in ip_exceptions):
                        return None

        # Don't lock down if the URL matches an exception pattern.
        if self.url_exceptions:
            url_exceptions = compile_url_exceptions(self.url_exceptions)
        else:
            url_exceptions = compile_url_exceptions(
                getattr(settings, 'LOCKDOWN_URL_EXCEPTIONS', ()))
        for pattern in url_exceptions:
            if pattern.search(request.path):
                return None

        # Don't lock down if the URL resolves to a whitelisted view.
        try:
            resolved_path = resolve(request.path)
        except Resolver404:
            pass
        else:
            if resolved_path.func in getattr(
                    settings, 'LOCKDOWN_VIEW_EXCEPTIONS', []):
                return None

        # Don't lock down if outside of the lockdown dates.
        if self.until_date:
            until_date = self.until_date
        else:
            until_date = getattr(settings, "LOCKDOWN_UNTIL_DATE", None)

        if self.after_date:
            after_date = self.after_date
        else:
            after_date = getattr(settings, "LOCKDOWN_AFTER_DATE", None)

        if until_date or after_date:
            locked_date = False
            if until_date and datetime.datetime.now() < until_date:
                locked_date = True
            if after_date and datetime.datetime.now() > after_date:
                locked_date = True
            if not locked_date:
                return None

        form_data = request.POST if request.method == 'POST' else None
        if self.form:
            form_class = self.form
        else:
            form_class = get_lockdown_form(
                getattr(settings,
                        'LOCKDOWN_FORM',
                        'lockdown.forms.LockdownForm'))
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
            querystring = request.GET.copy()
            del querystring[self.logout_key]
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

        if self.extra_context:
            page_data.update(self.extra_context)

        return render(request, 'lockdown/form.html', page_data)

    def redirect(self, request):
        """Handle redirects properly."""
        url = request.path
        querystring = request.GET.copy()
        if self.logout_key and self.logout_key in request.GET:
            del querystring[self.logout_key]
        if querystring:
            url = '%s?%s' % (url, querystring.urlencode())
        return HttpResponseRedirect(url)
