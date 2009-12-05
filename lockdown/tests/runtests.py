#!/usr/bin/env python

from os.path import dirname, abspath
import sys

def runtests(*test_args):
    if not test_args:
        test_args = ['lockdown']
    parent = dirname(dirname(dirname(abspath(__file__))))
    sys.path.insert(0, parent)
    from tests import django_settings
    from django.test.utils import get_runner
    test_runner = get_runner(django_settings)
    failures = test_runner(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
