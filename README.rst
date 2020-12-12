===============
django-lockdown
===============

.. image:: https://github.com/Dunedan/django-lockdown/workflows/CI/badge.svg
    :target: https://github.com/Dunedan/django-lockdown/actions
    :alt: Build Status
.. image:: https://coveralls.io/repos/Dunedan/django-lockdown/badge.svg
    :target: https://coveralls.io/r/Dunedan/django-lockdown
    :alt: Test Coverage
.. image:: https://img.shields.io/pypi/v/django-lockdown.svg
    :target: https://pypi.org/project/django-lockdown/
    :alt: Latest Version

``django-lockdown`` is a reusable Django application for locking down an entire
site (or particular views), with customizable date ranges and preview
authorization.

Installation
============

Install from PyPI with ``easy_install`` or ``pip``::

    pip install django-lockdown

To use ``django-lockdown`` in your Django project:

1. Add ``'lockdown'`` to your ``INSTALLED_APPS``.
   If you want to use one of ``django-lockdowns`` default lock down forms,
   you'll additionally have to ensure that you have enabled
   ``django.contrib.auth`` as part of to your ``INSTALLED_APPS``.

2. To enable admin preview of locked-down sites or views with
   passwords, set the `LOCKDOWN_PASSWORDS`_ setting to a tuple of one or
   more plain-text passwords.

3. Protect the entire site by using middleware, or protect individual views
   by applying a decorator to them.
       
For more advanced customization of admin preview authorization, see
the `LOCKDOWN_FORM`_ setting.

Dependencies
------------

``django-lockdown`` requires `Python`_ 3.6 or later and `Django`_ 2.2 or later.

As an alternative to CPython `PyPy`_ 3.5 and 3.6 are supported as well.

.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/
.. _PyPy: https://pypy.org/

Usage
=====

Using the middleware
--------------------

To lock down the entire site, add the lockdown middleware to your middlewares::

    MIDDLEWARE = [
        # ...
        'lockdown.middleware.LockdownMiddleware',
    ]

Optionally, you may also add URL regular expressions to a
`LOCKDOWN_URL_EXCEPTIONS`_ setting.

Using the decorator
-------------------

- Import the decorator::

    from lockdown.decorators import lockdown

- Apply the decorator to individual views you want to protect. For example::

    @lockdown()
    def secret_page(request):
        # ...

The decorator accepts seven arguments:

``form``
  The form to use for providing an admin preview, rather than the form
  referenced by `LOCKDOWN_FORM`_. Note that this must be an actual form class,
  not a module reference like the setting.

``until_date``
  The date to use rather than the date provided by `LOCKDOWN_UNTIL`_.

``after_date``
  The date to use rather than the date provided by `LOCKDOWN_AFTER`_.

``logout_key``
  A preview logout key to use, rather than the one provided by
  `LOCKDOWN_LOGOUT_KEY`_.

``session_key``
  The session key to use, rather than the one provided by
  `LOCKDOWN_SESSION_KEY`_.
 
``url_exceptions``
  A list of regular expressions for which matching urls can bypass the lockdown
  (rather than using those defined in `LOCKDOWN_URL_EXCEPTIONS`_).

``remote_addr_exceptions``
 A list of IP-addresses or IP-subnets for which matching URLs can bypass the
 lockdown (rather than using those defined in
 `LOCKDOWN_REMOTE_ADDR_EXCEPTIONS`_).

``extra_context``
  A dictionary of context data that will be added to the default context data
  passed to the template.

Any further keyword arguments are passed to the admin preview form. The default
form accepts one argument:

``passwords``
  A tuple of passwords to use, rather than the ones provided by
  `LOCKDOWN_PASSWORDS`_.


Settings
========

LOCKDOWN_ENABLED
----------------

An optional boolean value that, if set to False, disables
``django-lockdown`` globally. Defaults to True (lock down enabled).


LOCKDOWN_PASSWORDS
------------------

One or more plain-text passwords which allow the previewing of the site or
views protected by django-lockdown::

    LOCKDOWN_PASSWORDS = ('letmein', 'beta')

If this setting is not provided (and the default `LOCKDOWN_FORM`_ is being
used), there will be no admin preview for locked-down pages.

If a `LOCKDOWN_FORM`_ other than the default is used, this setting has no
effect.

LOCKDOWN_URL_EXCEPTIONS
-----------------------

An optional list/tuple of regular expressions to be matched against incoming
URLs. If a URL matches a regular expression in this list, it will not be
locked. For example::

    LOCKDOWN_URL_EXCEPTIONS = (
        r'^/about/$',   # unlock /about/
        r'\.json$',   # unlock JSON API
    )

LOCKDOWN_VIEW_EXCEPTIONS
------------------------

An optional list of regular expressions to be matched against the
resolved views of incoming requests. If the URL of an incoming request
resolves to one of the views in the list, it will not be locked.
That's useful if you want to lock down a whole site using the middleware,
but want to whitelist some localized URLs.

For example::

    from yourapp import one_view_to_unlock, another_view_to_unlock

    LOCKDOWN_VIEW_EXCEPTIONS = [
        one_view_to_unlock,
        another_view_to_unlock
    ]

LOCKDOWN_REMOTE_ADDR_EXCEPTIONS
-------------------------------

An optional list of IP-addresses or IP-subnets to be matched against the
requesting IP-address (from `requests.META['REMOTE_ADDR']`). If the
requesting IP-address is in this list, it will not be locked. For example::

    LOCKDOWN_REMOTE_ADDR_EXCEPTIONS = [
        '127.0.0.1',
        '::1',
    ]

LOCKDOWN_TRUSTED_PROXIES
-------------------------------

A list of trusted proxy IP-addresses to be used in conjunction with 
`LOCKDOWN_REMOTE_ADDR_EXCEPTIONS` when a reverse-proxy or load balancer is used.
If the requesting IP address is from the trusted proxies list the last address from 
the `X-Forwared-For` header (from `requests.META['HTTP_X_FORWARDED_FOR']`) will be 
checked against `LOCKDOWN_REMOTE_ADDR_EXCEPTIONS` and locked or unlocked accordingly.

For example::

    LOCKDOWN_TRUSTED_PROXIES = [
        '172.17.0.1',
    ]
    
    LOCKDOWN_REMOTE_ADDR_EXCEPTIONS = [
        '172.17.0.5',
    ]

LOCKDOWN_UNTIL
--------------

Used to lock the site down up until a certain date. Set to a
``datetime.datetime`` object.

If neither ``LOCKDOWN_UNTIL`` nor `LOCKDOWN_AFTER`_ is provided (the default),
the site or views will always be locked.

LOCKDOWN_AFTER
--------------

Used to lock the site down after a certain date. Set to a ``datetime.datetime``
object.

See also: `LOCKDOWN_UNTIL`_.

LOCKDOWN_LOGOUT_KEY
-------------------

A key which, if provided in the query string of a locked URL, will log out the
user from the preview. 

LOCKDOWN_FORM
-------------

The default lockdown form allows admin preview by entering a preset
plain-text password (checked, by default, against the `LOCKDOWN_PASSWORDS`_
setting). To set up more advanced methods of authenticating access to
locked-down pages, set ``LOCKDOWN_FORM`` to the Python dotted path to a Django
``Form`` subclass. This form will be displayed on the lockout page. If the form
validates when submitted, the user will be allowed access to locked pages::

    LOCKDOWN_FORM = 'path.to.my.CustomLockdownForm'
    
A form for authenticating against ``django.contrib.auth`` users is provided
with django-lockdown (use ``LOCKDOWN_FORM = 'lockdown.forms.AuthForm'``). It
accepts two keyword arguments (in the ``lockdown`` decorator):

``staff_only``
  Only allow staff members to preview. Defaults to ``True`` (but the default
  can be provided as a `LOCKDOWN_AUTHFORM_STAFF_ONLY`_ setting).

``superusers_only``
  Only allow superusers to preview. Defaults to ``False`` (but the default
  can be provided as a `LOCKDOWN_AUTHFORM_SUPERUSERS_ONLY`_ setting).

LOCKDOWN_AUTHFORM_STAFF_ONLY
----------------------------

If using ``lockdown.forms.AuthForm`` and this setting is ``True``, only staff
users will be allowed to preview (True by default).

Has no effect if not using ``lockdown.forms.AuthForm``.

LOCKDOWN_AUTHFORM_SUPERUSERS_ONLY
---------------------------------

If using ``lockdown.forms.AuthForm`` and this setting is ``True``, only
superusers will be allowed to preview (False by default). Has no effect if not
using ``lockdown.forms.AuthForm``.

LOCKDOWN_SESSION_KEY
--------------------

Once a client is authorized for admin preview, they will continue to
be authorized for the remainder of their browsing session (using
Django's built-in session support). ``LOCKDOWN_SESSION_KEY`` defines
the session key used; the default is ``'lockdown-allow'``.


Templates
=========

``django-lockdown`` uses a single template, ``lockdown/form.html``. The
default template displays a simple "coming soon" message and the
preview authorization form, if a password via `LOCKDOWN_PASSWORDS`_ is set.

If you want to use a different template, you can use Djangos template
`loaders`_ to specify a path inside your project to search for templates,
before searching for templates included in ``django-lockdown``.

In your overwritten template the lockdown preview form is available in the
template context as ``form``.

.. _loaders: https://docs.djangoproject.com/en/2.1/ref/templates/api/#template-loaders
