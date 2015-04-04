#!/usr/bin/env python

import os
import sys

import django
from django.conf import settings


def runtests(*test_args):
    """Setup and run django-lockdowns test suite.

    This still uses the old django.test.simple.DjangoTestSuiteRunner for
    compatibility reasons with older Django versions and because of the
    abstract base classes which shouldn't be considered as tests, but are
    discovered by the newer django.test.runner.DiscoverRunner.
    """
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lockdown.tests.test_settings'

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        django.setup()
    except AttributeError:
        # Access one setting to trigger the initialization of the settings as
        # workaround for older Django versions
        settings.INSTALLED_APPS

    try:
        from django.test.runner import DiscoverRunner
        potential_test_args = ['lockdown.tests']
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        test_runner = DjangoTestSuiteRunner(interactive=False)
        potential_test_args = ['lockdown']
    else:
        test_runner = DiscoverRunner(interactive=False)

    if not test_args:
        test_args = potential_test_args
    failures = test_runner.run_tests(test_args)
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])
