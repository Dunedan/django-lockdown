#!/usr/bin/env python

import os, sys

from django.conf import settings


def runtests(*test_args):
    if not test_args:
        test_args = ['lockdown']
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        INSTALLED_APPS = ('django.contrib.sessions', 'lockdown'),
        ROOT_URLCONF='lockdown.tests.urls',
    )
    from django.test.utils import get_runner
    test_runner = get_runner(settings)
    failures = test_runner(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
