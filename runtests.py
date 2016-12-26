#!/usr/bin/env python

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def runtests(*test_args):
    """Setup and run django-lockdowns test suite."""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lockdown.tests.test_settings'

    django.setup()

    if not test_args:
        test_args = ['lockdown.tests']

    test_runner = get_runner(settings)()
    failures = test_runner.run_tests(test_args)
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])
