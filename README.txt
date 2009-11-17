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

    2. To enable admin preview of locked-down sites or views with a
       single password, set the `LOCKDOWN_PASSWORD`_ setting to a
       plain-text password.

    3. To lock down the entire site, add
       ``'lockdown.middleware.LockdownMiddleware'`` to your
       ``INSTALLED_APPS`` setting. Optionally you may also add URL
       regular expressions to the `LOCKDOWN_URL_EXCEPTIONS`_ setting.

    4. To protect only certain views, apply the
       ``lockdown.decorators.lockdown`` decorator to the views you
       want to protect.

For more advanced customization of admin preview authorization, see
the `LOCKDOWN_FORM`_ setting.

Settings
========

LOCKDOWN_PASSWORD
-----------------

The plain-text password required to preview a site or views protected
by django-lockdown::

    LOCKDOWN_PASSWORD = 'letmein'

If neither this setting nor `LOCKDOWN_FORM`_ is provided, there will
be no admin preview for locked-down pages.

LOCKDOWN_URL_EXCEPTIONS
-----------------------

Optional: a list/tuple of regular expressions to be matched against
incoming URLs. If a URL matches a regular expression in this list, it
will not be locked::

    LOCKDOWN_URL_EXCEPTIONS = (r'^/about/$',  # unlock /about/
                               r'\.json$')    # unlock JSON API

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

