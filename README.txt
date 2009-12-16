===============
django-lockdown
===============

A simple Django reusable application for locking down an entire site
(or particular views), with customizable date ranges and preview authorization.

Installation
============

Install from PyPI with ``easy_install`` or ``pip``::

    pip install django-lockdown

or get the `in-development version`_::

    pip install django-lockdown==tip

.. _in-development version: http://bitbucket.org/carljm/django-lockdown/get/tip.gz#egg=django_lockdown-tip

To use ``django-lockdown`` in your Django project:

    1. Add ``'lockdown'`` to your ``INSTALLED_APPS`` setting.

    2. To enable admin preview of locked-down sites or views with
       passwords, set the `LOCKDOWN_PASSWORDS`_ setting to a tuple of one or
       more plain-text passwords.

    3. Protect the entire site by using middleware, or protect individual views
       by applying a decorator to them.
       
For more advanced customization of admin preview authorization, see
the `LOCKDOWN_FORM`_ setting.

Dependencies
------------

``django-lockdown`` requires `Django`_ 1.1 or later.

.. _Django: http://www.djangoproject.com/

Usage
=====

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

Any further keyword arguments are passed to the admin preview form. The default
form accepts one argument:

``passwords``
  A tuple of passwords to use, rather than the ones provided by
  `LOCKDOWN_PASSWORDS`_.


Settings
========

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

A key which, if provided in the querystring of a locked URL, will log out the
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

Django-lockdown uses a single template, ``lockdown/form.html``. The
default template displays a simple "coming soon" message and the
preview authorization form.

If you override this template, the lockdown preview form is available
in the template context as ``form``.
