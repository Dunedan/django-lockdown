===============
django-lockdown
===============

A simple Django reusable application for locking down an entire site
(or particular views), with customizable preview authorization
(defaults to single password).

Installation
============

Install from PyPI with ``easy_install`` or ``pip``::

    pip install django-lockdown

or get the `in-development version`_::

    pip install django-lockdown==dev

.. _in-development version: http://bitbucket.org/carljm/django-lockdown/get/tip.gz#egg=django_lockdown-dev

To use ``django-lockdown`` in your Django project:

    1. Add ``'lockdown'`` to your ``INSTALLED_APPS`` setting.

    2. To enable admin preview of locked-down sites or views with
       passwords, set the `LOCKDOWN_PASSWORDS`_ setting to a tuple of one or
       more plain-text passwords.

    3. Protect the entire site by using middleware, or protect individual views
       by applying a decorator to them.
       
For more advanced customization of admin preview authorization, see
the `LOCKDOWN_FORM`_ setting.

Using the middleware
--------------------

To lock down the entire site, add the lockdown middleware to your
``MIDDLEWARE_CLASSES`` setting::

    MIDDLEWARE_CLASSES = (
        # ...
        'lockdown.middleware.LockdownMiddleware',
    )
    
Optionally, you may also add URL regular expressions to a
`LOCKDOWN_URL_EXCEPTIONS`_ setting.

Using the decorator
-------------------

Apply the decorator to individual views you want to protect. For example::

    @lockdown()
    def secret_page(request):
        # ...

The decorator accepts four arguments:

``form``
  The form to use for providing an admin preview, rather than the form
  referenced by ``settings.LOCKDOWN_FORM``. Note that this must be an actual
  form class, not a module reference like the setting. 

``logout_key``
  A preview logout key to use, rather than the one provided by
  ``settings.LOCKDOWN_LOGOUT_KEY``.

``session_key``
  The session key to use, rather than the one provided by
  ``settings.LOCKDOWN_SESSION_KEY``.
 
``url_exceptions``
  A list of regular expressions for which matching urls can bypass the
  lockdown (rather than using those defined in
  ``settings.LOCKDOWN_URL_EXCEPTIONS``).

Any further keyword arguments are passed to the admin preview form. The default
form accepts one argument::

``passwords``
  A tuple of passwords to use, rather than the ones provided by
  ``settings.LOCKDOWN_PASSWORDS``.


Settings
========

LOCKDOWN_PASSWORDS
------------------

One or more plain-text passwords which allow the previewing of the site or
views protected by django-lockdown::

    LOCKDOWN_PASSWORDS = ('letmein', 'beta')

If this setting is not provided (and the default ``LOCKDOWN_FORM`` is being
used), there will be no admin preview for locked-down pages.

LOCKDOWN_URL_EXCEPTIONS
-----------------------

An optional list/tuple of regular expressions to be matched against incoming
URLs. If a URL matches a regular expression in this list, it will not be
locked. For example::

    LOCKDOWN_URL_EXCEPTIONS = (
        r'^/about/$',   # unlock /about/
        r'\.json$',   # unlock JSON API
    )

LOCKDOWN_LOGOUT_KEY
-------------------

A key which, if provided in the querystring of a locked URL, will log out the
user from the preview. 

LOCKDOWN_FORM
-------------

By default, django-lockdown allows admin preview by entering a preset
plain-text `LOCKDOWN_PASSWORD`_. To set up more advanced methods of
authenticating access to locked-down pages, set ``LOCKDOWN_FORM`` to
the Python dotted path to a Django ``Form`` subclass. This form will
be displayed on the lockout page. If the form validates when
submitted, the user will be allowed access to locked pages::

    LOCKDOWN_FORM = 'path.to.my.CustomLockdownForm'

LOCKDOWN_SESSION_KEY
--------------------

Once a client is authorized for admin preview, they will continue to
be authorized for the remainder of their browsing session (using
Django's built-in session support). ``LOCKDOWN_SESSION_KEY`` defines
the session key used; the default is ``'lockdown-allow'``.


Templates
=========

Django-lockdown uses a single template, ``lockdown/form.html``. The
default template displays a simple "coming soon" message and the
password entry form.

If you override this template, the lockdown preview form is available
in the template context as ``form``.
