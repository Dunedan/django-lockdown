CHANGES
=======

5.0.0 (Unreleased)
------------------

- Remove support for end-of-life Django versions (2.2, 3.0 and 3.1).

- Remove support for end-of-life Python versions (3.6 and 3.7).

- Add support for Django 3.2, 4.0, 4.1, 4.2 and 5.0.

- Add support for Python 3.10, 3.11 and 3.12.

4.0.0 (2021-02-14)
------------------

- Remove support for end-of-life Django versions (1.11, 2.0 and 2.1).

- Add support for Python 3.9 and remove support for Python 3.5.

- Add support for Django 3.1.

3.0.0. (2020-01-01)
-------------------

- Added support for Python 3.8.

- Added support for Django 3.0.

- Removed support for Python 2.7 and 3.4.

2.0.0 (2019-05-26)
------------------

- Added support for proxies when using IP-address based lockdown exceptions.

- This introduces a breaking change: Installations running behind a proxy will
  need to set the newly introduced ``LOCKDOWN_TRUSTED_PROXIES``, otherwise
  access won't be granted anymore, when accessing the site through a proxy.

- Added the ability to whitelist views when locking down a whole site using
  the middleware.

- Added support for Django 2.2.

- Only require ``mock`` as separate third-party test dependency for
  Python <3.3.

- Fix detection of compacted IP-addresses.

- This introduces a breaking change for users which make use of the
  ``REMOTE_ADDR_EXCEPTIONS`` feature and passed the IP-addresses to except as
  byte strings in the configuration. While it's unlikely somebody did that
  with Python 3, it's the default for Python 2. With this version, byte
  strings don't work anymore, but using unicode strings is required.

- Add the ability to specify IP-subnets for remote addresses exception.

1.6.0 (2018-11-25)
------------------

- Drops support for Django <=1.10.

- Drops support for Python 3.3.

- Add the ability to bypass the lockdown for configured IP-addresses.

- Integrate pre-commit for code style checks during commit and CI.

- Added support for Django 2.1.

- Add support for Python 3.7.

- Add support for PyPy.

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
