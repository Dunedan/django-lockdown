CHANGES
=======

tip (unreleased)
----------------

1.5.0 (2017-12-05)
------------------

- Add support for Django 2.0

- Improve the code style in some areas

1.4.2 (2017-04-07)
------------------

- Fix formatting for PyPi


1.4.1 (2017-04-07)
------------------

- Fix problem with upload for PyPi


1.4.0 (2017-04-06)
------------------

- Refactor tests to use Mocks

- Add support for Python 3.6

- Add support for Django 1.11


1.3 (2016-08-07)
----------------

- Adds support for Django 1.10.

- Adds support for providing additional context data to the lockdown template.


1.2 (2015-12-03)
----------------

- Adds support for Python 3.5.

- Adds support for Django 1.9.

- Drops support for Django <=1.7.

- Fixes not working URL exceptions when specifying them in the decorator
  arguments.

- Improves tests.

1.1 (2015-04-06)
----------------

- Proper new version after 0.1.2 and 0.1.3 have been tagged after the release
  of 1.0. Contains all new features of 0.1.2 and 0.1.3, most notably support
  for Python 3.

- Last version of django-lockdown with support for Django 1.3, 1.5 and 1.6.
  Upcoming versions will only support Django versions with official security
  support. For the time being these are Django 1.4 LTS, 1.7 and 1.8 LTS.

- Fixes testing for Django >=1.7

0.1.3 (2014-03-15) (never released)
-----------------------------------

- Added ``LOCKDOWN_ENABLED`` setting.

- Removed Django 1.1 backport of ``decorator_from_middleware_with_args``.

0.1.2 (2014-03-15) (never released)
-----------------------------------

- Require at least Django 1.3.

- Fixed the test runner script to work with recent Django versions.

- Added the csrf_token template tag to the included form template.

- Minor syntax adjustments for Python 3 compatibility.

1.0 (2013-07-10)
----------------

- BACKWARDS INCOMPATIBLE: Allow multiple passwords (the passwords setting has
  changed from ``LOCKDOWN_PASSWORD`` to ``LOCKDOWN_PASSWORDS``).

- Decorator changed to a callable decorator (so settings can be overridden for
  an individual decorator).

- Add ``AuthForm`` which can be used to allow previewing from authenticated
  users (via ``django.contrib.auth``).

- Allow locking up until or only after certain dates.

0.1.1 (2009-11-24)
------------------

- Fix setup.py so ``tests`` package is not installed.

0.1 (2009-11-16)
----------------

- Initial release.
