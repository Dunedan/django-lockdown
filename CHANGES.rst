CHANGES
=======

0.1.3 (2014.03.15)
------------------

- Added ``LOCKDOWN_ENABLED`` setting.

- Removed Django 1.1 backport of ``decorator_from_middleware_with_args``.

0.1.2 (2014.03.15)
------------------

- Require at least Django 1.3.

- Fixed the test runner script to work with recent Django versions.

- Added the csrf_token template tag to the included form template.

- Minor syntax adjustments for Python 3 compatibility.

- Allow multiple passwords (the passwords setting has changed from
  ``LOCKDOWN_PASSWORD`` to ``LOCKDOWN_PASSWORDS``.

- Decorator changed to a callable decorator (so settings can be overridden for
  an individual decorator).

- Add ``AuthForm`` which can be used to allow previewing from authenticated
  users (via ``django.contrib.auth``).

- Allow locking up until or only after certain dates.

0.1.1 (2009.11.24)
------------------

- Fix setup.py so ``tests`` package is not installed.

0.1 (2009.11.16)
----------------

- Initial release.
