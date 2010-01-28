CHANGES
=======

tip (unreleased)
----------------

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
