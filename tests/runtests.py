#!/usr/bin/env python

import os, sys

parent = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))
sys.path.insert(0, parent)

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'

from django.test.utils import get_runner
from django.conf import settings

def runtests():
    test_runner = get_runner(settings)
    failures = test_runner(['tests'], verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
