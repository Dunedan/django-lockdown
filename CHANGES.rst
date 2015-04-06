CHANGES
=======

1.1 (2015.04.06)
------------------

- Proper new version after 0.1.2 and 0.1.3 have been tagged after the release
  of 1.0. Contains all new features of 0.1.2 and 0.1.3, most notably support
  for Python 3.

- Last version of django-lockdown with support for Django 1.3, 1.5 and 1.6.
  Upcoming versions will only support Django versions with official security
  support. For the time being these are Django 1.4 LTS, 1.7 and 1.8 LTS.

- Fixes testing for Django >=1.7

0.1.3 (2014.03.15) (never released)
------------------

- Added ``LOCKDOWN_ENABLED`` setting.

- Removed Django 1.1 backport of ``decorator_from_middleware_with_args``.

0.1.2 (2014.03.15) (never released)
------------------

- Require at least Django 1.3.

- Fixed the test runner script to work with recent Django versions.

- Added the csrf_token template tag to the included form template.

- Minor syntax adjustments for Python 3 compatibility.

1.0 (2013.07.10)
------------------

- BACKWARDS INCOMPATIBLE: Allow multiple passwords (the passwords setting has
  changed from ``LOCKDOWN_PASSWORD`` to ``LOCKDOWN_PASSWORDS``).

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
